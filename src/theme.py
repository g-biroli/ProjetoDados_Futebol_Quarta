"""Identidade visual "placar de futebol" (navy / laranja / dourado / vermelho),
inspirada no boletim de classificacao usado pelo grupo (POS/JOGADOR/PTS/V/E/D/G/A).

Nao reproduz a logo do grupo nem qualquer marca de terceiros - apenas o
layout (cabecalho com rodada/data, tabela de classificacao, paineis de
artilharia/assistencias, legenda de desempate) e a paleta de cores.
"""

import html

import pandas as pd
import streamlit as st

NAVY = "#0d1b4c"
ORANGE = "#e8752b"
GOLD = "#f2c14e"
RED = "#a4222f"
INK_ON_DARK = "#ffffff"

BAND_COLORS = [NAVY, ORANGE, GOLD]
# Texto branco so tem contraste seguro sobre o navy escuro; laranja e dourado
# (claros) usam texto navy para manter leitura confortavel.
BAND_TEXT = ["#ffffff", NAVY, NAVY]

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.sb-header {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    background: {NAVY};
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 18px;
}}

.sb-title-main {{
    font-family: 'Archivo Black', 'Inter', sans-serif;
    font-size: 1.9rem;
    color: {INK_ON_DARK};
    line-height: 1.1;
}}

.sb-title-sub {{
    color: {GOLD};
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    margin-top: 2px;
}}

.sb-badges {{
    display: flex;
    gap: 10px;
}}

.sb-badge {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 8px;
    padding: 6px 14px;
    text-align: center;
}}

.sb-badge-label {{
    display: block;
    font-size: 0.65rem;
    color: {GOLD};
    letter-spacing: 0.05em;
    font-weight: 600;
}}

.sb-badge-value {{
    display: block;
    font-family: 'Archivo Black', 'Inter', sans-serif;
    font-size: 1.15rem;
    color: {INK_ON_DARK};
}}

.sb-table-wrap {{
    overflow-x: auto;
    border-radius: 10px;
    border: 1px solid rgba(11,11,11,0.08);
    margin-bottom: 18px;
}}

table.sb-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
}}

table.sb-table caption {{
    text-align: left;
    background: {RED};
    color: {INK_ON_DARK};
    font-weight: 700;
    padding: 8px 12px;
    font-size: 0.85rem;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}}

table.sb-table th {{
    background: {NAVY};
    color: {INK_ON_DARK};
    padding: 8px 10px;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    text-align: center;
    position: sticky;
    top: 0;
}}

table.sb-table th.sb-col-jogador {{
    text-align: left;
}}

table.sb-table td {{
    padding: 7px 10px;
    text-align: center;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
}}

table.sb-table td.sb-col-jogador {{
    text-align: left;
    font-weight: 700;
}}

.wc-stripe {{
    height: 6px;
    border-radius: 999px;
    margin: 0 0 22px 0;
    background: linear-gradient(90deg, {NAVY}, {ORANGE}, {GOLD}, {RED});
}}

.wc-title {{
    font-family: 'Archivo Black', 'Inter', sans-serif;
    font-size: 2.3rem;
    line-height: 1.15;
    color: #0b0b0b;
    margin-bottom: 0.1rem;
}}

.wc-subtitle {{
    color: #52514e;
    font-size: 0.95rem;
    margin-bottom: 1.1rem;
}}

.wc-kpi-row {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
    margin-bottom: 8px;
}}

.wc-kpi {{
    background: #fcfcfb;
    border: 1px solid rgba(11, 11, 11, 0.08);
    border-top: 4px solid var(--wc-accent, {NAVY});
    border-radius: 10px;
    padding: 14px 16px;
}}

.wc-kpi .wc-kpi-label {{
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #52514e;
}}

.wc-kpi .wc-kpi-value {{
    font-family: 'Archivo Black', 'Inter', sans-serif;
    font-size: 1.7rem;
    color: #0b0b0b;
    margin: 4px 0 2px 0;
    line-height: 1.1;
}}

.wc-kpi .wc-kpi-sub {{
    font-size: 0.78rem;
    color: #52514e;
}}

.sb-tiebreak {{
    background: #fcfcfb;
    border: 1px solid rgba(11,11,11,0.08);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.8rem;
    color: #52514e;
}}

.sb-tiebreak b {{
    color: {NAVY};
}}

.stTabs [data-baseweb="tab"] {{
    font-weight: 600;
}}
</style>
"""


def apply_theme() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str | None = None) -> None:
    st.markdown(f'<div class="wc-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="wc-subtitle">{html.escape(subtitle)}</div>', unsafe_allow_html=True)
    st.markdown('<div class="wc-stripe"></div>', unsafe_allow_html=True)


def kpi_row(cards: list[tuple[str, str, str, str]]) -> None:
    """cards: lista de (label, valor, sublabel, cor_de_destaque)."""
    parts = ['<div class="wc-kpi-row">']
    for label, value, sub, accent in cards:
        parts.append(
            f'<div class="wc-kpi" style="--wc-accent:{accent}">'
            f'<div class="wc-kpi-label">{html.escape(label)}</div>'
            f'<div class="wc-kpi-value">{html.escape(value)}</div>'
            f'<div class="wc-kpi-sub">{html.escape(sub)}</div>'
            f"</div>"
        )
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def scoreboard_header(title: str, rodada_label: str, data_label: str) -> None:
    st.markdown(
        f"""
        <div class="sb-header">
            <div>
                <div class="sb-title-main">{html.escape(title)}</div>
                <div class="sb-title-sub">Classificacao</div>
            </div>
            <div class="sb-badges">
                <div class="sb-badge">
                    <span class="sb-badge-label">Rodada</span>
                    <span class="sb-badge-value">{html.escape(rodada_label)}</span>
                </div>
                <div class="sb-badge">
                    <span class="sb-badge-label">Data</span>
                    <span class="sb-badge-value">{html.escape(data_label)}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def classification_table(df: pd.DataFrame, caption: str = "Classificacao geral") -> None:
    """Tabela POS/JOGADOR/PTS/V/E/D/GOLS/ASSISTENCIA/G+A no estilo placar,
    com uma faixa de cor por linha (decorativa, ciclando navy/laranja/dourado
    - nao representa o time de fato disputado, essa informacao nao esta
    disponivel de forma estruturada na planilha)."""
    columns = [
        ("POS", "POS"),
        ("JOGADOR", "Jogador"),
        ("PTS", "PTS"),
        ("VITORIA", "V"),
        ("EMPATE", "E"),
        ("DERROTA", "D"),
        ("GOLS", "G"),
        ("ASSISTENCIA", "A"),
        ("GA", "G+A"),
    ]

    rows_html = []
    for i, (_, row) in enumerate(df.iterrows()):
        band = BAND_COLORS[i % len(BAND_COLORS)]
        text = BAND_TEXT[i % len(BAND_TEXT)]
        cells = []
        for col, _ in columns:
            css_class = "sb-col-jogador" if col == "JOGADOR" else ""
            cells.append(f'<td class="{css_class}">{html.escape(str(row[col]))}</td>')
        rows_html.append(f'<tr style="background:{band};color:{text}">{"".join(cells)}</tr>')

    header_html = "".join(
        f'<th class="{"sb-col-jogador" if col == "JOGADOR" else ""}">{html.escape(label)}</th>'
        for col, label in columns
    )

    table_html = (
        '<div class="sb-table-wrap"><table class="sb-table">'
        f"<caption>{html.escape(caption)}</caption>"
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{''.join(rows_html)}</tbody>"
        "</table></div>"
    )
    st.markdown(table_html, unsafe_allow_html=True)


def mini_ranking_table(df: pd.DataFrame, value_col: str, caption: str, top_n: int = 10) -> None:
    """Painel lateral simples (Nº, Jogador, valor) tipo 'Artilharia'/'Assistencias'."""
    top = df.nlargest(top_n, value_col)[["JOGADOR", value_col]].reset_index(drop=True)

    rows_html = []
    for i, row in top.iterrows():
        band = BAND_COLORS[i % len(BAND_COLORS)]
        text = BAND_TEXT[i % len(BAND_TEXT)]
        rows_html.append(
            f'<tr style="background:{band};color:{text}">'
            f'<td>{i + 1}</td>'
            f'<td class="sb-col-jogador">{html.escape(str(row["JOGADOR"]))}</td>'
            f'<td>{html.escape(str(row[value_col]))}</td>'
            f"</tr>"
        )

    table_html = (
        '<div class="sb-table-wrap"><table class="sb-table">'
        f"<caption>{html.escape(caption)}</caption>"
        f'<thead><tr><th>Nº</th><th class="sb-col-jogador">Jogador</th><th>{html.escape(value_col)}</th></tr></thead>'
        f"<tbody>{''.join(rows_html)}</tbody>"
        "</table></div>"
    )
    st.markdown(table_html, unsafe_allow_html=True)


def tiebreak_note() -> None:
    st.markdown(
        '<div class="sb-tiebreak"><b>Criterios de desempate:</b> '
        "1&ordm; pontos &middot; 2&ordm; gols + assistencias &middot; "
        "3&ordm; gols &middot; 4&ordm; assistencias</div>",
        unsafe_allow_html=True,
    )
