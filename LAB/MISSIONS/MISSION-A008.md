# MISSION-A008 — a malha: `l` converge, e para onde?

Estado: **`PROPOSED` — NÃO AUTORIZADA A EXECUTAR** · Data: 2026-08-28
Autorizada a escrever por `WRITEBACK-034`; autorizada como missão por `WRITEBACK-024`.
Regime: ataque ao `L1.1`, a maior incerteza remanescente.

> **Pré-registro.** Escrito antes de qualquer corrida. Exige leitura de Rodrigo antes de
> executar (`CLAUDE.md` §2).
> **Fonte varrida** (lição do `E005`) e **adendos de release varridos** (lição do
> `I003-ADDENDUM-001`): o `E001-ADDENDUM-005` já contém o sinal exploratório que esta missão
> ataca, e o `E001-ADDENDUM-002` já dá `t₀ = M_s a₀²/(2 A_ex γ)`, usada no §4.

## 1. Por que esta e não outra
Hierarquia das incertezas medidas hoje:

| origem | efeito em `l` |
|---|---|
| convergência residual mumax3↔`saf.cu` | `0,052 %` |
| diferença contra o valor publicado `10.98` | `0,18 %` |
| **malha (`L1.1`)** | **`1,01 %`** |

A malha domina por 20×. E há um sinal desconfortável esperando: o `E001-ADDENDUM-005`
registrou, como **exploratório**, que os dois pontos existentes extrapolam para
`l(a→0) ≈ 10.74–10.81 nm` — **afastando-se** do `10.98` publicado. É o único lugar do
laboratório onde uma medida aponta para desacordo, e está parado há quatro dias com a ressalva
de que **dois pontos não fixam a ordem de convergência**.

Esta missão acrescenta o terceiro e o quarto ponto.

## 2. A pergunta, e o que ela NÃO é
**Pergunta:** `l(a)` converge sob refino, e o limite é compatível com `10.96` ou com `~10.78`?

**NÃO é um teste do `C-1`.** O `C-1` é comparação **casada em malha** — nós e o artigo usamos
1 nm. Ele continua válido qualquer que seja o resultado. O que esta missão decide é se ele
pode ou não ser lido como afirmação sobre o **contínuo**. O `E001-ADDENDUM-005` já fechou
parcialmente essa leitura; aqui ela fecha por medida.

## 3. Ferramenta: mumax3, e a razão é técnica
`t₀ = M_s a₀²/(2 A_ex γ)` muda **4× a cada refino pela metade** (`E001-ADDENDUM-002`). Com o
RK4 de passo fixo do `saf.cu`, cada malha exigiria recalcular `dt` à mão. **O mumax3 usa passo
adaptativo e não cai nessa armadilha** — e aqui isso deixa de ser conveniência e vira a escolha
correta de ferramenta.

Além disso, **isto é relaxação estática**: nenhuma dinâmica dirigida é executada, logo o
bloqueio da `A007` não é tocado nem contornado.

## 4. Malhas e pontos já existentes
Caixa fixa em 100 nm, PBC, ponto do `C-1` (`A_int = 0.02`, `K₀ = 0.6`, `T = 0`).

| `a` [nm] | grade | mumax3 | `saf.cu` (selado) |
|---|---|---|---|
| 2.00 | 50×50×2 | a medir | — |
| 1.00 | 100×100×2 | a medir | `10.9607` (`R001` tight) |
| 0.50 | 200×200×2 | a medir | `10.8500` (`R001` mesh05) |
| 0.25 | 400×400×2 | a medir | a medir **se o custo permitir** |

Os dois pontos selados do `saf.cu` servem de **checagem cruzada nas malhas onde existem**, não
de substitutos.

**`l` é medido pelo estimador cego do `AUDIT-002` em todos os casos**, com `a` passado como
argumento. Uma régua só.

## 5. `AM-0` — pré-testes, antes de qualquer leitura de tendência
1. **Custo medido antes de comprometer** (regra do `E001`): cronometrar `a = 0.5 nm` primeiro.
   Se `0.25 nm` extrapolar para além de **1 h**, executar só as três malhas maiores e declarar
   a série de três, sem tentar a quarta.
2. **Estado comparável em cada malha:** `|Q₁| = |Q₂| = 1.0000` e par **não coaxial**. Malha que
   falhe é **excluída e relatada**, não consertada.
3. **Convergência da SAÍDA, não da entrada** (`R2` do §6.1, e a lição direta do `A005R2`):
   em cada malha, `minimize()` repetido até `l` variar `< 0.001 nm` entre chamadas
   consecutivas. **O torque não é critério aqui** — ele é norma-do-máximo sobre uma célula e,
   em float32, mede o piso da máquina.
4. **Regressão:** em `a = 1 nm`, o `l` do mumax3 deve reproduzir o `10.9551` do `A005R2/ck4`
   dentro de `0.005 nm`. Se não reproduzir, o setup mudou e a missão para.

## 6. `AM-1` — PRIMÁRIO: a série converge? (comparação, sem limiar)
Com `l(2.0)`, `l(1.0)`, `l(0.5)` e, se houver, `l(0.25)`, formar a razão de refino

```
r = | l(a/2) − l(a) |  /  | l(a) − l(2a) |
```

| | previsão para `r` |
|---|---|
| **`H_converge`** — esquema de 2ª ordem convergindo | `r ≈ 0.25` |
| **`H_nao_converge`** — `l` ainda muda de forma sustentada | `r ≳ 0.7` |

**Sem limiar absoluto.** As duas hipóteses preveem valores diferentes da **mesma** razão,
calculada dos mesmos dados. Reporto `r` e a banda entre elas.

**Checagem de poder, antes do dado:** os dois pontos existentes dão
`|10.8500 − 10.9607| = 0.1107 nm`. Se `r ≈ 0.25`, o próximo passo move `l` em `~0.028 nm`
(`0.25 %`) — **muito acima** da estabilidade de saída exigida no `AM-0.3` (`0.001 nm`).
O teste tem margem de ~28×. Se `r ≳ 0.7`, move `~0.078 nm`. **As duas são distinguíveis.**

## 7. `AM-2` — SECUNDÁRIO: o limite, e só se `AM-1` disser que converge
**Só executar se `AM-1` classificar `H_converge`.** Extrapolação de Richardson com a ordem
**estimada dos três últimos pontos**, não assumida.

- Se `l(a→0)` for compatível com `10.96` dentro da dispersão: o refino **não** desloca o
  resultado, e o `C-1` pode ser lido como aproximando o contínuo.
- Se `l(a→0)` cair em `10.74–10.81`: o sinal do `E001-ADDENDUM-005` **confirma-se**, e o `C-1`
  fica **definitivamente restrito à comparação casada em malha**. Isso é resultado, não falha.
- Se `AM-1` der `H_nao_converge`: **não há extrapolação**. Relatar a série e parar.

O `E001-ADDENDUM-005` extrapolou de **dois** pontos e foi declarado exploratório por isso.
Com três pontos a ordem é estimável; com dois, não era. **Este é o único motivo pelo qual a
extrapolação deixa de ser exploratória** — e se só houver três malhas úteis, ela permanece
exploratória e será rotulada assim.

## 8. Taxonomia de falha
| resultado | significado, decidido antes |
|---|---|
| `AM-0.4` (regressão) falha | setup mudou; missão para, sem série |
| malha excluída por `AM-0.2` | relatar; se sobrarem menos de três malhas, **sem `AM-1`** |
| `r ≈ 0.25` | `H_converge`; segue para `AM-2` |
| `r ≳ 0.7` | `H_nao_converge`; **sem extrapolação**; a série é o resultado |
| `r` entre as bandas | inconclusivo; relatar sem escolher lado |

## 9. Limites que já viajam junto
- **`L-G` intocado.** Um solver a mais não muda que leitura do modelo e inicialização são
  compartilhadas.
- **Não testa o `C-1`**, e não o revoga em nenhum desfecho (§2).
- Caixa fixa de 100 nm: refinar a malha **não** afasta as imagens periódicas. Um efeito de
  caixa permaneceria em todas as malhas e é indistinguível daqui. **Limite declarado.**
- mumax3 é float32; em `0.25 nm` o campo de troca é 16× o de 1 nm, e o piso de precisão pode
  degradar. O `AM-0.3` mede isso pela estabilidade de `l`, não presume.
- Estática, `T = 0`, um ponto de parâmetros, um acoplamento.
- Nenhuma dinâmica: o bloqueio da `A007` não é tocado.

## 10. Provenance
`LAB/EVIDENCE/A008/`, com `AI-PROVENANCE.json` antes do selo (`CLAUDE.md` §6.2). Estados do
`R001` são **lidos**, nunca reescritos. Nenhum binário de outra missão escreve aqui.

## 11. Gate
`G-A008` = `AM-0` (custo medido, estados comparáveis, saída estável, regressão) ∧ **`AM-1` com
veredito**. `AM-2` é condicional e não faz parte do gate.
**Passar o gate não é aceite.**

---

# ADENDO-001 — 2026-08-28, escrito ANTES de qualquer corrida da `A008`

Rotulado e datado conforme `CLAUDE.md` §3. Acrescenta obrigações de proveniência que passaram
a vigorar com a `DATA-001` (`WB-031`, `WB-035`) e que **não existiam** quando o §10 foi escrito.

## A1 — o pacote de evidência nasce completo
`LAB/EVIDENCE/A008/` deve conter, **antes do selo**:

1. **`AI-PROVENANCE.json`** (`CLAUDE.md` §6.2) — sistemas e papéis, contexto persistente com
   hash, ações executáveis, checkpoints humanos, camadas de validação, **limites de
   independência** e limites conhecidos. Validado por `scripts/check_ai_provenance.py`.
2. **`EVIDENCE-MANIFEST.json`** — manifesto funcional exigido pela `DATA-001`. Sua ausência foi
   o que deixou o `A005R2` em `SEALED_CORRUPT` até o `WB-036`.
3. **`RUN-RECEIPT.json` por processo**, via `scripts/run_with_receipt.py`: comando vetorial,
   `cwd`, tempos, código de saída ou timeout, hashes, parâmetros, outputs e agente executor.
   O recibo começa em `RUNNING` **antes** do processo e é finalizado **mesmo em erro ou
   timeout**. A ausência disso na `A005R2` está registrada em
   `RELEASE-A005R2-ADDENDUM-002.md`.

**Se um processo rodar sem recibo, o recibo NÃO é fabricado depois.** A lacuna é declarada no
manifesto com `generated_by: "UNRECORDED"`, como no `A005R2`.

## A2 — independência declarada, não presumida
O `AI-PROVENANCE.json` deve declarar explicitamente que **mumax3 é solver de terceiros** mas que
**leitura do modelo, parâmetros e inicialização continuam meus**, e que os estados do `R001`
usados como checagem cruzada vêm do **mesmo laboratório**. Se executor e validador forem a
mesma linhagem, declarar `SELF_VALIDATION` e nomear a camada compensatória — que aqui é o
**estimador cego do `AUDIT-002`**, régua de linhagem distinta.

## A3 — `cwd` fixo
Todo processo roda a partir de `/home/rodrigo/pesquisa/SAF` (`ENVIRONMENT.md`). Em 2026-08-27
a deriva de `cwd` criou a árvore anômala `LAB/EVIDENCE/LAB/`, que hoje é `UNSEALED` e não pode
ser removida (`WB-031`). O recibo registra o `cwd` de cada processo, o que torna essa falha
**detectável** em vez de invisível.

## A4 — o que NÃO muda
Pergunta, hipóteses, malhas, `AM-0`, `AM-1`, `AM-2`, taxonomia, limites e gate permanecem
**exatamente** como escritos acima. Este adendo é de proveniência, não de critério.
