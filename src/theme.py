"""Identidade visual do app: paleta vibrante e tipografia bold, no espirito da
Copa do Mundo 2026, sem reproduzir a logo ou marca oficial da FIFA."""

import html

import streamlit as st

from src.charts import PALETTE

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
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
    border-top: 4px solid var(--wc-accent, #2a78d6);
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
    color: #006300;
}}

.stTabs [data-baseweb="tab"] {{
    font-weight: 600;
}}
</style>
"""


def apply_theme() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str | None = None) -> None:
    st.markdown(f'<div class="wc-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="wc-subtitle">{subtitle}</div>', unsafe_allow_html=True)
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
