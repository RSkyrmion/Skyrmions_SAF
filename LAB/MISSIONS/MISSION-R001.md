# MISSION-R001 — Reprodução do estado ligado não-coaxial em T=0

```yaml
mission_state:
  lifecycle: TERMINAL_AWAITING_HUMAN   # executada; gate G-R001 passou; ver RELEASES/RELEASE-R001.md
  epistemic_regime: REPRODUCTION
  scientific_verdict: PASS
  evidence_strength: BOUNDED
  human_acceptance: PENDING
  freeze_status: NOT_FROZEN
  material_status: RELEASE_SEALED
  external_action_authorization: NOT_AUTHORIZED
```

## Objetivo humano
Ter uma primeira reprodução pequena, barata e falsificável — e, no caminho, validar a parte
mais frágil do setup antes que qualquer coisa dependa dela.

## Pergunta
Uma re-implementação independente do modelo micromagnético do PRL 086701 relaxa para um par
de skyrmions **não-coaxial** com comprimento de ligação compatível com l = 10.98 nm, no
regime de acoplamento fraco?

## Regime epistemológico
`REPRODUCTION` — re-implementação independente. Os dados originais não são públicos, então
isto **não** é re-execução; a força da evidência fica limitada pela precisão de leitura do
artigo e pela correção do solver próprio.

## Ferramenta
Código CUDA próprio (decisão humana, `WRITEBACK-002`). Consequência epistemológica que deve
ser carregada até o aceite: **não há solver de referência validado por terceiros**. Um bug no
nosso código é indistinguível de uma falha de reprodução, a menos que a escada de verificação
abaixo passe primeiro. Esta é a razão de a escada existir.

## Escopo
Somente T = 0, sem excitação (ΔK = 0, B = 0), acoplamento fraco. Saída: um escalar.

**Fora de escopo (não construir, mesmo que o artigo descreva):** termo térmico `Bth` da
Eq. (A2), Runge-Kutta estocástico de 2ª ordem, excitações sinc, modos de breathing,
autopropulsão, Figs. 3–6. São maquinaria de R002+.

---

## Semantic lock (§11 do Core) — derivações do executor, não decisão humana

Todos os itens abaixo respondem por evidência (teste de FD ou benchmark), não por autoridade.

### SL-1 — Discretização é 2D, sem eixo z
A Eq. (A3) é `H = ∫dS[E1 d + E2 d + Aint m1·m2]`: uma integral **areal**. Cada camada é um
campo 2D; `d` é um multiplicador escalar da densidade de energia intralayer. Não há
discretização em z, não há espaçador geométrico, não há `Nz`.
→ Duas redes 2D de 100×100 células de 1×1 nm², PBC em x e y.

### SL-2 — Fator 1/d no campo interlayer  **[RISCO MAIS ALTO DO CÓDIGO]**
O artigo escreve `Beff,i = −Ms⁻¹(δH/δmi)`. Tomado literalmente sobre a Eq. (A3), isso
**omite um fator 1/d**. A forma dimensionalmente correta é:

```
Beff,i = −(1/(Ms·d)) · δH/δmi
```

- intralayer:  −(1/(Ms·d))·d·δEi/δmi = −(1/Ms)·δEi/δmi   (padrão)
- interlayer:  **Beff_int,i = −Aint·mj/(Ms·d)**

Checagem de magnitude: Aint/(Ms·d) = 0.02e-3/(0.58e6 · 0.4e-9) ≈ **0.086 T** (acoplamento
fraco). Errar isto é um fator de 2.5×10⁹. Validado por FD (VL-1) e por estado uniforme (VL-2).

### SL-3 — Campos efetivos analíticos
```
exchange:     (2A/Ms) ∇²mi
anisotropia:  (2K/Ms) mz(i) ẑ
DMI:          (2Di/Ms) [∇mz(i) − (∇·mi) ẑ]
interlayer:   −(Aint/(Ms·d)) mj
```
Armadilha discreta: `∇·` e `∇mz` devem usar **o mesmo stencil de diferença central**, senão
os operadores discretos deixam de ser adjuntos e a energia não decresce monotonicamente.
Derivação à mão não pega isso; FD pega.

### SL-4 — l é medido pela Eq. (1), com correção de PBC
`l = |R1 − R2|`, `Ri = (1/Qi)∫d²r r ϱi(r)`, `ϱ = (1/4π) m·(∂x m × ∂y m)`.
**Não** usar o centro de `mz`.
Em um toro, `∫r·ϱ d²r` é mal definida e "o par fica centrado" é frágil — ele pode derivar
durante a relaxação. Cada CTC é calculada como **média circular ponderada por ϱ**
(desdobrada em torno do pico de |ϱ|), e `l` usa a diferença de **imagem mínima**.

### SL-5 — Relaxação é damping-only
T = 0 e só o ponto fixo importa; a trajetória não é evidência aqui.
`dm/dt ∝ −m×(m×Beff)`, passo adaptativo, critério de parada por torque máximo.

### SL-6 — Inicialização: quiralidade deve casar com o sinal de D de cada camada
Fundos de `mz` opostos, ansatz de parede de domínio de 360°, separação inicial 10 nm,
cargas e quiralidades opostas. Com `D1 = −D2`, **o ansatz de cada camada deve casar com o
sinal de D da sua própria camada**. Emparelhar errado é a causa mais provável do modo de
falha "relaxa para o ramo coaxial" — que é erro de inicialização, não refutação do artigo.

### SL-7 — Estimador de carga topologica: Berg-Luscher, nao diferencas finitas
Registrado **durante** a execucao de VL-3 (2026-08-21), com o motivo, porque altera uma
medida depois do criterio ter sido fixado.

Primeira execucao de VL-3: skyrmion relaxou saudavel (mz minimo = -0.993, nucleo totalmente
revertido, torque 9.8e-6 T, convergido) mas `|Q| = 0.984` — 1.6% fora do alvo de |Q|=1. A
densidade de carga por diferencas centrais subestima |Q| sistematicamente para skyrmions
compactos; e' artefato de discretizacao do estimador, nao do estado relaxado.

Substituido pelo estimador de rede de Berg-Luscher (angulo solido por plaqueta,
`tan(Omega/2) = m1.(m2 x m3)/(1 + m1.m2 + m2.m3 + m3.m1)`), que soma exatamente um inteiro
na rede. Resultado: `Q = -1.0000`.

**Por que isto nao e' ajustar o criterio ao resultado:** o criterio que forcou a troca e' a
*integralidade de Q*, uma propriedade topologica conhecida a priori e **independente** do
alvo de 10.98 nm. A energia relaxada e' identica antes e depois da troca
(`-4.699163e-18 J`), confirmando que mudou a medida e nao o estado. A banda de aceite de `l`
nao foi tocada. Se a troca tivesse sido feita para mover `l` para dentro da banda, seria
INV-05 e estaria errada.

O mesmo estimador pondera a CTC da Eq. (1), por consistencia.

## Questões fechadas / dissolvidas
- **QA-01 — convenção de K0: FECHADA.** A Eq. (A4) lista apenas exchange, anisotropia,
  Zeeman e DMI. Não há termo de demagnetização no Hamiltoniano simulado; ele está absorvido
  em `K0`. → usar `K = K0 = 0.6 MJ/m³`, sem demag. O valor nu de `Ku` nunca é necessário e o
  sinal de ±½μ0Ms² não afeta a reprodução. (Reconfirmada por extração direta do PDF.)
- **QA-02 — unidades de Aint no mumax3: DISSOLVIDA.** Era artefato da ferramenta abandonada.
  Com integral areal e código próprio, `Aint` entra em J/m² sem conversão. Ver SL-2.

---

## Parâmetros (End Matter, Apêndice A)
| símbolo | valor |
|---|---|
| d1 = d2 | 0.4 nm |
| A1 = A2 | 15 pJ/m |
| D1 = −D2 | 3.05 mJ/m² |
| Ms1 = Ms2 | 0.58 MA/m |
| Aint | 0.02 mJ/m² (acoplamento fraco) |
| K = K0 | 0.6 MJ/m³ (ΔK = 0) |
| grade | 100 × 100 nm², células 1 × 1 nm², PBC |
| B | 0 |

Checagens de consistência (derivadas, não do artigo): `Dc = 4√(AK)/π = 3.82 mJ/m²`, logo
`κ = D/Dc = 0.80` < 1 → fundo ferromagnético estável, skyrmions metaestáveis: o regime certo.
`√(A/K) = 5 nm` → parede bem resolvida por células de 1 nm. `l ≈ 11 nm` em caixa de 100 nm:
auto-interação via PBC é modesta mas **não nula** — ver VL-5.

## Escada de verificação (gates internos, em ordem; nenhum pode ser pulado)
- **VL-1 — FD field-vs-energy.** Escrever a energia discreta `H(m1,m2)` primeiro. Perturbar
  uma componente de um spin por ε em configurações aleatórias e comparar
  `Beff` numérico com o analítico, **termo a termo**. Pega erro de sinal, de fator 2 e de
  stencil de PBC numa só passada.
- **VL-2 — estado uniforme.** `m1=m2=+ẑ` → `H_int = +Aint·Área`;  `m1=+ẑ, m2=−ẑ` →
  `−Aint·Área`. Isola o fator areal/1-d de SL-2.
- **VL-3 — skyrmion único.** Uma camada, `Aint=0`: relaxa, `|Q| = 1` dentro de ~1%, sem
  colapso e sem espiral. `κ = 0.80` diz que isto **tem** de funcionar; se falhar, nada a
  jusante importa.
- **VL-4 — par acoplado.** Só depois de VL-1..3. Registrar `l(t)` ao longo de toda a
  relaxação e assertar `Q1 = −Q2` com `|Q| ≈ 1`. `l → 0` identifica imediatamente o ramo.
- **VL-5 — malha.** Rerun com células de 0.5 nm (ver critério abaixo).

## Critério de aceite — **FIXADO ANTES DE QUALQUER EXECUÇÃO**
Fixado agora, enquanto o resultado ainda é desconhecido. Deixar o valor observado informar a
tolerância é exatamente a falha que INV-05 nomeia (descoberta virando confirmação).

1. VL-1 a VL-4 passam;
2. a relaxação termina no ramo **não-coaxial** (`l` converge para valor finito, não para 0);
3. **`l` ∈ [10.43, 11.53] nm**  (10.98 nm ± 5%).

## Critério de falha / inconclusão
- Skyrmion colapsa ou explode → falha material do setup, não resultado científico.
- Relaxa para o ramo **coaxial** → suspeitar de SL-6 (emparelhamento quiralidade/D) antes de
  qualquer interpretação física. Não é refutação.
- **`l` fora da tolerância → `INCONCLUSIVO`, não refutação.** O follow-up designado é VL-5
  (rerun com célula de 0.5 nm). Isto está escrito aqui para que "quase dentro" não vire
  silenciosamente "perto o suficiente".
- VL-1 falhando bloqueia tudo: é bug de código, não física.

## Gate final
`G-R001`: passa se os três critérios de aceite forem satisfeitos **e** a evidência estiver
materializada em `EVIDENCE/R001/`. Falhar qualquer um bloqueia R002.

## Stop rules
- Não iniciar R002 (espectros / Fig. 6) sem nova autorização de Rodrigo.
- Contatar os autores para pedir dados é **ação externa**: requer autorização explícita e
  separada. Não é parte desta missão.
- Se VL-3 falhar e a causa não for evidente, parar e escalar em vez de ajustar parâmetros.

## Evidência esperada
`EVIDENCE/R001/` : fonte CUDA, logs de VL-1..VL-5, estado final da magnetização de ambas as
camadas, série `l(t)`, valor final de `l`, `Q1`, `Q2`.
