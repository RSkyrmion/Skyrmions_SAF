# WRITEBACK-031 — autorização de execução de `DATA-001`

Data: 2026-08-27 · Autoridade: Rodrigo

## Decisão humana (literal)

> "Autorizo a execução conjunta da MISSION-DATA-001 com sua ERRATA-001, sem remoções em LAB/EVIDENCE/."

## Interpretação registrada

Está autorizada a execução metodológica conjunta de `MISSION-DATA-001.md` e
`MISSION-DATA-001-ERRATA-001.md`: inventário somente leitura, verificadores, selo seguro,
schemas, recibos, catálogo, política de retenção, auditoria histórica, fixtures, testes e
exportação exclusivamente local em `/tmp`.

O limite “sem remoções” é literal: nenhum arquivo ou diretório em `LAB/EVIDENCE/` pode ser
apagado, movido, substituído, restaurado ou normalizado. Em particular, permanecem onde estão
o `.pyc` extra de `A005`, a árvore anômala `LAB/EVIDENCE/LAB/` e os cinco payloads divergentes
de `A005R`. Criar e selar o novo diretório `LAB/EVIDENCE/DATA-001/`, previsto na missão, está
autorizado; ele não altera evidência anterior.

## Limites

- Passar `G-DATA-001` não é aceite humano da missão.
- Não há autorização para rede, upload, depósito, DOI, backup externo, licença ou freeze.
- Não há autorização para executar simulação científica nem outra missão.
- A corrupção histórica deve permanecer visível; recalcular o selo de `A005R` seria violação.

## Próximo head/estado

`STATE-2026-08-27-m`

