from class_cliente import Cliente
from class_UC import Endereco, UC
from class_valores_fatura import ValoresFatura
from class_leitura import Leitura
from class_itensdafatura import ItensDaFatura
from class_medidor import Medidor
from class_tributos import Tributos
from class_leitor_de_fatura import PdfReader
from FormatoB import ClienteFormatoB, MedidorFormatoB, TributosFormatoB, EnderecoFormatoB, ItensDaFaturaFormatoB

class Fatura:
    def __init__(self, pdf):
        self.__pdf = PdfReader(pdf)
        formato = self.__pdf.formato()
        if formato == "A":
            self.__cliente = Cliente(self.__pdf)
            self.__campo_endereco = Endereco(self.__pdf)
            self.__itens_da_fatura = ItensDaFatura(self.__pdf)
            self.__medidor_val = Medidor(self.__pdf)
            self.__tributos_val = Tributos(self.__pdf)
        else:
            self.__cliente = ClienteFormatoB(self.__pdf)
            self.__campo_endereco = EnderecoFormatoB(self.__pdf)
            self.__itens_da_fatura = ItensDaFaturaFormatoB(self.__pdf)
            self.__medidor_val = MedidorFormatoB(self.__pdf)
            self.__tributos_val = TributosFormatoB(self.__pdf)
        self.__uc = UC(self.__pdf)
        self.__valores = ValoresFatura(self.__pdf)
        self.__leituras_fat = Leitura(self.__pdf)

    # nome do cliente
    def nome_cliente(self):
        return self.__cliente.cliente()

    # numero da uc
    def numero_uc(self):
        return self.__uc.uc()

    # endereco
    def endereco(self):
        return self.__campo_endereco.endereco()

    # cep
    def numero_cep(self):
        return self.__campo_endereco.cep()

    # valores da fatura
    def valores_da_fatura(self):
        return self.__valores.valores_fatura()

    # leituras
    def leituras(self):
        return  self.__leituras_fat.leituras()

    # itens da fatura
    def itens_fatura(self):
        return self.__itens_da_fatura.itens_fatura()

    # valor total dos intes da fatura
    def itens_total(self):
        return self.__itens_da_fatura.total()

    # medidor
    def medidor(self):
        return self.__medidor_val.tabela_de_valores()

    # tributos
    def tributos(self):
        return self.__tributos_val.tributos()

    def cpf_cnpj(self):
        return self.__cliente.cpf_cnpj()