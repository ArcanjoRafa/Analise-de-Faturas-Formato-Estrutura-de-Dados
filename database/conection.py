from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

# CRIANDO CONEXAO COM O BANCO DE DADOS
engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/postgres")
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
