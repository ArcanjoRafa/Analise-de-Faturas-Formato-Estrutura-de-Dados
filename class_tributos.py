

class Tributos:
    def __init__(self, pdf):
        self.__pis = pdf.tributos()["PIS"]
        self.__cofins = pdf.tributos()["COFINS"]
        self.__icms = pdf.tributos()["ICMS"]




