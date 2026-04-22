# -*- coding: utf-8 -*-
import unicodedata
import streamlit as st

def format_currency(value):
    """Converte um float para string no formato R$ 1.234,56"""
    try:
        if value is None:
            return "R$ 0,00"
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"

def parse_currency(curr_str):
    """Converte uma string formatada (R$ 1.234,56) para float (1234.56)"""
    if not curr_str or not isinstance(curr_str, str):
        return 0.0
    try:
        # Remove símbolos, pontos de milhar e troca vírgula decimal por ponto
        clean_str = curr_str.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
        return float(clean_str)
    except (ValueError, TypeError):
        return 0.0

def clean_text(text):
    """Remove acentos, espaços extras e converte para maiúsculas (Padronização para o Banco)"""
    if not text or not isinstance(text, str):
        return ""
    try:
        # Normaliza caracteres (ex: 'ã' vira 'a' + '~') e remove os acentos
        nfkd_form = unicodedata.normalize('NFKD', text)
        text_normalized = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        return text_normalized.upper().strip()
    except Exception:
        return text.upper().strip()

def get_role_color(role):
    """Helper visual para indicar o nível de acesso no sistema"""
    return "blue" if role == "admin" else "gray"