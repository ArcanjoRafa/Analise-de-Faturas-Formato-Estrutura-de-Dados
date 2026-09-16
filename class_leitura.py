
class Leitura:
    def __init__(self, pdf):
        leitura_anterior, leitura_atual, dias, proxima_leitura = pdf.extrair_leituras()
        self.__leitura_anterior = leitura_anterior
        self.__leitura_atual = leitura_atual
        self.__dias = dias
        self.__proxima_leitura = proxima_leitura

    @property
    def leitura_anterior(self):
        return self.__leitura_anterior
    @leitura_anterior.setter
    def leitura_anterior(self, valor_leitura_anterior):
        self.__leitura_anterior = valor_leitura_anterior

    @property
    def leitura_atual(self):
        return self.__leitura_atual

    @leitura_atual.setter
    def leitura_atual(self, valor_leitura_atual):
        self.__leitura_atual = valor_leitura_atual

    @property
    def dias(self):
        return self.__dias

    @dias.setter
    def dias(self, valor_dias):
        self.__dias = valor_dias

    @property
    def proxima_leitura(self):
        return self.__proxima_leitura

    @proxima_leitura.setter
    def proxima_leitura(self, valor_proxima_leitura):
        self.__proxima_leitura = valor_proxima_leitura