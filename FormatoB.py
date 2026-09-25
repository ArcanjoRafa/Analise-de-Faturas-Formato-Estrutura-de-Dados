from models.class_tributos import Tributo
from models.class_cliente import Cliente
from models.class_medidor import Medidor

class ClienteFormatoB(Cliente):
    _LOC_CLIENTE = {"x0": 15.720000267028809, "y0": 82.96173095703125}

class MedidorFormatoB(Medidor):
    _MED_LOC = (20.15999984741211, 577.8538208007812)


class EnderecoFormatoB:
    _ENDERECO_LOC = {"x0": 15.0, "y0": 99.90929412841797}
    _UC_LOC =  {"x0": 188.63999938964844, "y0": 108.62928009033203}
    def __init__(self, pdf):
        self.pdf = pdf

    def __encontrando_valores(self):
        cep = ""
        endereco = ""
        pdf_words = self.pdf.pdf_words_type2(0)
        for word in pdf_words:
            if abs(word[1] - self._ENDERECO_LOC["y0"]) <= 5 and word[2] < self._UC_LOC["x0"]:
                if word[6] == 0:
                    endereco += word[4] + " "
                if word[6] == 1:
                    cep += word[4] + " "
        return {"endereco": endereco, "cep": cep}

    def endereco(self):
        return self.__encontrando_valores()["endereco"]

    def cep(self):
        return self.__encontrando_valores()["cep"]


class TributosFormatoB(Tributo):
    _PALAVRAS_CHAVES = ["PIS/PASEP", "COFINS", "ICMS"]


class ItensDaFaturaFormatoB:
    _ITENS_DA_FATURA_LOC = {"x0": 7.920000076293945, "y0": 384.27130126953125}
    _TOTAL_LOC = {"x0": 133.1999969482422, "y0": 470.25909423828125}

    def __init__(self, pdf):
        self.pdf = pdf

    def total(self):
        pdf_words = self.pdf.pdf_words_type2(0)
        TOTAL_INFO = []
        for word in pdf_words:
            if abs(word[1] - self._TOTAL_LOC["y0"]) <= 3 and word[0] > self._TOTAL_LOC["x0"]:
                TOTAL_INFO.append(word[4])
        return TOTAL_INFO

    def __lista_de_itens(self):
        pdf_words = self.pdf.pdf_words_type2(0)
        lista_de_itens = []
        for word in pdf_words:
            if abs(word[1] > self._ITENS_DA_FATURA_LOC["y0"] + 3) and abs(word[1] < self._TOTAL_LOC["y0"] - 3):
                lista_de_itens.append(word)
        return lista_de_itens

    def itens_fatura(self):
        lista_de_itens = self.__lista_de_itens()
        itens_da_fatura = []
        itens = []
        itens_inciais_loc = []
        item_inicial = None
        for item in lista_de_itens:
            if lista_de_itens[0] == item:
                item_inicial = item
                itens_inciais_loc.append(item_inicial)
            else:
                if item[1] > item_inicial[1] + 5:
                    item_inicial = item
                    itens_inciais_loc.append(item_inicial)

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

        return itens_da_fatura

