# WRITEBACK-036 — regularização do `A005R2`, catálogo e correção do `STATE`

Data: 2026-08-28 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Autorizo os três pontos apontados"

referindo-se aos três itens que apresentei: (1) escrever `EVIDENCE-MANIFEST.json` em
`LAB/EVIDENCE/A005R2/` e resselar; (2) reconstruir `LAB/DATA-CATALOG.json`; (3) confirmar que
o `WRITEBACK-033` é autorização válida da `MISSION-A005R2`, para corrigir o `STATE.md`.

## 1. Exceção explícita ao `WRITEBACK-035`
O `WB-035` estabeleceu que o aceite da `DATA-001` "não autoriza remover, restaurar, mover,
editar ou **resselar** nada em `LAB/EVIDENCE/`". Esta autorização **abre uma exceção estreita e
nomeada**: acrescentar `EVIDENCE-MANIFEST.json` ao `A005R2` e regerar o `SHA256SUMS.txt`
daquele diretório.

**Nada mais é tocado.** Permanecem exatamente onde estão, sem alteração:
`A005R` (`SEALED_CORRUPT`, cinco payloads `UNRECOVERED`), os `__pycache__` de `A003` e `A005`
(`SEALED_CONTAMINATED`), e a árvore anômala `LAB/EVIDENCE/LAB/` (`UNSEALED`).

## 2. Correção factual do `STATE.md` — a autorização existia
O `STATE.md` registrava "Execução material de `A005R2`, **sem autorização válida localizada**".

**Isso é factualmente incorreto.** A autorização é o `WRITEBACK-033`, gravado em
`2026-08-28 09:40:50`, com a fala literal de Rodrigo: *"Autorizo A005R2 formalmente e
reproduzir limpo"*. O `WRITEBACK-035`, gravado às `10:11:35` — trinta minutos depois — **não
cita o `WB-033` nem o `WB-034`** (zero ocorrências).

**Causa:** trabalho concorrente de dois agentes. O outro agente procurou autorização, não
localizou o writeback recém-escrito, e registrou a ausência de boa-fé. O `STATE` herdou.

**Efeito:** a `MISSION-A005R2` deixa de ser `PROCEDURALLY_UNAUTHORIZED`. O `WB-035` item 4
fica **superado neste ponto específico** — e apenas neste. Os demais itens dele seguem
íntegros, inclusive que o aceite da `DATA-001` **não promove os números do `A005R2`**.

**O que NÃO muda:** a classificação `NONCONVERGENT`, o gate reprovado, os critérios `AC2-1/2/3`
não executados, e o fato de que `l = 10.9551 nm` é **medida de degrau, não veredito**, e **não
revisa o `C-15`**.

**E o que continua irregular, sem confusão:** a execução de **2026-08-27, 15:00–16:07** — a que
quebrou o selo do `A005R` — permanece **não autorizada**, exatamente como o `WB-033` §2
registrou. A regularização aqui é da `A005R2` de hoje, não daquela.

## 3. Lacuna de método reconhecida: `RUN-RECEIPT.json`
O `ENVIRONMENT.md` determina que corridas futuras **devem** usar `RUN-RECEIPT.json`
(`scripts/run_with_receipt.py`). Executei os cinco processos da escada `A005R2` **sem recibo
algum**. Norma vigente, descumprida por desconhecimento do ledger reorganizado.

**Não se fabrica recibo retroativo.** O `EVIDENCE-MANIFEST.json` do `A005R2` declara
`generated_by: "UNRECORDED"` nos recursos afetados, e o `RELEASE-A005R2` ganha adendo com esta
lacuna. Corridas futuras — a começar pela `A008` — nascem com recibo.

## 4. O que esta autorização NÃO faz
Não aceita `A004`, `A005R2` ou `A008`. Não desbloqueia `A007`. Não autoriza executar a `A008`.
Não é freeze, publicação ou ação externa. Não promove nenhum número.

## Próximo head/estado
`STATE-2026-08-28-e`
