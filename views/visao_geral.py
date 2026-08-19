"""Classificacao acumulada de todas as rodadas: artilheiro, garcom, lider, bagres e graficos."""

from datetime import datetime

import streamlit as st

from src.charts import assign_player_colors, bar_ranking, pie_share, ved_bar
from src.data import bagre_ranking, load_data, overall_table
from src.pdf_report import build_pdf
from src.theme import (
    apply_theme,
    bagre_note,
    bagre_table,
    bagre_trophy,
    classification_table,
    kpi_row,
    mini_ranking_table,
    page_footer,
    page_header,
)

apply_theme()
page_header("\U0001F3C6 Visao Geral", "Classificacao acumulada de todas as rodadas")

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
bagres_geral = bagre_ranking(overall, top_n=3)

lider = overall.iloc[0]
artilheiro = overall.sort_values("GOLS", ascending=False).iloc[0]
garcom = overall.sort_values("ASSISTENCIA", ascending=False).iloc[0]
rodadas_disputadas = int(df["RODADA"].nunique())

kpi_row([
    ("\U0001F3C6 Lider", lider["JOGADOR"], f"{int(lider['PTS'])} pts", player_colors[lider["JOGADOR"]]),
    ("\U000026BD Artilheiro", artilheiro["JOGADOR"], f"{int(artilheiro['GOLS'])} gols", player_colors[artilheiro["JOGADOR"]]),
    ("\U0001F3AF Garcom de assistencias", garcom["JOGADOR"], f"{int(garcom['ASSISTENCIA'])} assist.", player_colors[garcom["JOGADOR"]]),
    ("\U0001F4C5 Rodadas disputadas", str(rodadas_disputadas), "", "#FF3D00"),
])

bagre_table(bagres_geral, "Top 3 bagres do geral")
bagre_note()
bagre_trophy()

st.divider()
classification_table(overall, caption="\U0001F3C6 Classificacao geral")

col1, col2 = st.columns(2)
with col1:
    mini_ranking_table(overall, "GOLS", "\U000026BD Artilharia geral")
with col2:
    mini_ranking_table(overall, "ASSISTENCIA", "\U0001F3AF Assistencias geral")

st.divider()
st.subheader("\U0001F4CA Analises visuais")

fig_gols_rank = bar_ranking(overall, "GOLS", "Artilharia - Top 20", player_colors)
fig_assist_rank = bar_ranking(overall, "ASSISTENCIA", "Assistencias - Top 20", player_colors)
fig_gols_pie = pie_share(overall, "GOLS", "Fatia de gols por jogador")
fig_ved = ved_bar(overall, "Vitorias, empates e derrotas - Top 20 (por pontos)")

row1_col1, row1_col2 = st.columns(2)
row1_col1.pyplot(fig_gols_rank, use_container_width=True)
row1_col2.pyplot(fig_assist_rank, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)
row2_col1.pyplot(fig_gols_pie, use_container_width=True)
row2_col2.pyplot(fig_ved, use_container_width=True)

st.divider()
st.subheader("\U0001F4C4 Relatorio em PDF")
st.caption("Gera um PDF com os mesmos indicadores, tabelas e graficos exibidos acima.")

if st.button("Gerar relatorio PDF"):
    kpis = {
        "Lider": f"{lider['JOGADOR']} ({int(lider['PTS'])} pts)",
        "Artilheiro": f"{artilheiro['JOGADOR']} ({int(artilheiro['GOLS'])} gols)",
        "Garcom de assistencias": f"{garcom['JOGADOR']} ({int(garcom['ASSISTENCIA'])} assistencias)",
        "Rodadas disputadas": str(rodadas_disputadas),
    }

    figures = [
        ("Artilharia - Top 20", fig_gols_rank, "P"),
        ("Assistencias - Top 20", fig_assist_rank, "P"),
        ("Fatia de gols por jogador", fig_gols_pie, "L"),
        ("Vitorias, empates e derrotas", fig_ved, "P"),
    ]

    with st.spinner("Gerando PDF..."):
        pdf_bytes = build_pdf(kpis, overall, bagres_geral, figures)

    st.download_button(
        "Baixar PDF",
        data=pdf_bytes,
        file_name=f"relatorio_futebol_quarta_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
    )

page_footer()
