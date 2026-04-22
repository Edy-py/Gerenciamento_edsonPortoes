# -*- coding: utf-8 -*-
import unicodedata

def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def parse_currency(curr_str):
    if not curr_str: return 0.0
    try:
        return float(curr_str.replace("R$ ", "").replace(".", "").replace(",", "."))
    except:
        return 0.0

def clean_text(text):
    if not text: return ""
    nfkd_form = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).upper().strip()