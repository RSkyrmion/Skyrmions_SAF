# MISSION-A005R — casar a convergência, e refazer o que dependia dela

Estado: **`AUTHORIZED`** por `WRITEBACK-025` · Data: 2026-08-27
Regime: revisão do `A005` + remedição do `MV-2` do `A003`

> **Pré-registro.** Escrito antes de qualquer corrida. Submetido à leitura de Rodrigo antes da
> execução (`CLAUDE.md` §2).

## 1. O defeito que esta missão corrige
O `A005` comparou dois códigos deixando **cada um parar na sua própria tolerância**: `saf.cu`
em `1.0e−6 T`, mumax3 em `4.5e−5 T` — **45× mais frouxo**. Isso não compara os códigos;
compara os padrões deles. Décimo defeito de desenho, e de tipo novo: **não casar uma
configuração numérica entre os dois lados de uma comparação.**

**Correção pré-registrada:** casar a tolerância em **`1.0e−6 T`**, o valor que o `saf.cu` usa
desde o `E002`. O valor é escolhido **pelo casamento**, não pelo resultado — e está fixado
aqui, antes de qualquer corrida.

## 2. `AC-0` — o casamento é VERIFICADO, não assumido
O `RelaxTorqueThreshold` (`relax.go:17`) governa o `relax()`. O `minimize()` tem critério
próprio (`MinimizerStop`). **Ler os dois no fonte** e ajustar o que for preciso; depois
**imprimir o `MaxTorque` final** e conferir.

- **PASSA se** `MaxTorque_final ≤ 1.0e−6 T`.
- **Se o mumax3 não alcançar `1e−6`**, reportar o melhor atingível e **declarar o casamento
  parcial**, com o fator residual explícito. Os critérios seguintes passam a ser lidos com esse
  fator ao lado. **Isto é desfecho previsto, não fracasso.**

## 3. `AC-1` — o `AR-0` refeito, agora em forma de COMPARAÇÃO
O `AR-0` usava limiar absoluto (`|v| < 0.05 cm/s`) — a forma que o `CLAUDE.md` §6.1 `R1` diz
para evitar. E ele era apertado demais: o **próprio `saf.cu`**, a `tol = 1e−6` e `θ = 0`, dá
`0.0399 cm/s` na janela de 10–20 ns (`E002`, `PV-1`, dado selado). Margem de só 25 %.

**Forma nova:** comparar a deriva do mumax3 com a do `saf.cu` **na mesma janela e com a mesma
tolerância**.

| | previsão para `v_mumax3 / v_saf.cu` |
|---|---|
| **`H_casado`** — a deriva do `AR-0` era só o torque residual | `≈ 1` (dentro de fator 2) |
| **`H_residual`** — há outra coisa no mumax3 | `≫ 2`, e no limite os `25 000×` do `A005` |

`v_saf.cu` é **medido do dado selado** (`E002/prop_pv1_noise200ns.dat`, janela 5–19 ns, a mesma
usada no `A005`), não citado de memória.

## 4. `AC-2` — o `AR-1` refeito (o critério primário do `A005`)
`θ = 30°`, sem excitação, 20 ns, convergência casada. Decompor no referencial da ligação.

| | previsão para `\|v_∥\|` |
|---|---|
| **`H_comum`** | `≈ 0.9 cm/s`, ao longo da ligação (o `saf.cu` dá `0.91745`) |
| **`H_nosso`** | `≈ 0` |

O `A005` já viu `0.822` **contaminado** por deriva residual perpendicular. Com o casamento, a
contaminação some e o número fica limpo. **Predição registrada:** `v_∥` deve ficar **próximo
dos `0.822`** já vistos — porque a componente **ao longo da ligação** não é a contaminada. Se
mudar muito, a decomposição do `A005` §4 estava errada.

## 5. `AC-3` — o `MV-2` refeito, e a predição que pode falhar
Relaxar o par no ponto do `C-1` com convergência casada e medir `l` **pelo estimador cego do
`AUDIT-002`** — a mesma régua do `A003`.

**Predição registrada, e ela é falsificável:** se os `−0.30 %` do `C-15` são **em parte**
descasamento de convergência, então `l_mumax3` deve **SUBIR** na direção dos `10.9607` — porque
o `E003` mediu que relaxação mais frouxa dá `l` **menor** (`1e−5` ⇒ `10.9529`;
`1e−6` ⇒ `10.9607`).

| | previsão |
|---|---|
| **`H_convergência`** | `l_mumax3` sobe, e `\|Δl\|/l` **diminui** abaixo de `0.30 %` |
| **`H_código`** | `l_mumax3` fica em `≈ 10.928`; os `−0.30 %` são diferença real entre os códigos |

**Se `l` DESCER**, as duas hipóteses estão erradas e isso é achado — a explicação de
convergência do `RELEASE-A005` §5 cai.

## 6. Taxonomia de falha
| resultado | significado, decidido antes |
|---|---|
| `AC-0` não alcança `1e−6` | casamento **parcial**; tudo abaixo é lido com o fator residual ao lado |
| `AC-1` razão `≈ 1` | a deriva do `AR-0` era torque residual. **`A007` DESBLOQUEIA** |
| `AC-1` razão `≫ 2` | há outra coisa no mumax3; **`A007` segue bloqueada** e vira investigação |
| `AC-2` `v_∥ ≈ 0.9` | **`H_comum`**: o artefato é de discretização. `L9.1` ganha apoio |
| `AC-2` `v_∥ ≈ 0` | **`H_nosso`** — achado grave, tocaria o `C-8` |
| `AC-3` `l` sobe | a ressalva do `C-15` **resolve-se**; o acordo do `A003` era melhor que o medido |
| `AC-3` `l` estável | os `−0.30 %` são **diferença real de código**; a ressalva cai e o `C-15` fica **mais forte** |
| `AC-3` `l` desce | a explicação de convergência está **errada**; achado |

## 7. Limites
- **O `C-15` não é revogado** por esta missão, aconteça o que acontecer. Os `−0.30 %` estão
  medidos; o que muda é a **leitura**.
- A inicialização segue a mesma nos dois códigos (`L15.3`).
- Um ângulo por corrida, 20 ns, malha de 1 nm, `α = 0.02`, um ponto de parâmetros.
- mumax3 é float32; `saf.cu` é double. Uma tolerância de `1e−6 T` pode estar perto do piso do
  float32 — **se estiver, o `AC-0` vai mostrar**, e isso é informação, não fracasso.
- `L-G` intocado.

## 8. Provenance
`LAB/EVIDENCE/A005R/`. Reusa `ovf.py` e o estimador cego, ambos selados. **Nenhum arquivo de
outra missão é reescrito.**

## 9. Gate
`G-A005R` = `AC-0` (casado ou casamento parcial quantificado) ∧ `AC-1` ∧ `AC-2` ∧ `AC-3`,
cada um **com veredito**. **Passar o gate não é aceite.**
