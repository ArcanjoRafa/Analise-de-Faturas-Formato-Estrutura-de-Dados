from dataclasses import dataclass

@dataclass
class Leitura:
    l_anterior: str
    l_atual: str
    dias: str
    l_proxima: str
    id: int = None
    fatura_id : int = None

