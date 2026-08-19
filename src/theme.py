"""Identidade visual do app: base preto/branco (Copa do Mundo 26), com as
cores vibrantes da paleta oficial usadas como destaque (KPIs, graficos,
medalhas) e nao como fundo de tabela inteira - mantendo as tabelas de
classificacao limpas e faceis de ler.

Nao reproduz a logo da FIFA/Copa do Mundo nem qualquer marca de terceiros -
apenas a paleta de cores e o espirito "preto e branco com destaque dourado".
"""

import html

import pandas as pd
import streamlit as st

from src.charts import BRONZE, GOLD, PALETTE, SILVER

BLACK = "#000000"
WHITE = "#ffffff"
INK = "#111111"
INK_MUTED = "#5c5c5c"
ROW_ALT = "#f7f7f7"
BORDER = "rgba(0,0,0,0.08)"

MEDALS = {1: "\U0001F947", 2: "\U0001F948", 3: "\U0001F949"}  # 🥇 🥈 🥉
MEDAL_BORDER = {1: GOLD, 2: SILVER, 3: BRONZE}

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
    background: {BLACK};
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 18px;
}}

.sb-title-main {{
    font-family: 'Archivo Black', 'Inter', sans-serif;
    font-size: 1.9rem;
    color: {WHITE};
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
    color: {WHITE};
}}

.sb-table-wrap {{
    overflow-x: auto;
    border-radius: 10px;
    border: 1px solid {BORDER};
    margin-bottom: 18px;
}}

table.sb-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    background: {WHITE};
}}

table.sb-table caption {{
    text-align: left;
    background: {BLACK};
    color: {WHITE};
    font-weight: 700;
    padding: 8px 12px;
    font-size: 0.85rem;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}}

table.sb-table th {{
    background: {BLACK};
    color: {WHITE};
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
    color: {INK};
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
    border-bottom: 1px solid {BORDER};
}}

table.sb-table td.sb-col-jogador {{
    text-align: left;
    font-weight: 700;
}}

table.sb-table tr.sb-row-alt td {{
    background: {ROW_ALT};
}}

table.sb-table tr.sb-row-medal td:first-child {{
    box-shadow: inset 4px 0 0 0 var(--medal-color);
}}

.wc-stripe {{
    height: 6px;
    border-radius: 999px;
    margin: 0 0 22px 0;
    background: linear-gradient(90deg, {", ".join(PALETTE)});
}}

.wc-title {{
    font-family: 'Archivo Black', 'Inter', sans-serif;
    font-size: 2.3rem;
    line-height: 1.15;
    color: {INK};
    margin-bottom: 0.1rem;
}}

.wc-subtitle {{
    color: {INK_MUTED};
    font-size: 0.95rem;
    margin-bottom: 1.1rem;
}}

.wc-kpi-row {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-bottom: 8px;
}}

.wc-kpi {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-top: 4px solid var(--wc-accent, {BLACK});
    border-radius: 10px;
    padding: 14px 16px;
}}

.wc-kpi .wc-kpi-label {{
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: {INK_MUTED};
}}

.wc-kpi .wc-kpi-value {{
    font-family: 'Archivo Black', 'Inter', sans-serif;
    font-size: 1.7rem;
    color: {INK};
    margin: 4px 0 2px 0;
    line-height: 1.1;
}}

.wc-kpi .wc-kpi-sub {{
    font-size: 0.78rem;
    color: {INK_MUTED};
}}

.sb-tiebreak {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.8rem;
    color: {INK_MUTED};
}}

.sb-tiebreak b {{
    color: {INK};
}}

.gh-button {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: {BLACK};
    color: {WHITE} !important;
    text-decoration: none !important;
    padding: 10px 18px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
}}

.gh-button:hover {{
    background: #222;
}}

.credit-line {{
    color: {INK_MUTED};
    font-size: 0.85rem;
    margin-top: 4px;
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
                <div class="sb-title-main">\U000026BD {html.escape(title)}</div>
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


def _medal_row_attrs(pos: int) -> str:
    if pos in MEDAL_BORDER:
        return f' class="sb-row-medal" style="--medal-color:{MEDAL_BORDER[pos]}"'
    return ""


def classification_table(df: pd.DataFrame, caption: str = "Classificacao geral") -> None:
    """Tabela POS/JOGADOR/PTS/V/E/D/GOLS/ASSISTENCIA/G+A limpa (fundo branco,
    zebra sutil), com medalha de ouro/prata/bronze nos 3 primeiros colocados."""
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
        pos = int(row["POS"])
        row_class = "sb-row-alt" if i % 2 == 1 else ""
        cells = []
        for col, _ in columns:
            css_class = "sb-col-jogador" if col == "JOGADOR" else ""
            value = html.escape(str(row[col]))
            if col == "POS" and pos in MEDALS:
                value = f"{value} {MEDALS[pos]}"
            cells.append(f'<td class="{css_class}">{value}</td>')
        attrs = f' class="{row_class}"' if row_class else ""
        medal_attrs = _medal_row_attrs(pos)
        if medal_attrs:
            attrs = medal_attrs
        rows_html.append(f"<tr{attrs}>{''.join(cells)}</tr>")

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
    """Painel lateral simples (Nº, Jogador, valor) tipo 'Artilharia'/'Assistencias',
    tambem com medalha nos 3 primeiros."""
    top = df.nlargest(top_n, value_col)[["JOGADOR", value_col]].reset_index(drop=True)

    rows_html = []
    for i, row in top.iterrows():
        pos = i + 1
        row_class = "sb-row-alt" if i % 2 == 1 else ""
        pos_label = f"{pos} {MEDALS[pos]}" if pos in MEDALS else str(pos)
        attrs = _medal_row_attrs(pos) or (f' class="{row_class}"' if row_class else "")
        rows_html.append(
            f"<tr{attrs}>"
            f"<td>{pos_label}</td>"
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


def github_button(url: str, label: str = "Ver codigo no GitHub") -> None:
    st.markdown(
        f'<a class="gh-button" href="{html.escape(url)}" target="_blank">{html.escape(label)}</a>',
        unsafe_allow_html=True,
    )
