"""Pagina protegida para o administrador inserir um novo dia de jogo."""

from datetime import date

import pandas as pd
import streamlit as st

from src.auth import logout_button, require_admin_login
from src.data import load_data
from src.sheets_writer import SheetsNotConfigured, append_match_day
from src.theme import apply_theme, page_header

st.set_page_config(page_title="Inserir Dados - Futebol de Quarta", layout="wide")
apply_theme()
page_header("Inserir novo dia de jogo", "Area restrita ao administrador do grupo.")

if not require_admin_login():
    st.stop()

logout_button()

df_raw = load_data()
known_players = sorted(df_raw["JOGADOR"].unique()) if not df_raw.empty else []

st.subheader("1. Data do jogo")
match_date = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")

st.subheader("2. Jogadores e estatisticas do dia")
st.caption(
    "Adicione uma linha por jogador presente. O numero de partidas de cada "
    "um e calculado automaticamente como vitorias + derrotas + empates."
)
if known_players:
    st.caption("Jogadores ja cadastrados: " + ", ".join(known_players))

empty_rows = pd.DataFrame(
    columns=["JOGADOR", "GOLS", "ASSISTENCIA", "VITORIA", "DERROTA", "EMPATE"]
)
edited = st.data_editor(
    empty_rows,
    num_rows="dynamic",
    use_container_width=True,
    key="new_match_rows",
    column_config={
        "JOGADOR": st.column_config.TextColumn("Jogador", required=True),
        "GOLS": st.column_config.NumberColumn("Gols", min_value=0, step=1, default=0),
        "ASSISTENCIA": st.column_config.NumberColumn("Assistencias", min_value=0, step=1, default=0),
        "VITORIA": st.column_config.NumberColumn("Vitorias", min_value=0, step=1, default=0),
        "DERROTA": st.column_config.NumberColumn("Derrotas", min_value=0, step=1, default=0),
        "EMPATE": st.column_config.NumberColumn("Empates", min_value=0, step=1, default=0),
    },
)

rows = edited.copy()
rows["JOGADOR"] = rows["JOGADOR"].astype(str).str.strip().str.upper()
rows = rows[rows["JOGADOR"].str.len() > 0]

for col in ["GOLS", "ASSISTENCIA", "VITORIA", "DERROTA", "EMPATE"]:
    rows[col] = pd.to_numeric(rows[col], errors="coerce").fillna(0).clip(lower=0).astype(int)

rows["PARTIDAS"] = rows["VITORIA"] + rows["DERROTA"] + rows["EMPATE"]
rows.insert(0, "DATA", match_date.strftime("%d/%m/%Y"))

if not rows.empty:
    st.subheader("3. Conferir antes de salvar")
    st.dataframe(rows, use_container_width=True, hide_index=True)

    duplicated = sorted(set(rows["JOGADOR"]) & set(
        df_raw.loc[df_raw["DATA"].dt.date == match_date, "JOGADOR"]
    )) if not df_raw.empty else []
    if duplicated:
        st.warning(
            "Ja existe registro para esta data com: " + ", ".join(duplicated) +
            ". Salvar novamente vai duplicar essas linhas na planilha."
        )

    if st.button("Confirmar e salvar na planilha", type="primary"):
        try:
            with st.spinner("Salvando na planilha..."):
                qtd = append_match_day(rows)
            load_data.clear()
            st.success(f"{qtd} linha(s) adicionada(s) com sucesso.")
        except SheetsNotConfigured as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Falha ao salvar na planilha: {exc}")
else:
    st.info("Adicione ao menos um jogador com nome preenchido para salvar.")
