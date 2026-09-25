from dataclasses import dataclass
@dataclass
class Medidor:
    numero_medidor : str


@dataclass
class SumarioEletrico:
    grandeza : str
    posto_horario : str
    leitura_anterior : str
    leitura_atual : str
    const_medidor : str
    consumo_kwh : str
    id: int = None
