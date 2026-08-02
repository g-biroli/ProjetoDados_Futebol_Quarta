"""Carga e tratamento dos dados do futebol de quarta a partir do Google Sheets."""

import io

import pandas as pd
import requests
import streamlit as st

SHEET_ID = "1Dlxe4xHllf27ILFaQsRBle0Ui_-VQrz1l2o_o--_DME"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit?usp=sharing"

NUMERIC_COLS = ["GOLS", "ASSISTENCIA", "VITORIA", "DERROTA", "EMPATE", "PARTIDAS"]


@st.cache_data(ttl=300, show_spinner="Carregando dados da planilha...")
def load_data() -> pd.DataFrame:
    """Baixa a planilha publica do Google Sheets e devolve os dados tratados."""
    response = requests.get(CSV_URL, timeout=15)
    response.raise_for_status()

    df = pd.read_csv(io.StringIO(response.content.decode("utf-8")))
    df.columns = [c.strip().upper() for c in df.columns]

    required = {"DATA", "JOGADOR", *NUMERIC_COLS}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes na planilha: {', '.join(sorted(missing))}")

    df["JOGADOR"] = df["JOGADOR"].astype(str).str.strip().str.upper()
    df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")

    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df = df.dropna(subset=["DATA"])
    df = df[df["JOGADOR"] != ""]

    return df.sort_values("DATA").reset_index(drop=True)


def player_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Consolida as estatisticas de cada jogador no periodo selecionado."""
    summary = (
        df.groupby("JOGADOR")
        .agg(
            DIAS_JOGADOS=("DATA", "nunique"),
            PARTIDAS=("PARTIDAS", "sum"),
            GOLS=("GOLS", "sum"),
            ASSISTENCIAS=("ASSISTENCIA", "sum"),
            VITORIAS=("VITORIA", "sum"),
            DERROTAS=("DERROTA", "sum"),
            EMPATES=("EMPATE", "sum"),
        )
        .reset_index()
    )

    partidas_seguras = summary["PARTIDAS"].replace(0, pd.NA)
    dias_seguros = summary["DIAS_JOGADOS"].replace(0, pd.NA)

    summary["APROVEITAMENTO_%"] = (
        (summary["VITORIAS"] / partidas_seguras * 100).round(1).fillna(0)
    )
    summary["MEDIA_GOLS_DIA"] = (summary["GOLS"] / dias_seguros).round(2).fillna(0)
    summary["MEDIA_ASSIST_DIA"] = (
        (summary["ASSISTENCIAS"] / dias_seguros).round(2).fillna(0)
    )
    summary["PARTICIPACOES_GOL"] = summary["GOLS"] + summary["ASSISTENCIAS"]

    return summary.sort_values("GOLS", ascending=False).reset_index(drop=True)


def matches_held(df: pd.DataFrame) -> int:
    """Total de jogos (mini-partidas) realmente disputados no periodo.

    A coluna PARTIDAS e um valor por dia (repetido em cada linha de jogador
    daquele dia), entao somar a coluna direto por linha multiplicaria o total
    pela quantidade de jogadores presentes. O total correto e a soma do maior
    valor de PARTIDAS observado em cada dia distinto.
    """
    if df.empty:
        return 0
    return int(df.groupby("DATA")["PARTIDAS"].max().sum())


def cumulative_timeseries(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """Serie temporal acumulada (por jogador e data) para GOLS ou ASSISTENCIA."""
    ts = (
        df.groupby(["JOGADOR", "DATA"])[metric]
        .sum()
        .reset_index()
        .sort_values("DATA")
    )
    ts["CUM"] = ts.groupby("JOGADOR")[metric].cumsum()
    return ts


def winrate_timeseries(df: pd.DataFrame) -> pd.DataFrame:
    """Aproveitamento (%) acumulado por jogador ao longo do tempo."""
    ts = (
        df.groupby(["JOGADOR", "DATA"])
        .agg(VITORIA=("VITORIA", "sum"), PARTIDAS=("PARTIDAS", "sum"))
        .reset_index()
        .sort_values("DATA")
    )
    ts["VITORIA_CUM"] = ts.groupby("JOGADOR")["VITORIA"].cumsum()
    ts["PARTIDAS_CUM"] = ts.groupby("JOGADOR")["PARTIDAS"].cumsum()
    partidas_seguras = ts["PARTIDAS_CUM"].replace(0, pd.NA)
    ts["APROVEITAMENTO_%"] = (
        (ts["VITORIA_CUM"] / partidas_seguras * 100).round(1).fillna(0)
    )
    return ts
