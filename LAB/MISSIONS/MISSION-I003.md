# MISSION-I003 — o par se desligou na malha fina por causa do PASSO DE TEMPO?

Estado: **`AUTHORIZED`** por `WRITEBACK-017` · Data: 2026-08-26
Regime: diagnóstico numérico. Fecha (ou não) o `RF-4` inválido do `E004R`.

> **Pré-registro.** Escrito antes de qualquer corrida. **Primeiro pré-registro submetido à
> revisão de Rodrigo antes da execução**, sob a regra do `CLAUDE.md` §2 adotada hoje.

## 1. O fato
No `RF-4` do `E004R`, a corrida de controle em malha de `0.5 nm` **desligou o par**: `l` foi de
`10.848` a `28.466 nm` e o par percorreu `295 nm` numa caixa de `100`. `Q` permaneceu `∓1`.
A corrida usou `dt = 10 fs`, o mesmo da malha de `1 nm`.

## 2. As duas hipóteses
- **`H_dt`** — é o **passo de tempo**. `B₀ = 2A/(M_s a²)` vai de `51.7` para `206.9 T` ao
  refinar de `1.0` para `0.5 nm`; a precessão mais rápida quadruplica, e `10 fs` deixa de
  resolver. Predição: com `dt` escalado por `a²` (`2.5 fs`), o par **permanece ligado**.
- **`H_física`** — a `0.5 nm` o estado ligado não existe, ou é instável sob LLG. Predição: o
  par se desliga **também** com `dt = 2.5 fs`.

## 3. Critério primário `ID-1` — comparação, mesmo instrumento (`R1`)
Mesma malha (`0.5 nm`), mesmo estado inicial, mesma janela: **`dt = 10 fs` contra `dt = 2.5 fs`**.
Grandeza: `l` ao fim de **4 ns**.

| | previsão para `l(4 ns)` a `dt = 2.5 fs` |
|---|---|
| **`H_dt`** | `≈ 10.85 nm` — permanece no valor de equilíbrio |
| **`H_física`** | cresce sem parar, como a `10 fs` |

**Sem limiar absoluto.** As duas hipóteses preveem comportamentos qualitativamente diferentes
da mesma grandeza medida do mesmo jeito. A referência `10 fs` é **remedida aqui**, na janela de
4 ns, para a comparação ser casada — não importada do `E004R`.

**Checagem de poder:** no `E004R` a `10 fs` o `l` já havia saído de `10.85` para além de
`11 nm` bem dentro dos primeiros nanossegundos (chegou a `28.47` em 20 ns). Quatro
nanossegundos bastam para separar "ficou em 10.85" de "disparou". Se em 4 ns **nenhuma** das
duas se mover, a janela foi curta demais e o `ID-1` é **INDETERMINADO** — declarado agora.

## 4. `ID-0` — controle de sanidade (`R2`: na grandeza que o critério consome)
`max‖m‖−1 < 1e−9` nas duas corridas, e `|Q| = 1.0000` no início. Se a norma degradar, o
problema é de integração e não se lê `l` como física.

## 5. Taxonomia
| resultado | significado, decidido antes |
|---|---|
| `l ≈ 10.85` a 2.5 fs, dispara a 10 fs | **`H_dt`**. O `RF-4` do `E004R` foi **erro meu de passo de tempo**, e o artefato de comensurabilidade **pode** ser remedido em malha fina — em missão própria |
| dispara nas duas | **`H_física`** — o estado ligado não sobrevive a `0.5 nm` sob LLG. Isso seria **grave**: tocaria a convergência de malha (`L1.1`) e mereceria missão própria |
| nenhuma se move em 4 ns | INDETERMINADO; janela curta |

## 6. Limites
- **Não** mede a deriva espúria em malha fina — isso era o `RF-4`, e continua **não medido**.
- Um ângulo (`θ = 30°`), um acoplamento, 4 ns.
- **`L-G` intocado.**

## 7. Provenance
Reusa o `saf_prop4r` **selado** do `E004R`? **Não** — os caminhos de escrita dele apontam para
`E004R/`. Derivar `LAB/EVIDENCE/I003/saf_dt.cu`, redirecionar, verificar por `grep`. §4 do
`CLAUDE.md`; a cicatriz é o `R001`.

## 8. Custo
`0.5 nm` custa `49.6 s/ns` a `dt = 10 fs` (medido no `E004R`). Duas corridas de 4 ns:
`~200 s` + `~800 s` (a de 2.5 fs é 4× mais cara) ≈ **17 min**, mais duas relaxações.

## 9. Gate
`G-I003` = `ID-0` ∧ `ID-1` com veredito. **Passar o gate não é aceite.**
