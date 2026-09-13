import fitz

pdf = r"C:\Users\rafae\Downloads\Energisa_2026-05_1.769.293.017-27.pdf"

with fitz.open(pdf) as pdf:
    pdf_words = pdf[0].get_text("words", sort=True)

ITENS_DA_FATURA_LOC = {"x0": 7.920000076293945, "y0": 384.27130126953125}
TOTAL_LOC = {"x0": 133.1999969482422, "y0": 470.25909423828125}


# valores do total
TOTAL_INFO = []
for word in pdf_words:
    if abs(word[1] - TOTAL_LOC["y0"]) <= 3 and word[0] > TOTAL_LOC["x0"]:
        TOTAL_INFO.append(word[4])
print(TOTAL_INFO)

lista_de_itens = []
for word in pdf_words:
    if abs(word[1] > ITENS_DA_FATURA_LOC["y0"] + 3) and abs(word[1] < TOTAL_LOC["y0"] - 3):
        lista_de_itens.append(word)

itens_da_fatura = []
itens = []
itens_inciais_loc = []
item_inicial = None
for item in lista_de_itens:
    if lista_de_itens[0] == item:
        item_inicial = item
        itens_inciais_loc.append(item_inicial)
        print(item_inicial)
    else:
        if item[1] > item_inicial[1] + 5:
            item_inicial = item
            itens_inciais_loc.append(item_inicial)
            print(item_inicial)

titulo = ""
for inicial in itens_inciais_loc:
    for item in lista_de_itens:
        if abs(item[1] - inicial[1]) <= 2:
            if item[5] == inicial[5] and item[6] == inicial[6]:
                titulo += item[4] + " "
            else:
                itens.append(item[4])
    itens.insert(0, titulo)

    itens_da_fatura.append(itens)
    itens = []
    titulo = ""






