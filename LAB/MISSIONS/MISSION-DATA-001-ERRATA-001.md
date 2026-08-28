# ERRATA-001 de MISSION-DATA-001 — integridade de `A005R` e árvore anômala

Estado: **`NORMATIVA — acompanha a proposta não autorizada`** · Data: 2026-08-27  
Origem: validação de integridade posterior à criação de `MISSION-DATA-001.md`

Este documento preserva o pré-registro original e corrige fatos que a validação final revelou.
Ele não autoriza executar a missão, editar evidência, recalcular selo, restaurar arquivo, apagar
artefato ou aceitar claim. Para leitura e eventual autorização, `MISSION-DATA-001.md` e esta
errata formam uma única proposta.

## 1. Correções factuais

1. A árvore `LAB/EVIDENCE/LAB/EVIDENCE/A005/` não está estritamente vazia: contém
   `ar1_fora_eixo.mx3`, arquivo de **zero byte**, com `mtime` 2026-08-27 11:04:06 -03:00.
   Ela continua sem missão e sem selo.
2. Há **18** diretórios com `SHA256SUMS.txt`, mas somente **17** validam integralmente.
   `LAB/EVIDENCE/A005R/SHA256SUMS.txt`, criado em 2026-08-27 14:44:14 -03:00, diverge dos
   cinco arquivos abaixo, todos regravados depois do selo:

| arquivo | `mtime` observado | SHA-256 esperado pelo selo | SHA-256 observado |
|---|---|---|---|
| `RUN-LOG.txt` | 15:45:23 | `f9e34a925535691e6aff479842b66e9fe50d10f8b13707779b3c21e247015a16` | `5b27abdd9a1a5e2f5ecb48ddce86d97b52121dab1290b969d7488906cc8d0354` |
| `ac1_theta0.mx3` | 15:45:06 | `164b6f3903d5555b9f39e63f6344d0bb5c243d3afffdc8eb8bf24d67b2350829` | `b65606bded03885046f803f1be99028d6657b2fed893cab5706456676a9d13b1` |
| `ac2_theta30.mx3` | 15:45:06 | `d3c8391d336ca082d1c317168211938e661104b98234bc36c1a530844700c8c4` | `0ddb120d4e7f70be6ffacda771b2bc3232b19672ea4ab4515552eb453663ab22` |
| `ac3_par.mx3` | 15:45:06 | `30891880494fc48cb2a22174c3117155ded3c39f025f5bfb9fd7ef30efedf246` | `83e4e390a19f0f10ffeb302f9bc60f78881e3bec4147e695f2830e5c5a93b46b` |
| `run_batch.sh` | 15:45:06 | `abc6fe79fe6966b5f1ba530695aedf3af65655776f2e9a444947edc8f41bf552` | `3000180933246ddb8c703ce9660175ae9a66575ed839327128d630723f2b5b59` |

O `RUN-LOG.txt` observado identifica uma execução mumax3 iniciada às 15:45:06 e um diretório
de saída em `/tmp/claude-1000/.../scratchpad/`. Nenhum processo correspondente estava ativo
quando a divergência foi caracterizada. Isso demonstra regravação posterior ao selo; não
determina, por si só, quem iniciou a execução nem permite reconstruir os cinco bytes originais.

3. `LAB/EVIDENCE/A005/__pycache__/ovf.cpython-311.pyc` continua sendo arquivo extra posterior
   ao selo de `A005`. Os arquivos listados no selo de `A005` validam; o estado correto do
   diretório é `SEALED_CONTAMINATED`, não `SEALED_CORRUPT`.
4. O estado correto de `A005R` é `SEALED_CORRUPT`: o próprio manifesto existe, mas cinco
   arquivos que ele cobre não têm mais os hashes registrados.

## 2. Emendas normativas à missão

As seguintes substituições prevalecem em caso de conflito com `MISSION-DATA-001.md`:

- Em §1 item 2, ler “árvore anômala contendo um arquivo de zero byte”, não “árvore vazia”.
- Em `DH-0`, o inventário basal deve registrar **17 selos válidos, um selo corrupto (`A005R`),
  uma árvore não selada com arquivo de zero byte e um selo contaminado por arquivo extra
  (`A005`)**.
- Em `DH-1`, o verificador deve detectar os cinco mismatches de `A005R` além do extra de
  `A005`, sem aceitar qualquer um deles como baseline limpo.
- Em `DH-6`, “18 selos” significa 18 manifestos encontrados, com o estado individual correto;
  não significa 18 selos válidos.
- Em `DH-8`, a auditoria histórica deve incluir os cinco arquivos divergentes, os hashes
  esperado/observado e a cronologia acima. Não deve atribuir autor sem evidência funcional.
- Em `DA-0`, passam as contagens corrigidas desta errata.
- Em `DA-6`, o catálogo passa somente se expuser `A005=SEALED_CONTAMINATED`,
  `A005R=SEALED_CORRUPT`, os outros 17 selos como válidos e a árvore anômala como não selada.
- `DA-7` passa se **nenhum novo mismatch** for introduzido, os 17 selos hoje válidos
  continuarem válidos, os hashes esperados de `A005R` forem preservados como registro e a
  corrupção histórica continuar explicitamente reprovada. Ele não exige nem permite
  “corrigir” `A005R` recalculando `SHA256SUMS.txt`.

## 3. Preservação e recuperação

Se `DATA-001` for autorizada, a primeira atividade será um snapshot somente leitura dos
metadados e hashes atuais em `/tmp`, seguido da busca **read-only** por cópia verificável dos
cinco payloads originais em backup já existente. Sem cópia cujo hash bata com o manifesto,
marcar cada original como `UNRECOVERED`; nunca inferir seu conteúdo a partir do arquivo atual.

Qualquer restauração, cópia para dentro de `EVIDENCE/`, novo selo ou mudança de autoridade
exige proposta e autorização específicas. Esta missão pode diagnosticar e catalogar o dano,
mas não altera o registro histórico para fazê-lo parecer íntegro.

