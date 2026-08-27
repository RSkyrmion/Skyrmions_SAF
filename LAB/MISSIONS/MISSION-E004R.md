# MISSION-E004R — revisão do `E004`: responder o `EF-1` e fechar o que dá para fechar

Estado: **`AUTHORIZED`** por `WRITEBACK-015` · Data: 2026-08-26
Regime: revisão. Completa `MISSION-E004`, que está `REVISION_REQUESTED`.

> **Pré-registro.** Escrito antes de qualquer corrida nova.

## 1. O que deu errado no `E004`, em uma linha
O `EF-0` usou como escala de ruído a **dispersão entre janelas**, que na verdade mede o
**decaimento transiente** — sistemático e comum às nove frequências (razão `0.44` em todas).
Uma curva com fator 7 de contraste foi declarada plana.

## 2. A correção de desenho: eliminar a causa, não trocar o limiar
Trocar `5×` por outro número seria repetir a família de erros. **A causa é o transiente.**
Esta revisão o **elimina**: corridas de **300 ns**, longas o bastante para o sistema estar
estacionário, e então a comparação entre janelas volta a ser o que eu queria que fosse — uma
medida de **ruído**, não de transiente.

Base do 300 ns, medida e não suposta: o `RELEASE-E002-ADDENDUM-001` mediu decaimento
geométrico de razão `0.358` por janela de 25 ns, isto é `τ ≈ 24 ns`. Aos 200 ns restavam
`0.66 %`; aos 300 ns restam `~0.01 %`. **Isto fecha o `L7.3` de passagem.**

## 3. Frequências e corridas
`17.00, 17.50, 17.75, 18.00, 18.25 GHz` — **cinco pontos a 300 ns**, cercando com folga o
`f_pico = 17.78` que o `E004` viu a 100 ns. O máximo fica no interior, e a parábola de três
pontos fica bem determinada.

Ponto de operação idêntico: `θ = 0°`, SBM, `ΔK/K₀ = 0.005`, `α = 0.02`, acoplamento fraco,
malha de 1 nm, caixa de 100 nm, PBC, `T = 0`.

**O dado de 100 ns do `E004` NÃO é reanalisado como se fosse novo.** Eu já o vi; qualquer
critério aplicado a ele deixou de ser cego. Ele entra apenas como **predição a ser testada**
(§4, `RF-1`).

## 4. Critérios pré-registrados

### `RF-0` — o estado é estacionário? (pré-teste, por frequência)
Em cada uma das cinco corridas, comparar `v_⊥` nas janelas `150–225 ns` e `225–300 ns`.
**PASSA naquela frequência se `|v(225–300)/v(150–225) − 1| < 1 %`.**
Frequências que não passarem são **excluídas** do ajuste e relatadas como não estacionárias.
Se **menos de três** frequências passarem, não há parábola e a missão relata isso sem veredito.

### `RF-0.1` — a escala de ruído, agora medida de verdade
Com o sistema estacionário, o desvio `|v(225–300)/v(150–225) − 1|` de cada frequência é
**ruído genuíno**. A escala de ruído `σ_rel` é a **média** desses cinco desvios.
Ela é medida **depois** das corridas mas **antes** de qualquer julgamento — e, ao contrário do
`E004`, não há escolha: a definição está fixada aqui.

### `RF-1` — PRIMÁRIO: o pico coincide com a ressonância do modo?
`f_pico` por ajuste parabólico dos três pontos em torno do máximo, na janela `225–300 ns`.
`σ(f_pico)` por propagação Monte Carlo de `σ_rel` (semente fixada: `20260826`).

**Tem veredito somente se `σ(f_pico) < 0.10 GHz`.** (Mais apertado que os `0.25` do `E004`:
a diferença a resolver é `17.78` vs `18.00`, ou seja `0.22 GHz`, e um `σ` de `0.25` não a
separa. Esta é a lição do `A2` aplicada com a conta feita.)

**Com veredito:**
- `|f_pico − f_SBM| ≤ 2σ_combinado` → **o pico coincide** com a ressonância do modo; a
  afirmação do artigo sobrevive.
- `|f_pico − f_SBM| > 2σ_combinado` → **discrepância real**: nesta implementação a
  autopropulsão tem pico **deslocado** da ressonância de breathing. Relatar assim, sem resgate.

`σ_combinado = √(σ(f_pico)² + σ(f_SBM)²)`, com `f_SBM` e seu erro vindos do `RF-2`.

### `RF-2` — a ressonância de breathing, remedida com precisão suficiente
O `E001` deu `18.00 GHz` com resolução de `0.1 GHz` (janela sinc de 10 ns). **Isso não basta**
para julgar uma diferença de `0.22 GHz` — seria comparar contra uma régua de resolução
comparável ao efeito.
Repetir o `ev3` do `E001` com janela de **40 ns** ⇒ resolução `0.025 GHz`, quatro vezes melhor.
`f_SBM` = centroide dos bins acima de meia altura; `σ(f_SBM)` = meia resolução, `0.0125 GHz`.

**Predição registrada:** o `E004` a 100 ns deu `f_pico = 17.78`. Se `RF-1` a 300 ns devolver
algo materialmente diferente, o número do `E004` estava contaminado pelo transiente — e isso
**é resultado**, não conserto.

### `RF-3` — `L5.3`: a régua sob travessia da fronteira periódica
Nunca testada em nenhuma missão; o `AUDIT-002` a declarou explicitamente fora do escopo.
Relaxar o par **centrado na fronteira** (deslocado de meia caixa em `x`) e comparar `l` e `Q`
com os do par centrado.
**PASSA se** `|Δl| < 0.001 nm` e `|Q| = 1.0000` nos dois. Falha ⇒ **a régua tem um buraco** e
isso vira limite grave, retroativo a tudo que usou posição.

### `RF-4` — `L9.1` parcial: o artefato de comensurabilidade é força de rede?
Predição: se a deriva espúria fora do eixo é **força de rede**, ela deve **cair fortemente**
com o refino da malha; se for de outra origem, não.
Repetir o controle do `E003` (`θ = 30°`, sem excitação) com malha de **0.5 nm**.
**Exploratório, sem limiar:** relatar o fator de redução. Uma queda de ordem de grandeza apoia
"força de rede"; uma queda pequena a refuta. **Não fecha a causa** — mede uma consequência.

## 5. Taxonomia de falha
| resultado | significado, decidido antes |
|---|---|
| `RF-0` reprova ≥3 frequências | sem parábola; missão relata "não estacionário a 300 ns" e para |
| `σ(f_pico) ≥ 0.10 GHz` | `RF-1` **INDETERMINADO** de novo, e desta vez com a escala de ruído correta — o que significaria que **5 pontos não bastam**, não que o critério está errado |
| pico coincide | afirmação do artigo **sobrevive** a um teste que podia refutá-la |
| pico deslocado | **discrepância real**, e ela ganha apoio independente do `EP-3` do `E002`, que viu o mesmo sentido no ABM |
| `RF-3` falha | buraco na régua; **limite grave e retroativo** |

## 6. O que esta missão NÃO resolve — declarado agora
- **`L-G`**: exige ação de sistema ou externa. Nenhuma autorizada. **Continua acima de tudo.**
- **`D-1`/`D-2`/`D-3`**: dependem dos autores; ação de Rodrigo.
- **`L8.4`**: os 10 % (`0.8°`) do `E003` seguem sem explicação.
- **`L2.3`** e **`L1.1`**: outras físicas, missões próprias.
- A **causa** do artefato de comensurabilidade: o `RF-4` mede consequência, não causa.

## 7. Provenance
Reusa `LAB/EVIDENCE/E004/saf_prop4` — **não**: os caminhos dele apontam para `E004/`. Derivar
`LAB/EVIDENCE/E004R/saf_prop4r.cu`, redirecionar, verificar por `grep`. Regra §4 do
`CLAUDE.md`; a cicatriz é o `R001`.

## 8. Custo estimado, antes de comprometer
5 × 300 ns a `11.15 s/ns` ≈ **4,6 h**; `RF-2` (40 ns) ≈ 8 min; `RF-3` ≈ 10 min;
`RF-4` (malha 0.5 nm) ≈ 30 min. **Total ≈ 5,4 h.**

## 9. Gate
`G-E004R` = `RF-0` (≥3 frequências) ∧ `RF-2` medido ∧ **`RF-1` com veredito**.
Ao contrário do `G-E004`, **este gate exige que o critério primário tenha veredito** — o
defeito do gate anterior, registrado no `RELEASE-E004.md` §5, está corrigido aqui.
**Passar o gate não é aceite.**
