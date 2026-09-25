from models.class_fatura import Fatura
from pathlib import Path
from time import sleep

pdfs_pasta = r"C:\Users\rafae\Downloads\pdfs_fatura"

dir_path = Path(pdfs_pasta)
path_files = list(dir_path.glob("*.pdf"))


def pdfs(pdfs):
    print("Todos os pdfs listados:")
    for num, pdf in enumerate(pdfs, 1):
        print(f"{num}) {pdf.stem}")
    print(f"total de pdfs: {len(pdfs)}")
    while True:
        try:
            pdf_escolhido = int(input("Visualizar pdf: "))
            return str(pdfs[pdf_escolhido - 1])
        except ValueError:
            print("Este comando é inválido")
        except IndexError:
            print("Nao existe nenhum pdf nesta posiçao")
        sleep(1)
        print("tente novamente")

pdf_escolhido = pdfs(path_files)
print(f"Gerando informaçoes do Pdf: {pdf_escolhido}")
sleep(1)

fatura = Fatura(pdf_escolhido)


print(f"{fatura.cliente.nome_cliente}.............................................................................. "
f"{fatura.leitura.leitura_anterior} {fatura.leitura.leitura_atual} {fatura.leitura.dias} {fatura.leitura.proxima_leitura}\n")
print(f"{fatura.uc.endereco} - {fatura.uc.cep}............... {fatura.uc.numero_uc}\n")
print(f"{fatura.cliente.cpf_cnpj}\n")
print(f"{fatura.valores_fatura.mes_ref}  {fatura.valores_fatura.vencimento}  {fatura.valores_fatura.pagar}\n")

for item in fatura.itens_fatura:
    print(f"{item.nome_item}...{item.unid}...{item.quant}...{item.preco_unit}...{item.valor_total}...{item.pis_cofins}"
          f"...{item.base_calc_icms}...{item.aliq_icms}...{item.icms}...{item.tarifa_unit}")



for tributo in fatura.tributos:
    print(f"{tributo.nome}......{tributo.base_calc}...{tributo.aliquota}...{tributo.valor}")
print("\n")

for valor in fatura.sumarios_eletricos:
    print(f"{fatura.medidor.numero_medidor}...{valor.grandeza}...{valor.posto_horario}...{valor.leitura_anterior}"
          f"...{valor.leitura_atual}..."
          f"{valor.const_medidor}...{valor.consumo_kwh}")