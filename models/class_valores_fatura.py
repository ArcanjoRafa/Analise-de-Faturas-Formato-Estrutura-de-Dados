from dataclasses import dataclass

@dataclass
class ValoresFatura:
    mes_ref: str
    vencimento: str
    pagar: str
    apresentacao : str
    id: int = None
    uc_id: int = None
    medidor_id : int = None