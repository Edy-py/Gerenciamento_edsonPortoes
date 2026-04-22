# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from database import get_session, Estoque
from utils import clean_text, format_currency, parse_currency

def render_estoque():
    st.markdown('<h1 style="text-align: center;">Gestão de Estoque - Edson Portões</h1>', unsafe_allow_html=True)
    session = get_session()
    
    # CSS para o visual profissional
    st.markdown("""
        <style>
            div[data-testid="stExpander"] { border: 1px solid #4B5563; border-radius: 10px; background-color: #1F2937; margin-bottom: 1rem; }
            .stButton>button { border-radius: 8px; height: 3.5em; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    tipo_operacao = st.radio("Escolha a operação:", 
                             ["Visualizar / Cadastrar", "Atualizar por ID"], 
                             horizontal=False)

    # --- LÓGICA DE CADASTRO ---
    if tipo_operacao == "Visualizar / Cadastrar":
        # Removido o parâmetro 'expanded': agora ele abre/fecha naturalmente no clique
        with st.expander("➕ CADASTRAR NOVO PRODUTO", expanded=False):
            nome = st.text_input("Nome do Produto", placeholder="Ex: MOTOR ROSSI")
            c1, c2, c3 = st.columns(3)
            qtd = c1.number_input("Qtd Inicial", min_value=1, value=1)
            p_custo = c2.number_input("Custo (R$)", min_value=0.0, format="%.2f")
            p_venda = c3.number_input("Venda Sugerida (R$)", min_value=0.0, format="%.2f")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_b1, col_b2 = st.columns(2)
            
            if col_b1.button("💾 SALVAR PRODUTO", use_container_width=True, type="primary"):
                nome_up = clean_text(nome)
                if nome_up:
                    if session.query(Estoque).filter_by(nome_produto=nome_up).first():
                        st.warning("⚠️ Produto já existe.")
                    else:
                        novo = Estoque(nome_produto=nome_up, quantidade=qtd, 
                                       preco_custo=format_currency(p_custo),
                                       preco_venda_un=format_currency(p_venda))
                        session.add(novo)
                        session.commit()
                        st.success(f"✅ {nome_up} cadastrado!")
                        
                        st.rerun()
                else:
                    st.error("Nome obrigatório.")
            
            if col_b2.button("CANCELAR", use_container_width=True):
                st.rerun()

    # --- LÓGICA DE ATUALIZAÇÃO POR ID ---
    else:
        with st.expander("🔧 EDITOR DE PRODUTO (POR ID)", expanded=False):
            id_editar = st.number_input("Digite o ID do Produto:", min_value=1, step=1)
            produto_edit = session.query(Estoque).filter_by(id=id_editar).first()
            
            if produto_edit:
                st.info(f"Editando: **{produto_edit.nome_produto}**")
                novo_nome = st.text_input("Novo Nome", value=produto_edit.nome_produto)
                ce1, ce2, ce3 = st.columns(3)
                nova_qtd = ce1.number_input("Nova Qtd", min_value=0, value=produto_edit.quantidade)
                novo_pc = ce2.number_input("Novo Custo", value=parse_currency(produto_edit.preco_custo), format="%.2f")
                novo_pv = ce3.number_input("Novo Venda", value=parse_currency(produto_edit.preco_venda_un), format="%.2f")
                
                st.markdown("<br>", unsafe_allow_html=True)
                cb1, cb2 = st.columns(2)
                
                if cb1.button("CONFIRMAR ALTERAÇÃO", use_container_width=True, type="primary"):
                    produto_edit.nome_produto = clean_text(novo_nome)
                    produto_edit.quantidade = nova_qtd
                    produto_edit.preco_custo = format_currency(novo_pc)
                    produto_edit.preco_venda_un = format_currency(novo_pv)
                    session.commit()
                    st.success("✅ Alterações salvas!")
                    st.rerun()
                    
                if cb2.button("VOLTAR / CANCELAR", use_container_width=True):
                    st.rerun()
            else:
                st.warning("⚠️ Insira um ID válido para carregar os dados.")

    st.markdown("---")

    # --- TABELA DE VISUALIZAÇÃO ---
    st.subheader("Estoque Disponível")
    dados = session.query(Estoque).all()
    if dados:
        df = pd.DataFrame([(i.id, i.nome_produto, i.quantidade, i.preco_custo, i.preco_venda_un) for i in dados],
                          columns=['ID', 'PRODUTO', 'QTD', 'CUSTO UN.', 'VENDA UN.'])
        
        busca = st.text_input("Buscar produto...", placeholder="Digite para filtrar...").upper()
        if busca:
            df = df[df['PRODUTO'].str.contains(busca)]

        st.dataframe(df, use_container_width=True, hide_index=True)
        
        total_inv = sum(i.quantidade * parse_currency(i.preco_custo) for i in dados)
        st.metric("Total Investido (Custo)", format_currency(total_inv))
    else:
        st.info("O estoque está vazio.")

    session.close()