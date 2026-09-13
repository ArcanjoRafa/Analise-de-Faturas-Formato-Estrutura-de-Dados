

class Tributos:
    _PALAVRAS_CHAVES = ["PIS", "COFINS", "ICMS"]

    def __init__(self, pdf):
        self.pdf = pdf

    def tributos(self):
        palavras =  self.pdf.pdf_words_type2(0)
        possiveis_tributos = []


        for p in palavras:
            if p[4] in self._PALAVRAS_CHAVES:
                possiveis_tributos.append(p)

        tributos_loc = [possiveis_tributos[-1], possiveis_tributos[-2], possiveis_tributos[-3]]

        tributos_info = {}
        for tributo in tributos_loc:
            tributos_val = []
            for p in palavras:
                if abs(p[1] - tributo[1]) <= 3 and p[0] > tributo[2]:
                    tributos_val.append(p[4])
            tributos_info[tributo[4]] = tributos_val
        return tributos_info


