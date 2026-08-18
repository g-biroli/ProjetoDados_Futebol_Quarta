"""Resultado individual de uma rodada especifica."""

import streamlit as st

from src.data import load_data, round_table
from src.theme import (
    apply_theme,
    classification_table,
    mini_ranking_table,
    page_header,
    scoreboard_header,
    tiebreak_note,
)

st.set_page_config(page_title="Visao da Rodada - Futebol de Quarta", layout="wide")
apply_theme()
page_header("Visao da Rodada")

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
classification_table(round_df, caption=f"Classificacao - Rodada {rodada}")

col1, col2 = st.columns(2)
with col1:
    mini_ranking_table(round_df, "GOLS", "Artilharia da rodada", top_n=10)
with col2:
    mini_ranking_table(round_df, "ASSISTENCIA", "Assistencias da rodada", top_n=10)

tiebreak_note()
