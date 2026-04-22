# -*- coding: utf-8 -*-
import streamlit as st
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

# Puxa a URL do Secrets (configurar no painel do Streamlit Cloud)
@st.cache_resource
def get_engine():
    try:
        db_url = st.secrets["database"]["url"]
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        return create_engine(db_url)
    except:
        return create_engine('sqlite:///estoque_edson.db')

engine = get_engine()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()