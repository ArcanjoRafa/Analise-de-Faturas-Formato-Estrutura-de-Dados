import re

class Cliente:
    _LOC_CLIENTE = {"x0": 50.040000915527344, "y0": 162.30575561523438}
    def __init__(self, pdf):
        self.pdf = pdf

    def __client_group(self):
        for word in self.pdf.pdf_words_type2(0):
            if (abs(word[0] - self._LOC_CLIENTE["x0"]) <= 3 and
                (self._LOC_CLIENTE["y0"] - 1) <= word[1] <= (self._LOC_CLIENTE["y0"] + 1)):
                return word[5]

    def cliente(self):
        cliente = ""
        group = self.__client_group()
        for word in self.pdf.pdf_words_type2(0):
            if word[5] == group:
                cliente += word[4] + " "
        return cliente

    def cpf_cnpj(self):
        texto = self.pdf.pdf_text(0)
        match = re.search(r"CNPJ/CPF(/RANI)?:\s*([0-9X./-]+)", texto)
        if match:
            cpf_cnpj = match.group(2)
            return cpf_cnpj