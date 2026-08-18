"""Geracao do relatorio em PDF com os mesmos indicadores e graficos da pagina."""

import os
import tempfile
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

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

MINI_TABLE_COLUMNS = [
    ("JOGADOR", "Jogador", 60),
    ("VALUE", "Total", 25),
]


class Report(FPDF):
    def header(self) -> None:
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Futebol de Quarta - Relatorio de Estatisticas", align="C")
        self.ln(14)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")


def _render_table(pdf: FPDF, columns: list[tuple[str, str, int]], rows: pd.DataFrame) -> None:
    col_widths = [w for _, _, w in columns]
    headers = [label for _, label, _ in columns]
    field_names = [name for name, _, _ in columns]

    with pdf.table(col_widths=col_widths, text_align="CENTER", line_height=6) as table:
        header_row = table.row()
        for h in headers:
            header_row.cell(h)
        for _, record in rows.iterrows():
            row = table.row()
            for field in field_names:
                value = record[field]
                row.cell(str(value) if isinstance(value, str) else f"{value:g}")


def build_pdf(
    kpis: dict[str, str],
    overall_df: pd.DataFrame,
    mini_tables: list[tuple[str, pd.DataFrame]],
    figures: list[tuple[str, plt.Figure | None]],
) -> bytes:
    """mini_tables: lista de (titulo, dataframe com colunas JOGADOR e VALUE)."""
    pdf = Report(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_text_color(*_hex_to_rgb("#52514e"))
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(3)

    pdf.set_text_color(*_hex_to_rgb("#0b0b0b"))
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Indicadores gerais", ln=True)
    pdf.set_font("Helvetica", "", 10)
    for label, value in kpis.items():
        pdf.cell(0, 6, f"{label}: {value}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Classificacao geral", ln=True)
    pdf.set_font("Helvetica", "", 8)
    _render_table(pdf, TABLE_COLUMNS, overall_df)

    for title, mini_df in mini_tables:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(*_hex_to_rgb("#0b0b0b"))
        pdf.cell(0, 8, title, ln=True)
        pdf.set_font("Helvetica", "", 9)
        _render_table(pdf, MINI_TABLE_COLUMNS, mini_df)

    tmp_files: list[str] = []
    try:
        for title, fig in figures:
            if fig is None:
                continue
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(*_hex_to_rgb("#0b0b0b"))
            pdf.cell(0, 8, title, ln=True)

            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            tmp.close()
            fig.savefig(tmp.name, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
            tmp_files.append(tmp.name)
            pdf.image(tmp.name, x=15, w=260)
    finally:
        for path in tmp_files:
            try:
                os.unlink(path)
            except OSError:
                pass

    return bytes(pdf.output())


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
