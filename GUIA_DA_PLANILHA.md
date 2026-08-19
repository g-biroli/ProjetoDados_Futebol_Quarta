# Guia rapido: como alimentar a planilha do Fut Quarta

Esse guia e pra quem vai preencher os resultados depois de cada rodada. Nao
precisa saber nada de programacao - e so seguir o passo a passo abaixo.

## Por que isso importa

O site (Visao da Rodada, Visao Geral, artilharia, bagres etc.) e **100%
automatico**. Ele le direto a planilha do Google Drive. Ou seja: assim que
alguem preenche a rodada certinho na planilha, o site se atualiza sozinho em
ate 5 minutinhos - ninguem precisa mexer em nada alem da planilha.

Por isso o unico jeito do site quebrar ou mostrar numero errado e a planilha
ser preenchida fora do padrao. Segue o passo a passo certinho e ta tudo certo.

## Passo a passo, toda rodada

1. **Preencha o jogo normalmente**, na aba da rodada (igual sempre fizeram:
   duplicando a aba modelo, anotando os times, os gols e assistencias de
   cada jogo).
2. Aquela aba calcula sozinha uma tabelinha de resultado da rodada (com as
   colunas **Nº, NOME, PTS, V, E, D, GOLS, ASSIST., G+A**).
3. **Copie essa tabelinha e cole no final da aba "BASE JOGOS"** - direto
   embaixo da ultima linha preenchida, sem pular nenhuma linha em branco.
4. Nas duas colunas que sobram (**RODADA** e **DATA**), preencha:
   - `RODADA`: o numero da rodada (a rodada anterior + 1).
   - `DATA`: a data do jogo, no formato dia/mes/ano (ex.: `19/8/2026`).
5. Pronto. Nao precisa salvar em lugar nenhum, nao precisa avisar ninguem,
   nao precisa mexer no GitHub. O site ja pega isso sozinho.

## Regras de ouro (pra nao quebrar nada)

- **Nao mude o nome das colunas** da aba "BASE JOGOS" (`Nº`, `NOME`, `PTS`,
  `V`, `E`, `D`, `GOLS`, `ASSIST.`, `G+A`, `RODADA`, `DATA`) e nao mude a
  ordem delas.
- **Nao apague a coluna em branco da frente** nem as duas linhas de titulo
  que ficam acima do cabecalho - o site espera exatamente esse formato pra
  ler a planilha certo.
- **Escreva o nome do jogador sempre do mesmo jeito.** Se um jogo o nome tem
  ponto e no outro nao (`A. LEE` vs `A LEE` vs `ANDERSON LEE`), o site vai
  achar que sao duas pessoas diferentes e a estatistica do jogador fica
  errada/dividida. Bater o olho na lista de nomes ja usados antes de colar
  ajuda a evitar isso.
- **Nao deixe linha em branco no meio** da aba "BASE JOGOS" entre uma rodada
  e outra.
- Se errar alguma coisa depois de colar, so corrigir direto na celula errada
  - nao precisa apagar a rodada inteira e recomecar.

## Quando o resultado aparece no site

- **Visao da Rodada**: assim que a rodada nova tiver pelo menos uma linha na
  planilha, ela ja aparece no seletor de rodadas.
- **Visao Geral**: os numeros de todo mundo (classificacao, artilharia,
  assistencias, bagres) somam automaticamente todas as rodadas que estiverem
  na planilha.
- Leva no maximo uns 5 minutos entre colar na planilha e aparecer no site
  (e um cache curto so pra nao sobrecarregar o Google a cada pessoa que abre
  o painel).

Duvida ou algo estranho no site? Fala com o Gabriel Biroli.
