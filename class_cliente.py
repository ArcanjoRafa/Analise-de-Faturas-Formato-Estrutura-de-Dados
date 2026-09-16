class Cliente:
    def __init__(self, pdf):
        self._cliente = pdf.extrair_nome_cliente()
        self._cpf_cnpj = pdf.extrair_cpf_cnpj()

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, valor_cliente):
        self._cliente = valor_cliente

    @property
    def cpf_cnpj(self):
        return self._cpf_cnpj

    @cpf_cnpj.setter
    def cpf_cnpj(self, valor_cpf_cnpj):
        self._cpf_cnpj = valor_cpf_cnpj