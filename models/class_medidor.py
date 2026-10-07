from dataclasses import dataclass
@dataclass
class Medidor:
    numero_medidor : str


@dataclass
class SumarioEletrico:
    grandeza : str
    posto_h : str
    l_anterior : str
    l_atual : str
    const : str
    consumo : str
    id: int = None
    medidor_id : int = None
    fatura_id = int = None