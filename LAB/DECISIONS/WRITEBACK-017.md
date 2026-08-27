# WRITEBACK-017 — três regras no `CLAUDE.md`, revisão do pré-registro, e `MISSION-I003`

Data: 2026-08-26 · Autoridade: Rodrigo

## Decisões humanas (literais)
> "Escrever as três regras no CLAUDE.md §6 ... > Aprovado"

> "Adotar a revisão do pré-registro antes de rodar — você lê um documento, dez minutos. Quatro
> dos nove defeitos foram pegos assim; os cinco que passaram foram os que ninguém reviu. ->
> aprovado"

> "O teste do RF-4 (se foi o passo de tempo que desligou o par na malha fina). 7 minutos. >
> executar o teste"

## 1. Regras de desenho de critério — `CLAUDE.md` §6.1 (escrito)
`R1` critério é comparação, não limiar · `R2` convergência se checa na saída · `R3` o gate
exige veredito do critério primário. Cada uma com a cicatriz que a originou, e a tabela que
mostra o padrão sem exceção: todos os critérios em forma de comparação funcionaram, todos os
em forma de limiar absoluto falharam.

## 2. Revisão do pré-registro — `CLAUDE.md` §2 + **hook** (escrito)
Entrou na lista do §2 (coisas que exigem autorização explícita) **e** virou hook de `nvcc`,
que é o passo imediatamente anterior à primeira execução de uma missão. Agora são **oito**
regras aplicadas pelo harness.

**Por que hook e não só regra escrita:** o §9 diz que "hook desligado = regra volta a depender
do meu julgamento", e foi exatamente o meu julgamento que falhou nove vezes. Uma regra que
depende de eu lembrar dela é a categoria de defesa que já se mostrou insuficiente.
`/hooks` revisa ou desliga.

## 3. `MISSION-I003` autorizada
Pré-registro em `LAB/MISSIONS/MISSION-I003.md`. **Execução retida até Rodrigo ler o
pré-registro** — primeira aplicação da regra do item 2, adotada minutos antes.

## Próximo head/estado
`STATE-2026-08-26-c`
