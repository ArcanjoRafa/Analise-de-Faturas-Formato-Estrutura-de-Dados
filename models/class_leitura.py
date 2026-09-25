from dataclasses import dataclass

@dataclass
class Leitura:
    leitura_anterior: str
    leitura_atual: str
    dias: str
    proxima_leitura: str
    id: int = None

