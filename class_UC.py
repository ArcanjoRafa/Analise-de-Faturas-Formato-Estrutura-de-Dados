class UC:
    def __init__(self, pdf):
        self._uc = pdf.extrair_uc()
        self._endereco = pdf.extrair_endereco()
        self._cep = pdf.extrair_cep()

    @property
    def uc(self):
        return self._uc

    @uc.setter
    def uc(self, valor_uc):
        self._uc = valor_uc

    @property
    def endereco(self):
        return self._endereco

    @endereco.setter
    def endereco(self, valor_endereco):
        self._endereco = valor_endereco

    @property
    def cep(self):
        return self._cep

    @cep.setter
    def cep(self, valor_cep):
        self._cep = valor_cep
