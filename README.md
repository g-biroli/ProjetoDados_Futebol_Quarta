# Futebol Quarta-Feira - Playball 2 Pompeia

Painel em Streamlit com o placar do futebol semanal do grupo: classificacao
geral, artilharia, assistencias e analises visuais.

## Paginas

- **Pagina Inicial** - apresentacao do projeto (sem dados), logo do grupo e
  creditos.
- **Visao da Rodada** - resultado de uma rodada especifica (escolhida num
  seletor), no formato "placar" (classificacao da rodada + artilharia e
  assistencias daquela rodada).
- **Visao Geral** - classificacao acumulada de todas as rodadas: lider,
  artilheiro geral, garcom de assistencias geral, tabela completa (com
  medalha de ouro/prata/bronze nos 3 primeiros) e graficos (ranking de
  artilharia/assistencias, fatia de gols por jogador, vitorias/empates/
  derrotas). Tem tambem um botao para baixar tudo em PDF.

## Como os dados fluem (de verdade)

Isso e a parte mais importante pra confiar no numero que aparece na tela,
entao vale explicar com detalhe:

1. O grupo joga na quarta, e alguem cola o resultado da rodada na aba
   **"BASE JOGOS"** da planilha (`Controle_FUT_Quarta.xlsx`, no Google
   Drive) - uma linha por jogador, com a coluna `RODADA` identificando o
   numero da rodada e `PTS/V/E/D/GOLS/ASSIST./G+A` ja calculados pela
   propria planilha.
2. **O app le essa aba direto da planilha a cada acesso** (`src/data.py`,
   funcao `load_data`) - nao existe um passo manual de "publicar" ou
   "sincronizar". A unica coisa entre a rodada ser colada na planilha e
   aparecer no app e um cache de **5 minutos** (pra nao bater no Google a
   cada clique de cada pessoa que abre o painel). Ou seja: cole a rodada,
   espere no maximo 5 minutos (ou forco a atualizacao reiniciando a pagina
   depois desse tempo), e ela aparece sozinha tanto na Visao da Rodada
   (novo item no seletor de rodadas) quanto na Visao Geral (somada ao
   acumulado).
3. **Fallback**: se a planilha estiver fora do ar ou a permissao de
   compartilhamento mudar, o app cai para o ultimo snapshot salvo em
   `data/base_jogos.csv`, em vez de quebrar. Esse arquivo e mantido por uma
   [GitHub Action](.github/workflows/update-data.yml) que roda toda
   quinta-feira e tambem pode ser rodada manualmente (Actions > "Atualizar
   dados do futebol" > "Run workflow", ou `python scripts/fetch_data.py`
   localmente). Em uso normal esse arquivo nao chega a ser lido - ele existe
   so pra o app nao ficar fora do ar se o Google Sheets falhar.
4. A planilha precisa continuar compartilhada como "Qualquer pessoa com o
   link - Leitor" pra essa leitura direta funcionar sem senha/API key.

## Regras da classificacao

- **Pontos**: 3 por vitoria + 1 por empate (padrao futebol).
- **Desempate**: 1º pontos, 2º gols + assistencias, 3º gols, 4º assistencias.

## Logo do grupo

Salve o arquivo da logo em `assets/logo.png` (ver `assets/README.md`). A
Pagina Inicial mostra automaticamente assim que o arquivo existir.

## Rodar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run home.py
```

## Publicar no Streamlit Community Cloud

1. Suba este repositorio no GitHub (`git push`).
2. Acesse [share.streamlit.io](https://share.streamlit.io) e conecte sua conta
   do GitHub.
3. Clique em "New app", selecione o repositorio, a branch e defina o arquivo
   principal como `home.py`.
4. Clique em "Deploy". O Streamlit Cloud instala o `requirements.txt` e gera
   uma URL publica para compartilhar com o grupo.

## Estrutura

- `home.py` - ponto de entrada; define a navegacao (`st.navigation`) entre as paginas.
- `views/pagina_inicial.py` - apresentacao do projeto.
- `views/visao_rodada.py` - placar de uma rodada especifica.
- `views/visao_geral.py` - classificacao geral, graficos e PDF.
- `src/data.py` - leitura e tratamento dos dados (planilha ao vivo, com fallback local).
- `src/charts.py` - graficos (matplotlib) reutilizados na pagina e no PDF.
- `src/pdf_report.py` - montagem do relatorio em PDF (fpdf2).
- `src/theme.py` - paleta de cores, tipografia e componentes visuais (cabecalho, tabela de classificacao com medalhas, KPIs, botao do GitHub).
- `scripts/fetch_data.py` - baixa a planilha e atualiza `data/base_jogos.csv` (fallback).
- `.github/workflows/update-data.yml` - GitHub Action que roda o script acima toda semana.
- `assets/logo.png` - logo do grupo (adicionar manualmente, nao vai por padrao no repositorio).

## Identidade visual

Baseada na paleta oficial da FIFA World Cup 26: preto e branco como base
(cabecalhos, tabelas, texto), dourado como destaque premium (lider, medalha
de ouro) e as cores vibrantes da paleta (azul, laranja, verde, roxo, vermelho,
lima) nos graficos - uma cor fixa por jogador, a mesma em todos os graficos e
no PDF. As tabelas de classificacao usam fundo branco com zebra sutil (em vez
de cor solida por linha) para ficarem limpas e faceis de ler, com os 3
primeiros colocados destacados com medalha de ouro/prata/bronze.
