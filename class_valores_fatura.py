import re

class ValoresFatura:
    def __init__(self, valores):
        self.__mes_ref =  valores["MES_REF"]
        self.__vencimento = valores["VENCIMENTO"]
        self.__pagar = valores["PAGAR"]

    @property
    def mes_ref(self):
        return self.__mes_ref
    @mes_ref.setter
    def mes_ref(self, valor):
        self.__mes_ref = valor

    @property
    def vencimento(self):
        return self.__vencimento
    @vencimento.setter
    def vencimento(self, valor):
        self.__vencimento = valor
        
    @property
    def pagar(self):
        return self.__pagar
    @pagar.setter
    def pagar(self, valor):
        self.__pagar = valor