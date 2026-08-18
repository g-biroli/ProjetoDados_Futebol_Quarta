# Futebol de Quarta

Painel em Streamlit com o placar do futebol semanal do grupo: classificacao
geral, artilharia, assistencias e evolucao de cada jogador ao longo das
rodadas.

## Paginas

- **Home** - apresentacao do projeto (sem dados).
- **Visao da Rodada** - resultado de uma rodada especifica (escolhida num
  seletor), no formato "placar" (classificacao da rodada + artilharia e
  assistencias daquela rodada).
- **Visao Geral** - classificacao acumulada de todas as rodadas: lider,
  artilheiro geral, garcom de assistencias geral, tabela completa e graficos
  de evolucao (gols, assistencias e pontos acumulados por jogador). Tem
  tambem um botao para baixar tudo em PDF.

## Fonte de dados

Os dados vem da aba **"LS_BASE_JOGOS"** da planilha do grupo no Google Drive
(uma linha por jogador, por rodada, ja com PTS/V/E/D/GOLS/ASSIST./G+A
calculados). A planilha precisa continuar compartilhada como "Qualquer
pessoa com o link - Leitor".

O app **nao busca a planilha a cada acesso**. Em vez disso:

1. Uma [GitHub Action](.github/workflows/update-data.yml) roda toda
   quinta-feira (as 12:00 UTC) e baixa a aba `LS_BASE_JOGOS`, salvando em
   `data/base_jogos.csv`.
2. Se o conteudo mudou, a Action commita e da push desse arquivo no
   repositorio.
3. O app le sempre `data/base_jogos.csv`. No Streamlit Community Cloud, um
   push no repositorio dispara um redeploy automatico, entao o painel reflete
   os dados novos pouco depois da Action rodar.

Isso deixa o app rapido e simples (nao depende do Google em tempo de
execucao) e da ao grupo uma cadencia previsivel de atualizacao. Para forcar
uma atualizacao fora do horario programado, va em Actions > "Atualizar dados
do futebol" > "Run workflow" no GitHub, ou rode localmente:

```bash
python scripts/fetch_data.py
git add data/base_jogos.csv
git commit -m "chore: atualizar dados"
git push
```

Se `data/base_jogos.csv` ainda nao existir (ex.: primeiro clone do repo antes
da Action rodar), o app busca a planilha diretamente como alternativa.

## Regras da classificacao

- **Pontos**: 3 por vitoria + 1 por empate (padrao futebol).
- **Desempate**: 1º pontos, 2º gols + assistencias, 3º gols, 4º assistencias.

## Rodar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/fetch_data.py   # gera data/base_jogos.csv com os dados atuais
streamlit run home.py
```

## Publicar no Streamlit Community Cloud

1. Suba este repositorio no GitHub (`git push`), incluindo `data/base_jogos.csv`.
2. Acesse [share.streamlit.io](https://share.streamlit.io) e conecte sua conta
   do GitHub.
3. Clique em "New app", selecione o repositorio, a branch e defina o arquivo
   principal como `home.py`.
4. Clique em "Deploy". O Streamlit Cloud instala o `requirements.txt` e gera
   uma URL publica para compartilhar com o grupo.
5. As paginas `Visao da Rodada` e `Visao Geral` aparecem automaticamente no
   menu lateral (todo arquivo dentro de `pages/` vira uma pagina no app).

## Estrutura

- `home.py` - pagina de apresentacao (sem dados).
- `pages/1_Visao_da_Rodada.py` - placar de uma rodada especifica.
- `pages/2_Visao_Geral.py` - classificacao geral, graficos de evolucao e PDF.
- `src/data.py` - leitura e tratamento dos dados (local ou planilha).
- `src/charts.py` - graficos de evolucao (matplotlib), reutilizados na pagina e no PDF.
- `src/pdf_report.py` - montagem do relatorio em PDF (fpdf2).
- `src/theme.py` - paleta de cores, tipografia e componentes visuais (cabecalho, tabela de classificacao, paineis de ranking).
- `scripts/fetch_data.py` - baixa a planilha e atualiza `data/base_jogos.csv`.
- `.github/workflows/update-data.yml` - GitHub Action que roda o script acima toda semana.

## Identidade visual

As tabelas de classificacao usam um layout "placar" (navy / laranja / dourado
/ vermelho) inspirado no boletim que o grupo ja usa para registrar os jogos.
A faixa de cor de cada linha e decorativa (alterna entre as 3 cores) - a
planilha nao guarda de forma estruturada em qual time (T1/T2/T3) cada
jogador jogou em cada rodada, entao essa informacao nao e usada para colorir
as linhas.
