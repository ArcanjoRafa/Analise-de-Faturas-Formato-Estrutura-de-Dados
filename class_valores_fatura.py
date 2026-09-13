import re

class ValoresFatura:
    def __init__(self, pdf):
        self.pdf = pdf

    def valores_fatura(self):
        texto = self.pdf.pdf_text(0)
        match = re.search(r'([A-Za-zÀ-ÿ]+\s*/\s*\d{4})\s+(\d{2}/\d{2}/\d{4})\s+R\$\s*([\d.]+,\d{2})', texto)
        if match:
            valores_fat = {
                "MES_REF": match.group(1),
                "VENCIMENTO": match.group(2),
                "PAGAR": match.group(3)
            }
            return  valores_fat