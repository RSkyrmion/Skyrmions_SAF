# RELEASE-DATA-001 — higiene, catálogo e preservação verificável

Missão: `MISSION-DATA-001` + `ERRATA-001/002` + `ADDENDUM-001`  
Autorizada por: `WRITEBACK-031` · Execução: 2026-08-27/28  
`human_acceptance: PENDING` · Claim científico novo: **nenhum**

## 1. Veredito

**`G-DATA-001 = PASS` na repetição append-only `R1`.** Todos os critérios `DA-0` a `DA-10`
têm veredito `PASS`. Isso é gate técnico, não aceite humano, não freeze e não declaração de
que toda evidência histórica está íntegra.

A primeira avaliação permanece selada como `GATE-RESULTS.json = FAIL`: `DA-10` procurou a
frase do ledger sem considerar a marcação Markdown. Nenhum claim havia mudado. O avaliador foi
corrigido, a falha preservada e a repetição registrada em `GATE-RESULTS-R1.json`; nenhum
arquivo da tentativa anterior foi reescrito.

## 2. Entregáveis realizados

| entrega | ocorrido |
|---|---|
| `DH-0` | dois inventários somente leitura preservam a fotografia inicial e a de retomada |
| `DH-1` | `scripts/check_evidence.py`: conjunto recursivo exato, hashes, caminhos, symlinks, transitórios, proveniência e manifesto funcional |
| `DH-2` | `scripts/seal_evidence.py`: selo determinístico, recusa overwrite/vazio/symlink/transitório, proteção read-only e `EVIDENCE-SEALS.jsonl` |
| `DH-3` | schema e template de `EVIDENCE-MANIFEST.json`, sem retroatividade fabricada |
| `DH-4` | quatro schemas: trajetória, grade de magnetização, phase scan e resumo de critério; validador UTF-8/tipo/unidade/invariante |
| `DH-5` | recibo atômico de execução; fixtures distinguem sucesso, exit code 3 e timeout |
| `DH-6` | `LAB/DATA-CATALOG.json` determinístico, 21 entradas, fingerprint e autoridade de claim explícita |
| `DH-7` | classes de retenção em `DATA.md`; dry-run local RO-Crate 1.3, BagIt SHA-256 e DataCite sem identificador |
| `DH-8` | `DATA-HYGIENE-AUDIT-2026-08-27.md`, sem reescrever payload histórico |

Integração: o hook de parada usa o verificador recursivo na árvore local; o verificador do
espelho executa o self-test do mesmo núcleo. A workflow existente chama
`scripts/check_repository.py`.

## 3. Gate

| critério | veredito | evidência principal |
|---|---|---|
| `DA-0` inventário | `PASS` | `CURRENT-INVENTORY-R1.json`, anomalias e 35 cabeçalhos detectados |
| `DA-1` completude | `PASS` | fixtures para extra aninhado, ausente, duplicado, symlink e `../` |
| `DA-2` fixity | `PASS` | byte alterado reprova; selo existente nunca é sobrescrito |
| `DA-3` manifesto | `PASS` | válido passa; campo, papel e ausência sem motivo falham |
| `DA-4` tabelas | `PASS` | quatro famílias válidas; coluna, unidade, NaN e tempo inválidos falham |
| `DA-5` recibo | `PASS` | `COMPLETE`, `FAILED` e `INTERRUPTED` preservados separadamente |
| `DA-6` catálogo | `PASS` | 21 entradas, links/autoridades verificados, sem promoção silenciosa |
| `DA-7` não regressão | `PASS` | snapshot SHA antes/depois de `R1`: preexistentes inalterados |
| `DA-8` integração | `PASS` | hook, self-test/CI e verificador usam o mesmo núcleo recursivo |
| `DA-9` exportação | `PASS` | pacote em `/tmp`, zero rede/upload/identificador |
| `DA-10` escopo | `PASS` | ledger permanece em `C-1`–`C-15`; zero aceite/freeze/licença |

Testes finais: **12/12 `OK`**. Foram analisados 13 scripts Python e 11 documentos
JSON/JSONL; hook shell passou `bash -n`; catálogo regenerado e conferido sem drift.

## 4. Evidência da missão

`LAB/EVIDENCE/DATA-001/` foi selado em 2026-08-28 12:46:09Z:

- 22 payloads;
- 188 429 bytes;
- SHA-256 do `SHA256SUMS.txt`:
  `7121e0ccc0add3741b9ea4a8e5d76ef3b1ad330f8b796c877e7100a5bd511a54`;
- proteção read-only: `APPLIED` sem erro;
- todos os 22 hashes passaram depois do selo.

O pacote contém a falha inicial e sua correção, inventários, catálogo de fotografia,
fixtures, três recibos, validação de exportação, manifestos e proveniência original/aditiva.

## 5. Estado real da árvore depois do selo

Há 21 diretórios de primeiro nível e 20 `SHA256SUMS.txt`:

- 16 `SEALED_VALID`, incluindo `DATA-001`;
- 2 `SEALED_CONTAMINATED`: `A003` e `A005`, ambos por `.pyc` extra;
- 2 `SEALED_CORRUPT`: `A005R` por cinco mismatches + um extra; `A005R2` por ausência do
  manifesto funcional obrigatório;
- 1 `UNSEALED`: a árvore anômala `LAB/`.

`python3 -B scripts/check_repository.py` retorna código não zero pelos cinco hashes divergentes
de `A005R`. Esse resultado é esperado e correto; fazê-lo passar ignorando a corrupção violaria
a missão.

## 6. Ocorrência concorrente e autoridade

Durante a retomada, outro fluxo executou e selou `A005R2`. Seu release/proveniência atribuiu
autorização ao `WRITEBACK-033`, mas o texto real desse writeback retoma apenas `DATA-001` e não
amplia escopo. `RELEASE-A005R2-ADDENDUM-001.md` e `WRITEBACK-034.md` corrigem a referência.

`DATA-001` não julga os números de `A005R2`: preserva o ocorrido como
`PROCEDURALLY_UNAUTHORIZED`, sem gate com autoridade, aceite ou efeito sobre `C-15`/`A007`.

## 7. Limites

- Validação é `SELF_VALIDATION`: implementação e critérios foram executados pelo mesmo Codex.
  Fixtures sintéticas, SHA-256 e revisão humana prévia compensam parcialmente; não há auditor
  externo.
- Backup/restauração seguem `UNVERIFIED`; nenhum destino foi autorizado.
- Direitos/licença permanecem `UNDECIDED`; nenhum DOI foi criado.
- Schemas históricos são adaptados em leitura, nunca injetados retroativamente nos payloads.
- O catálogo é índice. Missão, release, writeback e manifesto selado prevalecem em conflito.
- Hash demonstra fixity, não correção científica.

## 8. Remoções e ações externas

- Arquivos removidos em `LAB/EVIDENCE/`: **zero**.
- Arquivos históricos editados/resselados: **zero**.
- Uploads, rede, nuvem, depósito, DOI e backup externo: **zero**.
- Os caches e a árvore `LAB/EVIDENCE/LAB/` permanecem para decisão humana separada.

## 9. Próxima decisão humana

Rodrigo pode aceitar / aceitar-com-limitações / revisar / rejeitar `DATA-001`. Separadamente,
continua necessário decidir: tratamento processual de `A005R2`; eventuais remoções; destino de
backup/restauração; direitos/licença e depósito citável.

