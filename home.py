"""Ponto de entrada do app: define a navegacao entre as paginas."""

import streamlit as st

st.set_page_config(page_title="Futebol de Quarta", layout="wide")

pages = [
    st.Page("views/pagina_inicial.py", title="Pagina Inicial", icon="\U000026BD", default=True),
    st.Page("views/visao_rodada.py", title="Visao da Rodada", icon="\U0001F4C5"),
    st.Page("views/visao_geral.py", title="Visao Geral", icon="\U0001F3C6"),
]

st.navigation(pages).run()
