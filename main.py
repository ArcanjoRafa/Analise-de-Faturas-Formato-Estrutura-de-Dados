from visuals.pdf_visual import Visual
from pathlib import Path
from database.conection import Session
from database.persistencia import salvar_fatura
from models.class_fatura import Fatura

pdfs_pasta = r"C:\Users\rafae\Downloads\pdfs_fatura"
dir_path = Path(pdfs_pasta)
path_files = list(dir_path.glob("*.pdf"))


pdf = Visual(path_files)
# print(pdf.visualizar_pdf())

# fatura_escolhida = pdf.fatura()
# session = Session()
# salvar_fatura(fatura_escolhida, session)

numero = 0
for file in path_files:
     try:
         fatura = Fatura(str(file))
         with Session() as session:
             salvar_fatura(fatura, session)
             numero += 1
             print(f"O pdf {numero} foi salvo no banco com sucesso!")
     except Exception as erro:
         print(f"Erro em {file.stem}: {erro}")
