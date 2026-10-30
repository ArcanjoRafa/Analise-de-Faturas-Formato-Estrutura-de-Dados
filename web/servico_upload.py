# Regras de upload da página web: validação, alocação do arquivo na pasta,
# pipeline (Fatura -> salvar_fatura) e histórico da sessão (só visual, em memória).
import hashlib
import re
from datetime import datetime
from pathlib import Path

from database.conection import Session
from database.persistencia import salvar_fatura
from models.class_fatura import Fatura

# Pasta oficial de PDFs do sistema — a mesma que o main.py lê.
PASTA_PDFS = Path(r"C:\Users\rafae\Downloads\pdfs_fatura")
PASTA_PDFS.mkdir(parents=True, exist_ok=True)

# Caracteres proibidos em nomes de arquivo no Windows.
_CARACTERES_PROIBIDOS = re.compile(r'[\\/:*?"<>|]')

# Histórico em MEMÓRIA — decisão do dono: o histórico da página é apenas a
# visualização das tentativas desta sessão do servidor. Nada de tabela no
# banco nem no models. Zera quando o servidor reinicia; os registros de
# verdade são a fatura no banco e o PDF na pasta.
HISTORICO = []
_proximo_id = 1


class ErroValidacao(Exception):
    """Arquivo recusado antes de qualquer processamento (resposta HTTP 400)."""


def sanitizar_nome(nome):
    """Remove componentes de caminho e troca caracteres proibidos no Windows por '_'."""
    nome = Path(nome).name
    return _CARACTERES_PROIBIDOS.sub("_", nome)


def _hash_bytes(conteudo):
    return hashlib.sha256(conteudo).hexdigest()


def alocar_arquivo(nome, conteudo):
    """Decide onde o PDF fica em PASTA_PDFS. Questão de ARQUIVO — não define status.

    - Nome não existe na pasta: salva com o nome original.
    - Nome existe + conteúdo idêntico (SHA-256): não salva de novo,
      devolve o caminho do arquivo que já estava na pasta.
    - Nome existe + conteúdo diferente: salva com o próximo sufixo livre
      ("nome (2).pdf", "nome (3).pdf", ...) — o original nunca é sobrescrito.
    """
    caminho = PASTA_PDFS / nome
    if not caminho.exists():
        caminho.write_bytes(conteudo)
        return caminho
    if _hash_bytes(conteudo) == _hash_bytes(caminho.read_bytes()):
        return caminho
    numero = 2
    while True:
        candidato = PASTA_PDFS / f"{caminho.stem} ({numero}){caminho.suffix}"
        if not candidato.exists():
            candidato.write_bytes(conteudo)
            return candidato
        numero += 1


def processar_upload(nome_original, conteudo):
    """Fluxo completo de um arquivo enviado pela página.

    - Extensão que não seja .pdf levanta ErroValidacao (HTTP 400, sem histórico).
    - O pipeline (Fatura + salvar_fatura) roda SEMPRE que o arquivo é um PDF:
      estar na pasta NÃO marca duplicado — o único critério de DUPLICADO é
      salvar_fatura devolver ("DUPLICADO", None), ou seja, UC + mês de
      referência já estarem no banco.
    - Exceção em qualquer ponto do pipeline -> status FALHA com a mensagem.
      O arquivo permanece na pasta.

    Devolve {"status": "SUCESSO" | "DUPLICADO" | "FALHA", "mensagem": ...}.
    """
    nome = sanitizar_nome(nome_original)
    if not nome.lower().endswith(".pdf"):
        raise ErroValidacao("Apenas arquivos .pdf são aceitos.")

    caminho_final = alocar_arquivo(nome, conteudo)

    try:
        fatura = Fatura(str(caminho_final))
        with Session() as session:
            resultado, _fatura_id = salvar_fatura(fatura, session)
        status = resultado  # "SUCESSO" ou "DUPLICADO"
        erro = None
    except Exception as excecao:
        status = "FALHA"
        erro = str(excecao)

    registrar_historico(nome, caminho_final.name, status, erro)

    if status == "SUCESSO":
        mensagem = "Fatura salva no banco de dados com sucesso."
    elif status == "DUPLICADO":
        mensagem = "Fatura duplicada: esta UC + mês de referência já está no banco."
    else:
        mensagem = f"Falha ao processar o PDF: {erro}"

    return {"status": status, "mensagem": mensagem}


def registrar_historico(nome_pdf, nome_arquivo_salvo, status, erro):
    """Guarda a tentativa na memória do servidor — o histórico é só visual."""
    global _proximo_id
    HISTORICO.append({
        "id": _proximo_id,
        "nome_pdf": nome_pdf,
        "nome_arquivo_salvo": nome_arquivo_salvo,
        "data_upload": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "erro": erro if status == "FALHA" else None,
    })
    _proximo_id += 1


def buscar_historico():
    """Tentativas desta sessão do servidor, mais recente primeiro."""
    return list(reversed(HISTORICO))


def obter_linha_historico(id_registro):
    """Busca uma linha do histórico da sessão pelo id; devolve None se não existir."""
    for linha in HISTORICO:
        if linha["id"] == id_registro:
            return linha
    return None
