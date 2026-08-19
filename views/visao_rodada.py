"""Resultado individual de uma rodada especifica."""

import streamlit as st

from src.data import bagre_ranking, load_data, round_table
from src.theme import (
    apply_theme,
    bagre_note,
    bagre_table,
    bagre_trophy,
    classification_table,
    mini_ranking_table,
    page_footer,
    page_header,
    scoreboard_header,
)

apply_theme()
page_header("\U0001F4C5 Visao da Rodada")

try:
    df = load_data()
except Exception as exc:
    st.error(f"Nao foi possivel carregar os dados: {exc}")
    st.stop()

if df.empty:
    st.warning("Ainda nao ha rodadas registradas.")
    st.stop()

rodadas = sorted(df["RODADA"].unique(), reverse=True)
rodada = st.selectbox("Escolha a rodada", options=rodadas, format_func=lambda r: f"Rodada {r}")

round_df = round_table(df, rodada)
data_da_rodada = round_df["DATA"].iloc[0].strftime("%d/%m/%Y")

scoreboard_header("Fut Quarta", f"{rodada}", data_da_rodada)

bagre_table(bagre_ranking(round_df, top_n=3), "Top 3 bagres da rodada")
bagre_note()
bagre_trophy()

st.divider()
classification_table(round_df, caption=f"Classificacao - Rodada {rodada}")

col1, col2 = st.columns(2)
with col1:
    mini_ranking_table(round_df, "GOLS", "\U000026BD Artilharia da rodada")
with col2:
    mini_ranking_table(round_df, "ASSISTENCIA", "\U0001F3AF Assistencias da rodada")

page_footer()
