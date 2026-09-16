
class Tributo:
    def __init__(self, tributo):
        self.__nome = tributo[0]
        self.__base_calc = tributo[1]
        self.__aliquota = tributo[2]
        self.__valor = tributo[3]

    @property
    def base_calc(self):
        return self.__base_calc
    @base_calc.setter
    def base_calc(self, valor):
        self.__base_calc = valor

    @property
    def aliquota(self):
        return self.__aliquota
    @aliquota.setter
    def aliquota(self, valor):
        self.__aliquota = valor

    @property
    def valor(self):
        return self.__valor
    @valor.setter
    def valor(self, valor):
        self.__valor = valor




