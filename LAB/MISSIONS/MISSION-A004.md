# MISSION-A004 — `D-1`: 𝒟 calculada do estado do mumax3

Estado: **`AUTHORIZED`** por `WRITEBACK-024` · Data: 2026-08-27
Regime: auditoria por ferramenta independente · **sem corrida nova**

> **Pré-registro.** Escrito antes de qualquer cálculo. Submetido à leitura de Rodrigo antes da
> execução (`CLAUDE.md` §2).

## 1. A pergunta
O `PV-0` do `E002` mediu `½(𝒟₁+𝒟₂) = 19.4306e−15 N·s/m` no nosso estado, contra `~15` lidos do
eixo da Fig. 2(c) — que **não traz expoente**. Ficaram duas leituras (`D-1`):
- **R1** — eixo em `10⁻¹⁵ N·s/m`: a diferença é **real**, a forma do nosso skyrmion difere do
  deles em **+29.5 %**.
- **R2** — os autores calcularam com `γ₀ = μ₀γ` e rotularam N·s/m: é só o **rótulo**, e o
  acordo real é `+3.1 %`.

Com os autores fora de alcance, isto não se resolve perguntando. Mas **desloca-se**.

## 2. O que o mumax3 acrescenta, e o que NÃO acrescenta
Calcular 𝒟 do estado do **mumax3** (`A003`, selado) com o mesmo estimador.

- Se `𝒟_mumax3 ≈ 𝒟_saf.cu`, então sob **R1** seriam **os dois códigos** que diferem do artigo
  em ~30 % — dois códigos independentes, com DMI e PBC de autores diferentes, e que já
  concordam no raio a `0.019 %` (`MV-1`). Isso torna R1 **menos plausível**, sem refutá-la.
- Se `𝒟_mumax3` diferir muito de `𝒟_saf.cu`, então o `PV-0` estava medindo uma peculiaridade
  do nosso estado, e **R1 volta a ser a leitura natural**.

**Não fecha o `D-1`.** Só os autores fechariam. Isto é deslocamento de plausibilidade,
declarado como tal **antes** do cálculo, e será relatado como tal.

## 3. Critério `AD-1` — comparação, sem limiar externo (`R1` do §6.1)
Grandeza: `I = √(det ∫∂_μm·∂_νm d²r)`, **adimensional** — imune ao prefator, que é justamente
a ambiguidade em disputa.

| | previsão |
|---|---|
| **as duas implementações têm a mesma forma** | `I_mumax3 ≈ I_saf.cu` (a menos do que o `MV-1` já mostrou: `0.019 %` no raio) |
| **o `PV-0` mediu peculiaridade nossa** | `I_mumax3` afastado de `I_saf.cu` |

**Sem limiar absoluto.** Reporto `I` dos dois e a razão, com a escala de referência já medida:
o `MV-1` deu `0.019 %` de diferença no raio, e o `C-12` mediu que `3.2 %` de diferença de
tamanho produz efeito detectável. **Poder:** se a razão ficar dentro de ~1 %, as formas são as
mesmas para todo efeito; se passar de ~5 %, não são.

## 4. `AD-0` — o estado é comparável? (pré-teste)
Os dois estados são do **par acoplado** no mesmo ponto, mas relaxados por códigos diferentes:
`l_saf.cu = 10.9607`, `l_mumax3 = 10.9279 nm` (`−0.30 %`). Registro isso agora: **a comparação
de 𝒟 herda essa diferença de `0.30 %` no comprimento de ligação**, e portanto uma diferença de
𝒟 abaixo de ~1 % **não é distinguível** dela.

## 5. Taxonomia de falha
| resultado | significado, decidido antes |
|---|---|
| `I` iguais a <1 % | **R1 fica menos plausível**; o `D-1` segue **aberto**, com plausibilidade deslocada |
| `I` diferem >5 % | o `PV-0` media peculiaridade nossa; **R1 volta a ser a leitura natural** e isso é achado |
| entre 1 % e 5 % | inconclusivo; relatar sem escolher lado |

## 6. Limites
- **Não fecha o `D-1`.** §2.
- Os dois estados partem da **mesma inicialização** (`L15.3`).
- O estimador de 𝒟 é **meu** nos dois casos — não há régua independente aqui, ao contrário do
  `MV-2`, que usou o estimador cego. O `AUDIT-002` nunca cobriu 𝒟.
- Um ponto de parâmetros; `L-G` intocado.

## 7. Provenance
Usa `EVIDENCE/A003/mfinal_par_mumax3.dat` (selado) e `EVIDENCE/R001/mfinal_weak.dat` (selado).
Script novo em `EVIDENCE/A004/`. **Nenhum arquivo de outra missão é reescrito.**

## 8. Gate
`G-A004` = `AD-0` registrado ∧ `AD-1` com veredito (qualquer dos três).
**Passar o gate não é aceite, e não fecha o `D-1`.**
