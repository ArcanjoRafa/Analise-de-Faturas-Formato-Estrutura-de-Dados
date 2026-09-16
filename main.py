from class_fatura import Fatura
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

def verifica_cpf(cpf):
    return 0

print(verifica_cpf(fatura.cpf_cnpj()))

