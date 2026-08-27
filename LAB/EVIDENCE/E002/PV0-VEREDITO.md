# PV-0 — VEREDITO: **FALHOU**

Pré-registro: `MISSION-E002.md` §5. Critério: `½(𝒟₁+𝒟₂) ∈ [13.5, 16.5]×10⁻¹⁵ N·s/m`,
`|𝒟_xx−𝒟_yy|/𝒟_xx < 0.05`, `|𝒟_xy|/𝒟_xx < 0.05`.

| quantidade | medido | critério | |
|---|---|---|---|
| `½(𝒟₁+𝒟₂)` | **19.4306e−15 N·s/m** | [13.5, 16.5] | **FALHOU** (+29.5 %) |
| `\|𝒟_xx−𝒟_yy\|/𝒟_xx` | 0.0021 | < 0.05 | passou |
| `\|𝒟_xy\|/𝒟_xx` | 0.0000 | < 0.05 | passou |

**Critério pré-registrado que falha, falhou.** Não é reinterpretado abaixo. O que segue
diagnostica a causa, como a taxonomia do §7 manda ("erro de unidade/`d` é o primeiro
suspeito"), e delimita o que a falha contamina.

## O primeiro suspeito foi descartado: não é unidade, não é `d`, não é bug
1. **`d` vs `a₀`:** usar `a₀ = 1 nm` no lugar de `d = 0.4 nm` daria 48.6e−15 — 2,5× **mais**
   longe. A escolha `d` é a que aproxima. A discrepância não é 2,5× nem potência de 10.
2. **O estimador foi verificado contra a energia de troca**, que é validada por diferenças
   finitas desde a `VL-1` do `R001`. Como `E_ex = A d ∫|∇m|²d²r`, vale
   `𝒟_xx+𝒟_yy = (M_s d/γ)·E_ex/(A d)` por um caminho que não passa pelo meu tensor:

   | rota | `𝒟_xx+𝒟_yy` |
   |---|---|
   | tensor, diferenças centradas | `3.886160e−14` |
   | energia de troca (validada por FD) | `3.954856e−14` |
   | razão | **1.017677** |

   A diferença de 1,77 % é **só o estêncil** (avançada na energia de ligação vs centrada no
   tensor); a previsão analítica para esta suavidade de malha era ~2,5 %. O estimador está
   certo.
3. **Não depende da tolerância de relaxação.** Sobre os estados **selados** do `R001`:
   `mfinal_weak` (1e−5) → `19.4308e−15`; `mfinal_weak_tight` (1e−6) → `19.4306e−15`.
4. **Reprodução cruzada:** o `dissip()` em CUDA e o `diag_dissip.py` em Python/numpy dão
   `𝒟_xx = 1.945083e−14` — os mesmos dígitos.

## O que sobra: uma discrepância de 29,5 %, com duas leituras
Em termos da integral adimensional `I = √(det ∫∂_μm·∂_νm d²r)`, o meu skyrmion dá
`I = 14.748` (raio a `m_z=0` de **5.946 nm**, contra `Δ = √(A/K) = 5.000 nm`).

- **Leitura R1 — a que pré-registrei, e a única dimensionalmente consistente.** O eixo da
  Fig. 2(c) está em `10⁻¹⁵ N·s/m` (só assim `M_s d/γ` fecha em N·s/m). Então o valor deles é
  `I = 11.385`, e o meu é **+29,5 %**. Isto seria uma diferença real de **forma/tamanho** do
  skyrmion — camada que nada neste laboratório jamais testou: o `R001` validou a *separação*
  `l`, nunca o *raio*.
- **Leitura R2 — hipótese levantada DEPOIS da falha, e registrada como tal.** Se os autores
  calcularam numericamente com `γ₀ = μ₀γ = 2.21277e5 m/(A·s)` (o artigo diz "gyromagnetic
  **factor**") e rotularam N·s/m, o eixo estaria em `10⁻⁹` e o valor deles seria `I = 14.307`
  — **+3,1 %** do meu.

**R2 não repara o PV-0 e não será usada para isso.** É um número bonito achado depois do
fato, exatamente a forma de raciocínio que já recusei duas vezes (`l(140 nm) = 10.9566` e a
extrapolação de Richardson). Fica no registro **como hipótese, nunca como resultado**. Ambas
as leituras exigem que o rótulo do eixo omita um expoente; não é decidível daqui — exigiria o
dado dos autores ou uma terceira implementação.

## O que a falha contamina — e o que não contamina
- **`EP-5` (integral da Eq. 4) NÃO é afetado.** `G = 4π(M_s d/γ)Q` e `𝒟 = (M_s d/γ)·I`, logo
  no integrando `G/(α𝒟) = 4πQ/(αI)` o prefator **cancela exatamente**, e
  `v_sp = −(ω/α)∮[Q/I]dl`. Qual das duas leituras é a certa **não muda o valor** de `EP-5`.
- **`EP-1`, `EP-2`, `EP-3`, `EP-4` não usam 𝒟.** Dependem só da CTC (Eq. 1), cuja régua está
  verificada por implementação cega independente (`C-5`, `AUDIT-002`).
- **A amplitude relativa do ciclo** `Δ𝒟/𝒟` também é invariante ao prefator. A Fig. 2(c) dá
  `±0.6/15.0 = ±4.0 %`. Comparar a minha com essa é a única discriminação disponível entre R1
  e R2 sem dado externo — e é **observação exploratória declarada aqui, antes das corridas de
  produção**, não critério.

## Consequência formal
O `PV-0` entra no gate `G-E002`. **O gate, portanto, JÁ NÃO PODE PASSAR.** Como no `A002`,
a missão segue e relata o que sobrevive; não se converte falha em aprovação.

A cláusula do §7 "nenhuma velocidade é relatada até resolver" é atendida no único sentido
honesto disponível: a causa foi isolada (não é minha unidade nem meu estimador) e a
ambiguidade que sobra foi **provada não-propagante** para todos os critérios de velocidade.

## Defeito de DESENHO do critério — registrado, não reparado
O `PV-0` comparou um `𝒟` **absoluto** contra um eixo de figura cujo expoente **está ausente**
do rótulo. Um critério assim **não consegue distinguir** "a forma do meu skyrmion difere" de
"o rótulo omite um expoente" — que é exatamente a ambiguidade R1/R2 acima. Foi mal
pré-registrado. Fica registrado como **falha de desenho, não reparada em aprovação**, como a
regra de poder do `RELEASE-R002` §2.

O critério que teria discriminado — e que era barato — é a **amplitude relativa** do ciclo,
`Δ𝒟/𝒟`, invariante ao prefator. Ele não foi pré-registrado. É relatado como exploratório e
**não conta como resultado desta missão**.
