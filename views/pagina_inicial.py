"""Pagina inicial: apresentacao do projeto (sem dados)."""

from pathlib import Path

import streamlit as st

from src.theme import apply_theme, github_button

LOGO_PATH = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
GITHUB_URL = "https://github.com/g-biroli/ProjetoDados_Futebol_Quarta"

apply_theme()

col_logo, col_text = st.columns([1, 3], vertical_alignment="center")

with col_logo:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    else:
        st.markdown(
            '<div style="font-size:4rem; text-align:center;">\U0001F3C6</div>',
            unsafe_allow_html=True,
        )

with col_text:
    st.markdown(
        '<div class="wc-title">\U000026BD Futebol Quarta-Feira Playball 2 Pompeia</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="wc-stripe"></div>', unsafe_allow_html=True)

if not LOGO_PATH.exists():
    st.caption(
        "Logo do grupo ainda nao adicionada - salve o arquivo da logo em "
        "`assets/logo.png` no repositorio para ela aparecer aqui."
    )

st.markdown(
    """
Dados e estatisticas dos participantes da resenha do fut. Cada gol,
assistencia, vitoria e derrota e registrada. Nosso objetivo e descobrir quem
e o Lionel Messi, Neymar e CR7, mas tambem identificar os bagres Rony
Rustico, Robinho Jr e Memphis Depay.

Os dados vem direto de uma planilha compartilhada no Google Drive.
"""
)

st.markdown(
    "> \U0001F3C6 **Aqui e raca, resenha e zero compromisso com a tatica.**"
)

st.divider()

st.markdown('<div class="credit-line">Desenvolvido por <b>Gabriel Biroli</b></div>', unsafe_allow_html=True)
st.write("")
github_button(GITHUB_URL, "Ver codigo no GitHub")
