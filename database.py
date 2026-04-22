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
        # Tenta pegar a URL do secrets
        if "database" in st.secrets:
            db_url = st.secrets["database"]["url"]
        else:
            # Se não achar, usa o SQLite local (para não crashar o app)
            return create_engine('sqlite:///estoque_edson.db')

        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        
        # pool_pre_ping é VITAL para o Streamlit Cloud não perder a conexão
        return create_engine(db_url, pool_pre_ping=True, pool_recycle=3600)
    except Exception:
        return create_engine('sqlite:///estoque_edson.db')

# Inicializa o motor
engine = get_engine()

# SÓ CRIA AS TABELAS SE NÃO FOR SQLITE (OU SE VOCÊ QUISER TESTAR)
try:
    Base.metadata.create_all(engine)
except Exception as e:
    st.error(f"Erro ao criar tabelas no Banco: {e}")

Session = sessionmaker(bind=engine)

def get_session():
    return Session()