# WRITEBACK-030 — correção factual append-only da proposta `DATA-001`

Data: 2026-08-27 · Natureza: registro técnico, **sem nova decisão humana**

## Contexto humano vigente

> "Consegue criar uma missao com as melhorias destacadas para este sistema?"

## Ocorrido

Na validação posterior a `WRITEBACK-029`, a checagem dos 18 `SHA256SUMS.txt` revelou que
`A005R` tem cinco divergências. Os arquivos observados têm `mtime` posterior ao selo e foram
regravados por uma execução iniciada às 15:45:06. A árvore antes descrita como vazia contém,
na realidade, um `ar1_fora_eixo.mx3` de zero byte.

Como missões e decisões são append-only, `MISSION-DATA-001.md` e `WRITEBACK-029.md` não foram
reescritos. A correção normativa foi registrada em
`MISSION-DATA-001-ERRATA-001.md`; os dois documentos devem ser lidos juntos.

## Limites

- Nenhum arquivo em `LAB/EVIDENCE/` foi editado, removido, restaurado ou resselado nesta
  correção.
- Os cinco mismatches não foram normalizados nem promovidos a novo baseline.
- A proposta continua `PROPOSED — NÃO AUTORIZADA`.
- As duas remoções descritas na missão continuam exigindo autorização literal separada.
- Não há nova decisão humana sobre execução, aceite, freeze, backup, licença ou depósito.

## Próximo head/estado

`STATE-2026-08-27-l`

