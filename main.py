# -*- coding: utf-8 -*-
import streamlit as st
import base64
from auth import login, logout  # Importando o novo módulo de segurança
from visualizacao import render_dashboard
from estoque import render_estoque
from vendas import render_vendas

# --- FUNÇÃO PARA CARREGAR A IMAGEM LOCAL ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Edson Portões - Gestão",
    page_icon="🏭", 
    layout="wide"
)

# --- SISTEMA DE LOGIN ---
# O código só executa se o login for bem-sucedido
if login():
    # Adiciona botão de sair na barra lateral
    logout()
    
    # Se o usuário logado não for admin, ocultamos botões de salvamento/exclusão via CSS
    if st.session_state.role != "admin":
        st.markdown("<style>button[kind='primary'] {display:none !important;}</style>", unsafe_allow_html=True)

    # --- CARREGAMENTO DA LOGO ---
    try:
        img_path = "midia/logo_nova.png" 
        logo_base64 = get_base64_of_bin_file(img_path)
    except Exception as e:
        st.error(f"Erro ao carregar imagem: {e}")
        logo_base64 = ""

    # --- CSS PERSONALIZADO ---
    st.markdown(f"""
        <style>
            /* Variáveis de Identidade */
            :root {{
                --amarelo-edson: #FFD700;
                --azul-edson: #0047AB;
            }}

            /* 1. Banner Principal */
            .banner-header {{
                background-image: url("data:image/png;base64,{logo_base64}");
                background-size: contain;
                background-repeat: no-repeat;
                background-position: center;
                height: 250px; 
                margin-bottom: 25px;
                border-bottom: 5px solid var(--amarelo-edson);
            }}

            /* 2. Expanders (Ajustados para o Modo Claro) */
            div[data-testid="stExpander"] {{
                border: 2px solid var(--azul-edson) !important;
                border-radius: 12px !important;
                background-color: #FFFFFF !important; 
                margin-bottom: 1rem !important;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
            }}

            div[data-testid="stExpander"] summary p {{
                color: var(--azul-edson) !important;
                font-weight: bold !important;
                font-size: 1.1rem;
            }}

            /* 3. Estilo das Abas (Tabs) */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 10px;
                justify-content: center;
            }}
            .stTabs [data-baseweb="tab"] {{
                border-radius: 8px 8px 0px 0px;
                padding: 12px 25px;
                font-weight: bold;
                color: var(--azul-edson) !important;
                background-color: rgba(0, 71, 171, 0.05);
            }}
            .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
                background-color: var(--amarelo-edson) !important;
                color: #000000 !important;
                border: 1px solid var(--azul-edson);
            }}

            /* 4. Botões Primários */
            .stButton button[kind="primary"] {{
                background-color: var(--amarelo-edson) !important;
                color: #000000 !important;
                font-weight: bold;
                border-radius: 10px;
                height: 3em;
                border: 1px solid #B8860B;
            }}

            /* Títulos das seções em Azul para combinar com o logo Rossi */
            h1, h2, h3 {{
                color: var(--azul-edson) !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    # --- EXIBIÇÃO DO BANNER ---
    st.markdown('<div class="banner-header"></div>', unsafe_allow_html=True)

    # --- NAVEGAÇÃO ---
    # Passamos o parâmetro readonly para os módulos baseado no cargo (role) do usuário
    is_readonly = (st.session_state.role != "admin")
    
    tabs = st.tabs(["Visualização", "Estoque", "Vendas"])

    with tabs[0]:
        render_dashboard()

    with tabs[1]:
        render_estoque(readonly=is_readonly)

    with tabs[2]:
        render_vendas(readonly=is_readonly)