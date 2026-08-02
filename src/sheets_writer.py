"""Escrita de novas linhas na planilha do Google Sheets via service account.

Requer que a planilha esteja compartilhada (como Editor) com o e-mail da
service account configurada em st.secrets["gcp_service_account"]. Veja o
README para o passo a passo de criacao das credenciais no Google Cloud.
"""

import pandas as pd
import streamlit as st

from src.data import SHEET_ID

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

COLUMN_ORDER = ["DATA", "JOGADOR", "GOLS", "ASSISTENCIA", "VITORIA", "DERROTA", "EMPATE", "PARTIDAS"]


class SheetsNotConfigured(RuntimeError):
    pass


@st.cache_resource(show_spinner=False)
def _get_worksheet():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError as exc:  # pragma: no cover
        raise SheetsNotConfigured(
            "Dependencias do Google Sheets nao instaladas (gspread / google-auth)."
        ) from exc

    if "gcp_service_account" not in st.secrets:
        raise SheetsNotConfigured(
            "Credenciais da service account do Google nao configuradas em "
            "st.secrets['gcp_service_account']. Veja o README."
        )

    creds_info = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).sheet1


def append_match_day(rows: pd.DataFrame) -> int:
    """Anexa uma ou mais linhas (um dia de jogo) na planilha. Retorna a quantidade gravada."""
    worksheet = _get_worksheet()
    values = rows[COLUMN_ORDER].values.tolist()
    worksheet.append_rows(values, value_input_option="USER_ENTERED")
    return len(values)
