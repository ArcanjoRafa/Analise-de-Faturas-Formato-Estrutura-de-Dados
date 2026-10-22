from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, Date, Integer, TEXT, ForeignKey
from database.conection import Base
from datetime import date
from decimal import Decimal

class Cliente(Base):
    __tablename__ = "clientes"

    id : Mapped[int] = mapped_column(primary_key=True)
    nome : Mapped[str] = mapped_column(TEXT)
    cpf_cnpj : Mapped[str] = mapped_column(String(50))

class UnidadeConsumidora(Base):
    __tablename__ = "unidadeconsumidora"

    id : Mapped[int] = mapped_column(primary_key=True)
    uc : Mapped[str] = mapped_column(String(30))
    cep : Mapped[str] = mapped_column(TEXT)
    endereco : Mapped[str] = mapped_column(TEXT)
    cliente_id : Mapped[int] = mapped_column(ForeignKey("clientes.id"))

class Medidor(Base):
    __tablename__ = "medidor"

    id : Mapped[int] = mapped_column(primary_key=True)
    numero : Mapped[str] = mapped_column(String(50))

class ValoresFatura(Base):
    __tablename__ = "fatura"

    id : Mapped[int] = mapped_column(primary_key=True)
    valor_total : Mapped[Decimal] = mapped_column(Numeric(10,2))
    vencimento : Mapped[date] = mapped_column(Date)
    mes_ref : Mapped[date] = mapped_column(Date)
    data_apresentacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    nome_pdf: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    uc_id : Mapped[int] = mapped_column(ForeignKey("unidadeconsumidora.id"))
    medidor_id : Mapped[int] = mapped_column(ForeignKey("medidor.id"))

class SumarioEletrico(Base):
    __tablename__ = "sumarioeletrico"

    id: Mapped[int] = mapped_column(primary_key=True)
    grandeza : Mapped[str] = mapped_column(String(50))
    posto_h : Mapped[str] = mapped_column(String(10))
    l_anterior : Mapped[Decimal] = mapped_column(Numeric(10,4))
    l_atual : Mapped[Decimal] = mapped_column(Numeric(10,4))
    const : Mapped[Decimal] = mapped_column(Numeric(10,4))
    consumo : Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    medidor_id : Mapped[int] = mapped_column(ForeignKey("medidor.id"))
    fatura_id: Mapped[int] = mapped_column(ForeignKey("fatura.id"))

class Leitura(Base):
    __tablename__ = "leitura"

    id: Mapped[int] = mapped_column(primary_key=True)
    l_anterior : Mapped[date] = mapped_column(Date)
    l_atual : Mapped[date] = mapped_column(Date)
    dias : Mapped[int] = mapped_column(Integer)
    l_proxima : Mapped[date] = mapped_column(Date)
    fatura_id : Mapped[int] = mapped_column(ForeignKey("fatura.id"))

class Tributo(Base):
    __tablename__ = "tributo"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome : Mapped[str] = mapped_column(String(50))
    aliquota : Mapped[Decimal] = mapped_column(Numeric(5, 2))
    base_calc : Mapped[Decimal] = mapped_column(Numeric(10,2))
    valor : Mapped[Decimal] = mapped_column(Numeric(10,2))
    fatura_id : Mapped[int] = mapped_column(ForeignKey("fatura.id"))

class ItemDaFatura(Base):
    __tablename__ = "item_fatura"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome_item : Mapped[str] = mapped_column(String(100))
    unid : Mapped[str | None] = mapped_column(String(20), nullable=True)
    quant : Mapped[Decimal | None] = mapped_column(Numeric(10,4), nullable=True)
    preco_unit : Mapped[Decimal | None] = mapped_column(Numeric(10,4), nullable=True)
    valor_total : Mapped[Decimal | None] = mapped_column(Numeric(10,2), nullable=True)
    pis_cofins : Mapped[Decimal | None] = mapped_column(Numeric(10,2), nullable=True)
    base_calc_icms : Mapped[Decimal | None] = mapped_column(Numeric(10,2), nullable=True)
    aliq_icms : Mapped[Decimal | None] = mapped_column(Numeric(10,2), nullable=True)
    icms : Mapped[Decimal | None] = mapped_column(Numeric(10,2), nullable=True)
    tarifa_unit : Mapped[Decimal | None] = mapped_column(Numeric(10,4), nullable=True)
    fatura_id : Mapped[int] = mapped_column(ForeignKey("fatura.id"))



