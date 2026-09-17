import fitz
import pdfplumber
import re

class PdfReader:
    def __init__(self, pdf):
        self._pdf = pdf
        self.pdf_words = self.__words(0)
        self.pdf_words_type2 = self.__words_type2(0)
        self.pdf_text = self.__text(0)

    def __words(self, page):
        with pdfplumber.open(self._pdf) as pdf:
            first_page = pdf.pages[page]
            return first_page.extract_words()

    def __words_type2(self,page):
        with fitz.open(self._pdf) as pdf:
            return pdf[page].get_text("words", sort='true')

    def __text(self, page):
        with pdfplumber.open(self._pdf) as pdf:
            first_page = pdf.pages[page]
            return first_page.extract_text()

    def formato(self):
        with fitz.open(self._pdf) as pdf:
            tamanho = pdf[0].rect.width

        return "B" if tamanho > 600 else "A"

    def __dados_UC(self):
        match = re.search(r"\d+\.\d+\.\d+(?:\.\d+)?-\d{2}", self.pdf_text)
        if match:
            numero_uc = match.group(0)
            dados_UC = next(w for w in self.pdf_words if w['text'] == numero_uc)
            return dados_UC

    # UC
    def extrair_uc(self):
         return self.__dados_UC()['text']


    def extrair_endereco(self):
        dados_uc = self.__dados_UC()
        end = [w['text'] for w in self.pdf_words if dados_uc['top'] < w['top']
               <= dados_uc['top'] + 8 and w['x1'] < dados_uc['x0']]
        endereco = ' '.join(end)
        return endereco


    def extrair_cep(self):
        possiveis_ceps = []
        for w in self.pdf_words:
            if len(w['text']) == 8 and 178 <= w['top'] <= 186:
                possiveis_ceps.append(w)
        cep = possiveis_ceps[-1]['text']
        return cep

    _LOC_CLIENTE = {"x0": 50.040000915527344, "y0": 162.30575561523438}
    def __client_group(self):
        for word in self.pdf_words_type2:
            if (abs(word[0] - self._LOC_CLIENTE["x0"]) <= 3 and
                (self._LOC_CLIENTE["y0"] - 1) <= word[1] <= (self._LOC_CLIENTE["y0"] + 1)):
                return word[5]

    def extrair_nome_cliente(self):
        cliente = ""
        group = self.__client_group()
        for word in self.pdf_words_type2:
            if word[5] == group:
                cliente += word[4] + " "
        return cliente

    def extrair_cpf_cnpj(self):
        match = re.search(r"CNPJ/CPF(/RANI)?:\s*([0-9X./-]+)", self.pdf_text)
        if match:
            cpf_cnpj = match.group(2)
            return cpf_cnpj

    _MED_LOC = (39.0, 579.5043334960938, 69.36003112792969, 584.4683227539062)
    def __medidor_info(self):
        palavras = self.pdf_words_type2
        for p in palavras:
            if abs(p[1] - self._MED_LOC[1]) <= 3 and abs(p[0] - self._MED_LOC[0]) <= 3:
                medidor_group = p[5]
                medidor = p[4]
                return {"medidor": medidor, "grupo": medidor_group}

    def extrair_numero_medidor(self):
        medidor = self.__medidor_info()["medidor"]
        return medidor

    _LINHA_RESERVADO = 7
    def __valores(self):
        info_medidor = self.__medidor_info()
        medidor_grupo = info_medidor["grupo"]
        medidor = info_medidor["medidor"]
        palavras = self.pdf_words_type2
        medidor_valores = []
        for p in palavras:
            if p[5] == medidor_grupo:
                if p[6] != self._LINHA_RESERVADO:
                    if p[7] != 0:
                        medidor_valores[-1] += ' ' + p[4]
                    else:
                        if p[4] != medidor:
                            medidor_valores.append(p[4])
        return medidor_valores

    def extrair_tabela_medidor(self):
        valores = self.__valores()
        tabela = []
        inicio = 0
        final = 6
        for _ in range(0, len(valores), 6):
            tabela.append(valores[inicio: final])
            inicio = final
            final += 6
        return tabela

    _NOMES_LEITURAS = ['leitura anterior:', 'leitura atual:', 'n dias:', 'proxima leitura:']
    def extrair_leituras(self):
        leituras = {}

        match = re.search(r"\d{2}/\d{2}/\d{4}\s+\d{2}/\d{2}/\d{4}\s+\d+\s+\d{2}/\d{2}/\d{4}", self.pdf_text)

        if match:
            leituras_dados = match.group(0).split()
            for leitura, dado  in zip(self._NOMES_LEITURAS, leituras_dados):
                leituras[leitura] = dado
        return tuple(leituras.values())

    _PALAVRAS_CHAVES = ["PIS", "COFINS", "ICMS"]
    def extrair_tributos(self):
        palavras =  self.pdf_words_type2
        possiveis_tributos = []


        for p in palavras:
            if p[4] in self._PALAVRAS_CHAVES:
                possiveis_tributos.append(p)

        tributos_loc = [possiveis_tributos[-1], possiveis_tributos[-2], possiveis_tributos[-3]]

        tributos_info = {}
        for tributo in tributos_loc:
            tributos_val = [tributo[4]]
            for p in palavras:
                if abs(p[1] - tributo[1]) <= 3 and p[0] > tributo[2]:
                    tributos_val.append(p[4])
            tributos_info[tributo[4]] = tributos_val
        return tributos_info

    def valores_fatura(self):
        texto = self.pdf_text
        match = re.search(r'([A-Za-zÀ-ÿ]+\s*/\s*\d{4})\s+(\d{2}/\d{2}/\d{4})\s+R\$\s*([\d.]+,\d{2})', texto)
        if match:
            valores_fat = {
                "MES_REF": match.group(1),
                "VENCIMENTO": match.group(2),
                "PAGAR": match.group(3)
            }
            return valores_fat


    def __loc_total(self):
        for word in self.pdf_words_type2:
            if word[4] == "TOTAL:":
                return word

    def total(self):
        palavras = self.pdf_words_type2
        valores_totais = [p[4] for p in palavras if abs(p[1] - self.__loc_total()[1]) <= 3]
        return valores_totais

    def itens_fatura(self):
        palavras = self.pdf_words_type2

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