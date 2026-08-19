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
  medalha de ouro/prata/bronze nos 3 primeiros), Top 3 bagres do geral e
  graficos (ranking Top 20 de artilharia/assistencias, fatia de gols por
  jogador, vitorias/empates/derrotas). Tem tambem um botao para baixar tudo
  em PDF.

Tanto a Visao da Rodada quanto a Visao Geral mostram um **Top 3 bagres**: os
3 piores colocados pelo criterio "mais derrotas, depois menos gols, depois
menos assistencias" - com o trofeu "Bagre D'Or" (`assets/bagre_score.jpg`) e
o icone do bagre (`assets/icone_bagre.png`, fundo removido automaticamente)
ao lado do nome de cada um.

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
- **Desempate** (usado so para ordenar, sem uma legenda visivel na tela):
  1º pontos, 2º gols + assistencias, 3º gols, 4º assistencias.
- **Bagre**: 1º mais derrotas, 2º menos gols, 3º menos assistencias (o
  inverso do criterio acima).

## Imagens do grupo (assets/)

- `assets/logo.png` - logo do grupo, usada na Pagina Inicial (grande, no
  topo) e no rodape de todas as paginas.
- `assets/bagre_score.jpg` - trofeu "Bagre D'Or", mostrado abaixo do Top 3
  bagres.
- `assets/icone_bagre.png` - icone do bagre ao lado do nome de cada bagre nas
  tabelas (gerado a partir de `icone_bagre.jpg` com o fundo removido).

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

Modo escuro (fundo preto), no espirito da logo do grupo, com a paleta oficial
da FIFA World Cup 26 como destaque: dourado para premium (lider, 1º lugar,
Top 3 bagres), prata e bronze para 2º/3º lugar, e as cores vibrantes da
paleta (azul, laranja, verde, lima, vermelho, roxo) nos graficos - uma cor
fixa por jogador, a mesma em todos os graficos e no PDF. Nas tabelas de
classificacao, a 1a linha fica em ouro, a 2a em prata e a 3a em bronze; as
demais usam fundo escuro com zebra sutil. O PDF replica exatamente as mesmas
cores, tabelas e graficos da pagina, com o tamanho de cada imagem calculado
para nunca cortar (paginas em retrato para os rankings Top 20, que sao mais
altos, e paisagem para a tabela e o grafico de pizza).
