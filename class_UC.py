import re

class UC:
    def __init__(self, pdf):
        self.pdf = pdf

    def _dados_UC(self):
        texto = self.pdf.pdf_text(0)
        match = re.search(r"\d+\.\d+\.\d+(?:\.\d+)?-\d{2}", texto)
        if match:
            numero_uc = match.group(0)
            dados_UC = next(w for w in self.pdf.pdf_words(0) if w['text'] == numero_uc)
            return dados_UC

    # UC
    def uc(self):
         return self._dados_UC()['text']


class Endereco:
    def __init__(self, pdf):
        self.pdf = pdf
        self.__uc = UC(self.pdf)

    def endereco(self):
        dados_uc = self.__uc._dados_UC()
        end = [w['text'] for w in self.pdf.pdf_words(0) if dados_uc['top'] < w['top']
               <= dados_uc['top'] + 8 and w['x1'] < dados_uc['x0']]
        endereco = ' '.join(end)
        return endereco

        # cep

    def cep(self):
        possiveis_ceps = []
        for w in self.pdf.pdf_words(0):
            if len(w['text']) == 8 and 178 <= w['top'] <= 186:
                possiveis_ceps.append(w)
        cep = possiveis_ceps[-1]['text']
        return cep