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

@st.cache_resource
def get_engine():
    if "database" not in st.secrets:
        st.warning("⚠️ Chave [database] não encontrada em secrets.toml. A usar SQLite local.")
        return create_engine('sqlite:///estoque_edson.db')

    db_url = st.secrets["database"]["url"]

    
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    try:
        eng = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=1800
        )
    
        with eng.connect() as conn:
            pass
        return eng
    except Exception as e:
        st.error(f"❌ Erro crítico ao ligar ao Supabase: {e}")
        st.stop()

engine = get_engine()

try:
    Base.metadata.create_all(engine)
except Exception as e:
    st.error(f"Erro na sincronização do Banco: {e}")

Session = sessionmaker(bind=engine)

def get_session():
    return Session()