# Servidor Flask da página de upload de faturas.
# Rodar a partir da raiz do projeto: python web/app.py
import sys, pathlib

# Bootstrap: faz "python web/app.py" funcionar a partir da raiz do projeto
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from flask import Flask, abort, jsonify, render_template, request, send_file
from datetime import date
import calendar

from web.servico_upload import (
    PASTA_PDFS,
    ErroValidacao,
    buscar_historico,
    obter_linha_historico,
    processar_upload,
)

from database.conection import Session
from database.models import Cliente, UnidadeConsumidora, ValoresFatura

app = Flask(__name__)


@app.route("/")
def pagina_upload():
    """Página principal: campo de upload e histórico de tentativas."""
    return render_template("upload.html")


@app.route("/configuracoes")
def pagina_configuracoes():
    """Página de configurações: por enquanto, alternar tema claro/escuro."""
    return render_template("configuracoes.html")


@app.route("/api/historico")
def api_historico():
    """JSON com as linhas do histórico, mais recente primeiro."""
    return jsonify(buscar_historico())


@app.route("/api/upload", methods=["POST"])
def api_upload():
    """Recebe o multipart (campo "arquivo") e roda o fluxo de upload."""
    arquivo = request.files.get("arquivo")
    if arquivo is None or not arquivo.filename:
        return jsonify({"status": "RECUSADO", "mensagem": "Nenhum arquivo foi enviado."}), 400
    try:
        resultado = processar_upload(arquivo.filename, arquivo.read())
    except ErroValidacao as erro:
        return jsonify({"status": "RECUSADO", "mensagem": str(erro)}), 400
    return jsonify(resultado)


@app.route("/api/download/<int:id_registro>")
def api_download(id_registro):
    """Serve o PDF de uma linha do histórico com o nome original do upload."""
    linha = obter_linha_historico(id_registro)
    if linha is None:
        abort(404)
    caminho = PASTA_PDFS / linha["nome_arquivo_salvo"]
    if not caminho.is_file():
        abort(404)
    return send_file(caminho, as_attachment=True, download_name=linha["nome_pdf"])


# ---------------- Gestão de Clientes ----------------

@app.route("/clientes")
def pagina_clientes():
    """Página de gestão de clientes."""
    return render_template("clientes.html")


@app.route("/api/clientes")
def api_clientes():
    """JSON lista de clientes [{id, nome, cpf_cnpj}].
    Query params opcionais:
      q        -> busca em nome ILIKE OU cpf_cnpj ILIKE
      documento -> filtra apenas por cpf_cnpj ILIKE
    """
    q = (request.args.get("q") or "").strip()
    documentos = request.args.getlist("documento")

    with Session() as session:
        query = session.query(Cliente)
        if q:
            like = "%" + q + "%"
            query = query.filter(
                (Cliente.nome.ilike(like)) | (Cliente.cpf_cnpj.ilike(like))
            )
        if documentos:
            query = query.filter(Cliente.cpf_cnpj.in_(documentos))

        clientes = query.order_by(Cliente.nome).all()
        return jsonify(
            [{"id": c.id, "nome": c.nome, "cpf_cnpj": c.cpf_cnpj} for c in clientes]
        )


@app.route("/api/clientes", methods=["POST"])
def api_criar_cliente():
    """Recebe JSON {nome, cpf_cnpj}, valida, rejeita duplicado (409) e insere."""
    dados = request.get_json(silent=True) or {}
    nome = (dados.get("nome") or "").strip()
    cpf_cnpj = (dados.get("cpf_cnpj") or "").strip()

    if not nome or not cpf_cnpj:
        return jsonify({"status": "ERRO", "mensagem": "Nome e CPF/CNPJ são obrigatórios."}), 400

    with Session() as session:
        existente = session.query(Cliente).filter_by(cpf_cnpj=cpf_cnpj).first()
        if existente:
            return jsonify({"status": "DUPLICADO", "mensagem": "CPF/CNPJ já cadastrado."}), 409

        cliente = Cliente(nome=nome, cpf_cnpj=cpf_cnpj)
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return jsonify(
            {"id": cliente.id, "nome": cliente.nome, "cpf_cnpj": cliente.cpf_cnpj}
        ), 201


@app.route("/api/clientes/<int:id_cliente>", methods=["DELETE"])
def api_excluir_cliente(id_cliente):
    """Exclui o cliente pelo id; retorna 204 ou 404 se não existir."""
    with Session() as session:
        cliente = session.get(Cliente, id_cliente)
        if cliente is None:
            return jsonify({"status": "ERRO", "mensagem": "Cliente não encontrado."}), 404
        session.delete(cliente)
        session.commit()
        return "", 204


@app.route("/api/clientes/documentos")
def api_clientes_documentos():
    """JSON com todos os CPF/CNPJ existentes [{id, nome, cpf_cnpj}] para o filtro lateral."""
    with Session() as session:
        documentos = session.query(Cliente).order_by(Cliente.nome).all()
        return jsonify(
            [{"id": d.id, "nome": d.nome, "cpf_cnpj": d.cpf_cnpj} for d in documentos]
        )

# ---------------- Auditoria de Faturas ----------------


@app.route("/auditoria")
def pagina_auditoria():
    """Página de auditoria de faturas: filtros de cliente, UC e período de referência."""
    return render_template("auditoria.html")


@app.route("/api/ucs")
def api_ucs():
    """JSON [{id, uc}] das UCs do cliente selecionado (dropdown cascata da auditoria)."""
    cliente_id = request.args.get("cliente_id", type=int)
    with Session() as session:
        query = session.query(UnidadeConsumidora)
        if cliente_id is not None:
            query = query.filter_by(cliente_id=cliente_id)
        ucs = query.order_by(UnidadeConsumidora.uc).all()
        return jsonify([{"id": u.id, "uc": u.uc} for u in ucs])


@app.route("/api/faturas")
def api_faturas():
    """JSON lista de faturas filtradas para a página de auditoria.

    Query params opcionais:
      cliente_id -> filtra por cliente
      uc_id      -> filtra por unidade consumidora
      de         -> YYYY-MM (mes_ref a partir do primeiro dia do mês)
      ate        -> YYYY-MM (mes_ref até o último dia do mês)
    """
    cliente_id = request.args.get("cliente_id", type=int)
    uc_id = request.args.get("uc_id", type=int)
    de = request.args.get("de", type=str)
    ate = request.args.get("ate", type=str)

    with Session() as session:
        rows = (
            session.query(
                Cliente.nome.label("cliente"),
                UnidadeConsumidora.uc.label("numero_uc"),
                ValoresFatura.mes_ref,
                ValoresFatura.valor_total,
                ValoresFatura.vencimento,
                ValoresFatura.nome_pdf,
            )
            .join(UnidadeConsumidora, ValoresFatura.uc_id == UnidadeConsumidora.id)
            .join(Cliente, UnidadeConsumidora.cliente_id == Cliente.id)
        )
        if cliente_id is not None:
            rows = rows.filter(Cliente.id == cliente_id)
        if uc_id is not None:
            rows = rows.filter(UnidadeConsumidora.id == uc_id)

        if de:
            ano, mes = de.split("-")
            rows = rows.filter(ValoresFatura.mes_ref >= date(int(ano), int(mes), 1))
        if ate:
            ano, mes = ate.split("-")
            ultimo_dia = calendar.monthrange(int(ano), int(mes))[1]
            rows = rows.filter(ValoresFatura.mes_ref <= date(int(ano), int(mes), ultimo_dia))

        faturas = rows.order_by(Cliente.nome, ValoresFatura.mes_ref).all()

        return jsonify(
            [
                {
                    "cliente": fatura.cliente,
                    "numero_uc": fatura.numero_uc,
                    "mes_ref": fatura.mes_ref.strftime("%Y-%m"),
                    "valor_total": float(fatura.valor_total),
                    "vencimento": fatura.vencimento.strftime("%Y-%m-%d"),
                    "nome_pdf": fatura.nome_pdf,
                    "status": "validado",
                }
                for fatura in faturas
            ]
        )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
