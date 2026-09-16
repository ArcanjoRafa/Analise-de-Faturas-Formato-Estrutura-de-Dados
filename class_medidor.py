
class Medidor:
    def __init__(self, medidor):
        self.__numero_medidor = medidor


        tabela = pdf.extrair_tabela_medidor()
        self.__sumarios_eletricos = []
        for linha in tabela:
            sumario = SumarioEletrico(linha[1], linha[2], linha[3], linha[4], linha[5])
            self.__sumarios_eletricos.append(sumario)

    @property
    def numero_medidor(self):
        return self.__numero_medidor

    @numero_medidor.setter
    def numero_medidor(self, valor):
        self.__numero_medidor = valor

    @property
    def sumarios_eletricos(self):
        return self.__sumarios_eletricos

    @sumarios_eletricos.setter
    def sumarios_eletricos(self, valor):
        self.__sumarios_eletricos = valor


class SumarioEletrico:
    def __init__(self, posto_horario, leitura_anterior, leitura_atual, const_medidor, consumo_kwh):
        self.__posto_horario = posto_horario
        self.__leitura_anterior = leitura_anterior
        self.__leitura_atual = leitura_atual
        self.__const_medidor = const_medidor
        self.__consumo_kwh = consumo_kwh

    @property
    def posto_horario(self):
        return self.__posto_horario

    @posto_horario.setter
    def posto_horario(self, valor_posto_horario):
        self.__posto_horario = valor_posto_horario

    @property
    def leitura_anterior(self):
        return self.__leitura_anterior

    @leitura_anterior.setter
    def leitura_anterior(self, valor_leitura_anterior):
        self.__leitura_anterior = valor_leitura_anterior

    @property
    def leitura_atual(self):
        return self.__leitura_atual

    @leitura_atual.setter
    def leitura_atual(self, valor_leitura_atual):
        self.__leitura_atual = valor_leitura_atual

    @property
    def const_medidor(self):
        return self.__const_medidor

    @const_medidor.setter
    def const_medidor(self, valor_const_medidor):
        self.__const_medidor = valor_const_medidor

    @property
    def consumo_kwh(self):
        return self.__consumo_kwh

    @consumo_kwh.setter
    def consumo_kwh(self, valor_consumo_kwh):
        self.__consumo_kwh = valor_consumo_kwh