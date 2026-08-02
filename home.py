"""Painel de estatisticas do futebol de quarta - dados vindos do Google Sheets."""

from datetime import datetime

import streamlit as st

from src.charts import assign_player_colors, bar_ranking, line_evolution
from src.data import cumulative_timeseries, load_data, matches_held, player_summary, winrate_timeseries
from src.pdf_report import build_pdf
from src.theme import apply_theme, kpi_row, page_header

st.set_page_config(
    page_title="Futebol de Quarta - Estatisticas",
    layout="wide",
)

apply_theme()
page_header("Futebol de Quarta - Estatisticas")

with st.sidebar:
    st.header("Filtros")
    if st.button("Atualizar dados da planilha"):
        load_data.clear()
        st.rerun()

try:
    df_raw = load_data()
except Exception as exc:
    st.error(
        "Nao foi possivel carregar os dados da planilha. Verifique se ela continua "
        f"compartilhada como 'Qualquer pessoa com o link'. Detalhe: {exc}"
    )
    st.stop()

if df_raw.empty:
    st.warning("A planilha ainda nao possui registros.")
    st.stop()

min_date, max_date = df_raw["DATA"].min().date(), df_raw["DATA"].max().date()

with st.sidebar:
    date_range = st.date_input(
        "Periodo",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

df = df_raw[
    (df_raw["DATA"].dt.date >= start_date) & (df_raw["DATA"].dt.date <= end_date)
]

if df.empty:
    st.warning("Nenhum registro no periodo selecionado.")
    st.stop()

summary = player_summary(df)
player_colors = assign_player_colors(summary["JOGADOR"].tolist())

# ---------------------------------------------------------------- KPIs ----
artilheiro = summary.iloc[0]
garcom = summary.sort_values("ASSISTENCIAS", ascending=False).iloc[0]
mais_presente = summary.sort_values("DIAS_JOGADOS", ascending=False).iloc[0]
total_dias = df["DATA"].nunique()
total_partidas = matches_held(df)

kpi_row([
    ("Artilheiro", artilheiro["JOGADOR"], f"{int(artilheiro['GOLS'])} gols", player_colors[artilheiro["JOGADOR"]]),
    ("Garcom de assistencias", garcom["JOGADOR"], f"{int(garcom['ASSISTENCIAS'])} assist.", player_colors[garcom["JOGADOR"]]),
    ("Mais presente", mais_presente["JOGADOR"], f"{int(mais_presente['DIAS_JOGADOS'])} dias", player_colors[mais_presente["JOGADOR"]]),
    ("Dias de jogo no periodo", str(total_dias), "", "#eda100"),
    ("Partidas disputadas", str(total_partidas), "", "#e34948"),
])

st.caption(
    "Dias de jogo = numero de quartas em que o jogador participou. "
    "Partidas disputadas = total de jogos internos realizados no periodo "
    "(vitorias + derrotas + empates de cada dia, sem repetir por jogador)."
)

st.divider()

tab_ranking, tab_evolucao, tab_dados = st.tabs(["Ranking", "Evolucao", "Dados brutos"])

with tab_ranking:
    st.subheader("Classificacao geral")
    st.dataframe(
        summary.rename(
            columns={
                "JOGADOR": "Jogador",
                "DIAS_JOGADOS": "Dias",
                "PARTIDAS": "Partidas",
                "GOLS": "Gols",
                "ASSISTENCIAS": "Assistencias",
                "VITORIAS": "Vitorias",
                "DERROTAS": "Derrotas",
                "EMPATES": "Empates",
                "APROVEITAMENTO_%": "Aproveitamento %",
                "MEDIA_GOLS_DIA": "Media gols/dia",
                "MEDIA_ASSIST_DIA": "Media assist/dia",
                "PARTICIPACOES_GOL": "Participacoes em gol",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    rank_col1, rank_col2 = st.columns(2)
    fig_gols = bar_ranking(summary, "GOLS", "Artilharia - Top 8", player_colors)
    fig_assist = bar_ranking(summary, "ASSISTENCIAS", "Assistencias - Top 8", player_colors)
    rank_col1.pyplot(fig_gols, use_container_width=True)
    rank_col2.pyplot(fig_assist, use_container_width=True)

with tab_evolucao:
    st.subheader("Evolucao ao longo do tempo")
    default_players = summary.nlargest(5, "GOLS")["JOGADOR"].tolist()
    players = st.multiselect(
        "Jogadores para comparar (max. 8)",
        options=summary["JOGADOR"].tolist(),
        default=default_players,
        max_selections=8,
    )

    fig_gols_evo = fig_assist_evo = fig_win_evo = None

    if players:
        ts_gols = cumulative_timeseries(df, "GOLS")
        ts_assist = cumulative_timeseries(df, "ASSISTENCIA")
        ts_win = winrate_timeseries(df)

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

        fig_win_evo = line_evolution(
            ts_win[ts_win["JOGADOR"].isin(players)], players, "APROVEITAMENTO_%",
            "Aproveitamento acumulado (%)", "Aproveitamento %", player_colors,
        )
        st.pyplot(fig_win_evo, use_container_width=True)
    else:
        st.info("Selecione ao menos um jogador para ver a evolucao.")

with tab_dados:
    st.subheader("Dados brutos (planilha tratada)")
    st.dataframe(
        df.sort_values("DATA", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Baixar dados em CSV",
        df.to_csv(index=False).encode("utf-8-sig"),
        file_name="futebol_quarta_dados.csv",
        mime="text/csv",
    )

st.divider()
st.subheader("Relatorio em PDF")
st.caption("Gera um PDF com os mesmos indicadores e graficos exibidos acima.")

if st.button("Gerar relatorio PDF"):
    kpis = {
        "Artilheiro": f"{artilheiro['JOGADOR']} ({int(artilheiro['GOLS'])} gols)",
        "Garcom de assistencias": f"{garcom['JOGADOR']} ({int(garcom['ASSISTENCIAS'])} assistencias)",
        "Jogador mais presente": f"{mais_presente['JOGADOR']} ({int(mais_presente['DIAS_JOGADOS'])} dias)",
        "Dias de jogo no periodo": str(total_dias),
        "Partidas disputadas": str(total_partidas),
        "Periodo": f"{start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}",
    }

    figures = [
        ("Artilharia - Top 8", fig_gols),
        ("Assistencias - Top 8", fig_assist),
        ("Gols acumulados", fig_gols_evo),
        ("Assistencias acumuladas", fig_assist_evo),
        ("Aproveitamento acumulado", fig_win_evo),
    ]

    with st.spinner("Gerando PDF..."):
        pdf_bytes = build_pdf(kpis, summary, figures)

    st.download_button(
        "Baixar PDF",
        data=pdf_bytes,
        file_name=f"relatorio_futebol_quarta_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
    )
