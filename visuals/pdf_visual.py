from time import sleep
from models.class_fatura import Fatura

class Visual:
    def __init__(self, path):
        self.pdfs = path

    def __pdfs(self):
        print("Todos os pdfs listados:")
        for num, pdf in enumerate(self.pdfs, 1):
            print(f"{num}) {pdf.stem}")
        print(f"total de pdfs: {len(self.pdfs)}")
        while True:
            try:
                pdf_escolhido = int(input("Visualizar pdf: "))
                return str(self.pdfs[pdf_escolhido - 1])
            except ValueError:
                print("Este comando é inválido")
            except IndexError:
                print("Nao existe nenhum pdf nesta posiçao")
            sleep(1)
            print("tente novamente")

    def __pdf_escolhido(self):
        pdf_escolhido = self.__pdfs()
        return Fatura(pdf_escolhido)

    def visualizar_pdf(self):
        while True:
            fatura = self.__pdf_escolhido()  # uma única vez

            print(
                f"{fatura.cliente.nome_cliente}.............................................................................. "
                f"{fatura.leitura.leitura_anterior} {fatura.leitura.leitura_atual}"
                f" {fatura.leitura.dias} {fatura.leitura.proxima_leitura}\n")
            print(f"{fatura.uc.endereco} - {fatura.uc.cep}............... "
                  f"{fatura.uc.numero_uc}\n")
            print(f"{fatura.cliente.cpf_cnpj}\n")
            print(f"{fatura.valores_fatura.mes_ref}  {fatura.valores_fatura.vencimento}  "
                  f"{fatura.valores_fatura.pagar}\n")

            for item in fatura.itens_fatura:
                print(
                    f"{item.nome_item}...{item.unid}...{item.quant}...{item.preco_unit}...{item.valor_total}...{item.pis_cofins}"
                    f"...{item.base_calc_icms}...{item.aliq_icms}...{item.icms}...{item.tarifa_unit}")

            for tributo in fatura.tributos:
                print(f"{tributo.nome}......{tributo.base_calc}...{tributo.aliquota}...{tributo.valor}")
            print("\n")

            for valor in fatura.sumarios_eletricos:
                print(
                    f"{fatura.medidor.numero_medidor}...{valor.grandeza}...{valor.posto_horario}..."
                    f"{valor.leitura_anterior}"
                    f"...{valor.leitura_atual}..."
                    f"{valor.const_medidor}...{valor.consumo_kwh}")
            sleep(1)
            try:
                resposta = input("DESEJA VISUALIZAR MAIS ALGUM PDF?[S/N]: ").capitalize()[0]
                if resposta != "S":
                    return
            except IndexError:
                return
