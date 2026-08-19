"""Carga e tratamento dos dados do futebol de quarta.

Fonte de dados: aba "BASE JOGOS" da planilha do grupo no Google Drive - a
aba onde o proprio grupo cola os resultados de cada rodada (uma linha por
jogador, por rodada, ja com PTS/V/E/D/GOLS/ASSIST./G+A calculados). Assim
que uma rodada nova e adicionada la (com a coluna RODADA identificando o
numero da rodada), o app busca a planilha de novo (cache de poucos minutos)
e a Visao da Rodada e a Visao Geral refletem os dados automaticamente - sem
nenhum passo manual. Veja o README para mais detalhes e o fallback usado
quando a planilha esta temporariamente inacessivel.
"""

import io
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

SHEET_ID = "1t8gQRAYeODvDrsITIkZJPh3u-kZ6g3k7"
BASE_JOGOS_GID = "943973938"  # aba "BASE JOGOS"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={BASE_JOGOS_GID}"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"

LOCAL_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "base_jogos.csv"

# A aba "BASE JOGOS" tem 2 linhas de titulo antes do cabecalho real e uma
# coluna em branco na frente (layout pensado para leitura visual na planilha).
HEADER_ROW_INDEX = 2

# Ordem de desempate oficial do grupo: pontos, depois gols+assistencias,
# depois gols, depois assistencias (ver legenda "CRITERIOS DE DESEMPATE").
TIEBREAK_COLS = ["PTS", "GA", "GOLS", "ASSISTENCIA"]


def _clean(raw: pd.DataFrame) -> pd.DataFrame:
    raw = raw.loc[:, ~raw.columns.str.startswith("Unnamed")]

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


def _fetch_live() -> pd.DataFrame:
    response = requests.get(CSV_URL, timeout=15)
    response.raise_for_status()
    raw = pd.read_csv(io.StringIO(response.content.decode("utf-8")), skiprows=HEADER_ROW_INDEX)
    return _clean(raw)


def _read_local() -> pd.DataFrame:
    raw = pd.read_csv(LOCAL_DATA_PATH, skiprows=HEADER_ROW_INDEX)
    return _clean(raw)


@st.cache_data(ttl=300, show_spinner="Buscando dados atualizados da planilha...")
def load_data() -> pd.DataFrame:
    """Busca a planilha ao vivo (cache de 5 min, entao uma rodada nova
    aparece no app poucos minutos depois de ser colada em "BASE JOGOS").
    Se a planilha estiver inacessivel (sem internet, permissao alterada
    etc.), cai para o ultimo snapshot salvo em data/base_jogos.csv - ver
    scripts/fetch_data.py e o README."""
    try:
        return _fetch_live()
    except Exception:
        if LOCAL_DATA_PATH.exists():
            return _read_local()
        raise


def rank(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica o desempate oficial e numera a posicao (POS)."""
    ranked = df.sort_values(TIEBREAK_COLS, ascending=False).reset_index(drop=True)
    ranked.insert(0, "POS", ranked.index + 1)
    return ranked


def round_table(df: pd.DataFrame, rodada: int) -> pd.DataFrame:
    """Tabela de uma rodada especifica, com POS baseado no desempate oficial."""
    subset = df[df["RODADA"] == rodada].copy()
    return rank(subset)


def bagre_ranking(ranked_df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """Os 'bagres' sao literalmente os ultimos colocados da propria
    classificacao (por isso recebe um df ja processado por rank(),
    round_table() ou overall_table()) - o ultimo colocado vira o 1o bagre, o
    penultimo o 2o, e assim por diante. Empates seguem o mesmo criterio da
    classificacao normal (G+A, depois gols, depois assistencias), so que
    olhando pra ponta de baixo da tabela."""
    worst = ranked_df.tail(top_n).iloc[::-1].reset_index(drop=True).copy()
    worst["POS"] = range(1, len(worst) + 1)
    return worst


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
