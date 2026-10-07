from dataclasses import dataclass
@dataclass
class UnidadeConsumidora:
    numero_uc : str
    endereco : str
    cep : str
    id: int = None
    client_id : int = None

