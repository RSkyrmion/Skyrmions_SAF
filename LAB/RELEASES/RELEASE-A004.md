# RELEASE-A004 — `D-1`: as duas formas são idênticas a `0.003 %`

Missão: `MISSION-A004` · Autorizada por `WRITEBACK-024` · Execução: 2026-08-27
`human_acceptance: PENDING` · Evidência: `LAB/EVIDENCE/A004/` · Custo: < 1 min, sem corrida nova

## 1. Veredito
**`I_mumax3 / I_saf.cu = 1.000030` — `+0.003 %`. Gate `G-A004` passou.**
**A leitura R1 fica menos plausível. O `D-1` segue ABERTO.**

## 2. A medida
Grandeza: `I = √(det ∫∂_μm·∂_νm d²r)`, **adimensional** — imune ao prefator `M_s d/γ`, que é
justamente a ambiguidade em disputa.

| estado (selado) | `l` [nm] | `I` | `𝒟` [10⁻¹⁵ N·s/m] | `\|I_xx−I_yy\|/I_xx` |
|---|---|---|---|---|
| `saf.cu` (`R001/mfinal_weak`) | 10.9529 | **14.747793** | 19.4308 | 0.00206 |
| `mumax3` (`A003/mfinal_par`) | 10.9278 | **14.748240** | 19.4314 | 0.00207 |

`Q = ∓1.000000` nos dois. `|I_xy|/I_xx ≤ 1.2e−9` — perfil circular, como o artigo afirma.

**`AD-0`**, registrado antes: os dois `l` diferem `−0.229 %`, e foi declarado que uma diferença
de 𝒟 abaixo de ~1 % não seria distinguível disso. A diferença medida é `0.003 %` — **duas
ordens de grandeza abaixo** do que o próprio estado herda.

## 3. O que isto desloca
As duas leituras do eixo da Fig. 2(c), que **não traz expoente**:

| leitura | `I` implícito do artigo | o nosso | diferença |
|---|---|---|---|
| **R1** — eixo em `10⁻¹⁵ N·s/m` (a dimensionalmente consistente) | 11.385 | 14.748 | **+29.5 %** |
| **R2** — cálculo com `γ₀ = μ₀γ`, rótulo N·s/m | 14.307 | 14.748 | **+3.1 %** |

Sob **R1**, seriam **os dois códigos** a diferir do artigo em ~30 %: `saf.cu` e `mumax3`, com
troca, DMI e PBC escritos por autores diferentes, que já concordam no **raio do skyrmion
isolado a `0.019 %`** (`MV-1`) e agora na **integral de dissipação a `0.003 %`**.

**R1 fica menos plausível. Não refutada.**

## 4. O que esta missão NÃO faz — e foi declarado antes de calcular
- **NÃO fecha o `D-1`.** Só os autores fechariam, e eles estão fora de alcance
  (`WRITEBACK-024`). Isto é **deslocamento de plausibilidade**, não decisão.
- **O estimador de 𝒟 é MEU nos dois casos.** Ao contrário do `MV-2`, que usou o estimador cego
  do `AUDIT-002`, aqui **não há régua independente** — o `AUDIT-002` nunca cobriu 𝒟. Um erro
  meu no estimador afetaria os dois números igualmente e ficaria invisível.
- Os dois estados partem da **mesma inicialização** (`L15.3`).
- Um ponto de parâmetros. `L-G` intocado.

## 5. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar.
