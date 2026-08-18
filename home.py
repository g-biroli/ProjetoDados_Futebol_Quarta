"""Pagina inicial: apresentacao do projeto (sem dados)."""

import streamlit as st

from src.theme import apply_theme, page_header

st.set_page_config(page_title="Futebol de Quarta", layout="wide")
apply_theme()
page_header("Futebol de Quarta")

st.markdown(
    """
Toda quarta-feira, um grupo de amigos se encontra pra jogar bola - e desde a
primeira rodada a gente resolveu levar o placar a serio. Cada gol, assistencia,
vitoria e empate vira estatistica, e essas estatisticas viram esse painel.

Aqui voce acompanha:

- **Visao da Rodada** - o resultado de cada quarta, individualmente.
- **Visao Geral** - a classificacao acumulada de todas as rodadas: quem e o
  artilheiro, quem e o garcom das assistencias e quem lidera o campeonato.

Os dados vem direto da planilha que o grupo alimenta depois de cada rodada.

> Bola rolando, amizade nunca perde.
"""
)

st.caption("Use o menu lateral para navegar entre as paginas.")
