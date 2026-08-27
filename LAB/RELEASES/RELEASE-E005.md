# RELEASE-E005 — o amolecimento de amplitude reproduz. **Gate passou.**

Missão: `MISSION-E005` · Autorizada por `WRITEBACK-020` · Execução: 2026-08-26 18:35 → 2026-08-27 07:33
`human_acceptance: PENDING` · Evidência: `LAB/EVIDENCE/E005/`

> Pré-registro **lido e liberado por Rodrigo antes da execução** (`CLAUDE.md` §2).
> Alvo do artigo **extraído e selado antes de qualquer corrida** (`RA-3`).

## 1. Veredito
**`RA-1` PASSOU para `H_amplitude`.** O pico de `v_sp` **desce quando a amplitude sobe**, com o
sinal e a escala do artigo. **Gate `G-E005` passou.**

## 2. `RA-3` — o alvo, extraído ANTES (Fig. S4(c) do suplementar)
Render a 200 dpi, calibração por ticks **detectados** (5 ticks, `0.02703 GHz/px`), traçado por
máscara de cor **amostrada da própria figura** (as três cores dominantes do painel).

| `ΔK/K₀` | `f_pico` do artigo |
|---|---|
| 0.002 | `17.9176` |
| 0.004 | `17.7487` |
| 0.008 | `17.4649` |

Inclinação do artigo: **`−74.807 GHz`** por unidade de `ΔK/K₀`.

## 3. `RA-0` — convergência da SAÍDA (`R2` do §6.1)
| `ΔK/K₀` | pts | `f_pico` 150–225 | `f_pico` 225–300 | dif | `σ(f_pico)` | |
|---|---|---|---|---|---|---|
| 0.002 | 7 | 17.9656 | **17.9664** | `0.0009` | `0.0061` | PASSOU |
| 0.005 | 5 | 17.8192 | **17.8255** | `0.0063` | `0.0108` | PASSOU |
| 0.008 | 7 | 17.5485 | **17.5796** | `0.0311` | `0.0336` | PASSOU |

**A saída converge a 0.9–31 MHz enquanto as entradas (`v_⊥`) se movem 0.9–2.8 %.** É a lição do
`E003` aplicada corretamente — e é exatamente o que o `RF-0` do `E004R` errou ao checar `v_⊥`.

## 4. `RA-1` — PRIMÁRIO
| `ΔK/K₀` | nosso `f_pico` | artigo | diferença |
|---|---|---|---|
| 0.002 | `17.9664 ± 0.0061` | `17.9176` | **+0.0488** |
| 0.005 | `17.8255 ± 0.0108` | *(interpolado ~17.68)* | ~+0.15 |
| 0.008 | `17.5796 ± 0.0336` | `17.4649` | **+0.1147** |

**Inclinação medida `−64.470 GHz/unidade`** contra `−74.807` do artigo — **razão `0.862`**,
negativa e bem dentro da banda de fator 3 pré-registrada (`[−224.4, −24.9]`).
`H_fixo` previa inclinação ~0. **PASSOU para `H_amplitude`.**

### O que isto resolve
**A "discrepância" que eu reportei no `E004R` era amolecimento de amplitude.** Lá eu medi
`f_pico = 17.83` a `ΔK/K₀ = 0.005` e o comparei com `f_SBM = 17.96`, tratando os `0.13 GHz`
como candidato a desacordo. O `RA-1` mostra, por critério **pré-registrado**, que `f_pico`
depende da amplitude com o sinal e a escala do artigo — logo aquele deslocamento é o efeito
esperado, não um desacordo. **A pergunta que o `E004` e o `E004R` não responderam está
respondida, e a afirmação do artigo sobreviveu a um teste que podia refutá-la.**

## 5. `RA-2` — observação, NÃO critério
`f_pico(0.002) = 17.9664 ± 0.0061` contra `f_SBM = 17.9609 ± 0.0125` (`C-11`):
diferença `0.0055 GHz`, **`0.40 σ`**. Na amplitude mais baixa os dois **coincidem**.

**O pré-registro declarou o `RA-2` exploratório, sem limiar, e ele continua exploratório.**
Quem faz o trabalho aqui é o `RA-1`; o `RA-2` é um bônus que aponta na mesma direção. Não é
"a afirmação do artigo foi testada no limite linear" — é uma observação de que, na menor
amplitude medida, os dois números caem um sobre o outro.

## 6. A ressalva que fica aberta
**Os nossos picos estão sistematicamente ACIMA dos do artigo na mesma amplitude:** `+0.049 GHz`
a `0.002` e `+0.115` a `0.008`. O desvio **cresce com a amplitude**, o que é a mesma coisa que
a razão de inclinação `0.862`: **o nosso amolecimento é ~14 % mais fraco que o do artigo.**

O `RA-1` foi declarado, antes do dado, como teste de **sinal e escala** (banda de fator 3) e
não de valor — justamente porque o alvo é leitura de figura em eixo log. Portanto os 14 %
**não são reprovação de nada**; são uma diferença medida, registrada, e **não explicada**.

## 7. Limites
- **`L-G` intocado.** Décima quarta missão. Nada aqui é verificação independente: mesmo código,
  mesmo equilíbrio, mesma régua, e o alvo é uma figura, não dados dos autores.
- O alvo é **extração de figura em eixo logarítmico**. A posição do pico é robusta a isso, o
  valor absoluto de `v_sp` não seria — e por isso não foi comparado.
- O ponto `ΔK/K₀ = 0.005` vem do `E004R`, com grade de **5** frequências contra as **7** das
  outras duas amplitudes. Inomogeneidade registrada; o pico das três é interior à grade.
- A linha de ressonância que o artigo marca na `Fig. S4(c)` está em **18 GHz**, valor redondo;
  a nossa `f_SBM` medida é `17.9609`. A comparação do `RA-2` usa a nossa, não a deles.
- Um acoplamento (`A_int = 0.02`), um modo (SBM), um `α`, três amplitudes, sete frequências.
- **Não** reproduz a `Fig. S4` inteira: faltam ABM (painel d), acoplamento forte (a, b) e o
  painel (e), `v_sp` vs `α`.
- `D-1`, `D-2`, `D-3`, `L2.3`, `L1.1`, `L8.4`, `L9.1` **intocados**.

## 8. Registro de método
Esta missão existiu porque eu projetei o `E004` e o `E004R` **sem ter lido o suplementar
inteiro** — o alvo estava publicado o tempo todo, na `Fig. S4(c)`, no nosso ponto de operação
exato. Custou duas missões e ~8 h de GPU. Não é defeito de critério (a família dos nove do
`§6.1`): é **não ter varrido a fonte antes de desenhar**.
O `E005` foi a primeira missão a declarar no pré-registro que a fonte inteira foi varrida.

## 9. Custo
14 corridas de 300 ns, `3332–3335 s` cada. Total ≈ **13 h**.

## 10. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar. E, separadamente: o `E004` está
`REVISION_REQUESTED` desde o `WB-015`; **o `E005` entrega o que aquela revisão pedia**, e cabe
a Rodrigo decidir se isso encerra a pendência do `E004`.
