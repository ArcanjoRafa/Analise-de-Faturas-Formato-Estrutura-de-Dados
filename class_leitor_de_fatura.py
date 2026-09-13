import fitz
import pdfplumber

class PdfReader:
    def __init__(self, pdf):
        self._pdf = pdf

    def pdf_words(self, page):
        with pdfplumber.open(self._pdf) as pdf:
            first_page = pdf.pages[page]
            return first_page.extract_words()

    def pdf_words_type2(self, page):
        with fitz.open(self._pdf) as pdf:
            return pdf[page].get_text("words", sort='true')

    def pdf_text(self, page):
        with pdfplumber.open(self._pdf) as pdf:
            first_page = pdf.pages[page]
            return first_page.extract_text()

    def formato(self):
        with fitz.open(self._pdf) as pdf:
            tamanho = pdf[0].rect.width

        return "B" if tamanho > 600 else "A"


