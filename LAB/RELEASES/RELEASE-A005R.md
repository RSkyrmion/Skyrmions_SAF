# RELEASE-A005R — tentativa inconclusa: a convergência não chegou a produzir estado

Missão: `MISSION-A005R` · Autorizada por `WRITEBACK-025` · Execução: 2026-08-27,
11:19–14:19 · `human_acceptance: PENDING`  
Evidência: `LAB/EVIDENCE/A005R/` · custo observado: **3 h de parede**

## 1. Veredito operacional

**A execução ficou INCOMPLETA.** As três corridas chegaram a `relax()` e terminaram pelo
timeout externo de `3600 s`. Nenhuma alcançou o primeiro `print`, nenhuma entrou em
`minimize()` ou na dinâmica e nenhum arquivo OVF foi produzido.

O texto `LOTE A005R COMPLETO` no fim de `RUN-LOG.txt` significa somente que o laço do runner
percorreu os três nomes. **Não significa que a missão, uma corrida ou um critério completou.**

## 2. O que ocorreu em cada corrida

| corrida | alvo pré-registrado | término | produto científico |
|---|---|---|---|
| `ac3_par` | `AC-0` + `AC-3` | timeout `124`, `3600.01 s`, dentro de `relax()` | nenhum; `0` OVF |
| `ac1_theta0` | `AC-0` + `AC-1` | timeout `124`, `3600.01 s`, dentro de `relax()` | nenhum; `0` OVF |
| `ac2_theta30` | `AC-0` + `AC-2` | timeout `124`, `3600.01 s`, dentro de `relax()` | nenhum; `0` OVF |

O runner executou na ordem acima, com mumax3 `3.11.1`, malha `100×100×2`, célula
`1×1×0,4 nm³`, `RelaxTorqueThreshold=1e-6` e `MinimizerStop=1e-9`. O log não contém valor de
`MaxTorque` posterior ao início da relaxação, portanto **não há base para estimar o melhor
torque atingido**.

## 3. Critérios e gate

| item | estado | razão |
|---|---|---|
| `AC-0` | **UNEVALUATED** | nenhum `MaxTorque_final` foi impresso |
| `AC-1` | **UNEVALUATED** | dinâmica de `θ=0°` não começou |
| `AC-2` | **UNEVALUATED** | dinâmica de `θ=30°` não começou |
| `AC-3` | **UNEVALUATED** | nenhum estado foi salvo para o estimador cego |
| `G-A005R` | **UNEVALUATED** | o gate exige veredito nos quatro itens |

Isto não é `FAIL` científico das hipóteses do pré-registro. É uma **falha operacional de
viabilidade/desenho de execução**: `relax()` foi tratado como chamada monolítica, sem
checkpoint nem orçamento intermediário.

## 4. Efeito sobre claims e missões

- **`C-15` não muda.** `−0,30 %` continua sendo o valor aceito do `A003`, com a ressalva de
  convergência levantada pelo `A005`. `A005R` não forneceu número novo.
- **`A005` continua `REVISION_REQUESTED`.** `AR-0` falhou e `AR-1` continua sem veredito.
- **`A007` continua bloqueada.** Timeout não satisfaz o controle de comparabilidade.
- Nenhum dado desta tentativa pode sustentar claim sobre `H_comum`, `H_nosso`, deriva,
  comprimento de ligação ou piso de float32.

## 5. Achado que pode orientar novo desenho

O único achado promovível é operacional: tentar atingir `1e-6 T` por uma única chamada de
`relax()` consome pelo menos uma hora sem checkpoint observável neste sistema e nesta
configuração. Uma nova missão deve separar **viabilidade**, **escada de torque**,
**checkpoint**, **convergência da saída** e só então os critérios científicos.

## 6. Limites de proveniência

O log, scripts e configurações permitem reconstruir comandos, ordem, versões e timeouts. O
modelo exato do assistente que disparou as corridas não foi registrado na época; o manifesto
`AI-PROVENANCE.json` declara isso como desconhecido, em vez de fabricar detalhe retroativo.

## 7. Próxima decisão

Não há resultado científico para aceitar. A proposta `MISSION-A005R2.md` é um redesenho novo:
precisa ser lida e receber autorização literal separada antes de qualquer execução.

