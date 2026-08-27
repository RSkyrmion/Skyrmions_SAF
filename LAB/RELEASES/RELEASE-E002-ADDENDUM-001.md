# RELEASE-E002-ADDENDUM-001 — convergência do estacionário no SBM

Data: 2026-08-25 · Corrige/qualifica: `RELEASE-E002.md` §3 (`EP-2`) e §5.1
Origem: revisão que perguntou se o platô do SBM é platô ou é a corrida parando no meio da
descida. **A pergunta era certa, e a resposta muda uma das duas coisas.**

## O que foi medido
Médias por janela de 25 ns sobre `EVIDENCE/E002/prop_sbm_18.00GHz.dat`:

| janela | `l̄` [nm] | Δ | `v_⊥` [cm/s] | Δ |
|---|---|---|---|---|
| 0–25 | 10.75423 | | 33.72436 | |
| 25–50 | 10.52294 | −0.23129 | 14.42991 | −19.2944 |
| 50–75 | 10.43965 | −0.08329 | 7.42378 | −7.0061 |
| 75–100 | 10.40976 | −0.02989 | 4.90590 | −2.5179 |
| 100–125 | 10.39904 | −0.01072 | 4.00266 | −0.9032 |
| 125–150 | 10.39520 | −0.00384 | 3.67881 | −0.3239 |
| 150–175 | 10.39382 | −0.00138 | 3.56271 | −0.1161 |
| 175–200 | 10.39333 | −0.00049 | 3.52110 | −0.0416 |

As duas colunas decaem **geometricamente com razão ≈ 0.358** por janela, estável ao longo de
seis janelas.

## 1. `l̄` do SBM — CONVERGIDO. A §5.1 se sustenta.
Resíduo geométrico remanescente: `−0.00049 × 0.358/(1−0.358) = −0.00027 nm`, logo
**`l̄(∞) = 10.3931 nm`**. Está convergido a 3e−4 nm.
A coincidência de quatro dígitos com o `10.39 nm` que a Fig. 2(d) atribui ao ABM **não é
artefato de parada**, e a observação exploratória da §5.1 fica de pé como estava escrita —
inclusive o "não escolho uma leitura".
Para comparação, o ABM já estava plano: `10.98213 → 10.98239` nas últimas quatro janelas
(Δ final `+0.00002 nm`).

## 2. `v_⊥` do SBM — NÃO estava em platô. Isto corrige a §3.
Ao final da corrida `v_⊥` **ainda decaía**, `−0.0416 cm/s` na última janela. O número
pré-registrado — ajuste linear dos 150–200 ns, **`3.5400 cm/s`** — é, portanto, **uma travessia,
não um platô**, e o texto da §3 ("é o platô que bate") **está errado nesse ponto**.

Extrapolação geométrica do transiente restante:
`v_⊥(∞) ≈ 3.52110 − 0.0416 × 0.358/(1−0.358) = **3.498 cm/s**`.

**Isto é EXPLORATÓRIO.** A extrapolação não estava pré-registrada, a razão foi ajustada a
posteriori, e o `E001` já registra o precedente de extrapolação recusada como resultado
(Richardson, `ADDENDUM-005`). **Não substitui o `3.5400`**, que continua sendo o número
pré-registrado e o que o `EP-2` avaliou.

**O `EP-2` não muda:** 3.5400 e 3.498 estão ambos folgadamente dentro de `[2.45, 4.55]`, e o
alvo extraído é `3.50 ± 0.11` (um pixel). O que muda é o **limite que viaja junto**:

> **Limite novo:** a corrida SBM de 200 ns **não atingiu o estacionário** em `v_⊥`; a
> concordância com a Fig. 2(a) é de uma travessia a 200 ns, não de um valor assintótico
> medido. O artigo mostra o painel (a) plano a partir de ~150 ns e coloca os *insets* em
> t ≈ 679 ns — ou seja, **eles rodaram muito mais longe do que eu**.

## 3. Nota física, não medida
A contração de `l̄` de 10.9607 (equilíbrio) para 10.3931 nm sob SBM é de **−5.2 %**, na
direção coaxial. O artigo observa que, a `Γ = G/α𝒟̄` alto, "skyrmions grow too large in one of
the half-cycles, momentarily favoring the coaxial state". Com `α = 0.02` o meu `Γ` é **5×** o
da Fig. 3 (`α = 0.1`). É uma explicação **plausível e não testada** — registrada como
conjectura, não como achado.
