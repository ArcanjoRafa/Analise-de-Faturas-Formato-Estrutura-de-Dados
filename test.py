from class_leitor_de_fatura import PdfReader
from class_medidor import Medidor

pdf1 = r"C:\Users\Allvar\Downloads\Energisa_2026-08_1.377.997.017-49.pdf"
fatura1 = PdfReader(pdf1)

fatura1_medidor = fatura1.extrair_numero_medidor()

medidor1 = Medidor(fatura1_medidor)
print(medidor1)