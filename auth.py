# -*- coding: utf-8 -*-
import streamlit as st
import bcrypt

# Dicionário com usuários e senhas em texto simples
USERS = {
    "edy": {
        "role": "admin",
        "pass": b'$2b$12$hsQRLQAtFull/VV.jDHk0.dB5A4rtNZTcl9.dnes1MjOAPppa7OZu'
        },
    "edson": {
        "role": "admin",
        "pass": b'$2b$12$WwHi3TSbTGuYhgqDz0B4FuC4c0f8s5vhfmLJm6.YH7oKj1UEHTo92'
        },
    "giogrete": {
        "role": "admin",
        "pass": b'$2b$12$hZMVztYKGqqAczm9.lo2puWFshUsuIBMfoaT2QUFKnMclGafBfmFa'
        },
    "visitante": {
        "role": "viewer",
        "pass": b'$2b$12$TgJCJpwgJeFKhf9VU7uWL.98RalnnYSr0X3YXgT6nd/fU2r.dw2PC'
        }
}

def login():
    if "auth" not in st.session_state:
        st.session_state.auth = False
        st.session_state.role = None

    if not st.session_state.auth:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Acesso Seguro - Edson Portões")
            u = st.text_input("Usuário").lower().strip()
            p = st.text_input("Senha", type="password")
            
            if st.button("Entrar", use_container_width=True, type="primary"):
                if u in USERS:
                    # Verifica se a senha digitada (p) corresponde ao hash salvo
                    if bcrypt.checkpw(p.encode('utf-8'), USERS[u]["pass"]):
                        st.session_state.auth = True
                        st.session_state.role = USERS[u]["role"]
                        st.rerun()
                    else:
                        st.error("Senha incorreta.")
                else:
                    st.error("Usuário não encontrado.")
        return False
    return True

def logout():
    st.sidebar.markdown("---")
    st.sidebar.write(f"Sessão: **{st.session_state.role.upper()}**")
    if st.sidebar.button("🚪 Sair", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()