from extractors.class_leitor_de_fatura import PdfReader

class PdfReaderFormatoB(PdfReader):
    _LOC_CLIENTE = {"x0": 15.720000267028809, "y0": 82.96173095703125}
    _MED_LOC = (20.15999984741211, 577.8538208007812)
    _PALAVRAS_CHAVES = ["PIS/PASEP", "COFINS", "ICMS"]

    _ENDERECO_LOC = {"x0": 15.0, "y0": 99.90929412841797}
    _UC_LOC = {"x0": 188.63999938964844, "y0": 108.62928009033203}

    def __encontrando_valores(self):
        cep = ""
        endereco = ""
        pdf_words = self.pdf_words_type2
        for word in pdf_words:
            if abs(word[1] - self._ENDERECO_LOC["y0"]) <= 5 and word[2] < self._UC_LOC["x0"]:
                if word[6] == 0:
                    endereco += word[4] + " "
                if word[6] == 1:
                    cep += word[4] + " "
        return {"endereco": endereco, "cep": cep}

    def extrair_endereco(self):
        return self.__encontrando_valores()["endereco"]

    def extrair_cep(self):
        return self.__encontrando_valores()["cep"]

    _ITENS_DA_FATURA_LOC = {"x0": 7.920000076293945, "y0": 384.27130126953125}
    _TOTAL_LOC = {"x0": 133.1999969482422, "y0": 470.25909423828125}

    _COLUNAS = {
        "titulo": (0, 85),
        "unid": (85, 99.8),
        "quant": (99.8, 121.8),
        "preco_unit": (121.8, 146.5),
        "valor": (146.5, 172.6),
        "pis_cofins": (172.6, 196.8),
        "base_calc_icms": (196.8, 221.3),
        "aliq_icms": (221.3, 242.1),
        "icms": (242.1, 258.4),
        "tarifa_unit": (258.4, 999),
    }
    _ORDEM_COLUNAS = ["titulo", "unid", "quant", "preco_unit", "valor",
                      "pis_cofins", "base_calc_icms", "aliq_icms", "icms", "tarifa_unit"]

    def extrair_total(self):
        pdf_words = self.pdf_words_type2
        return [w[4] for w in pdf_words
                if abs(w[1] - self._TOTAL_LOC["y0"]) <= 3 and w[0] > self._TOTAL_LOC["x0"]]

    def __lista_de_itens(self):
        pdf_words = self.pdf_words_type2
        return [w for w in pdf_words
                if w[1] > self._ITENS_DA_FATURA_LOC["y0"] + 3 and w[1] < self._TOTAL_LOC["y0"] - 3]

    def __merge_linhas(self, dados_fatura):
        itens = []
        atual = None
        for linha in dados_fatura:
            if linha[0] != "":
                if atual is not None:
                    itens.append(atual)
                atual = linha.copy()
            else:
                if atual is None:
                    atual = linha.copy()
                else:
                    for i in range(len(linha)):
                        if linha[i] != "":
                            if atual[i] == "":
                                atual[i] = linha[i]
                            else:
                                atual[i] += " " + linha[i]
        if atual is not None:
            itens.append(atual)
        return itens

    def extrair_itens_fatura(self):
        palavras = self.__lista_de_itens()

        linhas = {}
        for p in palavras:
            y = round(p[1], 1)
            linhas.setdefault(y, []).append(p)

        for y in linhas:
            linhas[y].sort(key=lambda p: p[0])

        dados_fatura = []
        for y, palavras_linha in linhas.items():
            linha = {coluna: "" for coluna in self._COLUNAS}
            for p in palavras_linha:
                x_meio = (p[0] + p[2]) / 2
                for coluna, (inicio, fim) in self._COLUNAS.items():
                    if inicio <= x_meio < fim:
                        linha[coluna] += p[4] + " "
                        break
            dados_fatura.append([linha[c].strip() for c in self._ORDEM_COLUNAS])

        return self.__merge_linhas(dados_fatura)