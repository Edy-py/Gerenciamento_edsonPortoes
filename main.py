# -*- coding: utf-8 -*-
import streamlit as st
from visualizacao import render_dashboard
from estoque import render_estoque
from vendas import render_vendas

st.set_page_config(page_title="Controle de Estoque e Vendas", layout="wide", page_icon="📈")
st.title("Controle de Estoque e Vendas - Edson Portões")

tab_vis, tab_est, tab_ven = st.tabs(["Visualização", "Gerenciar Estoque", "Gerenciar Vendas"])

with tab_vis:
    render_dashboard()

with tab_est:
    render_estoque()

with tab_ven:
    render_vendas()