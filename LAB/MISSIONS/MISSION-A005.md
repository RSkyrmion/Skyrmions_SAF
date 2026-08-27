# MISSION-A005 — `L9.1`/`L8.4`: o artefato de rede aparece no mumax3?

Estado: **`AUTHORIZED`** por `WRITEBACK-024` · Data: 2026-08-27
Regime: auditoria por ferramenta independente. **E primeiro degrau da dinâmica do mumax3.**

> **Pré-registro.** Escrito antes de qualquer corrida. Submetido à leitura de Rodrigo antes da
> execução (`CLAUDE.md` §2).

## 1. A pergunta
O `E003` mediu, **sem excitação alguma**, deriva de `0.91745 cm/s` **ao longo da ligação**
quando o par é inicializado fora dos eixos da malha (`θ = 30°`), **constante** e não decadente.
O `I001` provou que é **movimento real e rígido**, não viés do rastreador. O `I002` mostrou que
é **hipersensível ao estado** (3.2 % de tamanho ⇒ 41 % em `v_∥`), e a causa (`L9.1`) segue
conjectural: força de rede tipo Peierls virando deriva giroscópica.

**A pergunta:** um segundo código, com discretização e integrador próprios, mostra o mesmo?

## 2. As duas hipóteses
- **`H_comum`** — é física de **discretização**, comum a qualquer malha quadrada neste
  `Γ = G/α𝒟̄`. Predição: `v_∥(mumax3) ≈ 0.9 cm/s`, ao longo da ligação.
- **`H_nosso`** — é peculiaridade da **nossa** implementação (estêncil, RK4 de passo fixo,
  relaxação que não converge fora do eixo). Predição: `v_∥(mumax3) ≈ 0`.

Duas previsões **diferentes da mesma grandeza**, em instrumentos diferentes. Sem limiar.

**Poder, medido:** no `E003` o `v_∥` variou `0.06 %` ao longo de 20 ns; as hipóteses distam
**100 %**. Margem ~1600×.

## 3. Esta missão é também o PRIMEIRO DEGRAU da dinâmica do mumax3
É o uso mais simples da LLG dele: **sem excitação**. Se o mumax3 não mantiver estático um
estado que deveria ser estático, a `A007` está em risco **antes de começar**. Por isso vem antes.

### `AR-0` — pré-teste: o mumax3 preserva o estado relaxado?
Relaxar **no eixo** (`θ = 0°`, comensurável, onde o `E003` mediu `7.1e−5 cm/s` — desprezível)
e rodar 20 ns de LLG com `α = 0.02`, sem excitação.
**PASSA se `|v| < 0.05 cm/s`** (menos de 5 % da grandeza em disputa).
**Se falhar, a `A005` para e a `A007` fica bloqueada.** É a lição do `relax()` do `A003`.

### `AR-0.1` — convergência da relaxação fora do eixo
`relax()` **e** `minimize()`, `maxTorque` registrado, `minimize()` repetido até estabilizar —
obrigatório desde o `A003` (`CLAUDE.md` §8).

## 4. Critério primário `AR-1`
`θ = 30°`, sem excitação, `α = 0.02`, 20 ns. Posição do par por CTC (Berg–Lüscher) sobre
estados salvos a cada 1 ns; `v` por ajuste linear; decomposição no referencial da ligação.

| | previsão para `\|v_∥\|` |
|---|---|
| **`H_comum`** | `≈ 0.9 cm/s` |
| **`H_nosso`** | `≈ 0` |

Reporto `v_∥`, `v_⊥` e o ângulo em relação à ligação. No `E003` a deriva estava a `+0.14°` da
ligação. Se o mumax3 der magnitude parecida em **outra direção**, é terceiro desfecho e será
relatado sem forçar escolha.

## 5. Taxonomia de falha
| resultado | significado, decidido antes |
|---|---|
| `AR-0` falha | mumax3 não preserva estado estático; **`A005` para, `A007` bloqueada** |
| `v_∥ ≈ 0.9`, ao longo da ligação | **`H_comum`**: artefato de discretização, não nosso. `L9.1` ganha apoio; **não fecha** a causa |
| `v_∥ ≈ 0` | **`H_nosso`**: é da nossa implementação. **Achado grave** — tocaria o `C-8`, cuja contaminação de `7.7°` foi explicada por ele |
| magnitude parecida, direção outra | terceiro desfecho; relatar sem escolher |

## 6. Limites
- **Não fecha o `L9.1`** nem o `L8.4`. Mede uma **consequência** em segundo código.
- mumax3 é **float32** com **passo adaptativo**; o `saf.cu` é double com RK4 fixo. Diferença
  pode vir daí, e isso é parte do que se mede.
- Um ângulo, um acoplamento, 20 ns, malha de 1 nm. `L-G` intocado.

## 7. Provenance
`LAB/EVIDENCE/A005/` — `.mx3`, `.ovf`, log as-run, hash do binário. Reusa o `ovf.py` selado.
**Nenhum arquivo de outra missão é reescrito.**

## 8. Gate
`G-A005` = `AR-0` ∧ `AR-0.1` ∧ `AR-1` com veredito. **Passar o gate não é aceite.**
