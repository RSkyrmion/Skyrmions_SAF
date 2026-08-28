# MISSION-A006 — `L2.3`: o ramo coaxial em `A_int = 0.12` existe?

Estado: **`PROPOSED` — NÃO AUTORIZADA A EXECUTAR** · Data: 2026-08-28
Autorizada como missão por `WRITEBACK-024`; ordem confirmada por `WRITEBACK-039`.
Regime: auditoria por segundo solver da **discrepância mais antiga do laboratório**.

> **Pré-registro.** Escrito antes de qualquer corrida. Exige leitura de Rodrigo antes de
> executar (`CLAUDE.md` §2). Fonte e adendos de release varridos (lições do `E005` e do
> `I003-ADDENDUM-001`): os números abaixo vêm de `EVIDENCE/R002/scan_full.csv` e
> `basin_test_fine.csv`, lidos na fonte, **não de memória**.

## 1. O fato, aberto desde o `R002`
O `L2.3` diz: em `A_int = 0.12` o artigo prevê ramo coaxial em `K₀ ∈ [0.126, 0.144]` e nós não
o encontramos. Mas o quadro completo é mais interessante que isso — **o ramo existe no nosso
código e estreita monotonicamente até desaparecer**:

| `A_int` | `K₀` coaxial encontrado (`R002`) | largura |
|---|---|---|
| 0.02 | `0.400 – 0.525` | `0.125` |
| 0.04 | `0.350 – 0.450` | `0.100` |
| 0.06 | `0.300 – 0.375` | `0.075` |
| 0.08 | `0.250 – 0.275` | `0.025` |
| 0.10 | **`0.200` apenas** | `0` (um ponto da grade) |
| 0.12 | **nenhum** | — |

O `ADDENDUM-001` do `R002` varreu fino em `0.12` (`K₀ = 0.128 / 0.132 / 0.136 / 0.140 / 0.144`,
passo `0.004`) com duas inicializações quase-coaxiais, e achou **não-coaxial em todas**, com
`l ≈ 19.4–19.6 nm`.

**Agravante já registrado:** naquela região a linha tracejada do artigo está **extrapolada** —
o último traço desenhado está em `A_int = 0.1066`.

## 2. A pergunta — e o que ela NÃO pode responder
**Pergunta:** um segundo solver, com discretização e minimizador próprios, encontra o ramo
coaxial em `A_int = 0.12` onde o nosso não encontra?

- **`H_ausente`:** o mumax3 também só encontra não-coaxial. Então **os dois códigos concordam**,
  e a divergência é com a **linha extrapolada da figura**, não com a nossa implementação.
- **`H_nosso`:** o mumax3 encontra coaxial em algum `K₀` da faixa. Então **o nosso código perde
  o ramo**, e o `C-2` é afetado — a afirmação "a fronteira reproduz a do artigo em cinco
  colunas" ganha uma exceção medida.

**O que esta missão NÃO decide:** se o artigo está certo. A previsão de coaxial em `0.12` vem
da **minha extrapolação da figura deles**, não de um traço desenhado. Nenhum solver aqui resolve
isso — só os autores, que estão fora de alcance (`WB-024`). **Declarado antes.**

## 3. `AC-0` — CONTROLE: o discriminador funciona onde a resposta é conhecida?
Antes de testar onde não achamos, testar onde **achamos**.

`A_int = 0.10`, `K₀ = 0.180 / 0.190 / 0.200 / 0.210 / 0.220` — em torno do único ponto coaxial
do `R002` (`K₀ = 0.200`, `l = 0.0398 nm`). Região onde a linha do artigo **está desenhada**.

**PASSA se** o mumax3 classificar **coaxial** em pelo menos um desses `K₀`.
**Se falhar, o `AC-1` é DESCARTADO** e a missão relata que os dois códigos discordam já onde a
resposta é conhecida — o que seria achado maior que o `L2.3`, e mudaria o alvo.

Taxonomia do `A002` §4 aplicada: degrau que falha invalida o degrau seguinte.

## 4. `AC-1` — PRIMÁRIO: `A_int = 0.12`
`K₀ = 0.128 / 0.132 / 0.136 / 0.140 / 0.144` — **exatamente** os cinco do
`R002-ADDENDUM-001`, para a comparação ser casada ponto a ponto.

**Três inicializações por ponto**, porque o `SL-B1`/`L2.4` registra que a região mapeada é a
**alcançável** a partir da inicialização:
1. **separação `0`** — exatamente coaxial. Se o coaxial é equilíbrio ali, partir dele deve
   permanecer nele;
2. **separação `0.5 nm`** — quase-coaxial, a mesma do `basin_test_fine`;
3. **separação `10 nm`** — a inicialização declarada no artigo.

| | previsão |
|---|---|
| **`H_ausente`** | nenhuma das 15 corridas termina coaxial |
| **`H_nosso`** | pelo menos uma termina coaxial |

**Sem limiar arbitrário.** As duas hipóteses preveem coisas qualitativamente diferentes do
mesmo observável, medido pela mesma régua.

## 5. Classificação — e a checagem de poder
`l` medido pelo **estimador cego do `AUDIT-002`**. **COAXIAL** se `l < 1.0 nm`;
**NÃO-COAXIAL** se `l > 5.0 nm`; entre os dois, **AMBÍGUO** e relatado como tal.

**Poder, medido e não estipulado:** no `R002`, coaxial deu `l = 0.004–0.043 nm` e não-coaxial
deu `l ≈ 19.5 nm` — **fator ~500** entre as classes. As bandas acima têm margem de mais de
uma ordem de grandeza de cada lado. **O discriminador não pode falhar por resolução.**

**Sanidade obrigatória:** `|Q₁| = |Q₂| = 1.0000` em toda corrida. `Q` fora disso significa
colapso ou explosão — a corrida é **excluída e relatada**, nunca classificada.

**Convergência na SAÍDA** (`R2` do §6.1): `minimize()` repetido até `l` variar `< 0.01 nm`
entre chamadas. Tolerância mais frouxa que a do `A008` (`0.001`) porque aqui a grandeza que
decide é a **classe**, separada por fator 500, não o valor de `l`.

## 6. Taxonomia de falha
| resultado | significado, decidido antes |
|---|---|
| `AC-0` falha | os códigos discordam **onde a resposta é conhecida**. `AC-1` descartado; achado maior que o `L2.3` |
| `AC-1` todas não-coaxiais | **`H_ausente`**: dois códigos independentes concordam. A divergência é com a **linha extrapolada**, não com a nossa implementação. `L2.3` **muda de natureza**, não fecha |
| `AC-1` alguma coaxial | **`H_nosso`**: o nosso código perde o ramo. **Afeta o `C-2`** e é o desfecho que dói |
| resultados `AMBÍGUO` | relatar por ponto, sem forçar classe |
| `Q` fora de `∓1` | corrida excluída e relatada |

## 7. Limites que já viajam junto
- **Não decide se o artigo está certo.** §2.
- **Leitura do modelo e parâmetros são os mesmos nos dois códigos.** Erro compartilhado
  sobrevive (`L3.3`).
- **Malha de 1 nm, caixa de 100 nm.** O `A008` acabou de mostrar que a malha move `l` em
  `1–2 %`; para uma **classificação** separada por fator 500 isso é irrelevante, mas na
  **fronteira** entre classes pode não ser. Declarado.
- Primeiro ponto deste laboratório em **acoplamento forte** — nenhuma das convenções foi
  verificada nesse regime, só herdada do `MV-0` do `A003` em `A_int = 0.02`.
- **`L-G` intocado.**

## 8. Provenance
`LAB/EVIDENCE/A006/`, com `AI-PROVENANCE.json`, `EVIDENCE-MANIFEST.json` e `RUN-RECEIPT.json`
por processo, `cwd` fixo — o padrão que a `A008` estreou.

## 9. Gate
`G-A006` = `AC-0` ∧ `AC-1` **com veredito** (`H_ausente`, `H_nosso` ou ambíguo relatado).
**Passar o gate não é aceite**, e nenhum desfecho fecha o `L2.3` — no melhor caso ele **muda de
natureza**, de "o nosso código não acha" para "dois códigos não acham".
