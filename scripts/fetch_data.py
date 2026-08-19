"""Baixa a aba 'BASE JOGOS' da planilha do grupo e salva em data/base_jogos.csv.

Esse arquivo e so um snapshot de seguranca (fallback usado pelo app quando a
planilha esta temporariamente inacessivel) - em uso normal, o app le a
planilha ao vivo (veja src/data.py). Rodado manualmente
(`python scripts/fetch_data.py`) ou pela GitHub Action semanal em
.github/workflows/update-data.yml. Sem dependencias do Streamlit de
proposito, para poder rodar em CI sem instalar o app inteiro.
"""

import sys
from pathlib import Path

import requests

SHEET_ID = "1t8gQRAYeODvDrsITIkZJPh3u-kZ6g3k7"
BASE_JOGOS_GID = "943973938"  # aba "BASE JOGOS"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={BASE_JOGOS_GID}"

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "base_jogos.csv"


def main() -> None:
    response = requests.get(CSV_URL, timeout=30)
    response.raise_for_status()

    content = response.content.decode("utf-8")
    if "NOME" not in content or "RODADA" not in content:
        print("Conteudo baixado nao parece ser a tabela esperada (faltam colunas).", file=sys.stderr)
        sys.exit(1)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Dados salvos em {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
