from visuals.pdf_visual import Visual
from pathlib import Path
from database.conection import Session
from database.persistencia import salvar_fatura

pdfs_pasta = r"C:\Users\rafae\Downloads\pdfs_fatura"
dir_path = Path(pdfs_pasta)
path_files = list(dir_path.glob("*.pdf"))


pdf = Visual(path_files)
print(pdf.visualizar_pdf())

# fatura_escolhida = pdf.fatura()

# session = Session()
#
# salvar_fatura(fatura_escolhida, session)


"""
for file in path_files:
fatura = Fatura(file)

session = Session()

salvar_fatura(fatura, session)

"""