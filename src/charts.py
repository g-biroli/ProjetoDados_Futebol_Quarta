"""Graficos matplotlib reutilizados tanto na pagina Streamlit quanto no PDF.

Paleta baseada nas cores oficiais da FIFA World Cup 26 fornecidas pelo grupo,
aplicada sobre fundo escuro (preto), que e a identidade visual do projeto.
Como duas das cores dadas (vermelho `#D50101` e vermelho profundo `#CE1125`)
ficam proximas demais em matiz para servir como series adjacentes num mesmo
grafico, so uma delas entra na rotacao categorica. A ordem abaixo prioriza
tanto o espacamento perceptual entre cores vizinhas quanto o contraste contra
o fundo preto (nao havia Node.js disponivel neste ambiente para rodar o
validador automatico do skill de dataviz, entao o espacamento foi feito
manualmente por matiz + luminancia, com contraste de texto calculado via
formula WCAG para cada cor - ver PALETTE_TEXT). Cada marca tambem recebe um
contorno claro fino, para nao "sumir" no fundo preto mesmo nas cores mais
escuras da paleta (roxo, verde-mexico).
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

BLUE = "#304FFE"
ORANGE = "#FF3D00"
BRIGHT_GREEN = "#00C852"
LIME = "#AFEA00"
DEEP_RED = "#CE1125"
PURPLE = "#6200EA"
MEXICO_GREEN = "#006847"

PALETTE = [BLUE, ORANGE, BRIGHT_GREEN, LIME, DEEP_RED, PURPLE, MEXICO_GREEN]
# Cor de texto com melhor contraste (WCAG) sobre cada cor da paleta, na mesma ordem.
PALETTE_TEXT = ["#ffffff", "#000000", "#000000", "#000000", "#ffffff", "#ffffff", "#ffffff"]

GOLD = "#D4AF37"
SILVER = "#C0C0C0"
BRONZE = "#CD7F32"

GOOD = BRIGHT_GREEN
NEUTRAL = GOLD
BAD = DEEP_RED

SURFACE = "#0d0d0d"
INK_PRIMARY = "#ffffff"
INK_SECONDARY = "#c9c9c9"
GRID = "#2b2b2b"
AXIS = "#4d4d4d"
MUTED = "#555555"
MARK_EDGE = "#0d0d0d"


def _style_ax(ax: plt.Axes) -> None:
    ax.set_facecolor(SURFACE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(AXIS)
    ax.spines["bottom"].set_color(AXIS)
    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK_SECONDARY, labelsize=9)


def assign_player_colors(players: list[str]) -> dict[str, str]:
    """Cor fixa por jogador (ordem alfabetica), estavel entre filtros e recargas.

    Como a cor segue a entidade (nunca a posicao no ranking), reordenar por
    data ou por metrica nao repinta ninguem - ver regra de cor do skill de
    dataviz ("color follows the entity, never its rank").
    """
    ordered = sorted(set(players))
    return {p: PALETTE[i % len(PALETTE)] for i, p in enumerate(ordered)}


def bar_ranking(
    summary_df: pd.DataFrame,
    metric: str,
    title: str,
    player_colors: dict[str, str],
    top_n: int = 20,
) -> plt.Figure:
    """Ranking horizontal (top N jogadores) para uma metrica como GOLS ou ASSISTENCIA."""
    data = summary_df.nlargest(top_n, metric)[["JOGADOR", metric]].iloc[::-1]
    colors = [player_colors.get(p, PALETTE[0]) for p in data["JOGADOR"]]

    height = max(4.5, 0.38 * len(data) + 1)
    fig, ax = plt.subplots(figsize=(7.5, height), facecolor=SURFACE)
    bars = ax.barh(
        data["JOGADOR"], data[metric], color=colors, height=0.65, zorder=3,
        edgecolor=MARK_EDGE, linewidth=0.8,
    )

    max_val = data[metric].max() if len(data) else 0
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + max_val * 0.02,
            bar.get_y() + bar.get_height() / 2,
            f"{width:g}",
            va="center",
            fontsize=9,
            color=INK_PRIMARY,
        )

    _style_ax(ax)
    ax.set_title(title, fontsize=13, color=INK_PRIMARY, loc="left", pad=10, fontweight="bold")
    ax.set_xlim(0, max_val * 1.15 if max_val else 1)
    fig.tight_layout()
    return fig


def pie_share(
    summary_df: pd.DataFrame,
    metric: str,
    title: str,
    top_n: int = 6,
) -> plt.Figure:
    """Rosca (donut) com a fatia de cada jogador no total da metrica (ex.: gols).
    Jogadores fora do top N entram agrupados em "Outros".

    As cores aqui sao atribuidas localmente (1a fatia = 1a cor da paleta, e
    assim por diante) em vez de usar a cor fixa de cada jogador - com poucas
    fatias visiveis de cada vez, isso garante que nenhuma cor se repita e a
    leitura fique clara (ao contrario da cor fixa por jogador, que e ordenada
    alfabeticamente e pode coincidir para dois jogadores do top N)."""
    top = summary_df.nlargest(top_n, metric)[["JOGADOR", metric]].copy()
    total = summary_df[metric].sum()
    outros = total - top[metric].sum()

    labels = top["JOGADOR"].tolist()
    values = top[metric].tolist()
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(labels))]
    text_colors = [PALETTE_TEXT[i % len(PALETTE_TEXT)] for i in range(len(labels))]

    if outros > 0:
        labels.append("Outros")
        values.append(outros)
        colors.append(MUTED)
        text_colors.append(INK_PRIMARY)

    fig, ax = plt.subplots(figsize=(7.5, 5.5), facecolor=SURFACE)
    wedges, _texts, autotexts = ax.pie(
        values,
        colors=colors,
        autopct=lambda pct: f"{pct:.0f}%" if pct >= 5 else "",
        pctdistance=0.78,
        startangle=90,
        wedgeprops=dict(width=0.45, edgecolor=SURFACE, linewidth=2),
    )
    for autotext, tcolor in zip(autotexts, text_colors):
        autotext.set_color(tcolor)
        autotext.set_fontsize(9)
        autotext.set_fontweight("bold")

    ax.set_title(title, fontsize=13, color=INK_PRIMARY, loc="left", pad=10, fontweight="bold")
    ax.legend(
        wedges,
        labels,
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        frameon=False,
        fontsize=9,
        labelcolor=INK_SECONDARY,
    )
    fig.tight_layout()
    return fig


def ved_bar(summary_df: pd.DataFrame, title: str, top_n: int = 20) -> plt.Figure:
    """Barras horizontais empilhadas de Vitorias/Empates/Derrotas dos top N (por PTS)."""
    data = summary_df.nlargest(top_n, "PTS")[["JOGADOR", "VITORIA", "EMPATE", "DERROTA"]].iloc[::-1]

    height = max(4.5, 0.38 * len(data) + 1)
    fig, ax = plt.subplots(figsize=(7.5, height), facecolor=SURFACE)
    left = [0] * len(data)
    for col, color, label in [
        ("VITORIA", GOOD, "Vitorias"),
        ("EMPATE", NEUTRAL, "Empates"),
        ("DERROTA", BAD, "Derrotas"),
    ]:
        text_color = "#ffffff" if color != NEUTRAL else "#000000"
        bars = ax.barh(
            data["JOGADOR"], data[col], left=left, color=color, height=0.65, label=label, zorder=3,
            edgecolor=MARK_EDGE, linewidth=0.8,
        )
        for bar, value in zip(bars, data[col]):
            if value > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:g}",
                    va="center",
                    ha="center",
                    fontsize=8,
                    color=text_color,
                )
        left = [l + v for l, v in zip(left, data[col])]

    _style_ax(ax)
    ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
    ax.grid(axis="y", visible=False)
    ax.set_title(title, fontsize=13, color=INK_PRIMARY, loc="left", pad=10, fontweight="bold")
    ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0), labelcolor=INK_SECONDARY)
    fig.tight_layout()
    return fig
