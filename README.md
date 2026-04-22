# Edson Portões - Sistema Inteligente de Gestão

Este projeto foi desenvolvido para resolver um problema real de gestão em uma loja familiar **Edson Portões**. O foco foi transformar processos manuais em uma plataforma digital intuitiva, integrando controle de inventário, fluxo de vendas e análise de dados financeiros.

---

## Objetivo do Projeto
O objetivo principal foi automatizar a operação da **Edson Portões**, substituindo anotações em papel por um sistema centralizado que oferece:
1.  **Precisão no Estoque:** Evitar a falta de materiais essenciais (motores, engrenagens).
3.  **Cálculo Automático de Lucro:** Eliminar erros manuais na precificação e fechamento de caixa.
4.  **Histórico Confiável:** Permitir auditorias e estornos de forma rápida e segura.

---

## Stack Tecnológica

Para este projeto, escolhi tecnologias que priorizam a velocidade de entrega (Time-to-Market) e a robustez dos dados:

* **Linguagem:** Python 3.11+
* **Interface (UI/UX):** [Streamlit](https://streamlit.io/) - Utilizado para criar uma interface web moderna com foco em usabilidade.
* **Persistência de Dados:** [SQLAlchemy](https://www.sqlalchemy.org/) & SQLite - Implementação de um ORM para garantir a integridade dos dados e facilitar a manutenção.
* **Análise de Dados:** [Pandas](https://pandas.pydata.org/) & [Plotly](https://plotly.com/) - Processamento e visualização de métricas de desempenho em tempo real.
* **Estilização:** CSS Customizado - Adaptado para a identidade visual da marca (Amarelo e Azul), com suporte nativo a temas Light/Dark.

---

## Desafios Técnicos Superados

* **Arquitetura Modular:** O projeto foi dividido em módulos (`estoque.py`, `vendas.py`, `visualizacao.py`) para facilitar a escalabilidade e a leitura do código.
* **Gerenciamento de Estado:** Uso avançado do `st.session_state` para criar um carrinho de compras dinâmico que persiste durante a navegação.
* **UI/UX Adaptativa:** Implementação de CSS injetado para garantir que os componentes do Streamlit seguissem a risca o branding da empresa, independentemente do dispositivo.
* **Segurança de Dados:** Lógica de estorno que garante a integridade referencial (devolve o produto ao estoque automaticamente ao cancelar uma venda).

---

## Visualização do Sistema

O sistema está organizado em três pilares fundamentais:
1.  **Visualização:** Visão macro do negócio (Total Investido, Faturação e Lucro Líquido).
2.  **Gestão de Estoque:** Operações de CRUD (Create, Read, Update, Delete) com busca otimizada.
3.  **Módulo de Vendas:** Interface de PDV (Ponto de Venda) simplificada para uso em tablets e PCs de oficina.

---

## Autor

- **E-mail:** `edilsonalvesprofissional@gmail.com`
- **Instagram:** `edy-py`
- **Linkedin:** [edy-py](www.linkedin.com/in/edy-py)  
- *Estudante de Ciência da Computação - Universidade Federal de Catalão (UFCAT)* Este projeto é um exemplo de como utilizo a tecnologia para gerar valor direto em negócios reais.

---
> *Nota: Este repositório serve como portfólio técnico.*
