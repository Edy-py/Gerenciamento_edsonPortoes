# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Estoque(Base):
    __tablename__ = 'estoque'
    id = Column(Integer, primary_key=True)
    nome_produto = Column(String, unique=True)
    quantidade = Column(Integer)
    preco_custo = Column(String) 
    preco_venda_un = Column(String) 

class Vendas(Base):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True)
    nome_prod = Column(String)
    qtd_vendida = Column(Integer)
    preco_venda_total = Column(String)
    data = Column(String)
    lucro = Column(Float)

engine = create_engine('sqlite:///estoque_edson.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()