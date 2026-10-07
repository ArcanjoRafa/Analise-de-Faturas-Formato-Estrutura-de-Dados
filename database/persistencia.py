from database.models import Cliente, UnidadeConsumidora, Medidor, ValoresFatura
from datetime import datetime
from decimal import Decimal


def salvar_fatura(fatura, session):
    # VERIFICA SE O CLIENTE EXISTE NO BANCO, CASO NAO EXISTA ELE É INSERIDO
    cliente_existe = session.query(Cliente).filter_by(cpf_cnpj= fatura.cliente.cpf_cnpj).first()
    if cliente_existe:
        cliente_db = cliente_existe
    else:
        cliente_db = Cliente(nome=fatura.cliente.nome_cliente, cpf_cnpj=fatura.cliente.cpf_cnpj)
        session.add(cliente_db)
        session.commit()
        print("cliente e cpf/cnpj adicionados no banco de dados")

    # VERIFICA SE A UNIDADE CONSUMIDORA EXISTE NO BANCO, CASO NAO EXISTA ELA É INSERIDA
    uc_existe = session.query(UnidadeConsumidora).filter_by(uc= fatura.uc.numero_uc).first()
    if uc_existe:
        uc_db = uc_existe
    else:
        uc_db = UnidadeConsumidora(uc=fatura.uc.numero_uc, cep=fatura.uc.cep, endereco=fatura.uc.endereco,
                                   cliente_id = cliente_db.id)
        session.add(uc_db)
        session.commit()

    medidor_existe = session.query(Medidor).filter_by(numero= fatura.medidor.numero_medidor).first()
    if medidor_existe:
        medidor_db = medidor_existe
    else:
        medidor_db = Medidor(numero=fatura.medidor.numero_medidor)
        session.add(medidor_db)
        session.commit()

    uc_id_existe = session.query(ValoresFatura).filter_by(uc_id=uc_db.id, mes_ref=fatura.valores_fatura.mes_ref).first()
    if uc_id_existe:
        print("Fatura ja existe no banco de dados")
        return

    valor = fatura.valores_fatura.pagar.replace(".", "").replace(",", ".")
    vencimento = datetime.strptime(fatura.valores_fatura.vencimento, "%d/%m/%Y").date()

    valorfatura_db = ValoresFatura(valor_total=Decimal(valor),
                                    vencimento=vencimento,
                                    mes_ref = fatura.valores_fatura.mes_ref,
                                    uc_id=uc_db.id, medidor_id= medidor_db.id)
    session.add(valorfatura_db)
    session.commit()