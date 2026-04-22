# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from database import get_session, Estoque, Vendas
from utils import format_currency, parse_currency
import datetime

def render_vendas(readonly=False):
    st.markdown('<h1 style="text-align: center;">Gerenciamento de Vendas</h1>', unsafe_allow_html=True)
    session = get_session()

    # Inicializa o carrinho na sessão se não existir
    if 'carrinho' not in st.session_state:
        st.session_state.carrinho = []

    # --- SEÇÃO 1: CARRINHO DE COMPRAS (APENAS ADMIN) ---
    if not readonly:
        with st.expander("🛒 MONTAR CARRINHO / NOVA VENDA", expanded=False):
            produtos_db = session.query(Estoque).all()
            lista_nomes_produtos = sorted([p.nome_produto for p in produtos_db])
            dict_produtos = {p.nome_produto: p for p in produtos_db}
            
            if lista_nomes_produtos:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    prod_sel = st.selectbox("Selecione o Produto", options=lista_nomes_produtos, index=0)
                
                if prod_sel:
                    obj_p = dict_produtos[prod_sel]
                    with col2:
                        qtd = st.number_input(f"Qtd (Estoque: {obj_p.quantidade})", 
                                              min_value=1, 
                                              max_value=max(1, obj_p.quantidade), 
                                              value=1)
                    with col3:
                        p_sugerido = parse_currency(obj_p.preco_venda_un)
                        preco_v_final = st.number_input("Preço Unitário (R$)", value=p_sugerido, format="%.2f")

                    if st.button("➕ Adicionar ao Carrinho", use_container_width=True, type="primary"):
                        st.session_state.carrinho.append({
                            "produto": prod_sel,
                            "qtd": qtd,
                            "preco": preco_v_final,
                            "subtotal": qtd * preco_v_final,
                            "custo_un": parse_currency(obj_p.preco_custo)
                        })
                        st.rerun()
            else:
                st.warning("⚠️ O estoque está vazio. Cadastre produtos antes de vender.")
    else:
        st.info("💡 **Modo de Visualização**: Apenas administradores podem realizar novas vendas.")

    # --- EXIBIÇÃO DO CARRINHO ---
    if st.session_state.carrinho:
        st.subheader("Itens da Venda Atual")
        df_cart = pd.DataFrame(st.session_state.carrinho)
        
        df_show = df_cart.copy()
        df_show['preco'] = df_show['preco'].apply(format_currency)
        df_show['subtotal'] = df_show['subtotal'].apply(format_currency)
        
        st.table(df_show[['produto', 'qtd', 'preco', 'subtotal']])
        
        total_venda = df_cart['subtotal'].sum()
        st.markdown(f"### Total: :green[{format_currency(total_venda)}]")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Finalizar Venda", use_container_width=True, type="primary"):
                for item in st.session_state.carrinho:
                    lucro_item = item['subtotal'] - (item['custo_un'] * item['qtd'])
                    
                    nova_venda = Vendas(
                        nome_prod=item['produto'],
                        qtd_vendida=item['qtd'],
                        preco_venda_total=format_currency(item['subtotal']),
                        data=datetime.datetime.now().strftime("%d/%m/%Y"),
                        lucro=lucro_item
                    )
                    session.add(nova_venda)
                    
                    # Baixa no Supabase
                    prod_est = session.query(Estoque).filter_by(nome_produto=item['produto']).first()
                    if prod_est:
                        prod_est.quantidade -= item['qtd']
                
                session.commit()
                st.session_state.carrinho = []
                st.success("🎉 Venda registrada no Supabase com sucesso!")
                st.rerun()
        with c2:
            if st.button("🗑️ Limpar Carrinho", use_container_width=True):
                st.session_state.carrinho = []
                st.rerun()

    st.divider()

    # --- SEÇÃO 2: HISTÓRICO E FILTROS (PARA TODOS) ---
    st.subheader("Histórico de Vendas")
    vendas_db = session.query(Vendas).order_by(Vendas.id.desc()).all()
    
    if vendas_db:
        df_vendas = pd.DataFrame([(v.id, v.nome_prod, v.qtd_vendida, v.preco_venda_total, v.data, v.lucro) for v in vendas_db],
                                 columns=['ID', 'Produto', 'Qtd', 'Valor Total', 'Data', 'Lucro'])
        
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            data_range = st.date_input("Filtrar por Período", [])
        
        if len(data_range) == 2:
            start, end = data_range
            df_vendas['Data_DT'] = pd.to_datetime(df_vendas['Data'], format='%d/%m/%Y').dt.date
            df_vendas = df_vendas[(df_vendas['Data_DT'] >= start) & (df_vendas['Data_DT'] <= end)]
            df_vendas = df_vendas.drop(columns=['Data_DT'])

        if not readonly:
            st.dataframe(df_vendas, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df_vendas[['ID', 'Produto', 'Qtd', 'Valor Total', 'Data']], use_container_width=True, hide_index=True)

        # Botão de Exportação de Vendas
        csv_vendas = df_vendas.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Baixar Histórico de Vendas (CSV)",
            data=csv_vendas,
            file_name=f'vendas_edson_portoes_{datetime.date.today()}.csv',
            mime='text/csv',
        )

        # --- SEÇÃO 3: CORREÇÃO / ESTORNO (APENAS ADMIN) ---
        if not readonly:
            with st.expander("CORRIGIR VENDA (ESTORNO)", expanded=False):
                id_estorno = st.number_input("Informe o ID da venda para cancelar:", min_value=1, step=1)
                if st.button("Confirmar Estorno / Devolução", type="secondary"):
                    venda_remover = session.query(Vendas).filter_by(id=id_estorno).first()
                    if venda_remover:
                        # Devolve ao estoque no Postgres
                        prod_est = session.query(Estoque).filter_by(nome_produto=venda_remover.nome_prod).first()
                        if prod_est:
                            prod_est.quantidade += venda_remover.qtd_vendida
                        
                        session.delete(venda_remover)
                        session.commit()
                        st.success(f"Venda ID {id_estorno} cancelada e itens devolvidos ao estoque!")
                        st.rerun()
                    else:
                        st.error("ID da venda não encontrado no banco de dados.")
    else:
        st.info("Nenhuma venda registrada no sistema até o momento.")

    session.close()