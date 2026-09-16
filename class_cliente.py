class Cliente:
    def __init__(self, nome_cliente, cpf_cnpj):
        self.__nome_cliente = nome_cliente
        self.__cpf_cnpj = cpf_cnpj

    @property
    def cliente(self):
        return self.__nome_cliente

    @cliente.setter
    def cliente(self, valor_cliente):
        self.__nome_cliente = valor_cliente

    @property
    def cpf_cnpj(self):
        return self.__cpf_cnpj

    @cpf_cnpj.setter
    def cpf_cnpj(self, valor_cpf_cnpj):
        self.__cpf_cnpj = valor_cpf_cnpj