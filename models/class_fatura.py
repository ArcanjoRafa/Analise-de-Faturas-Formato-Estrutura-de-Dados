from models.class_cliente import Cliente
from class_UC import UnidadeConsumidora
from class_valores_fatura import ValoresFatura
from class_leitura import Leitura
from class_itensdafatura import ItemDaFatura
from class_medidor import Medidor, SumarioEletrico
from class_tributos import Tributo
from extractors.class_leitor_de_fatura import PdfReader
from extractors.class_leitor_de_fatura_formatoB import PdfReaderFormatoB
import logging
logging.basicConfig(level=logging.WARNING)


class Fatura:
    def __init__(self, pdf):
        formato = PdfReader.formato(pdf)
        if formato == "A":
            self.pdf = PdfReader(pdf)
        else:
            self.pdf = PdfReaderFormatoB(pdf)

        nome_cliente = self.pdf.extrair_nome_cliente()
        cpf_cnpj = self.pdf.extrair_cpf_cnpj()
        valor_endereco = self.pdf.extrair_endereco()
        valor_cep = self.pdf.extrair_cep()
        valor_uc = self.pdf.extrair_uc()
        leitura_anterior, leitura_atual, dias, proxima_leitura = self.pdf.extrair_leituras()
        pis, cofins, icms = self.pdf.extrair_tributos()
        valor_medidor = self.pdf.extrair_numero_medidor()
        mes_ref, vencimento, pagar = self.pdf.extrair_valores_fatura()
        tabela = self.pdf.extrair_tabela_medidor()
        itens = self.pdf.extrair_itens_fatura()


        self.cliente = Cliente(nome_cliente, cpf_cnpj)
        self.uc = UnidadeConsumidora(valor_uc, valor_endereco, valor_cep)
        self.leitura = Leitura(leitura_anterior, leitura_atual, dias, proxima_leitura)
        self.tributos = [Tributo(*pis), Tributo(*cofins), Tributo(*icms)]
        self.medidor = Medidor(valor_medidor)
        self.sumarios_eletricos = []
        for linha in tabela:
            if len(linha) < 6:
                linha[-1] = tabela[-2][-2]
                logging.warning(f"Sumário elétrico incompleto, campo(s) faltando: {linha}")
                linha = linha + [None] * (6 - len(linha))
            sumario = SumarioEletrico(*linha)
            self.sumarios_eletricos.append(sumario)
        self.valores_fatura = ValoresFatura(mes_ref, vencimento, pagar)
        self.itens_fatura = [ItemDaFatura(*item) for item in itens]
