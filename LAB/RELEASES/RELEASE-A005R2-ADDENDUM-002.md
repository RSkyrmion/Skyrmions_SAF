# RELEASE-A005R2-ADDENDUM-002 — a lacuna de `RUN-RECEIPT.json`

Data: 2026-08-28 · Complementa: `RELEASE-A005R2.md`
Origem: dívida assumida no `WRITEBACK-036` §3 e não entregue naquele momento.

## 1. A lacuna
O `ENVIRONMENT.md` determina que **corridas futuras devem usar `RUN-RECEIPT.json`**
(`scripts/run_with_receipt.py`), com comando vetorial, `cwd`, tempos, código de saída/timeout,
hashes, parâmetros, seed, outputs e agente executor, começando em `RUNNING` antes do processo e
finalizado **mesmo em erro ou timeout**.

**As seis execuções da `A005R2` foram feitas sem recibo algum:**

| processo | script | duração | recibo |
|---|---|---|---|
| `V-0` torque inicial | `v0_torque_inicial.mx3` | `0.09 s` | **ausente** |
| degrau `F1` | `f1_degrau.mx3` | `3.88 s` | **ausente** |
| degrau `F2` | `f2_degrau.mx3` | `1.56 s` | **ausente** |
| degrau `F3` | `f3_degrau.mx3` | `0.06 s` | **ausente** |
| degrau `F4` | `f4_degrau.mx3` | `53.33 s` | **ausente** |
| repetição de `F4` | `f4rep_repeticao.mx3` | `390.69 s` | **ausente** |

## 2. Causa
Norma vigente, descumprida por **desconhecimento do ledger reorganizado**. Executei a missão
antes de reler o estado, e a obrigação de recibo nasceu na `DATA-001`, entre a minha última
leitura e a execução. O `CLAUDE.md` §1 manda reler o estado a cada sessão; não reli.

**Desconhecimento não é atenuante** — é a falha, não a desculpa.

## 3. O que NÃO foi feito, e por quê
**Recibo retroativo não foi fabricado.** Um recibo é um registro de execução; escrevê-lo depois
do fato, a partir de log, produziria um documento com a forma de evidência primária e o
conteúdo de reconstrução. Isso é pior que a ausência, porque a ausência é visível.

Em vez disso, o `EVIDENCE-MANIFEST.json` do `A005R2` declara **`generated_by: "UNRECORDED"`**
em todos os recursos derivados, e `known_gaps` registra a lacuna em texto.

## 4. O que isto afeta
- **Não afeta a integridade material.** O `A005R2` é `SEALED_VALID`; os hashes conferem.
- **Não afeta os números**, que já não eram promovíveis: a classificação foi `NONCONVERGENT`,
  `AC2-1/2/3` não foram executados, e `l = 10.9551 nm` é medida de degrau, não veredito.
- **Afeta a reconstrutibilidade.** Quem quiser repetir a escada tem os `.mx3`, o
  `run_ladder.sh` e o `LADDER-LOG.txt`, mas **não** tem o registro canônico de comando, `cwd`,
  código de saída e ambiente por processo. A reconstrução é possível e não é auditável no
  padrão que o laboratório passou a exigir.

## 5. O que muda daqui em diante
A `MISSION-A008` nasce com `RUN-RECEIPT.json` desde o primeiro processo, junto com
`AI-PROVENANCE.json` e `EVIDENCE-MANIFEST.json`. Registrado no adendo datado daquele
pré-registro.
