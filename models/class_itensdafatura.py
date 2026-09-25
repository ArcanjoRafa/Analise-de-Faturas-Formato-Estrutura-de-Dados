from dataclasses import dataclass

@dataclass
class ItemDaFatura:
       nome_item : str
       unid : str
       quant : str
       preco_unit : str
       valor_total : str
       pis_cofins : str
       base_calc_icms : str
       aliq_icms : str
       icms : str
       tarifa_unit : str
       id: int = None


@dataclass
class ItensTotal:
       valor: str
       pis_cofins : str
       base_calc_icms : str
       icms : str
       id: int = None