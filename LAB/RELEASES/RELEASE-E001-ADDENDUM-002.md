# ADENDO-002 a RELEASE-E001 — forma adimensional implementada e verificada

Data: 2026-08-24 · Motivado por Rodrigo, que forneceu a forma adimensional
Missão: `MISSION-E001`, ainda `TERMINAL_AWAITING_HUMAN`

> `RELEASE-E001.md` e o `ADENDO-001` **não foram editados**. Este adendo acrescenta.

## 1. A forma dada
```
dS_i/dτ = −1/(1+α²) [ S_i × H_i^eff + α S_i × (S_i × H_i^eff) ]
t = t₀ τ ,     t₀ = M_s a₀² / (2 A_ex γ)
```

## 2. Equivalência algébrica com a forma que eu implementei
Partindo de `dm/dt = −γ/(1+α²)[m×B + α m×(m×B)]`, com `t = t₀τ` e `B = B₀H`:
```
dm/dτ = −γ B₀ t₀ /(1+α²) [ m×H + α m×(m×H) ]
```
As duas coincidem **se e só se** `γ B₀ t₀ = 1`. Com `B₀ ≡ 2A_ex/(M_s a₀²)`:
```
γ B₀ t₀ = γ · (2A_ex/(M_s a₀²)) · (M_s a₀²/(2A_ex γ)) = 1   ✓
```
Ou seja, `t₀` **é** `1/(γB₀)`, e a escala natural de campo é o próprio prefator de troca.
Verificado no código: `γ B₀ t₀ = 1` exato em ponto flutuante.

```
B₀ = 2 A_ex/(M_s a₀²) = 51.724138 T      (= o coeficiente `ce` do meu kernel de troca)
t₀ = 1/(γ B₀)         = 1.097949e−13 s = 0.1098 ps
dt = 10 fs            = 0.091079 t₀     (≈ 11 passos RK4 por unidade natural)
```

## 3. Verificação NUMÉRICA — não bastava a álgebra
Álgebra equivalente não implica igualdade em ponto flutuante: as duas rotas multiplicam
números de magnitudes muito diferentes (`γ ~ 1.8e11` e `B ~ 50 T` contra `1` e `H ~ 1`) e
arredondam de formas distintas. Implementei **as duas** no mesmo binário (`k_llg` ganhou
`pref` e `fscale`) e integrei o **mesmo** par de skyrmions por 20 000 passos RK4 (0.2 ns) em
cada uma:

| `α` | `E` física [J] | `E` adimensional [J] | `\|ΔE\|/\|E\|` | `max \|S_fis − S_nd\|` | `rms` |
|---|---|---|---|---|---|
| 0.00 | −4.776259057781176e−18 | −4.776259057781176e−18 | **0.000e+00** | 3.61e−14 | 5.56e−15 |
| 0.02 | −4.784017082366692e−18 | −4.784017082366692e−18 | **0.000e+00** | 4.39e−14 | 5.12e−15 |
| 0.30 | −4.785434461815557e−18 | −4.785434461815557e−18 | **0.000e+00** | 5.56e−14 | 5.51e−15 |

Energias idênticas em **todos os 16 dígitos**. O desvio de configuração de `~5e−14` é o
acúmulo de arredondamento esperado ao longo de 20 000 passos (`ε_double = 2.2e−16`), e não
cresce com `α`. **As duas formulações são a mesma equação, também numericamente.**

## 4. Por que isto vale além da conferência
1. **Fecha a discussão do `1/(1+α²)` pelo lado construtivo.** O `ADENDO-001` mediu o fator via
   Larmor amortecida (`α=0.30`, efeito de 9 %, desvio `3e−15`). Aqui ele é exercido dentro do
   sistema completo, nas duas formulações, com o mesmo resultado.
2. **A rota adimensional fica disponível para o `E002`.** Trajetórias de ~3 µs em `t₀ = 0.11 ps`
   são ~2.7e7 unidades naturais; integrar em `τ` evita carregar `dt = 1e−14 s` e `γ = 1.8e11`
   em todo produto, que é melhor condicionado para corridas longas.
3. **É um teste que podia ter falhado.** Um erro de fator no meu `GAMMA_T`, no prefator de
   troca ou na definição de `B₀` apareceria imediatamente como divergência entre as rotas.

## 5. Artefato
Modo novo: `./saf_dyn ndcheck <alpha>`. Código em `EVIDENCE/E001/saf_dyn.cu`.
`SHA256SUMS.txt` atualizado.

## 6. Efeito na decisão pendente
Nenhum critério pré-registrado muda; `G-E001` continua passado. Acrescenta uma verificação
construtiva e deixa a formulação adimensional pronta para a próxima missão.
