"""Identidade visual do app: modo escuro (preto), no espirito da logo do
grupo e da Copa do Mundo 26, com as cores vibrantes da paleta oficial usadas
como destaque (KPIs, graficos, medalhas).

Nao reproduz a logo da FIFA/Copa do Mundo nem qualquer marca de terceiros -
apenas a paleta de cores e o espirito "preto com destaque dourado". As
imagens em assets/ (logo do grupo e trofeu "Bagre D'Or") sao do proprio
grupo.
"""

import base64
import html
from pathlib import Path

import pandas as pd
import streamlit as st

from src.charts import BRONZE, GOLD, PALETTE, SILVER

BLACK = "#000000"
WHITE = "#ffffff"
SURFACE = "#141414"
SURFACE_ALT = "#1c1c1c"
INK = "#f5f5f5"
INK_MUTED = "#a8a8a8"
BORDER = "rgba(255,255,255,0.12)"

MEDALS = {1: "\U0001F947", 2: "\U0001F948", 3: "\U0001F949"}  # 🥇 🥈 🥉
MEDAL_ROW_CLASS = {1: "sb-row-gold", 2: "sb-row-silver", 3: "sb-row-bronze"}

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"
BAGRE_ICON_PATH = ASSETS_DIR / "icone_bagre.png"
BAGRE_TROPHY_PATH = ASSETS_DIR / "bagre_score.jpg"


@st.cache_data(show_spinner=False)
def _img_data_uri(path: Path) -> str | None:
    if not path.exists():
        return None
    ext = path.suffix.lstrip(".").lower()
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return f"data:image/{mime};base64," + base64.b64encode(path.read_bytes()).decode()


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
    background: {SURFACE};
    border: 1px solid rgba(212,175,55,0.35);
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
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.2);
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
    background: {SURFACE};
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
    background: {SURFACE_ALT};
}}

table.sb-table tr.sb-row-gold td {{
    background: {GOLD};
    color: #000000;
    font-weight: 700;
}}

table.sb-table tr.sb-row-silver td {{
    background: {SILVER};
    color: #000000;
    font-weight: 700;
}}

table.sb-table tr.sb-row-bronze td {{
    background: {BRONZE};
    color: #000000;
    font-weight: 700;
}}

table.sb-table tr.sb-row-bagre td {{
    background: {GOLD};
    color: #000000;
    font-weight: 600;
}}

.bagre-icon {{
    height: 22px;
    width: auto;
    vertical-align: middle;
    margin-right: 6px;
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
    color: {WHITE};
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
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-top: 4px solid var(--wc-accent, {GOLD});
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
    color: {WHITE};
    margin: 4px 0 2px 0;
    line-height: 1.1;
}}

.wc-kpi .wc-kpi-sub {{
    font-size: 0.78rem;
    color: {INK_MUTED};
}}

.callout-phrase {{
    font-family: 'Archivo Black', 'Inter', sans-serif;
    font-size: clamp(1.6rem, 4vw, 2.6rem);
    color: {GOLD};
    text-align: center;
    line-height: 1.25;
    margin: 26px 0 10px 0;
}}

.callout-sub {{
    font-family: 'Archivo Black', 'Inter', sans-serif;
    font-size: clamp(1.2rem, 2.6vw, 1.8rem);
    color: {WHITE};
    text-align: center;
    line-height: 1.25;
    margin: 0 0 26px 0;
}}

.gh-button {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: transparent;
    color: {GOLD} !important;
    text-decoration: none !important;
    padding: 10px 18px;
    border: 1.5px solid {GOLD};
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
}}

.gh-button:hover {{
    background: {GOLD};
    color: #000000 !important;
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


def callout(text: str, variant: str = "primary") -> None:
    css_class = "callout-phrase" if variant == "primary" else "callout-sub"
    st.markdown(f'<div class="{css_class}">{html.escape(text)}</div>', unsafe_allow_html=True)


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


def classification_table(df: pd.DataFrame, caption: str = "Classificacao geral") -> None:
    """Tabela POS/JOGADOR/PTS/V/E/D/GOLS/ASSISTENCIA/G+A, com a 1a linha em
    ouro, a 2a em prata e a 3a em bronze - as cores da Copa representando o
    podio - e medalha ao lado da posicao."""
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
        cells = []
        for col, _ in columns:
            css_class = "sb-col-jogador" if col == "JOGADOR" else ""
            value = html.escape(str(row[col]))
            if col == "POS" and pos in MEDALS:
                value = f"{value} {MEDALS[pos]}"
            cells.append(f'<td class="{css_class}">{value}</td>')

        if pos in MEDAL_ROW_CLASS:
            row_class = MEDAL_ROW_CLASS[pos]
        elif i % 2 == 1:
            row_class = "sb-row-alt"
        else:
            row_class = ""
        attrs = f' class="{row_class}"' if row_class else ""
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


def mini_ranking_table(df: pd.DataFrame, value_col: str, caption: str, top_n: int = 20) -> None:
    """Painel tipo 'Artilharia'/'Assistencias' (Nº, Jogador, valor), com
    ouro/prata/bronze nos 3 primeiros."""
    top = df.nlargest(top_n, value_col)[["JOGADOR", value_col]].reset_index(drop=True)

    rows_html = []
    for i, row in top.iterrows():
        pos = i + 1
        pos_label = f"{pos} {MEDALS[pos]}" if pos in MEDALS else str(pos)

        if pos in MEDAL_ROW_CLASS:
            row_class = MEDAL_ROW_CLASS[pos]
        elif i % 2 == 1:
            row_class = "sb-row-alt"
        else:
            row_class = ""
        attrs = f' class="{row_class}"' if row_class else ""

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


def bagre_table(df: pd.DataFrame, caption: str) -> None:
    """Top 3 'bagres' (piores colocados: mais derrota, menos gol, menos
    assistencia) - todas as linhas em ouro, com o icone do bagre ao lado do
    nome de cada jogador."""
    icon_uri = _img_data_uri(BAGRE_ICON_PATH)
    columns = [
        ("POS", "POS"),
        ("JOGADOR", "Jogador"),
        ("VITORIA", "V"),
        ("EMPATE", "E"),
        ("DERROTA", "D"),
        ("GOLS", "G"),
        ("ASSISTENCIA", "A"),
    ]

    rows_html = []
    for _, row in df.iterrows():
        cells = []
        for col, _ in columns:
            css_class = "sb-col-jogador" if col == "JOGADOR" else ""
            value = html.escape(str(row[col]))
            if col == "JOGADOR" and icon_uri:
                value = f'<img src="{icon_uri}" class="bagre-icon" alt="">{value}'
            cells.append(f'<td class="{css_class}">{value}</td>')
        rows_html.append(f'<tr class="sb-row-bagre">{"".join(cells)}</tr>')

    header_html = "".join(
        f'<th class="{"sb-col-jogador" if col == "JOGADOR" else ""}">{html.escape(label)}</th>'
        for col, label in columns
    )

    table_html = (
        '<div class="sb-table-wrap"><table class="sb-table">'
        f"<caption>\U0001F41F {html.escape(caption)}</caption>"
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{''.join(rows_html)}</tbody>"
        "</table></div>"
    )
    st.markdown(table_html, unsafe_allow_html=True)


def bagre_trophy() -> None:
    """Exibe o trofeu 'Bagre D'Or' (assets/bagre_score.jpg), centralizado."""
    if not BAGRE_TROPHY_PATH.exists():
        return
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(str(BAGRE_TROPHY_PATH), use_container_width=True)


def github_button(url: str, label: str = "Ver codigo no GitHub") -> None:
    st.markdown(
        f'<a class="gh-button" href="{html.escape(url)}" target="_blank">{html.escape(label)}</a>',
        unsafe_allow_html=True,
    )


def page_footer() -> None:
    """Logo do grupo, centralizada, no rodape da pagina."""
    if not LOGO_PATH.exists():
        return
    st.write("")
    st.divider()
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image(str(LOGO_PATH), use_container_width=True)
