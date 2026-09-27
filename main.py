from visuals.pdf_visual import Visual
from pathlib import Path

pdfs_pasta = r"C:\Users\rafae\Downloads\pdfs_fatura"
dir_path = Path(pdfs_pasta)
path_files = list(dir_path.glob("*.pdf"))


pdf = Visual(path_files)
pdf.visualizar_pdf()

