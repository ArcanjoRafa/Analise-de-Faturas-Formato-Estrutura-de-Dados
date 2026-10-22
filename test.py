import fitz
from extractors.class_leitor_de_fatura import  PdfReader
pdf_test = r"C:\Users\rafae\Downloads\Energisa_2026-10_1.875.449.017-57.pdf"
pdf_test2 = r"C:\Users\rafae\Downloads\Energisa_2026-10_INTEGRAÇAO_MATRIZ_1.613.502.017-10.pdf"
pdf_test3 = r"C:\Users\rafae\Downloads\Energisa_2026-09_INTEGRAÇAO_MATRIZ_1.613.502.017-10.pdf"
#
test = PdfReader(pdf_test2)
words_pdf =test.pdf_words_type2

DATA_APRE_LOC = {"x0": 419.6938171386719, "y0": 95.9293212890625}
DATA_APRE_LOC_B = {"x0": 215.1900634765625, "y0": 666.2974853515625 }

# for w in words_pdf:
#     if abs(w[0] - DATA_APRE_LOC["x0"]) <= 3 and abs(w[1] - DATA_APRE_LOC["y0"]) <= 3:
#         data = w[4].split(":")[-1]
#         print(data)

for w in words_pdf:
    if abs(w[0] - DATA_APRE_LOC_B["x0"]) <= 3 and abs(w[1] - DATA_APRE_LOC_B["y0"]) <= 3:
            data = w[4].split(":")[-1]
            print(data)