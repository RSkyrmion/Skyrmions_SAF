# MISSION-I002 — a deriva espúria `v_∥` depende do ESTADO ou da EXCITAÇÃO?

Estado: **`AUTHORIZED`** por `WRITEBACK-016` · Data: 2026-08-26
Regime: caracterização de artefato. Resolve (ou não) o `L8.4` do `C-8`.

> **Pré-registro.** Escrito antes de qualquer código novo e de qualquer corrida.
> **Forma dos critérios:** comparação entre duas hipóteses que preveem valores **diferentes da
> mesma grandeza**, medida no mesmo instrumento. **Nenhum limiar absoluto.** É a regra que os
> nove defeitos desta linha de trabalho ensinaram: todo critério que funcionou foi comparação;
> todo critério que falhou foi limiar contra referência externa.

## 1. O fato que origina a missão
No `E003`, fora do eixo, a deriva ao longo da ligação vale:

| θ | `v_∥` **sem** excitação | `l` | `v_∥` **com** excitação | `l` | razão |
|---|---|---|---|---|---|
| 30.0° | `0.91745 cm/s` | `10.953 nm` | `0.81664` | `10.417 nm` | **0.890** |
| 22.5° | `0.90378` | `10.957` | `0.80054` | `10.420` | **0.886** |

Os `10 %` de resíduo do `L8.4` são exatamente esta razão. O par excitado é **4,9 % mais curto**
(contração sob SBM, já registrada no `RELEASE-E002` §5.1).

## 2. As duas hipóteses, e o que cada uma prevê
- **`H_estado`** — `v_∥` é força de rede, e depende do **estado** do par (aqui parametrizado
  por `l`). Então um par **não excitado** com `l ≈ 10.42` deve ter `v_∥ ≈ 0.82`, não `0.92`.
- **`H_excitação`** — `v_∥` é reduzida pela **excitação em si** (respiração, média temporal),
  não pelo estado. Então um par não excitado, seja qual for o `l`, mantém `v_∥ ≈ 0.92`.

## 3. Como obter `l` diferente sem excitar
`l` de equilíbrio depende de `K₀` — é o próprio diagrama do `R002`. `K₀` maior ⇒ parede
`Δ = √(A/K)` menor ⇒ skyrmion menor ⇒ `l` menor.
Varredura: **`K₀ = 0.55, 0.60, 0.65, 0.70 MJ/m³`**, `A_int = 0.02` fixo, `θ = 30°`, **sem
excitação**, 20 ns cada. `K₀ = 0.60` é o ponto do `E003` e serve de âncora.

## 4. Critério primário `IL-1` — uma razão contra outra razão
Grandeza: `R(l) ≡ v_∥(l) / v_∥(l = 10.953)`, sempre **sem excitação**, sempre no mesmo θ.

Interpolar `R` em `l = 10.417 nm` a partir da varredura de `K₀` e comparar com o **valor já
medido** no par excitado, `R_exc = 0.890`.

| | previsão para `R(10.417)` |
|---|---|
| **`H_estado`** | `≈ 0.890` — o ponto excitado cai **sobre** a curva não excitada |
| **`H_excitação`** | `≈ 1.000` — `v_∥` não muda com `l`, logo a queda tem de vir da excitação |

**Não há limiar.** As duas previsões distam `11 %`, e reporto `R(10.417)` medido entre elas.

**Checagem de poder, medida e não suposta:** no `E003` o `v_∥` do controle variou de `0.91697`
a `0.91756` ao longo de 20 ns — `0.06 %`. A precisão é, portanto, `~0.1 %`, contra hipóteses
separadas por `11 %`: **margem de ~100×**. Se o resultado sair entre as duas, é resultado
intermediário e será relatado como tal, sem escolher lado.

## 5. `IL-0` — pré-teste: os estados são comparáveis?
Para cada `K₀`: `|Q₁| = |Q₂| = 1.0000`, par **não coaxial**, e a ligação **não** encaixada em
eixo/espelho da malha (`θ_bond` a mais de 5° de `0/45/90°`).
**Descartar** qualquer `K₀` que falhe. **Se sobrarem menos de 3 pontos, ou se eles não
cercarem `l = 10.417`, o `IL-1` é INDETERMINADO** — não aprovado, não reprovado — e a missão
relata que a varredura não alcançou o alvo.

## 6. Convergência — checada na grandeza que o critério consome
`v_∥` é a própria grandeza discriminante (não uma entrada dela). Comparar `v_∥` nas janelas
`10–15` e `15–20 ns` de cada corrida. **Se variarem mais que `0.5 %`** (5× a variação medida no
`E003`), aquele ponto é declarado não convergido e **excluído**, não estendido.

Registro explicitamente que este é o ponto onde eu errei três vezes (`EF-0`, `RF-0`, e o offset
do `E003`): aqui a convergência é checada na **saída**, não nas entradas.

## 7. Taxonomia de falha
| resultado | significado, decidido antes |
|---|---|
| `R(10.417) ≈ 0.89` | **`H_estado`**: o `L8.4` fica **explicado** — eu comparei contra um controle no estado errado. O resíduo deixa de ser inexplicado |
| `R(10.417) ≈ 1.00` | **`H_excitação`**: o `L8.4` continua aberto e fica **mais interessante** — a excitação reduz a força de rede por mecanismo desconhecido |
| intermediário | as duas contribuem; relatar a partição, **sem escolher lado** |
| `IL-0` deixa <3 pontos | INDETERMINADO; a varredura não alcançou o alvo |

## 8. Limites — declarados antes
- `K₀` muda **mais que `l`**: muda o tamanho do skyrmion e `Δ = √(A/K)`. Portanto `H_estado`,
  se vencer, significa "**o estado** importa", **não** "`l` é a causa". A causa da força de
  rede continua sem teste (`L9.1`).
- Um acoplamento, um ângulo por ponto, 20 ns, malha de 1 nm.
- **Não** move o `C-8`: o teste de inclinação já era imune à contaminação.
- **`L-G` intocado.** Décima missão.

## 9. Provenance
`LAB/EVIDENCE/I002/saf_inst2.cu`, derivado do `saf_prop4r.cu` selado, caminhos redirecionados
antes da primeira execução e verificados por `grep`.

## 10. Gate
`G-I002` = `IL-0` (≥3 pontos, cercando 10.417) ∧ `IL-1` **com veredito**.
O gate exige veredito do critério primário — o defeito do `G-E004`, corrigido.
**Passar o gate não é aceite.**
