import fitz
from extractors.class_leitor_de_fatura import  PdfReader
pdf_test = r"C:\Users\rafae\Downloads\Energisa_2026-10_1.875.449.017-57.pdf"
pdf_test2 = r"C:\Users\rafae\Downloads\Energisa_2026-06_CENTRAL_MATRIZ.pdf"

test = PdfReader(pdf_test)

words_pdf =test.pdf_words_type2

for w in words_pdf:
    if 578 <= w[1] <= 640:
        print(w)
