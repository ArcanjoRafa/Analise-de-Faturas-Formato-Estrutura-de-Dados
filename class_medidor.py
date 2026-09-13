
class Medidor:
    _MED_LOC = (39.0, 579.5043334960938, 69.36003112792969, 584.4683227539062)
    _LINHA_RESERVADO = 7
    def __init__(self, pdf):
        self.pdf_words = pdf.pdf_words_type2(0)


    def __medidor_info(self):
        palavras = self.pdf_words
        for p in palavras:
            if abs(p[1] - self._MED_LOC[1]) <= 3 and abs(p[0] - self._MED_LOC[0]) <= 3:
                medidor_group = p[5]
                medidor = p[4]
                return {"medidor": medidor, "grupo": medidor_group}

    def __valores(self):
        info_medidor = self.__medidor_info()
        medidor_grupo = info_medidor["grupo"]
        medidor = info_medidor["medidor"]
        palavras = self.pdf_words
        medidor_valores = []
        for p in palavras:
            if p[5] == medidor_grupo:
                if p[6] != Medidor._LINHA_RESERVADO:
                    if p[7] != 0:
                        medidor_valores[-1] += ' ' + p[4]
                    else:
                        if p[4] != medidor:
                            medidor_valores.append(p[4])
        return medidor_valores

    def tabela_de_valores(self):
        valores = self.__valores()
        tabela = []
        inicio = 0
        final = 6
        for _ in range(0, len(valores), 6):
            tabela.append(valores[inicio: final])
            inicio = final
            final += 6
        return tabela