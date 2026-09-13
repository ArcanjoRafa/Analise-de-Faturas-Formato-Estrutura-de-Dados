import re

class Leitura:
    _NOMES_LEITURAS = ['leitura anterior:', 'leitura atual:', 'n dias:', 'proxima leitura:']

    def __init__(self, pdf):
        self.pdf = pdf

    def leituras(self):
        leituras = {}

        texto = self.pdf.pdf_text(0)
        match = re.search(r"\d{2}/\d{2}/\d{4}\s+\d{2}/\d{2}/\d{4}\s+\d+\s+\d{2}/\d{2}/\d{4}", texto)

        if match:
            leituras_dados = match.group(0).split()
            for leitura, dado  in zip(Leitura._NOMES_LEITURAS, leituras_dados):
                leituras[leitura] = dado
        return leituras