"""Geracao do relatorio em PDF - mesmo tema escuro e os mesmos graficos/tabelas da pagina.

Cada figura informa sua propria orientacao de pagina ("L" ou "P"): os
rankings de Top 20 ficam muito altos para caber numa pagina paisagem sem
cortar, entao usam retrato; a tabela de classificacao e o grafico de pizza
ficam melhor em paisagem. O tamanho de cada imagem e sempre calculado a
partir do espaco realmente disponivel na pagina (nunca um `w` fixo "no
chute"), para nenhum grafico sair cortado.
"""

import os
import tempfile
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
from fpdf.fonts import FontFace
from PIL import Image

from src.theme import BAGRE_ICON_PATH, BAGRE_TROPHY_PATH, LOGO_PATH

BAGRE_NOTE = (
    "Como funciona o ranking de bagre: leva em conta as piores posicoes de "
    "cada rodada e do geral, pela quantidade de vitorias, derrotas e "
    "empates. Em caso de empate, o criterio de desempate usa gols e "
    "assistencias."
)

BAGRE_ROW_H = 8

BLACK = (0, 0, 0)
DARK_SURFACE = (20, 20, 20)
DARK_ALT = (28, 28, 28)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
INK_MUTED = (168, 168, 168)

MARGIN = 15

TABLE_COLUMNS = [
    ("POS", "Pos.", 14),
    ("JOGADOR", "Jogador", 45),
    ("PTS", "Pts", 16),
    ("VITORIA", "V", 16),
    ("EMPATE", "E", 16),
    ("DERROTA", "D", 16),
    ("GOLS", "Gols", 18),
    ("ASSISTENCIA", "Assist.", 20),
    ("GA", "G+A", 18),
    ("RODADAS_JOGADAS", "Rodadas", 20),
]

BAGRE_COLUMNS = [
    ("POS", "Pos.", 16),
    ("JOGADOR", "Jogador", 55),
    ("VITORIA", "V", 20),
    ("EMPATE", "E", 20),
    ("DERROTA", "D", 20),
    ("GOLS", "Gols", 20),
    ("ASSISTENCIA", "Assist.", 24),
]

HEADER_STYLE = FontFace(fill_color=BLACK, color=WHITE)
DEFAULT_ROW = FontFace(fill_color=DARK_SURFACE, color=WHITE)
ALT_ROW = FontFace(fill_color=DARK_ALT, color=WHITE)
GOLD_ROW = FontFace(fill_color=GOLD, color=BLACK)
SILVER_ROW = FontFace(fill_color=SILVER, color=BLACK)
BRONZE_ROW = FontFace(fill_color=BRONZE, color=BLACK)


class Report(FPDF):
    def header(self) -> None:
        self.set_fill_color(*BLACK)
        self.rect(0, 0, self.w, self.h, style="F")
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*WHITE)
        self.set_y(10)
        self.cell(0, 10, "Futebol Quarta-Feira - Playball 2 Pompeia", align="C")
        self.ln(15)

    def footer(self) -> None:
        if LOGO_PATH.exists():
            self.image(str(LOGO_PATH), x=self.w / 2 - 6, y=self.h - 20, h=11)
        self.set_y(-8)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*INK_MUTED)
        self.cell(0, 6, f"Pagina {self.page_no()}", align="C")


def _row_style(pos_index: int) -> FontFace:
    if pos_index == 0:
        return GOLD_ROW
    if pos_index == 1:
        return SILVER_ROW
    if pos_index == 2:
        return BRONZE_ROW
    if pos_index % 2 == 1:
        return ALT_ROW
    return DEFAULT_ROW


def _render_table(pdf: FPDF, columns: list[tuple[str, str, int]], rows: pd.DataFrame) -> None:
    col_widths = [w for _, _, w in columns]
    headers = [label for _, label, _ in columns]
    field_names = [name for name, _, _ in columns]

    with pdf.table(col_widths=col_widths, text_align="CENTER", line_height=6, headings_style=HEADER_STYLE) as table:
        header_row = table.row()
        for h in headers:
            header_row.cell(h)
        for i, (_, record) in enumerate(rows.iterrows()):
            style = _row_style(i)
            row = table.row()
            for field in field_names:
                value = record[field]
                text = str(value) if isinstance(value, str) else f"{value:g}"
                row.cell(text, style=style)


def _render_bagre_table(pdf: FPDF, rows: pd.DataFrame) -> None:
    """Tabela dos bagres desenhada celula a celula (em vez de pdf.table()),
    pra poder colocar o icone do bagre ao lado do nome e colorir so a
    coluna POS (ouro/prata/bronze) - igual a tabela da pagina web."""
    badge_fill = {1: GOLD, 2: SILVER, 3: BRONZE}
    icon_ok = BAGRE_ICON_PATH.exists()
    icon_h = BAGRE_ROW_H - 3
    x0 = pdf.l_margin
    y = pdf.get_y()

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*BLACK)
    pdf.set_text_color(*WHITE)
    x = x0
    for _field, label, w in BAGRE_COLUMNS:
        pdf.set_xy(x, y)
        pdf.cell(w, BAGRE_ROW_H, label, border=1, align="C", fill=True)
        x += w
    y += BAGRE_ROW_H

    pdf.set_font("Helvetica", "", 8)
    for i, (_, record) in enumerate(rows.iterrows()):
        pos = i + 1
        x = x0
        for field, _label, w in BAGRE_COLUMNS:
            pdf.set_xy(x, y)
            value = record[field]
            text = str(value) if isinstance(value, str) else f"{value:g}"

            if field == "POS":
                pdf.set_fill_color(*badge_fill.get(pos, DARK_SURFACE))
                pdf.set_text_color(*BLACK)
                pdf.cell(w, BAGRE_ROW_H, text, border=1, align="C", fill=True)
            elif field == "JOGADOR":
                pdf.set_fill_color(*DARK_SURFACE)
                pdf.set_text_color(*WHITE)
                pdf.cell(w, BAGRE_ROW_H, "", border=1, fill=True)
                text_x = x + 2
                if icon_ok:
                    pdf.image(str(BAGRE_ICON_PATH), x=x + 2, y=y + 1.5, h=icon_h)
                    text_x = x + 2 + icon_h + 2
                pdf.set_xy(text_x, y)
                pdf.cell(w - (text_x - x) - 1, BAGRE_ROW_H, text, align="L")
            else:
                pdf.set_fill_color(*DARK_SURFACE)
                pdf.set_text_color(*WHITE)
                pdf.cell(w, BAGRE_ROW_H, text, border=1, align="C", fill=True)
            x += w
        y += BAGRE_ROW_H

    pdf.set_xy(x0, y)


def _fit_image(pdf: FPDF, image_path: str) -> None:
    """Coloca uma imagem ocupando o maior espaco possivel sem estourar a
    pagina, calculando o tamanho a partir da proporcao real do arquivo."""
    img = Image.open(image_path)
    aspect = img.height / img.width

    max_w = pdf.w - 2 * MARGIN
    max_h = pdf.h - pdf.get_y() - MARGIN

    w = max_w
    h = w * aspect
    if h > max_h:
        h = max_h
        w = h / aspect

    x = (pdf.w - w) / 2
    pdf.image(image_path, x=x, y=pdf.get_y(), w=w, h=h)


def _add_chart_page(pdf: FPDF, title: str, fig: plt.Figure, orientation: str, tmp_files: list[str]) -> None:
    pdf.add_page(orientation=orientation)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 10, title, ln=True)

    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.close()
    fig.savefig(tmp.name, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    tmp_files.append(tmp.name)
    _fit_image(pdf, tmp.name)


def build_pdf(
    kpis: dict[str, str],
    overall_df: pd.DataFrame,
    bagre_df: pd.DataFrame,
    figures: list[tuple[str, plt.Figure | None, str]],
) -> bytes:
    """figures: lista de (titulo, figura matplotlib, orientacao "L" ou "P")."""
    pdf = Report(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=MARGIN)
    pdf.add_page()

    pdf.set_text_color(*INK_MUTED)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(3)

    pdf.set_text_color(*GOLD)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Indicadores gerais", ln=True)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "", 10)
    for label, value in kpis.items():
        pdf.cell(0, 6, f"{label}: {value}", ln=True)
    pdf.ln(4)

    pdf.set_text_color(*GOLD)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Classificacao geral", ln=True)
    pdf.set_font("Helvetica", "", 8)
    _render_table(pdf, TABLE_COLUMNS, overall_df)

    tmp_files: list[str] = []
    try:
        pdf.add_page(orientation="L")
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(*GOLD)
        pdf.cell(0, 10, "Top 3 bagres", ln=True)
        _render_bagre_table(pdf, bagre_df)
        pdf.ln(4)

        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(*INK_MUTED)
        pdf.multi_cell(0, 5, BAGRE_NOTE)
        pdf.ln(2)

        if BAGRE_TROPHY_PATH.exists():
            _fit_image(pdf, str(BAGRE_TROPHY_PATH))

        for title, fig, orientation in figures:
            if fig is None:
                continue
            _add_chart_page(pdf, title, fig, orientation, tmp_files)
    finally:
        for path in tmp_files:
            try:
                os.unlink(path)
            except OSError:
                pass

    return bytes(pdf.output())
