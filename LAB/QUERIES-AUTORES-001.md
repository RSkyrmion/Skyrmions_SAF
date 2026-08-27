# QUERIES-AUTORES-001 — divergências a esclarecer com os autores do PRL 135, 086701

Origem: `WRITEBACK-011` (2026-08-25), instrução de Rodrigo.
Base factual: `RELEASE-E002.md` + `-ADDENDUM-001`, evidência selada em `LAB/EVIDENCE/E002/`.

> **Destinatário e limite.** Este documento existe para **Rodrigo** levar aos autores.
> Nada aqui foi enviado a ninguém. Contato externo é ação de Rodrigo (INV-16).
>
> **Postura.** São três pontos onde a minha re-implementação e o artigo discordam, ou onde o
> artigo admite mais de uma leitura. **Nenhum deles é afirmação de erro dos autores** — em
> dois dos três a explicação mais provável é uma imprecisão de rótulo/legenda, e em todos a
> hipótese de que o errado seja eu continua viva. O que se pede é a informação que decide.

## Contexto de uma linha, para quem receber
Re-implementação independente em CUDA do modelo das Eqs. (A1)–(A4), sem acesso aos dados
originais. No acoplamento fraco (`A_int = 0.02 mJ/m²`, `K₀ = 0.6 MJ/m³`, `α = 0.02`, malha de
1 nm, caixa de 100 nm, PBC, `T = 0`) ela reproduz: `l_eq = 10.9607 nm` (artigo: 10.98),
`v_sp = 3.54 cm/s` sob SBM a 18 GHz (Fig. 2a: 3.50) e `2.03 cm/s` sob ABM a 19.24 GHz
(Fig. 2b: 2.03).

---

# D-1 — Qual é o fator multiplicativo do eixo 𝒟 nas Figs. 2(c)/(d)?

**O que eu meço.** No equilíbrio, pela Eq. (2),
`[𝒟ᵢ]_μν = (M_s d/γ)∫d²r ∂_μmᵢ·∂_νmᵢ`, com `d = 0.4 nm` e `γ = 1.760859e11 rad s⁻¹ T⁻¹`:

    M_s d/γ                 = 1.317539e-15  N s/m
    integral adimensional I = 14.748
    1/2(𝒟₁+𝒟₂)             = 1.94306e-14  N s/m
    𝒟_xx/𝒟_yy − 1 = 0.0021 ,  𝒟_xy/𝒟_xx = 0.0000   (perfil circular, como o artigo diz)

**O que a figura mostra.** Eixo de 14.4 a 15.6, rotulado `½(𝒟₁+𝒟₂) (Ns/m)`, **sem expoente**.

**A dificuldade.** 15 N·s/m literais são ~10¹⁵ vezes o que a Eq. (2) produz com estes
parâmetros, logo há um fator ausente do rótulo. Duas leituras fecham, e elas levam a
conclusões físicas opostas:

| leitura | eixo em | `I` implícito | vs o meu (14.748) |
|---|---|---|---|
| **R1** — a dimensionalmente consistente | `10⁻¹⁵ N·s/m` | 11.385 | **+29.5 %** ⇒ forma do skyrmion difere |
| **R2** — cálculo com `γ₀ = μ₀γ = 2.2128e5 m A⁻¹ s⁻¹`, rótulo N·s/m | `10⁻⁹` | 14.307 | **+3.1 %** ⇒ só o rótulo |

**Evidência que tenho, e que não decide.** A **amplitude relativa** do ciclo de 𝒟 é
invariante a esse prefator: eu meço **±3.78 %** no estacionário sob SBM, contra **±4.0 %**
lidos da Fig. 2(c). Se a forma do skyrmion deles diferisse da minha em 30 %, seria surpreendente
a modulação relativa bater em 5 %. Isso **pesa** para R2, mas não fecha.

**Descartado por medida, não por suposição:** não é erro meu de unidade nem de `d`. O
estimador foi verificado contra a energia de troca — como `E_ex = A d ∫|∇m|²d²r`, vale
`𝒟_xx+𝒟_yy = (M_s d/γ)E_ex/(A d)` por um caminho independente: `3.886e-14` vs `3.955e-14`,
razão `1.0177`, sendo os 1,8 % apenas a diferença de estêncil (avançado vs centrado). Usar
`a₀ = 1 nm` no lugar de `d` afastaria por 2,5×.

### ▸ Pergunta
**Qual é o fator multiplicativo do eixo vertical das Figs. 2(c) e 2(d), e qual valor numérico
de `γ` foi usado na Eq. (2)?**

### ▸ Dado mínimo que resolveria
O valor de equilíbrio da **integral adimensional** `√(det ∫d²r ∂_μm·∂_νm)` — um único número,
sem unidade, que dispensa qualquer convenção. Alternativamente, a série `𝒟(t)` da Fig. 2(c).

---

# D-2 — Os dois `ℓ̄` das legendas (c) e (d) parecem trocados de painel

**O que eu meço** no estado estacionário (últimos 50 ns de corridas de 200 ns):

| excitação | meu `ℓ̄` | legenda do artigo |
|---|---|---|
| `ΔK/K₀ = 0.005` a 18.00 GHz (SBM) | **10.3931 nm** | Fig. 2(c), SBM: **10.98 nm** |
| `B₀ = 4 mT` a 19.24 GHz (ABM) | **10.9824 nm** | Fig. 2(d), ABM: **10.39 nm** |

Quatro dígitos, cruzados. **Em todo o resto os meus rótulos de modo concordam com o artigo:**
`ΔK` é invariante por reflexão especular e a resposta de `l(t)` sai em `ω` (17.9993 GHz);
`B_z` quebra inversão e a resposta sai em `2ω` (38.4785 GHz contra `2×19.24 = 38.48`); e as
**velocidades** caem no painel certo (3.54 vs 3.50 no SBM; 2.03 vs 2.03 no ABM).

**Convergência verificada** — não é a corrida parando no meio da descida: `ℓ̄` decai
geometricamente com razão 0.358 por janela de 25 ns, e o resíduo remanescente é `3e-4 nm`,
dando `ℓ̄(∞) = 10.3931 nm`. Sob ABM já estava plano (`Δ = +2e-5 nm` na última janela).

**Duas leituras.** (i) as legendas de (c) e (d) trocaram os dois valores; (ii) a legenda de (c)
repetiu o `ℓ = 10.98 nm` de **equilíbrio** que a própria Fig. 2(a) cita, em vez da média sob
excitação. A leitura (ii) explicaria (c) mas deixa (d) em aberto, já que sob ABM eu obtenho
10.98 e não 10.39.

**Isto não afeta o alvo de reprodução do equilíbrio**, que vem da legenda da Fig. 2(a) — par
relaxado com a excitação desligada, `ℓ = 10.98 nm` —, valor que a minha implementação
reproduz em 10.9607 nm.

### ▸ Pergunta
**No regime estacionário sob SBM a 18 GHz, `ℓ̄` permanece próximo de 10.98 nm ou contrai para
~10.39 nm? E sob ABM a 19.24 GHz?**

### ▸ Dado mínimo que resolveria
As séries `ℓ(t)` no estacionário usadas para as Figs. 2(c) e 2(d) — ou apenas as duas médias.

---

# D-3 — A forma do transiente de `v_pair(t)` na Fig. 2(a)

**O que eu meço** sob SBM (as duas curvas convergem para quase o mesmo valor tardio, mas por
caminhos diferentes):

| t | Fig. 2(a) | meu `v_⊥` (taxa instantânea) |
|---|---|---|
| 5 ns | ~20 | **43.5** |
| 25 ns | 9.6 | **21.3** |
| 45 ns | 6.1 | **11.3** |
| 85 ns | 4.0 | **5.0** |
| 135 ns | 3.5 | **3.69** |
| 175–200 ns | (plano) | 3.52, **ainda decaindo** |

**Hipótese testada e REJEITADA:** que a curva do artigo fosse média corrida
`(Y(t)−Y(0))/t` em vez de taxa instantânea. Se fosse, eu daria 12.2 cm/s aos 135 ns; a minha
taxa instantânea (3.69) é que se aproxima do 3.5 da figura. Logo a discordância é do
transiente, não de convenção de plotagem.

**Observação que possivelmente liga `D-2` e `D-3` numa só pergunta:** no meu SBM, `v_⊥` e `ℓ̄`
decaem com **a mesma razão geométrica, 0.358 por janela de 25 ns** — são a mesma relaxação. O
meu par migra ~5,2 % na direção coaxial (10.9607 → 10.3931 nm) enquanto a velocidade assenta.
Se o `ℓ̄` de vocês sob SBM realmente fica em 10.98, o meu sistema relaxa para **outro atrator**,
e os dois desacordos são um só. O artigo comenta que, a `Γ = G/α𝒟̄` alto, "skyrmions grow too
large in one of the half-cycles, momentarily favoring the coaxial state" — e com `α = 0.02` o
meu `Γ` é 5× o da Fig. 3 (`α = 0.1`). É conjectura minha, **não testada**.

### ▸ Perguntas
1. **Como `v_pair(t)` da Fig. 2(a) é calculada** — taxa instantânea, média por ciclo de
   excitação, ou outra janela?
2. **Qual é o estado em `t = 0`** e **como a excitação é ligada** (`sin` a partir do zero,
   `cos`, ou rampa)?
3. **Por quanto tempo a corrida da Fig. 2(a) foi de fato integrada?** Os *insets* estão em
   t ≈ 679 ns, muito além dos 200 ns do eixo; a minha corrida de 200 ns **ainda não havia
   estacionado**.

### ▸ Dado mínimo que resolveria
A série `v_pair(t)` da Fig. 2(a), ou a trajetória do centro de carga topológica desde `t = 0`.

---

# D-4 — Menor: a frequência de ressonância do ABM

O meu espectro de breathing (excitação sinc, janela de 10 ns, resolução 0.1 GHz) põe o pico
ABM em **19.40 GHz**, com o bin de 19.30 a 0.993 do pico, centroide acima de meia altura em
**19.348 GHz** e FWHM de 0.60 GHz. O artigo usa **19.24 GHz**. A diferença está dentro da
minha resolução, então provavelmente não é divergência.

Registro só porque **a velocidade de autopropulsão é plana a 0,77 % entre 19.24 e 19.40 GHz**
nas minhas corridas — bem menos sensível à dessintonia do que eu havia estimado, o que pode
ser útil a quem for comparar.

### ▸ Pergunta (opcional)
**Como `f_R` foi determinada na Fig. 6** — bin de pico, ajuste, ou centroide? E qual a
resolução em frequência daquele espectro?

---

# Resumo do pedido, se for para pedir uma coisa só
As **séries temporais no estado estacionário** que geraram as Figs. 2(a)–2(d) sob SBM no
acoplamento fraco: `ℓ(t)`, `𝒟₁(t)`, `𝒟₂(t)` e a posição do centro de carga topológica.
Elas resolvem `D-1`, `D-2` e `D-3` de uma vez.

# O que este documento NÃO afirma
Nada aqui verifica o artigo nem é verificado por ele. Todos os números acima vêm de **um único
código, o meu**, partindo do meu próprio estado de equilíbrio e medidos pela minha própria
régua. Em cada uma das três divergências, "o errado sou eu" continua sendo uma leitura viva.
