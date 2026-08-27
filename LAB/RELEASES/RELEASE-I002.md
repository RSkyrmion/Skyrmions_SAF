# RELEASE-I002 — a PREMISSA do teste caiu: `v_∥` não é função de `l`

Missão: `MISSION-I002` · Autorizada por `WRITEBACK-016` · Execução: 2026-08-26, 12:46–13:05
`human_acceptance: PENDING` · Evidência: `LAB/EVIDENCE/I002/`

## 1. Veredito
**`IL-1` NÃO É AVALIÁVEL, e o `L8.4` continua ABERTO.**
Não por indeterminação estatística, e não por defeito de desenho: **a premissa da missão foi
refutada pelo próprio dado.** O `IL-1` pergunta por `R(l) = v_∥(l)/v_∥(10.953)`, o que
pressupõe que `v_∥` seja **função de `l`**. Não é.

**Gate `G-I002` NÃO passou** (exige `IL-1` com veredito).

## 2. A medida
`θ = 30°`, **sem excitação**, 20 ns por ponto. Todos os quatro passam o `IL-0`
(`|Q| = 1.0000`, não coaxial, ligação a mais de 5° de eixo/espelho) e todos convergem no
`v_∥` — a grandeza que o critério consome — a `0.014–0.020 %` entre janelas.

| `K₀` [MJ/m³] | `l` [nm] | `𝒟` [10⁻¹⁵ N·s/m] | `Δ = √(A/K)` [nm] | **`v_∥`** [cm/s] |
|---|---|---|---|---|
| 0.55 | 6.4878 | 20.4725 | 5.222 | 0.24612 |
| 0.60 | 10.9531 | 19.4305 | 5.000 | **0.91745** |
| 0.65 | 11.5934 | 18.7363 | 4.804 | 0.73003 |
| 0.70 | 11.5875 | 18.1359 | 4.629 | 0.43226 |

## 3. O que refuta a premissa, em uma linha
**`K₀ = 0.65` e `K₀ = 0.70` têm o MESMO `l`** — `11.5934` e `11.5875 nm`, diferença de
`0.006 nm` (`0.05 %`) — **e `v_∥` difere por 41 %** (`0.730` contra `0.432`).

Um mesmo `l`, dois `v_∥`. Logo `R(l)` não é função, e nenhuma interpolação sobre ela significa
coisa alguma. **Registro que a interpolação ingênua daria `R(10.417) ≈ 0.912`, mais perto de
`H_estado` (0.890) que de `H_excitação` (1.000) — e que NÃO a uso**, porque interpolar uma
relação que os próprios dados mostram não ser unívoca é construir a resposta.

## 4. O que se aprendeu — e é mais forte que a pergunta original
Os dois estados de mesmo `l` diferem em **tamanho do skyrmion**: `𝒟 = 18.74` contra
`18.14e−15 N·s/m`, `3.2 %`. Uma diferença de `3.2 %` no tamanho produz **41 %** em `v_∥`.

**A deriva de rede é hipersensível ao estado** — cerca de **13× em amplificação relativa** —
e `l` não a parametriza. Isso é consistente com efeito de comensurabilidade, que oscila
rapidamente conforme a estrutura desliza em relação à malha, mas **é consistência, não teste**:
a causa (`L9.1`) segue sem verificação.

**Consequência prática:** a pergunta do `L8.4` — se os 11 % vêm do estado ou da excitação —
**não é separável variando `K₀`**, porque `K₀` move várias coisas ao mesmo tempo e `v_∥`
responde a elas de forma abrupta. Precisaria de um controle que reproduzisse o estado excitado
**sem excitar**, e eu não sei construir isso.

## 5. Uma predição minha que estava errada
Pré-registrei, no §3, que `K₀` maior ⇒ `Δ` menor ⇒ skyrmion menor ⇒ **`l` menor**. `Δ` e `𝒟`
de fato caem monotonicamente com `K₀`, mas **`l` sobe**: `6.49 → 10.95 → 11.59 → 11.59`.
O raciocínio "skyrmion menor logo ligação mais curta" estava errado, e é por isso que a
varredura não pousou onde eu queria: o alvo `l = 10.417` ficou num vão de `4.5 nm` entre dois
pontos, e não entre vizinhos.

## 6. Este fracasso NÃO é da família dos outros nove
Vale distinguir, porque a distinção importa para saber o que corrigir.
Os nove defeitos anteriores eram **de desenho**: limiar absoluto contra referência externa, ou
convergência checada na grandeza errada. **Aqui o critério estava bem-formado** — comparação
entre duas hipóteses prevendo valores diferentes da mesma grandeza, sem limiar, poder medido
(`~100×`), convergência checada na **saída**. Ele falhou por uma razão **científica**: a
premissa física sobre a qual foi construído é falsa.

Um pré-registro bom não impede isso, e não deveria. **É o tipo certo de fracasso.**

## 7. Limites
- **`L8.4` continua ABERTO**, e agora com uma razão medida para ser difícil.
- **`L9.1`** (a causa da força de rede) intocado.
- Um ângulo, um acoplamento, 20 ns, malha de 1 nm, quatro pontos.
- As quatro relaxações **não convergiram** (teto de 2×10⁶ iterações, torque `0.8–1.3e−5 T`) —
  o mesmo comportamento fora do eixo que o `E003` registrou. Os `v_∥` são estáveis a `0.02 %`
  ao longo dos 20 ns, mas partem de estados não plenamente relaxados.
- **`L-G` intocado.** Décima missão.

## 8. Custo
4 × 279 s ≈ 19 min.

## 9. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar.
