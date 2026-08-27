# RELEASE-I003 — era o passo de tempo. `H_dt` confirmado

Missão: `MISSION-I003` · Autorizada por `WRITEBACK-017` · Execução: 2026-08-26, 16:03–16:23
`human_acceptance: PENDING` · Evidência: `LAB/EVIDENCE/I003/`

> Primeiro pré-registro **lido e liberado por Rodrigo antes da execução**, sob a regra do
> `CLAUDE.md` §2 adotada horas antes. O hook de `nvcc` disparou na compilação.

## 1. Veredito: `H_dt`. **Gate `G-I003` passou.**
O par não se desligou na malha fina por física. **Desligou porque eu integrei com o passo
errado.**

| `dt` | `l(0)` | `l(1 ns)` | `l(2 ns)` | `l(3 ns)` | `l(4 ns)` |
|---|---|---|---|---|---|
| `10 fs` | 10.8483 | 12.0623 | 12.1928 | 12.3255 | **12.3880** |
| **`2.5 fs`** | 10.8483 | 10.8483 | 10.8483 | 10.8483 | **10.8483** |

Com `dt` escalado por `a²`, `l` fica **constante em quatro casas decimais** ao longo dos 4 ns.
`Q = ∓1.0000` nas duas. As previsões pré-registradas eram: `H_dt` ⇒ `l ≈ 10.85`;
`H_física` ⇒ dispara nas duas. **O dado cai inteiramente sobre `H_dt`.**

`ID-0` passou: `max‖m‖−1 = 3.3e−16` (10 fs) e `2.2e−16` (2.5 fs), critério `< 1e−9`.

**A causa é a que eu havia conjecturado e não testado:** `B₀ = 2A/(M_s a²)` vai de `51.7` para
`206.9 T` ao refinar de `1.0` para `0.5 nm`. O passo tem de escalar com `a²`, e `10 fs` deixa
de resolver a precessão mais rápida.

## 2. O que isto conserta no registro
O `RF-4` do `RELEASE-E004R` §6 está **explicado**: a corrida era inválida por erro meu de passo
de tempo, e não porque o estado ligado não sobreviva a `0.5 nm`. O desfecho alternativo —
`H_física` — teria sido grave, porque tocaria a convergência de malha (`L1.1`). **Não é o caso.**

## 3. Observação EXPLORATÓRIA — não pré-registrada, não é resultado desta missão
O §6 do pré-registro declarou explicitamente que o `I003` **não** mede a deriva espúria em
malha fina. Com o estado agora preservado, o número está no dado, e registro-o com essa
etiqueta em vez de omiti-lo:

| malha | `v_∥` | `v_⊥` |
|---|---|---|
| `1.0 nm` (`E003`, mesmo θ, mesma medida) | `0.91745 cm/s` | `0.00224` |
| `0.5 nm` (aqui, `dt = 2.5 fs`) | `0.20265 cm/s` | `0.00012` |

**Fator `4.5×` de redução ao refinar a malha pela metade.** Era exatamente a predição que o
`RF-4` do `E004R` queria testar — *"se a deriva espúria é força de rede, ela deve cair
fortemente com o refino"* — e ela **cai**.

**Isto NÃO fecha o `RF-4` nem o `L9.1`.** Dois pontos de malha não estabelecem a lei de escala,
a corrida é de 4 ns contra os 20 ns do `E003`, e o `I002` já mostrou que `v_∥` é hipersensível
a coisas que o refino também muda (`C-12`). É **consistência**, não teste. Fechar exigiria
missão própria, pré-registrada, com pelo menos três malhas.

## 4. Limites
- Um ângulo (`θ = 30°`), um acoplamento, 4 ns, duas malhas.
- A relaxação a `0.5 nm` **não convergiu** (teto de `2×10⁶` iterações, torque `2.755e−6 T`) —
  mesmo comportamento fora do eixo do `E003`. O estado de partida é o mesmo nas duas corridas,
  então a comparação é casada, mas ele não é equilíbrio pleno.
- **Consequência de método, que passa a valer para qualquer missão futura:** `dt` **tem** de
  escalar com `a²`. Nenhuma missão até aqui refinou malha em dinâmica, então nenhum resultado
  aceito está contaminado — mas o `L1.1`, se um dia for atacado com LLG, cai nesta armadilha.
- **`L-G` intocado.** Décima terceira missão.

## 5. Custo
`351.86 s` (10 fs) + `813.59 s` (2.5 fs) ≈ 19 min.

## 6. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar.
