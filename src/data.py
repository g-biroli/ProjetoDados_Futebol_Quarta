"""Carga e tratamento dos dados do futebol de quarta.

Fonte de dados: aba "LS_BASE_JOGOS" da planilha do grupo no Google Drive - uma
linha por jogador, por rodada, ja com PTS/V/E/D/GOLS/ASSIST./G+A calculados.
Em producao, essa aba e baixada uma vez por semana por uma GitHub Action (veja
scripts/fetch_data.py e .github/workflows/update-data.yml) e salva em
data/base_jogos.csv, que e o que o app le. Rodando localmente sem esse arquivo,
o app cai automaticamente para buscar direto da planilha publica.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

SHEET_ID = "1t8gQRAYeODvDrsITIkZJPh3u-kZ6g3k7"
BASE_JOGOS_GID = "487239639"  # aba "LS_BASE_JOGOS"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={BASE_JOGOS_GID}"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"

LOCAL_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "base_jogos.csv"

RAW_NUMERIC_COLS = ["PTS", "V", "E", "D", "GOLS", "ASSIST.", "G+A", "RODADA"]

# Ordem de desempate oficial do grupo: pontos, depois gols+assistencias,
# depois gols, depois assistencias (ver legenda "CRITERIOS DE DESEMPATE").
TIEBREAK_COLS = ["PTS", "GA", "GOLS", "ASSISTENCIA"]


def _clean(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.rename(
        columns={
            "NOME": "JOGADOR",
            "V": "VITORIA",
            "E": "EMPATE",
            "D": "DERROTA",
            "ASSIST.": "ASSISTENCIA",
            "G+A": "GA",
        }
    )
    df = df[["JOGADOR", "PTS", "VITORIA", "EMPATE", "DERROTA", "GOLS", "ASSISTENCIA", "GA", "RODADA", "DATA"]]

    df["JOGADOR"] = df["JOGADOR"].astype(str).str.strip().str.upper()
    df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")

    for col in ["PTS", "VITORIA", "EMPATE", "DERROTA", "GOLS", "ASSISTENCIA", "GA", "RODADA"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["DATA", "RODADA", "JOGADOR"])
    df = df[df["JOGADOR"] != ""]

    for col in ["PTS", "VITORIA", "EMPATE", "DERROTA", "GOLS", "ASSISTENCIA", "GA"]:
        df[col] = df[col].fillna(0).astype(int)
    df["RODADA"] = df["RODADA"].astype(int)

    df["PARTIDAS"] = df["VITORIA"] + df["EMPATE"] + df["DERROTA"]

    return df.sort_values(["RODADA", "JOGADOR"]).reset_index(drop=True)


@st.cache_data(ttl=600, show_spinner="Carregando dados...")
def load_data() -> pd.DataFrame:
    """Carrega os dados: preferencialmente do CSV versionado no repositorio
    (atualizado semanalmente pela GitHub Action), com fallback para a
    planilha publica quando esse arquivo nao existir (ex: 1a execucao local)."""
    if LOCAL_DATA_PATH.exists():
        raw = pd.read_csv(LOCAL_DATA_PATH)
    else:
        raw = pd.read_csv(CSV_URL)
    return _clean(raw)


def rank(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica o desempate oficial e numera a posicao (POS)."""
    ranked = df.sort_values(TIEBREAK_COLS, ascending=False).reset_index(drop=True)
    ranked.insert(0, "POS", ranked.index + 1)
    return ranked


def round_table(df: pd.DataFrame, rodada: int) -> pd.DataFrame:
    """Tabela de uma rodada especifica, com POS baseado no desempate oficial."""
    subset = df[df["RODADA"] == rodada].copy()
    return rank(subset)


def cumulative_timeseries(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """Evolucao acumulada (por jogador, ao longo das rodadas) de GOLS/ASSISTENCIA/PTS."""
    ts = df[["JOGADOR", "RODADA", "DATA", metric]].sort_values(["JOGADOR", "RODADA"]).copy()
    ts["CUM"] = ts.groupby("JOGADOR")[metric].cumsum()
    return ts


def overall_table(df: pd.DataFrame) -> pd.DataFrame:
    """Classificacao geral: soma de todas as rodadas, por jogador."""
    summary = (
        df.groupby("JOGADOR")
        .agg(
            PTS=("PTS", "sum"),
            VITORIA=("VITORIA", "sum"),
            EMPATE=("EMPATE", "sum"),
            DERROTA=("DERROTA", "sum"),
            GOLS=("GOLS", "sum"),
            ASSISTENCIA=("ASSISTENCIA", "sum"),
            GA=("GA", "sum"),
            RODADAS_JOGADAS=("RODADA", "nunique"),
        )
        .reset_index()
    )
    return rank(summary)
