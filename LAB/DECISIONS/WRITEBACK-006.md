# WRITEBACK-006 — OOMMF disponível: auditoria por solver independente autorizada

Data: 2026-08-24 · Autoridade: Rodrigo

## Decisão humana (literal)
> "o OOMMF está instalado em meu computador. Podemos usá-lo para executar os testes"

## Interpretação registrada — e seu limite
Leio isto como **autorização para executar**. Registro a leitura para ser auditável, como o
`WRITEBACK-004` fez: se estiver errada, corrija.

O que baixa o risco desta leitura, em relação à do `WRITEBACK-004`: rodar um solver
**instalado localmente** sobre **dados locais** não é ação externa (INV-16). Nada sai da
máquina. Nada é irreversível. E o bloqueio operacional que o `WRITEBACK-003` registrou —
*"instalar ou compilar qualquer solver"* — deixou de existir: já está instalado e compilado.

## O que fica autorizado
`MISSION-A002` — auditoria cruzada do `saf.cu` contra **OOMMF 2.0b0**, regime `AUDIT`.
Substitui na prática a `MISSION-A001`, que era desenhada para mumax3 e já trazia a
recomendação registrada de trocar por OOMMF.

## O que continua NÃO autorizado
- Etapa 2 do `AUDIT-001` (enviar o `saf.cu` ao auditor externo).
- Qualquer envio de código ou dados a serviço de terceiros.
- O estimador cego em Python discutido no chat — segue como **proposta**, não autorizado.

## Estado do ferramental (verificado, não assumido)
`OOMMF 2.0b0` em `/home/rodrigo/pesquisa/kMC/micromag/oommf_work/oommf`.
Classes necessárias presentes **no binário compilado**:
`Oxs_TwoSurfaceExchange` (acoplamento areal, J/m² — a razão de preferir OOMMF a mumax3),
`Oxs_DMExchange6Ngbr` (DMI interfacial, extensão local compilada),
`Oxs_PeriodicRectangularMesh`, `Oxs_UniformExchange`, `Oxs_UniaxialAnisotropy`,
`Oxs_CGEvolve`/`Oxs_MinDriver`.

## Próximo head/estado
`STATE-2026-08-24-i`

## Próxima decisão humana
Inalteradas e ainda pendentes: aceite de **R001**, **R002** e **AUDIT-001**.
Nova, depois da execução: aceite de **A002**.
