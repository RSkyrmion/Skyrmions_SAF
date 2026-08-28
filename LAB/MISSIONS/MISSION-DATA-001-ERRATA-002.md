# ERRATA-002 de MISSION-DATA-001 — contagem recursiva dos selos

Estado: **`NORMATIVA — missão autorizada por WB-031`** · Data: 2026-08-27  
Origem: execução de `DH-0` e `DH-1`, antes do gate

Esta errata resolve uma ambiguidade aritmética da `ERRATA-001` e acrescenta um arquivo extra
detectado em `A005R`. Não muda critérios em resposta a resultado científico; fixa o baseline
de integridade que a própria missão foi criada para medir. Os três documentos devem ser lidos
juntos. Nenhuma evidência foi removida ou alterada.

## Contagem canônica antes de criar `DATA-001`

- **19** diretórios de primeiro nível em `LAB/EVIDENCE/`;
- **18** contêm `SHA256SUMS.txt`;
- a checagem tradicional dos itens listados dá **17 manifests sem mismatch** e **1 com
  mismatch** (`A005R`), pois ela não detecta extras;
- a checagem recursiva dá **16 `SEALED_VALID`**, **1 `SEALED_CONTAMINATED` (`A005`)**,
  **1 `SEALED_CORRUPT` (`A005R`)** e **1 `UNSEALED` (`LAB`)**.

Portanto, “17 selos válidos” na `ERRATA-001` significa apenas “17 listas cujas entradas
hasheadas conferem”. Para integridade recursiva, a expressão correta é “16 selos válidos”.

## Achado adicional em `A005R`

Além dos cinco mismatches já registrados, `ac0_piso.mx3` está presente em `A005R`, tem
`mtime` 2026-08-27 15:44:09 -03:00 e não consta no `SHA256SUMS.txt` criado às 14:44:14.
O estado permanece `SEALED_CORRUPT`, que tem precedência sobre contaminação por arquivo extra.

## Efeito nos critérios

- `DA-0` usa a contagem canônica acima.
- `DA-6` exige que o catálogo mostre os quatro estados e registre também
  `A005R/ac0_piso.mx3` como extra.
- `DA-7` exige que os 16 `SEALED_VALID` permaneçam íntegros, que as entradas listadas de
  `A005` continuem conferindo e que todos os seis achados de `A005R` permaneçam explícitos.

