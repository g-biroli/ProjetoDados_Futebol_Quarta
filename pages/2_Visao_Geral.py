"""Classificacao acumulada de todas as rodadas: artilheiro, garcom, lider e evolucao."""

from datetime import datetime

import streamlit as st

from src.charts import assign_player_colors, line_evolution
from src.data import cumulative_timeseries, load_data, overall_table
from src.pdf_report import build_pdf
from src.theme import (
    apply_theme,
    classification_table,
    kpi_row,
    mini_ranking_table,
    page_header,
    tiebreak_note,
)

st.set_page_config(page_title="Visao Geral - Futebol de Quarta", layout="wide")
apply_theme()
page_header("Visao Geral", "Classificacao acumulada de todas as rodadas")

try:
    df = load_data()
except Exception as exc:
    st.error(f"Nao foi possivel carregar os dados: {exc}")
    st.stop()

if df.empty:
    st.warning("Ainda nao ha rodadas registradas.")
    st.stop()

overall = overall_table(df)
player_colors = assign_player_colors(overall["JOGADOR"].tolist())

lider = overall.iloc[0]
artilheiro = overall.sort_values("GOLS", ascending=False).iloc[0]
garcom = overall.sort_values("ASSISTENCIA", ascending=False).iloc[0]
rodadas_disputadas = int(df["RODADA"].nunique())

kpi_row([
    ("Lider", lider["JOGADOR"], f"{int(lider['PTS'])} pts", player_colors[lider["JOGADOR"]]),
    ("Artilheiro", artilheiro["JOGADOR"], f"{int(artilheiro['GOLS'])} gols", player_colors[artilheiro["JOGADOR"]]),
    ("Garcom de assistencias", garcom["JOGADOR"], f"{int(garcom['ASSISTENCIA'])} assist.", player_colors[garcom["JOGADOR"]]),
    ("Rodadas disputadas", str(rodadas_disputadas), "", "#e8752b"),
])

classification_table(overall, caption="Classificacao geral")

col1, col2 = st.columns(2)
with col1:
    mini_ranking_table(overall, "GOLS", "Artilharia geral", top_n=10)
with col2:
    mini_ranking_table(overall, "ASSISTENCIA", "Assistencias geral", top_n=10)

tiebreak_note()

st.divider()
st.subheader("Evolucao ao longo das rodadas")
default_players = overall.nlargest(5, "PTS")["JOGADOR"].tolist()
players = st.multiselect(
    "Jogadores para comparar (max. 8)",
    options=overall["JOGADOR"].tolist(),
    default=default_players,
    max_selections=8,
)

fig_gols_evo = fig_assist_evo = fig_pts_evo = None

if players:
    ts_gols = cumulative_timeseries(df, "GOLS")
    ts_assist = cumulative_timeseries(df, "ASSISTENCIA")
    ts_pts = cumulative_timeseries(df, "PTS")

    fig_gols_evo = line_evolution(
        ts_gols[ts_gols["JOGADOR"].isin(players)], players, "CUM",
        "Gols acumulados", "Gols", player_colors,
    )
    st.pyplot(fig_gols_evo, use_container_width=True)

    fig_assist_evo = line_evolution(
        ts_assist[ts_assist["JOGADOR"].isin(players)], players, "CUM",
        "Assistencias acumuladas", "Assistencias", player_colors,
    )
    st.pyplot(fig_assist_evo, use_container_width=True)

    fig_pts_evo = line_evolution(
        ts_pts[ts_pts["JOGADOR"].isin(players)], players, "CUM",
        "Pontos acumulados", "Pontos", player_colors,
    )
    st.pyplot(fig_pts_evo, use_container_width=True)
else:
    st.info("Selecione ao menos um jogador para ver a evolucao.")

st.divider()
st.subheader("Relatorio em PDF")
st.caption("Gera um PDF com os mesmos indicadores, tabelas e graficos exibidos acima.")

if st.button("Gerar relatorio PDF"):
    kpis = {
        "Lider": f"{lider['JOGADOR']} ({int(lider['PTS'])} pts)",
        "Artilheiro": f"{artilheiro['JOGADOR']} ({int(artilheiro['GOLS'])} gols)",
        "Garcom de assistencias": f"{garcom['JOGADOR']} ({int(garcom['ASSISTENCIA'])} assistencias)",
        "Rodadas disputadas": str(rodadas_disputadas),
    }

    artilharia_pdf = overall.nlargest(10, "GOLS")[["JOGADOR", "GOLS"]].rename(columns={"GOLS": "VALUE"})
    assistencias_pdf = overall.nlargest(10, "ASSISTENCIA")[["JOGADOR", "ASSISTENCIA"]].rename(columns={"ASSISTENCIA": "VALUE"})

    figures = [
        ("Gols acumulados", fig_gols_evo),
        ("Assistencias acumuladas", fig_assist_evo),
        ("Pontos acumulados", fig_pts_evo),
    ]

    with st.spinner("Gerando PDF..."):
        pdf_bytes = build_pdf(
            kpis,
            overall,
            [("Artilharia geral", artilharia_pdf), ("Assistencias geral", assistencias_pdf)],
            figures,
        )

    st.download_button(
        "Baixar PDF",
        data=pdf_bytes,
        file_name=f"relatorio_futebol_quarta_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
    )
