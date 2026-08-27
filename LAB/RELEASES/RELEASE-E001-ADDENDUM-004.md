# ADENDO-004 a RELEASE-E001 — reconciliação com `LAB/admensional_LLG.md`

Data: 2026-08-24 · Fonte fornecida por Rodrigo: `LAB/admensional_LLG.md`
Missão: `MISSION-E001`, ainda `TERMINAL_AWAITING_HUMAN`

## 1. O documento confirma tempo e campo — exatamente
O documento define `ω₀ = γ J_cel/m_i`, com `J_cel = 2aA` e `m_i = v_cel M_s = M_s a³`
(célula **cúbica**, §1: `v_cel = a³`). Substituindo:

```
ω₀ = γ (2aA)/(M_s a³) = 2γA/(M_s a²) = γ B₀        com B₀ = 2A/(M_s a²)
1/ω₀ = 9.107891e+12⁻¹ = 1.097949e−13 s
meu t₀ = M_s a²/(2Aγ) = 1.097949e−13 s             -> IDÊNTICO
```

## 2. E confirma a ressalva do `ADENDO-003` — pela própria relação do documento
O §3 do documento escreve a identidade **geral**:
`B_i^eff = (J_cel/m_i) b_i^eff`, isto é **`J_cel = m_i B₀`**.

É exatamente a identidade que usei no `ADENDO-003`. A diferença está só em `m_i`:

| geometria da célula | `m_i` | `J` resultante |
|---|---|---|
| cúbica `a³` (o documento) | `M_s a³ = 5.80e−22 A m²` | `2 a A = 3.00e−20 J` |
| filme `a × a × d` (**este modelo**) | `M_s a² d = 2.32e−22 A m²` | `2 A d = 1.20e−20 J` |

Verificado numericamente: `m_i B₀ = 1.200000e−20 J = 2 A d`, idêntico.
Razão entre as duas convenções: `a/d = 2.5`.

**Não há discordância.** `J_cel = 2aA` é a fórmula do documento **especializada para célula
cúbica**; a Eq. (A3) deste artigo é uma integral **areal** com `d` explícito e `d ≠ a`, e a
mesma fórmula do documento aplicada a essa geometria dá `2 A d`.

## 3. NOVO — a condição de validade `a ≤ λ_tr` nunca tinha sido checada neste laboratório
O documento (§1) impõe `a ≤ λ_tr`, com `λ_tr = √(2A/(μ₀ M_s²))`, para que a magnetização
dentro da célula esteja saturada e a aproximação micromagnética valha.

```
λ_tr = √(2A/(μ₀ M_s²)) = 8.424 nm
malha de 1.0 nm  ->  a/λ_tr = 0.1187   SATISFEITA (folga de ~8×)
malha de 0.5 nm  ->  a/λ_tr = 0.0594   SATISFEITA
```

Verificação **nova e favorável**: a discretização de 1 nm usada no `R001`/`R002` está
confortavelmente dentro do regime de validade micromagnética. O laboratório tinha checado
`κ = D/D_c = 0.80 < 1` (regime de skyrmion metaestável), mas **nunca** tinha checado
`a ≤ λ_tr`. Fica registrado.

## 4. Duas diferenças de escopo — a registrar antes que alguém use o documento como template
1. **Termo dipolar.** O documento carrega dipolar explícito, com peso
   `(1/4π)(a/λ_tr)² = 0.001121`. **Este modelo omite demag** (`QA-01`: absorvido em
   `K₀ = K_u + ½μ₀M_s²`, conforme o próprio artigo). Usar o documento sem remover o dipolar
   causaria **dupla contagem** contra `K₀`.
2. **Torque de transferência de spin.** O documento inclui STT (`v_j`, `ξ`, `c_j = ξv_j`).
   A Eq. (A1) do PRL **não tem STT**: a autopropulsão vem dos modos de breathing sob
   excitação de campo/anisotropia, não de corrente. Fora do escopo de `E001`/`E002` — mas é
   o caminho natural se a Fase 2 for estendida para acionamento por corrente.

Também: o documento não traz DMI, anisotropia uniaxial nem acoplamento interlayer, que são
exatamente os termos que este modelo precisa. Ele é o **esqueleto da adimensionalização**,
não o modelo completo.

## 5. Efeito nos resultados
**Nenhum.** Confirma o `ADENDO-002` (tempo/campo) e o `ADENDO-003` (energia), acrescenta a
verificação `a ≤ λ_tr` e delimita o que do documento se aplica a este modelo.
`G-E001` continua passado; nenhum critério pré-registrado muda.
