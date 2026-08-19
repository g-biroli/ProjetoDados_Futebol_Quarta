"""Pagina inicial: apresentacao do projeto (sem dados)."""

import streamlit as st

from src.theme import LOGO_PATH, apply_theme, callout, github_button

GITHUB_URL = "https://github.com/g-biroli/ProjetoDados_Futebol_Quarta"

apply_theme()

col1, col2, col3 = st.columns([1, 1.3, 1])
with col2:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    else:
        st.markdown(
            '<div style="font-size:5rem; text-align:center;">\U0001F3C6</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "Logo do grupo ainda nao encontrada - salve o arquivo em "
            "`assets/logo.png` no repositorio."
        )

st.markdown(
    '<div class="wc-title" style="text-align:center;">'
    "\U000026BD Futebol Quarta-Feira Playball 2 Pompeia</div>",
    unsafe_allow_html=True,
)
st.markdown('<div class="wc-stripe"></div>', unsafe_allow_html=True)

st.markdown(
    """
<div style="text-align:center; max-width:720px; margin:0 auto; line-height:1.6;">
Dados e estatisticas dos participantes da resenha do fut. Cada gol,
assistencia, vitoria e derrota e registrada.<br><br>
Nosso objetivo e descobrir quem e o Messi, o Neymar e o CR7 do grupo -
mas tambem apontar os bagres: Rony Rustico, Robinho Jr. e Memphis Depay.<br><br>
Os dados vem direto de uma planilha compartilhada no Google Drive.
</div>
""",
    unsafe_allow_html=True,
)

callout("\U0001F3C6 Aqui e raça, resenha e zero compromisso com a tatica.", variant="primary")
callout("QUEM VENCERÁ O TROFEU BAGRE D'OR?", variant="secondary")

st.divider()

col_credit, col_button = st.columns([2, 1], vertical_alignment="center")
with col_credit:
    st.markdown('<div class="credit-line">Desenvolvido por <b>Gabriel Biroli</b></div>', unsafe_allow_html=True)
with col_button:
    github_button(GITHUB_URL, "Ver codigo no GitHub")
