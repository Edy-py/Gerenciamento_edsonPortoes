# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from database import get_session, Estoque
from utils import clean_text, format_currency, parse_currency

def render_estoque(readonly=False):
    st.markdown('<h1 style="text-align: center;">Gestão de Estoque - Edson Portões</h1>', unsafe_allow_html=True)
    session = get_session()
    
    # Se o usuário não for admin, ele não vê as opções de rádio para cadastrar/editar
    if not readonly:
        tipo_operacao = st.radio("Escolha a operação:", 
                                 ["Visualizar / Cadastrar", "Atualizar por ID"], 
                                 horizontal=True)
    else:
        tipo_operacao = "Visualizar / Cadastrar"

    # --- LÓGICA DE CADASTRO (APENAS ADMIN) ---
    if tipo_operacao == "Visualizar / Cadastrar" and not readonly:
        with st.expander("➕ CADASTRAR NOVO PRODUTO", expanded=False):
            nome = st.text_input("Nome do Produto", placeholder="Ex: MOTOR ROSSI")
            c1, c2, c3 = st.columns(3)
            qtd = c1.number_input("Qtd Inicial", min_value=1, value=1)
            p_custo = c2.number_input("Custo (R$)", min_value=0.0, format="%.2f")
            p_venda = c3.number_input("Venda Sugerida (R$)", min_value=0.0, format="%.2f")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_b1, col_b2 = st.columns(2)
            
            if col_b1.button("SALVAR PRODUTO", use_container_width=True, type="primary"):
                nome_up = clean_text(nome)
                if nome_up:
                    if session.query(Estoque).filter_by(nome_produto=nome_up).first():
                        st.warning("⚠️ Produto já existe no sistema.")
                    else:
                        novo = Estoque(nome_produto=nome_up, 
                                       quantidade=qtd, 
                                       preco_custo=format_currency(p_custo),
                                       preco_venda_un=format_currency(p_venda))
                        session.add(novo)
                        session.commit()
                        st.success(f"✅ {nome_up} cadastrado com sucesso!")
                        st.rerun()
                else:
                    st.error("O nome do produto é obrigatório.")
            
            if col_b2.button("CANCELAR", use_container_width=True):
                st.rerun()

    # --- LÓGICA DE ATUALIZAÇÃO POR ID (APENAS ADMIN) ---
    elif tipo_operacao == "Atualizar por ID" and not readonly:
        with st.expander("EDITOR DE PRODUTO (POR ID)", expanded=True):
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
                    st.success("Alterações salvas no banco de dados!")
                    st.rerun()
                    
                if cb2.button("VOLTAR / CANCELAR", use_container_width=True):
                    st.rerun()
            else:
                st.warning("⚠️ Insira um ID válido para carregar os dados do Supabase.")

    st.markdown("---")

    # --- TABELA DE VISUALIZAÇÃO (PARA TODOS) ---
    st.subheader("Estoque Disponível")
    dados = session.query(Estoque).order_by(Estoque.nome_produto).all()
    
    if dados:
        # Criando o DataFrame para exibição
        df = pd.DataFrame([(i.id, i.nome_produto, i.quantidade, i.preco_custo, i.preco_venda_un) for i in dados],
                          columns=['ID', 'PRODUTO', 'QTD', 'CUSTO UN.', 'VENDA UN.'])
        
        # Campo de busca em tempo real
        busca = st.text_input("Buscar produto...", placeholder="Digite o nome para filtrar...").upper()
        if busca:
            df = df[df['PRODUTO'].str.contains(busca)]

        # Exibição da tabela estilizada
        if not readonly:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df[['ID', 'PRODUTO', 'QTD','VENDA UN.']], use_container_width=True, hide_index=True)
        
        # Métricas de resumo (Cálculo em tempo real do banco)
        total_inv = sum(i.quantidade * parse_currency(i.preco_custo) for i in dados)
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Total Investido (Custo)", format_currency(total_inv))
        with col_m2:
            # Botão de exportação disponível para todos os níveis de acesso
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Exportar Estoque para Excel (CSV)",
                data=csv,
                file_name='estoque_edson_portoes.csv',
                mime='text/csv',
                use_container_width=True
            )
    else:
        st.info("O estoque está vazio no momento.")

    session.close()