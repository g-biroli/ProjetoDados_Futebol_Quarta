"""Pagina inicial: apresentacao do projeto (sem dados)."""

import streamlit as st

from src.charts import GOLD
from src.theme import LOGO_PATH, apply_theme, callout, github_button

GITHUB_URL = "https://github.com/g-biroli/ProjetoDados_Futebol_Quarta"

apply_theme()

col1, col2, col3 = st.columns([2, 1, 2])
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
    f"""
<div style="text-align:center; max-width:760px; margin:0 auto; line-height:1.7;">
  <p style="font-size:1.2rem; font-weight:600; color:#ffffff; margin:0 0 16px 0;">
    Dados e estatísticas dos participantes da resenha do fut.<br>
    Cada gol, assistência, vitória e derrota é registrada.
  </p>
  <p style="font-size:1.05rem; color:#f5f5f5; margin:0 0 16px 0;">
    <span style="color:{GOLD}; font-weight:700;">Objetivo do projeto:</span>
    descobrir quem é o Messi, o Neymar e o CR7 do grupo - mas também apontar
    os bagres de cada rodada: Rony Rústico, Robinho Jr. e Memphis Depay.
  </p>
  <p style="font-size:1.2rem; font-weight:600; color:#ffffff; margin:0;">
    Os dados vêm direto de uma planilha compartilhada no Google Drive.
  </p>
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
