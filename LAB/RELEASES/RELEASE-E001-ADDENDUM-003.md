# ADENDO-003 a RELEASE-E001 — a unidade de energia do esquema adimensional

Data: 2026-08-24 · Motivado por Rodrigo: *"A energia é parametrizada em termos de
`J_ex = 2 a₀ A_ex`"*
Missão: `MISSION-E001`, ainda `TERMINAL_AWAITING_HUMAN`

## 1. O conjunto de unidades, agora completo
`ADENDO-002` fixou tempo e campo. Falta a energia. O conjunto auto-consistente é:

```
B₀   = 2 A_ex/(M_s a₀²)              = 51.724138 T
t₀   = 1/(γ B₀) = M_s a₀²/(2A_ex γ)  = 1.097949e−13 s
μ    = M_s a₀² d                     = 2.320000e−22 A m²      (momento por célula)
J_ex = μ B₀                          = 1.200000e−20 J
```

## 2. `J_ex = 2 a₀ A_ex` vale para célula CÚBICA; aqui a célula não é cúbica
A unidade de energia é fixada pela identidade que o `VL-1` verifica por diferenças finitas
(reconfirmada nesta sessão, erro relativo `4.95e−08`):
`B = −(1/μ) ∂H/∂m`, com `μ = M_s a₀² d`. Se `B̃ = B/B₀`, então necessariamente
`Ẽ = H/(μ B₀)`, ou seja **`J_ex = μ B₀`**.

```
μ B₀      = (M_s a₀² d)·(2A_ex/(M_s a₀²)) = 2 A_ex d  = 1.20e−20 J
2 A_ex a₀                                             = 3.00e−20 J
razão                                                 = a₀/d = 2.5
```

**As duas expressões coincidem se e só se `d = a₀`** — o caso de célula cúbica `a₀³`, para o
qual a forma `2 a₀ A_ex` é a correta. O modelo deste artigo usa `a₀ = 1 nm` no plano e
`d = 0.4 nm` de espessura (Eq. A3 é integral **areal**, com `d` explícito), logo aqui a
unidade é **`J_ex = 2 A_ex d`**.

## 3. Segundo caminho, independente do primeiro
A energia de troca discreta do modelo (forma confirmada pela derivação cega do `AUDIT-001`) é
`H_ex = A_ex d Σ_μ |m_{n+μ} − m_n|²`. Como `|Δm|² = 2(1 − m_i·m_j)`:
`H_ex = 2 A_ex d Σ_μ (1 − m_i·m_j)` — o coeficiente por ligação é **`2 A_ex d`**.
Bate com `μB₀` do §2. Dois caminhos, mesma resposta.

## 4. Por que a assimetria: tempo e campo não veem `d`, a energia vê
Em `B₀ = 2A_ex/(M_s a₀²)` o `d` da energia cancela contra o `d` do momento `μ = M_s a₀² d`.
Por isso `t₀` e `B₀` são independentes de `d`, e por isso o `ndcheck` do `ADENDO-002` fechou
com desvio `~5e−14` mesmo com `d ≠ a₀`. A energia, ao contrário, é `μ·B₀` — o `d` sobrevive.

Este é **exatamente** o mesmo `d`-versus-`a₀` do risco `SL-2` (o fator `1/d` no campo
interlayer), que precisou de quatro caminhos independentes para fechar. A mesma armadilha,
noutro lugar do esquema.

## 5. Números para referência
Energia de equilíbrio do par (`R001`, VL-4, acoplamento fraco): `−4.785440e−18 J`.

| unidade | valor de `H_eq` |
|---|---|
| `J_ex = 2 A_ex d = 1.20e−20 J` (auto-consistente aqui) | **−398.787** |
| `J_ex = 2 A_ex a₀ = 3.00e−20 J` (cúbica, `d = a₀`) | −159.515 |

Nota útil: `J_ex = 1.20e−20 J = 12 × 10⁻²¹ J`, e a Fig. 5(b)/(d) do artigo plota `E(R)` em
unidades de `10⁻²¹ J` na faixa de ~0 a −2.5. Ou seja, as energias de ligação do par são uma
fração pequena de `J_ex`, o que é consistente.

## 6. Efeito nos resultados
**Nenhum.** O código trabalha em SI (joules, tesla, segundos) do começo ao fim; a
adimensionalização é escolha de reporte. Nenhum claim muda, nenhum critério pré-registrado
muda, `G-E001` continua passado.

O risco que este adendo previne é de leitura: adimensionalizar a energia com `2 a₀ A_ex` neste
modelo daria valores **2.5× menores** e faria qualquer critério baseado em energia — por
exemplo comparar contra os perfis `E(R)` da Fig. 5 — ser lido errado por esse fator.
