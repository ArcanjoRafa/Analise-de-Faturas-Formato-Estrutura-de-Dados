

class ItensDaFatura:
    def __init__(self, pdf):
        self.pdf = pdf.pdf_words_type2(0)


    def __loc_total(self):
        for word in self.pdf:
            if word[4] == "TOTAL:":
                return word

    def total(self):
        palavras = self.pdf
        valores_totais = [p[4] for p in palavras if abs(p[1] - self.__loc_total()[1]) <= 3]
        return valores_totais

    def itens_fatura(self):
        palavras = self.pdf

        for p in palavras:
            if p[4] == 'Itens':
                itens_fatura_loc = p

        colunas = {
            'Itens da fatura': (0, 135),
            'Unid.': (135, 180),
            'Quant.': (180, 214),
            'Preço unit c tributo': (214, 250),
            'Valor': (250, 282),
            'PIS/COFINS': (282, 318),
            'Base calc ICMS': (318, 352),
            'Aliq ICMS': (352, 380),
            'ICMS': (380, 410),
            'Tarifa unit': (410, 433)
        }

        linhas = {}
        for p in palavras:
            if itens_fatura_loc[1] + 3 < p[1] < self.__loc_total()[1] and p[0] < 433:
                y = round(p[1], 1)
                if y not in linhas:
                    linhas[y] = []
                linhas[y].append(p)

        for y in linhas:
            linhas[y].sort(key=lambda p: p[0])

        ordem_colunas = [
            'Itens da fatura',
            'Unid.',
            'Quant.',
            'Preço unit c tributo',
            'Valor',
            'PIS/COFINS',
            'Base calc ICMS',
            'Aliq ICMS',
            'ICMS',
            'Tarifa unit'
        ]

        dados_fatura = []
        for y, palavras_linha in linhas.items():
            linha = {coluna: "" for coluna in colunas}

            for p in palavras_linha:
                x_meio = (p[0] + p[2]) / 2

                for coluna, (inicio, fim) in colunas.items():
                    if inicio <= x_meio < fim:
                        linha[coluna] += p[4] + " "
                        break
            dados_fatura.append([linha[coluna].strip() for coluna in ordem_colunas])

        linhas_corrigidas = []
        i = 0
        while i < len(dados_fatura):
            linha_atual = dados_fatura[i]

            # verifica se só tem descrição preenchida
            valores = [x for x in linha_atual[1:] if x != ""]
            if len(valores) == 0 and linha_atual[0] != "" and i + 1 < len(dados_fatura):
                proxima = dados_fatura[i + 1]
                nova_linha = [
                    linha_atual[j] if linha_atual[j] else proxima[j]
                    for j in range(len(linha_atual))
                ]
                linhas_corrigidas.append(nova_linha)
                i += 2
            else:
                linhas_corrigidas.append(linha_atual)
                i += 1

        linhas_finais = []
        for linha in linhas_corrigidas:
            if linha[0] == "":
                if linhas_finais:
                    linha_anterior = linhas_finais[-1]
                    for i in range(len(linha)):
                        if linha[i] != "":
                            if linha_anterior[i] == "":
                                linha_anterior[i] = linha[i]
                            else:
                                linha_anterior[i] += " " + linha[i]
                else:
                    linhas_finais.append(linha)
            else:
                linhas_finais.append(linha)

        return linhas_finais

    def itens_num(self):
        return len(self.itens_fatura())

