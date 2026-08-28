# WRITEBACK-038 — autorização limitada da `MISSION-STORAGE-001`

Data: 2026-08-28 · Autoridade: Rodrigo

## Decisão humana (literal)

> "Li e autorizo a execução da MISSION-STORAGE-001, exclusivamente ST-0 a ST-5, com pacotes temporários em /tmp. ST-6 e qualquer remoção permanecem não autorizados"

## Escopo autorizado

Está autorizada a execução de `ST-0` a `ST-5` conforme o pré-registro
`LAB/MISSIONS/MISSION-STORAGE-001.md`: baseline somente leitura, classificação, criação de
pacotes temporários fora do repositório, restauração também em `/tmp`, validação, auditoria de
cópias e produção de uma lista não executada de candidatos.

Também está autorizada a criação e o selo do novo diretório
`LAB/EVIDENCE/STORAGE-001/`, contendo somente os artefatos metodológicos previstos pela missão.
Essa criação não altera evidência anterior.

## Limites literais

- `ST-6` não está autorizada;
- nenhum arquivo ou diretório preexistente em `LAB/EVIDENCE/` pode ser removido, movido,
  substituído, editado, restaurado, normalizado ou resselado;
- pacotes volumosos podem existir somente em `/tmp` nesta execução;
- não há autorização para segunda cópia externa, rede, upload, depósito, DOI ou publicação;
- o `PERMANENT-FAILURE-HOLD` inteiro permanece intocado;
- passar gate técnico não autoriza desincorporação nem aceite científico.

Este writeback autoriza a execução limitada, mas não supera as proibições de remoção dos
`WRITEBACK-031` e `WRITEBACK-035`.

