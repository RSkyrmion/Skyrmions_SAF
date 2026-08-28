# RELEASE-STORAGE-001 — cópia fria tecnicamente íntegra, migração ainda não autorizável

Missão: `MISSION-STORAGE-001` · Autorizada por `WRITEBACK-038`  
Execução: 2026-08-28 · Evidência: `LAB/EVIDENCE/STORAGE-001/`  
Escopo executado: `ST-0`–`ST-5` · `ST-6`: **`NOT_AUTHORIZED`**  
Aceite humano: **`PENDING`**

## 1. Resultado

**`COLD_COPY_ONLY`.** Nenhum critério falhou, mas `G-STORAGE` não passou porque dois critérios
continuam `UNEVALUATED`:

- `SC-4`: empacotamento e validação foram feitos pela mesma linhagem Codex
  (`SELF_VALIDATION`), embora a restauração técnica tenha passado;
- `SC-6`: não existe segunda cópia em domínio de falha distinto; `/tmp` e o projeto estão no
  mesmo filesystem.

Consequentemente, o resultado não é `MIGRATION_READY` e não concede base para remover nenhum
original.

## 2. Empacotamento e economia medida

Foram criados 17 pacotes temporários `tar.zst` em
`/tmp/fpm-storage-001-20260828/packages/`:

| medida | bytes |
|---|---:|
| payloads elegíveis originais | `1.093.462.503` |
| pacotes comprimidos | `287.637.190` |
| redução de representação | `805.825.313` (`73,70 %`) |

Cada diretório tem manifesto externo, hash do pacote, lista dos payloads originais, tamanhos,
modos e tempos. Nenhum `SHA256SUMS.txt` histórico foi recalculado. Os pacotes e a árvore
restaurada ocupam temporariamente cerca de `1,381 GB` porque os originais continuam presentes,
como exigido pelo escopo.

## 3. Hold preservado

O `PERMANENT-FAILURE-HOLD` permaneceu fora de todos os pacotes e não mudou:

- `A005R/` inteiro, incluindo cinco mismatches e `ac0_piso.mx3` extra;
- `A003/` e `A005/` inteiros, com seus `__pycache__` históricos;
- a árvore anômala `LAB/EVIDENCE/LAB/` inteira.

O snapshot anterior e posterior confirmou igualdade de caminhos, bytes, modos e mtimes para
todo o acervo preexistente. `SC-0` e `SC-1` passaram.

## 4. Restauração e reprodução

Todos os 17 pacotes:

- passaram `zstd --test`;
- continham somente caminhos sob o diretório esperado;
- foram restaurados em árvore nova sob `/tmp`;
- reproduziram exatamente caminhos, bytes, modos e mtimes registrados;
- fizeram o `SHA256SUMS.txt` histórico passar sem edição.

Cinco analisadores selados foram reexecutados na árvore restaurada. A saída completa de todos
foi bit-idêntica à arquivada, por comparação SHA-256 sem tolerância e sem exclusões voláteis:

- `E002/analyze.py`;
- `E003/analyze3.py`;
- `E004/analyze4.py`;
- `E004R/analyze4r.py`;
- `E005/analyze5.py`.

Isso faz `SC-5` passar, mas não elimina a limitação de linhagem de `SC-4`.

## 5. Avaliação de descarte

`DEACCESSION-CANDIDATES.json` contém **zero candidatos e zero bytes**. A classificação
conservadora encontrou somente `COLD_PRESERVE` e `PERMANENT_HOLD`; não encontrou cadeia
completa suficiente para atribuir `REGENERABLE_CANDIDATE` a qualquer evidência existente.

Material `CLAIM_BEARING`, `FAILURE_RECORD`, `PERMANENT_HOLD` ou `UNEVALUATED` foi excluído de
antemão. `NON_CLAIM` não foi interpretado como descartável.

## 6. Gate

| critério | veredito |
|---|---|
| `SC-0` origem intacta | `PASS` |
| `SC-1` hold intacto | `PASS` |
| `SC-2` classificação completa | `PASS` |
| `SC-3` pacotes e manifests | `PASS` |
| `SC-4` restauração por linhagem compensatória | `UNEVALUATED — SELF_VALIDATION` |
| `SC-5` reprodução bit-idêntica | `PASS` |
| `SC-6` duas cópias independentes | `UNEVALUATED — SINGLE_COPY` |
| `SC-7` proposta segura | `PASS — lista vazia` |
| `SC-8` autoridade | `PASS — nenhuma remoção` |
| `SC-9` ciência intacta | `PASS` |

`G-STORAGE = NOT_PASS`; resultado permitido: **`COLD_COPY_ONLY`**.

## 7. O que permanece necessário

1. validação de restauração por linhagem compensatória realmente distinta;
2. segunda cópia em destino físico/de falha distinto, nomeado e autorizado;
3. somente se surgirem candidatos após essas camadas: novo writeback com lista literal e
   exceção estreita aos `WB-031`/`WB-035` para qualquer `ST-6`.

Os pacotes atuais são temporários, não backup e não destino de preservação. Nenhum arquivo foi
apagado, movido, substituído, normalizado, restaurado sobre a origem ou resselado.

