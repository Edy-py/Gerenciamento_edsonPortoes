# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database import get_session, Estoque, Vendas
from utils import format_currency

def render_dashboard(readonly=False):
    session = get_session()
    
    # Alertas de Reposição
    estoque = session.query(Estoque).all()
    itens_criticos = [i.nome_produto for i in estoque if i.quantidade <= 1]
    
    if itens_criticos:
        st.error(f"⚠️ **REPOR ESTOQUE:** {', '.join(itens_criticos)}")

    col1, col2, col3, col4 = st.columns(4)
    
    vendas = session.query(Vendas).all()

    if vendas:
        df_v = pd.DataFrame([(v.nome_prod, v.qtd_vendida, v.lucro, v.data) for v in vendas], 
                             columns=['Produto', 'Qtd', 'Lucro', 'Data'])
        
        df_v['Data'] = pd.to_datetime(df_v['Data'])
        
        col2.metric("Produto Mais Vendido", df_v.groupby('Produto')['Qtd'].sum().idxmax())

        if not readonly:
            col1.metric("Total de Vendas (Qtd)", len(vendas))
            col3.metric("Lucro Acumulado", format_currency(df_v['Lucro'].sum()))
        
        # produto mais vendido do mes
        hoje = datetime.now()
        mes_atual = hoje.month
        ano_atual = hoje.year
        
        df_mes = df_v[(df_v['Data'].dt.month == mes_atual) & (df_v['Data'].dt.year == ano_atual)]
        if not df_mes.empty:
            mais_vendido_mes = df_mes.groupby('Produto')['Qtd'].sum().idxmax()
        else:
            mais_vendido_mes = "Sem vendas"

        if not readonly:
            msg = f"Produto mais vendido do mês {mes_atual}"
            col4.metric(msg, mais_vendido_mes)

    else:
        col1.metric("Total de Vendas", 0)
        col2.metric("Produto Mais Vendido", "-")
        col3.metric("Lucro Acumulado", "R$ 0,00")

    st.subheader("Níveis de Estoque")
    if estoque:
        df_est = pd.DataFrame([(i.nome_produto, i.quantidade) for i in estoque], columns=['Produto', 'Qtd'])
        df_est['Status'] = df_est['Qtd'].apply(lambda q: 'Crítico' if q < 1 else ('Alerta' if q <= 5 else 'Ok'))
        
        fig = px.bar(df_est, x='Produto', y='Qtd', color='Status',
                     color_discrete_map={'Ok':'green', 'Alerta':'orange', 'Crítico':'red'},
                     text_auto=True)
        
        # O segredo é colocar o gráfico DENTRO do 'if estoque'
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum produto cadastrado no estoque para exibir o gráfico.")
        
    session.close()