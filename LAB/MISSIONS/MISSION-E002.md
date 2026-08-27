# MISSION-E002 — Fase 2: autopropulsão do par de skyrmions (Fig. 2, T = 0)

Estado: **`AUTHORIZED`** por `WRITEBACK-010` · Data: 2026-08-25
Regime: extensão controlada · Segunda missão da Fase 2

> **Pré-registro.** Escrito e congelado ANTES de escrever uma linha do código novo e ANTES de
> qualquer corrida de dinâmica. Os alvos numéricos foram extraídos da figura do artigo
> **antes** de existir qualquer número meu — a ordem está registrada no §2.

---

## 1. O que esta missão pergunta
O `E001` mostrou que a minha LLG tem dois modos de breathing na faixa e na ordem publicadas.
O artigo afirma que, excitados **monocromaticamente na ressonância**, esses modos produzem
**deriva líquida do par, estritamente perpendicular à ligação**. Esta é a afirmação central
do artigo. A pergunta é se ela aparece no meu código, e com que velocidade.

**Escopo:** Fig. 2 apenas — `T = 0`, acoplamento fraco, um ponto de parâmetros.
Fig. 3 (curvas de ressonância) e Fig. 4 (LLG estocástica, 3,116 µs) estão **fora**, por
`WRITEBACK-010`.

## 2. Alvos — extraídos da Fig. 2 ANTES de qualquer corrida

Procedimento declarado: `pdftoppm -r 200 -png` da p. 3; calibração pelos pixels dos ticks dos
eixos; traçado das curvas por máscara de cor (laranja `v_y`, azul `v_x`); o script e a saída
vão selados em `EVIDENCE/E002/`. **Nenhum número meu existia quando isto foi medido.**

| painel | excitação | alvo extraído | resolução de leitura |
|---|---|---|---|
| Fig. 2(a) | SBM, `ΔK/K₀ = 0.005`, **18 GHz** | `v_⊥ → 3.50 cm/s`, `v_∥ = 0.00` | 1 px = 0.11 cm/s |
| Fig. 2(b) | ABM, `B₀ = 4 mT`, **19.24 GHz** | `v_⊥ → 2.03 cm/s`, `v_∥ = 0.00` | 1 px = 0.011 cm/s |
| Fig. 2(c) | SBM, ciclo `l`–𝒟 | `l−l̄` ∈ ±1 pm; `½(𝒟₁+𝒟₂)` ∈ [14.4, 15.6] | — |
| Fig. 2(d) | ABM, ciclo `l`–Δ𝒟 | `l−l̄` ∈ ±0.05 pm; `½(𝒟₂−𝒟₁)` ∈ ±1.5 | — |

Ambas as curvas `v_⊥(t)` estão em platô entre 150 e 200 ns; os *insets* do artigo estão em
t ≈ 679 ns, logo o regime estacionário é atingido bem antes.

### Achado de leitura, medido e não suposto: o eixo 𝒟 da Fig. 2(c)/(d) omite o expoente
O rótulo diz literalmente `½(𝒟₁+𝒟₂) (Ns/m)`, com valores ≈ 15. Mas a Eq. (2),
`[𝒟ᵢ]_μν = (M_s d/γ)∫d²r ∂_μmᵢ·∂_νmᵢ`, dá `M_s d/γ = 1.3175e−15` N·s/m vezes uma integral
adimensional de ordem 10 ⇒ **𝒟 ~ 1.5e−14 N·s/m**. Os valores da figura estão portanto em
unidades de **10⁻¹⁵ N·s/m**, e o expoente foi omitido do rótulo. Registro isto **antes** de
medir, e ele vira o alvo do `PV-0`. Da mesma família da imprecisão de notação da Eq. (A1)
achada pelo `AUDIT-001`.

## 3. Ponto de operação e excitação
`A_int = 0.02 mJ/m²`, `K₀ = 0.6 MJ/m³`, `α = 0.02`, `B_dc = 0`, `T = 0`,
grade 100×100 nm², células 1×1 nm², PBC. Estado inicial = equilíbrio relaxado com a
excitação **desligada** (o mesmo protocolo do R001/E001).

Excitação **monocromática** (texto principal), não o sinc de banda larga do `E001`:
- **SBM:** `K(t) = K₀[1 + 0.005 sin(ωt)]`, `f = 18 GHz`.
- **ABM:** `B_z(t) = 4 mT · sin(ωt)`, `f = 19.24 GHz` (primária) e `f = 19.40 GHz` (secundária,
  ver `EP-3`).

## 4. Definições operacionais, fixadas antes de medir
- **Par:** `R_par = (R₁+R₂)/2`, com `Rᵢ` = centro de carga topológica da camada `i` (Eq. 1).
- **Eixos:** `ê_∥` = direção instantânea da ligação `R₁−R₂`; `ê_⊥` = perpendicular a ela.
  Fixados pela orientação **média** da ligação na janela de ajuste (a ligação pode reorientar;
  o artigo afirma que a deriva é perpendicular *seja qual for* a orientação).
- **`v_⊥`, `v_∥` estacionárias:** coeficiente angular do ajuste linear de `R_par·ê` sobre uma
  janela tardia de **≥ 50 ciclos** de excitação. Não é velocidade instantânea — a
  instantânea oscila na frequência de excitação, e a curva do artigo é claramente suavizada.
- **Desdobramento em PBC:** a trajetória de `R_par` é desdobrada por imagem mínima **entre
  amostras consecutivas**. Com deriva de 3,5 cm/s e amostragem de 2 ps, o passo é 7e−5 nm,
  ~10⁶× menor que meia caixa: o desdobramento é inequívoco.
- **𝒟:** Eq. (2), diferenças centradas em malha periódica, `M_s d/γ` com **`d = 0.4 nm`**
  (espessura da camada), não `a₀`. Ver `ADENDUM-003` do `E001`: é a mesma armadilha `d`-vs-`a₀`
  do `SL-2`, e a escolha errada erra por 2,5×.

## 5. Escada de validação — pré-testes baratos, ANTES das corridas de produção

### PV-0 — unidades e forma de 𝒟 (nenhuma dinâmica envolvida)
Calcular `[𝒟ᵢ]_μν` no estado de equilíbrio já selado.
**PASSA se** `½(𝒟₁+𝒟₂) ∈ [13.5, 16.5]×10⁻¹⁵ N·s/m` **e** `|𝒟_xy|/𝒟_xx < 0.05` **e**
`|𝒟_xx−𝒟_yy|/𝒟_xx < 0.05` (o artigo afirma `𝒟_xx ≃ 𝒟_yy`, `𝒟_xy ≃ 0` no acoplamento fraco).

**Checagem de poder, antes do dado:** esta banda de ±10 % **não** separa um erro de 10 % na
forma do meu skyrmion de um erro de 10 % nas unidades. Ela **rejeita** um fator 2,5
(`d` vs `a₀`) ou qualquer potência de 10. É teste de escala e de unidade, e será relatado só
como isso.

### PV-1 — piso de ruído de `l(t)` e 𝒟(t) (o teste que decide se as Figs. 2(c)/(d) existem)
As amplitudes-alvo são minúsculas: **2 pm** de pico-a-pico em `l` para o SBM e **0,1 pm** para
o ABM, sobre `l ≈ 10,4 nm` — isto é `2e−4` e `1e−5` em termos relativos.

**Mecanismo de ruído identificado antes de medir:** o `ctc()` herdado desdobra o toro em torno
da **célula de máximo |ρ|**. Conforme o par deriva, essa célula **salta**, mudando quais
células de cauda são reenroladas; uma cauda de peso 1e−7 reenrolada por `L = 100 nm` contribui
~0,01 pm — a mesma ordem do sinal do ABM.
**Mitigação aplicada ANTES da primeira corrida de produção, não depois:** a origem de
desdobramento passa a ser a CTC da amostra anterior (contínua), não o argmax.

**Medida do piso:** corrida com excitação **desligada** a partir do equilíbrio, mesma duração
e mesma cadência de amostragem das corridas de produção; pico-a-pico de `l(t)`, de
`½(𝒟₁+𝒟₂)(t)` e de `½(𝒟₂−𝒟₁)(t)`, no código **final**.

**Regra de morte, declarada agora — 1/5 da amplitude-alvo:**
- Fig. 2(c) (SBM) mensurável **só se** `pp_ruído(l) < 0.4 pm`.
- Fig. 2(d) (ABM) mensurável **só se** `pp_ruído(l) < 0.02 pm`.
Se o piso exceder, **aquele painel é declarado morto antes do dado** e não é relatado como
resultado — nem como "consistente dentro do ruído". Mesma disciplina que matou o critério
secundário do `R002`.

### PV-2 — controle de passo de tempo
Repetir uma janela de 20 ns de SBM com `dt = 5 fs` contra os `10 fs` de produção.
**PASSA se** `v_⊥` difere por `< 2 %` **e** `max||m|−1| < 1e−9` na corrida cheia.
**Se falhar, todas as velocidades são descartadas por não-convergência** e a missão não
produz afirmação de magnitude.

### PV-3 — custo antes do compromisso (regra que funcionou no `E001`)
Medir a taxa real (s/ns) numa corrida curta **antes** de comprometer os 200 ns. O `ctc()` é
código de host com 2 `atan2` por célula; amostrar `l` e 𝒟 a 2 ps é classe de custo diferente
de amostrar `⟨m_z⟩`. Se a cadência de 2 ps for cara demais, usar a maior cadência viável que
ainda dê **≥ 8 amostras por ciclo** de excitação, e declarar qual foi usada.

## 6. Critérios pré-registrados

### EP-1 — PRIMÁRIO: a deriva é perpendicular à ligação
Sob SBM **e** sob ABM, no estado estacionário: **`|v_∥| / |v_⊥| < 0.05`**.
É a afirmação estrutural central do artigo, e **pode falhar**: nada no meu código impõe
perpendicularidade. É o teste mais forte desta missão, e não depende de nenhuma leitura de
figura.

### EP-2 — PRIMÁRIO: magnitude da velocidade de autopropulsão
- **SBM @ 18 GHz:** `|v_⊥| ∈ [2.45, 4.55] cm/s` (alvo 3.50, banda **±30 %**).
- **ABM @ 19.24 GHz:** `|v_⊥| ∈ [1.02, 3.05] cm/s` (alvo 2.03, banda **±50 %**).

**Checagem de poder, antes do dado — e a razão de as bandas serem largas e diferentes.**
`v_sp` é **ressonante** (é o conteúdo da Fig. 3). Logo a comparação de magnitude é limitada
pelo quanto eu sei onde está a *minha* ressonância:
- O `E001` mediu `f_ABM = 19.40 GHz` com resolução de **0,1 GHz** (janela de 10 ns), ou seja
  `19.40 ± 0.05`. O artigo excita a **19.24 GHz**. A dessintonia é de **0,16 GHz**.
- Com `α = 0.02`, a largura de linha do modo é `Γ ≈ 2αf ≈ 0.78 GHz` (ou `αf ≈ 0.39 GHz` na
  convenção mais estreita). Numa resposta lorentziana, 0,16 GHz de dessintonia custa **~15 %**
  no primeiro caso e **~40 %** no segundo, e `v_sp` vai com o **quadrado** da resposta.
- **Consequência declarada agora: nenhuma banda mais apertada que ±40 % consegue separar erro
  de modelo de dessintonia no ABM.** A banda de ±50 % é, portanto, teste de **escala**, e a
  identidade de magnitude do ABM **não será alegada** a partir do `EP-2`, passe ou falhe.
- O SBM é mais benigno: a minha ressonância é 18.00 e o artigo cita "18", dessintonia
  ≤ 0,05 GHz ⇒ ≲ 5 %. Ali os ±30 % são teste de escala honesto.

### EP-3 — SECUNDÁRIO e DISCRIMINANTE: a dessintonia é medida, não suposta
Rodar o ABM também a **19.40 GHz** (a minha ressonância).
**Predição registrada: `v_⊥(19.40) > v_⊥(19.24)`.** Se sair o contrário, ou a minha atribuição
de ressonância ou a minha excitação está errada. Isto converte a ambiguidade do `EP-2` em
medida, em vez de deixá-la como ressalva.

### EP-4 — SECUNDÁRIO: a assinatura ω vs 2ω da ligação
Promovido do terciário **não medido** do `E001` (`L6.3`), que agora fica limpo sob excitação
monocromática. Espectro de potência de `l(t)` no estacionário:
**pico dominante em `f_drive` sob SBM e em `2·f_drive` sob ABM.**
É predição de simetria do artigo e **pode falhar**. Se falhar, enfraquece retroativamente a
atribuição de modos do `C-6`.
**Condicional ao `PV-1`:** se o piso matar o ramo ABM, o `EP-4` é relatado só para o SBM e a
metade ABM é declarada **não medida** — não "inconclusiva".

### EP-5 — EXPLORATÓRIO: o integral da Eq. (4)
`v_sp = −(ω/4π)∮(G/α𝒟)dl` contra `v_⊥` medida do deslocamento da CTC, no SBM fraco.
O artigo afirma que concordam. **Sem banda numérica pré-registrada** — não tenho número
publicado para o grau de acordo. Relatado como observação, nunca como resultado.
**E declarado desde já: é uma consistência interna do meu próprio código. Não toca `L-G`.**

## 7. Taxonomia de falha — pré-registrada
| o que falha | o que isso significa, decidido antes |
|---|---|
| `PV-0` | erro de unidade/`d` é o primeiro suspeito, não a física. Nenhuma velocidade é relatada até resolver |
| `PV-1` mata um painel | aquele painel **não é relatado**. Não vira "consistente dentro do ruído" |
| `PV-2` | todas as velocidades descartadas por não-convergência; missão sem claim de magnitude |
| `EP-1` | desacordo **estrutural** com o mecanismo do artigo. Relatar assim, sem resgate |
| `EP-1` passa, `EP-2` SBM fora da banda | discrepância real de magnitude no SBM |
| `EP-1` passa, `EP-2` ABM fora da banda | **não atribuível a erro de modelo sem o `EP-3`** — é o que a checagem de poder já disse |
| `EP-4` | atribuição de simetria dos modos errada; enfraquece o `C-6` retroativamente |

## 8. Provenance — a cicatriz do `R001`, tratada na causa (§4)
Código novo em **`LAB/EVIDENCE/E002/saf_prop.cu`**, derivado do `saf_dyn.cu` selado do `E001`
(que **não** é editado). O `saf_dyn.cu` tem caminhos de escrita `LAB/EVIDENCE/E001/...`
embutidos no `ev2` e no `ev3`; **todos** são redirecionados para `E002/` **antes da primeira
execução**, e a checagem é `grep -n 'EVIDENCE/' saf_prop.cu` mostrando **apenas** `E002` —
verificação por comando, não por olho. Selagem por `SHA256SUMS.txt` cobrindo **todos** os
arquivos ao final, código e dados.

## 9. Limites que já viajam junto, escritos antes do resultado
- **`L-G` intocado.** Isto é o meu código, partindo do meu equilíbrio, medido pela minha
  régua. O `E002` acrescenta um observável novo, **não** um verificador independente. Nenhum
  resultado desta missão pode ser dito "verificação independente" de coisa alguma.
- Os alvos da Fig. 2 são **extrações de figura** pelo procedimento do §2, não valores
  tabelados pelos autores.
- Um único ponto de parâmetros; malha de 1 nm; caixa de 100 nm; sem refino. A causa física de
  `L1.1` (a malha resolve a parede `Δ = 5 nm` apenas 5×) continua valendo aqui.
- `α = 0.02` e as frequências são as do artigo; a ressonância é a **minha**, com a incerteza
  de 0,05 GHz que o `EP-2` já contabiliza.
- Fig. 3 e Fig. 4 estão fora do escopo por `WRITEBACK-010`.

## 10. Gate
`G-E002` = `PV-0` ∧ `PV-1`(ramo SBM) ∧ `PV-2` ∧ `EP-1` ∧ `EP-2`(SBM).
**Passar o gate não é aceite.**
