"""Graficos matplotlib reutilizados tanto na pagina Streamlit quanto no PDF."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

PALETTE = [
    "#2a78d6",  # azul
    "#eb6834",  # laranja
    "#1baf7a",  # agua
    "#eda100",  # amarelo
    "#e87ba4",  # magenta
    "#008300",  # verde
    "#4a3aa7",  # violeta
    "#e34948",  # vermelho
]

SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"


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
    top_n: int = 8,
) -> plt.Figure:
    """Ranking horizontal (top N jogadores) para um metrica como GOLS ou ASSISTENCIAS."""
    data = summary_df.nlargest(top_n, metric)[["JOGADOR", metric]].iloc[::-1]
    colors = [player_colors.get(p, PALETTE[0]) for p in data["JOGADOR"]]

    fig, ax = plt.subplots(figsize=(7, 4.5), facecolor=SURFACE)
    bars = ax.barh(data["JOGADOR"], data[metric], color=colors, height=0.6, zorder=3)

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
    ax.set_title(title, fontsize=12, color=INK_PRIMARY, loc="left", pad=10)
    ax.set_xlim(0, max_val * 1.15 if max_val else 1)
    fig.tight_layout()
    return fig


def line_evolution(
    ts_df: pd.DataFrame,
    players: list[str],
    value_col: str,
    title: str,
    ylabel: str,
    player_colors: dict[str, str],
) -> plt.Figure:
    """Linha de evolucao temporal para uma lista de jogadores, uma cor fixa por jogador."""
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=SURFACE)

    for player in players:
        pdata = ts_df[ts_df["JOGADOR"] == player]
        if pdata.empty:
            continue
        color = player_colors.get(player, PALETTE[0])
        ax.plot(
            pdata["DATA"],
            pdata[value_col],
            marker="o",
            markersize=5,
            linewidth=2,
            color=color,
            label=player,
            zorder=3,
        )

    _style_ax(ax)
    ax.set_title(title, fontsize=12, color=INK_PRIMARY, loc="left", pad=10)
    ax.set_ylabel(ylabel, fontsize=9, color=INK_SECONDARY)
    ax.legend(
        frameon=False,
        fontsize=8,
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        labelcolor=INK_SECONDARY,
    )
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig
