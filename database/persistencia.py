from database.models import Cliente, UnidadeConsumidora, Medidor, ValoresFatura, SumarioEletrico, Tributo, Leitura, ItemDaFatura
from datetime import datetime
from datetime import date
from decimal import Decimal
import re


def para_decimal(texto):
    if texto is None or texto.strip() == "":
        return None
    return Decimal(texto.strip().replace(".", "").replace(",", "."))

def para_data(texto):
    return datetime.strptime(texto, "%d/%m/%Y").date()

MESES = {"JAN": 1, "FEV": 2, "MAR": 3, "ABR": 4, "MAI": 5, "JUN": 6,
         "JUL": 7, "AGO": 8, "SET": 9, "OUT": 10, "NOV": 11, "DEZ": 12}

def para_mes_ref(texto):
    mes, ano = texto.split("/")
    return date(int(ano), MESES[mes.strip()[:3].upper()], 1)


def salvar_fatura(fatura, session):
    # VERIFICA SE O CLIENTE EXISTE NO BANCO, CASO NAO EXISTA ELE É INSERIDO
    if "X" not in fatura.cliente.cpf_cnpj and "*" not in fatura.cliente.cpf_cnpj:
        cliente_existe = session.query(Cliente).filter_by(cpf_cnpj= fatura.cliente.cpf_cnpj).first()
    else:
        cpf_formatado = re.sub(r"[xX.*]+", "%", fatura.cliente.cpf_cnpj)
        cliente_existe = session.query(Cliente).filter(Cliente.cpf_cnpj.like(cpf_formatado)).first()
        if not cliente_existe:
             raise Exception("Cliente nao encontrado!")

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

    mes_ref = para_mes_ref(fatura.valores_fatura.mes_ref)
    uc_id_existe = session.query(ValoresFatura).filter_by(uc_id=uc_db.id, mes_ref= mes_ref).first()
    if uc_id_existe:
        print("Fatura ja existe no banco de dados")
        return

    valor = para_decimal(fatura.valores_fatura.pagar)
    vencimento = para_data(fatura.valores_fatura.vencimento)

    valorfatura_db = ValoresFatura(valor_total=Decimal(valor),
                                    vencimento=vencimento,
                                    mes_ref = mes_ref,
                                    data_apresentacao=para_data(fatura.valores_fatura.apresentacao)
                                        if fatura.valores_fatura.apresentacao else None,
                                    nome_pdf = fatura.nome_pdf,
                                    uc_id=uc_db.id, medidor_id= medidor_db.id)
    session.add(valorfatura_db)
    session.commit()

    for sumario in fatura.sumarios_eletricos:
        sumario_db = SumarioEletrico(
            grandeza=sumario.grandeza,
            posto_h=sumario.posto_h,
            l_anterior=para_decimal(sumario.l_anterior),
            l_atual=para_decimal(sumario.l_atual),
            const=para_decimal(sumario.const),
            consumo=para_decimal(sumario.consumo),
            medidor_id=medidor_db.id,
            fatura_id=valorfatura_db.id,
        )
        session.add(sumario_db)


    nomes_tributos = ("PIS", "COFINS", "ICMS")

    for nome, tributo in zip(nomes_tributos, fatura.tributos):
        tributo_db = Tributo(
            nome=nome,
            base_calc=para_decimal(tributo.base_calc),
            aliquota=para_decimal(tributo.aliquota),
            valor=para_decimal(tributo.valor),
            fatura_id=valorfatura_db.id,
        )
        session.add(tributo_db)

    leitura_db = Leitura(
        l_anterior=para_data(fatura.leitura.l_anterior),
        l_atual=para_data(fatura.leitura.l_atual),
        dias=int(fatura.leitura.dias),
        l_proxima=para_data(fatura.leitura.l_proxima),
        fatura_id=valorfatura_db.id,
    )
    session.add(leitura_db)

    for item in fatura.itens_fatura:
        item_db = ItemDaFatura(
            nome_item=item.nome_item,
            unid=item.unid or None,
            quant=para_decimal(item.quant),
            preco_unit=para_decimal(item.preco_unit),
            valor_total=para_decimal(item.valor_total),
            pis_cofins=para_decimal(item.pis_cofins),
            base_calc_icms=para_decimal(item.base_calc_icms),
            aliq_icms=para_decimal(item.aliq_icms),
            icms=para_decimal(item.icms),
            tarifa_unit=para_decimal(item.tarifa_unit),
            fatura_id=valorfatura_db.id,
        )
        session.add(item_db)

    session.commit()