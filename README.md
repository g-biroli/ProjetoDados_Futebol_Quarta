# Futebol de Quarta - Estatisticas

Painel em Streamlit com as estatisticas do futebol semanal do grupo: artilharia,
assistencias, aproveitamento e evolucao de cada jogador ao longo do tempo. Os
dados sao lidos direto da planilha do Google Sheets do grupo, o painel gera um
relatorio em PDF com os mesmos indicadores e graficos da pagina, e uma pagina
restrita permite ao administrador cadastrar novos dias de jogo direto pela web.

## Fonte de dados

A planilha precisa continuar compartilhada como **"Qualquer pessoa com o link -
Leitor"**, pois a leitura usa o CSV publico dela (sem credenciais). Colunas
esperadas (uma linha por jogador, por dia de jogo):

`DATA, JOGADOR, GOLS, ASSISTENCIA, VITORIA, DERROTA, EMPATE, PARTIDAS`

## Login da pagina "Inserir Dados"

A pagina `Inserir Dados` (menu lateral) exige login. As credenciais **nao
ficam no codigo**, ficam em `st.secrets`:

- Local: já criadas em `.streamlit/secrets.toml` (arquivo ignorado pelo git).
- Streamlit Community Cloud: configure o mesmo conteudo em
  **App settings > Secrets** depois do deploy (nunca commite esse arquivo).

Usuario: `ADM` — Senha: `FUTQUARTA123` (altere livremente em `secrets.toml`).

## Habilitar a escrita na planilha (service account do Google)

Para a pagina `Inserir Dados` conseguir gravar na planilha, crie uma service
account do Google Cloud com acesso de Editor a ela:

1. No [Google Cloud Console](https://console.cloud.google.com/), crie (ou
   reaproveite) um projeto.
2. Em "APIs e servicos", ative a **Google Sheets API** e a **Google Drive API**.
3. Em "Credenciais", crie uma **Conta de servico** (Service Account).
4. Na conta de servico criada, gere uma **chave** em formato JSON e baixe o
   arquivo.
5. Abra a planilha no Google Drive e compartilhe com o e-mail
   `...@....iam.gserviceaccount.com` (campo `client_email` do JSON) com
   permissao de **Editor**.
6. Copie os campos do JSON para dentro de `[gcp_service_account]` em
   `.streamlit/secrets.toml` (localmente) e em **App settings > Secrets** no
   Streamlit Cloud (em producao). O arquivo `.streamlit/secrets.toml` ja tem
   um modelo comentado com os campos esperados.

Enquanto esse passo nao for feito, o resto do app funciona normalmente (leitura
e graficos) - apenas o botao de salvar na pagina `Inserir Dados` mostra um
aviso pedindo para configurar as credenciais.

## Rodar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run home.py
```

## Publicar no Streamlit Community Cloud

1. Suba este repositorio no GitHub (`git push`). **Confira que
   `.streamlit/secrets.toml` nao foi commitado** (ele deve constar no
   `.gitignore`).
2. Acesse [share.streamlit.io](https://share.streamlit.io) e conecte sua conta
   do GitHub.
3. Clique em "New app", selecione o repositorio, a branch e defina o arquivo
   principal como `home.py`.
4. Em "Advanced settings > Secrets", cole o conteudo de `admin` e (se ja
   tiver) `gcp_service_account`, no mesmo formato TOML do arquivo local.
5. Clique em "Deploy". O Streamlit Cloud instala o `requirements.txt`
   automaticamente e gera uma URL publica para compartilhar com o grupo.
6. A pagina `Inserir Dados` aparece automaticamente no menu lateral (todo
   arquivo dentro de `pages/` vira uma pagina no app).
7. Sempre que a planilha for atualizada (manualmente ou pela pagina de
   insercao), os dados no app se atualizam sozinhos a cada 5 minutos (cache),
   ou na hora pelo botao "Atualizar dados da planilha" na barra lateral.

## Identidade visual

As cores dos graficos e da interface usam uma paleta vibrante multi-cor no
espirito da Copa do Mundo 2026, validada para leitura por pessoas com
daltonismo (cada cor tem contraste suficiente entre si). Cada jogador recebe
sempre a mesma cor em todos os graficos e no PDF, independente do filtro ou
ranking aplicado. Nao reproduzimos a logo, o trofeu ou a marca oficial da
FIFA/Copa do Mundo — apenas o espirito de cores vibrantes e tipografia bold.

## Estrutura

- `home.py` - pagina principal do Streamlit (KPIs, rankings, graficos, botao de PDF).
- `pages/1_Inserir_Dados.py` - pagina restrita para cadastrar um novo dia de jogo.
- `src/data.py` - leitura e tratamento dos dados da planilha.
- `src/charts.py` - graficos (matplotlib) reutilizados na pagina e no PDF.
- `src/pdf_report.py` - montagem do relatorio em PDF (fpdf2).
- `src/theme.py` - paleta de cores, fonte e componentes visuais (KPIs, header).
- `src/auth.py` - login simples baseado em `st.secrets`.
- `src/sheets_writer.py` - escrita de novas linhas na planilha (gspread).
