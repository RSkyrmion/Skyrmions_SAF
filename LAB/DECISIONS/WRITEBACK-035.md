# WRITEBACK-035 — aceite com limitações de `DATA-001`

Data: 2026-08-28 · Autoridade: Rodrigo

## Decisão humana (literal)

> "Aceitar DATA-001 com limitações"

## Decisão registrada

`MISSION-DATA-001`, suas duas erratas, o adendo de execução e
`RELEASE-DATA-001.md` passam a `ACCEPTED_WITH_LIMITATIONS`.

O aceite reconhece como camada metodológica vigente:

- verificação recursiva independente de Git e selo determinístico;
- manifesto funcional, schemas tabulares e recibos de execução;
- catálogo claim→dado, classes de retenção e auditoria histórica;
- exportação somente local e testes positivos/negativos;
- preservação append-only da primeira falha e da repetição `R1` que passou o gate.

## Limitações que permanecem vinculadas

1. A implementação e a validação são `SELF_VALIDATION`; fixtures e SHA-256 mitigam, mas não
   substituem auditor independente.
2. `A003` e `A005` permanecem `SEALED_CONTAMINATED`.
3. `A005R` permanece `SEALED_CORRUPT`; seus cinco payloads originais estão `UNRECOVERED`.
4. `A005R2` permanece `PROCEDURALLY_UNAUTHORIZED` e `SEALED_CORRUPT` por ausência do
   manifesto funcional; este aceite não a regulariza nem promove seus números.
5. A árvore anômala `LAB/EVIDENCE/LAB/` permanece `UNSEALED`.
6. Backup/restauração continuam `UNVERIFIED`; direitos/licença continuam `UNDECIDED`; não há
   depósito nem DOI.
7. `scripts/check_repository.py` continuar retornando erro pelos cinco hashes de `A005R` é
   comportamento correto, não dívida ocultável.
8. O catálogo é índice e não autoridade epistêmica; writebacks, releases e evidência selada
   prevalecem conforme seu papel.

## O que este aceite não autoriza

- não autoriza remover, restaurar, mover, editar ou resselar nada em `LAB/EVIDENCE/`;
- não autoriza aceitar `A004` ou `A005R2`, desbloquear `A007` ou executar outra missão;
- não autoriza backup externo, upload, depósito, DOI, mudança de licença ou publicação;
- não é freeze;
- não cria nem modifica claim científico: `C-1`–`C-15` permanecem exatamente como estavam.

## Próximo head/estado

`STATE-2026-08-28-d`

