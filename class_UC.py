class UC:
    def __init__(self, numero_uc,  endereco, cep):
        self.__numero_uc = numero_uc
        self.__endereco = endereco
        self.__cep = cep

    @property
    def uc(self):
        return self.__numero_uc

    @uc.setter
    def uc(self, valor_numero_uc):
        self.__numero_uc = valor_numero_uc

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, valor_endereco):
        self.__endereco = valor_endereco

    @property
    def cep(self):
        return self.__cep

    @cep.setter
    def cep(self, valor_cep):
        self.__cep = valor_cep
