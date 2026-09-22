from class_leitor_de_fatura import PdfReader
from class_leitor_de_fatura_formatoB import PdfReaderFormatoB
from class_medidor import Medidor, SumarioEletrico
from class_cliente import Cliente
from class_UC import UnidadeConsumidora

pdf1 = r"C:\Users\Allvar\Downloads\Energisa_2026-08_1.377.997.017-49.pdf"
pdf2 = r"C:\Users\rafae\Downloads\Energisa_2026-05_1.769.293.017-27.pdf"

pdf_formatoB = PdfReaderFormatoB(pdf2)
extrair_cliente = pdf_formatoB.extrair_nome_cliente()
extrair_cpf = pdf_formatoB.extrair_cpf_cnpj()
extrair_uc = pdf_formatoB.extrair_uc()
extrair_cep = pdf_formatoB.extrair_cep()
extrair_endereco = pdf_formatoB.extrair_endereco()
medidor_extraido = pdf_formatoB.extrair_numero_medidor()
tabela_medidor_extraido = pdf_formatoB.extrair_tabela_medidor()[0]

# pdf_uc = UnidadeConsumidora(numero_uc=extrair_uc, endereco=extrair_endereco, cep=extrair_cep)
# pdf_cliente = Cliente(nome_cliente=extrair_cliente, cpf_cnpj=extrair_cpf)
# print(f"nome cliente: {pdf_cliente.nome_cliente} -------------- cpf/cnpj: {pdf_cliente.cpf_cnpj}")
# print(f"numero uc: {pdf_uc.numero_uc}\nendereco: {pdf_uc.endereco}\ncep: {pdf_uc.cep}")

medidor = Medidor(numero_medidor=medidor_extraido)
tabela = SumarioEletrico(tabela_medidor_extraido[0], tabela_medidor_extraido[1], tabela_medidor_extraido[2],
                       tabela_medidor_extraido[3], tabela_medidor_extraido[4],tabela_medidor_extraido[5])

print(medidor)
print(tabela)