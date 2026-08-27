# RELEASE-E004 — `v_sp(f)`: a curva existe e é fortemente ressonante; o critério primário, não

Missão: `MISSION-E004` (+ `ADENDO-001`) · Autorizada por `WRITEBACK-013`
Execução **não supervisionada** por `WRITEBACK-014` · 2026-08-25, 16:01–18:29
`human_acceptance: PENDING` · Evidência: `LAB/EVIDENCE/E004/`

## 1. Veredito em duas linhas
**Existe uma ressonância de autopropulsão, forte e limpa: contraste de 86 %, pico em
`17.78 GHz`, convergido entre janelas a `0.029 GHz`.**
**E o meu critério primário `EF-1` está INDETERMINADO** — por um defeito de desenho meu, o
sexto desta linha de trabalho e da mesma família dos outros cinco.

## 2. A curva medida (as 9 frequências, `θ = 0°`, SBM, `ΔK/K₀ = 0.005`, `α = 0.02`)

| `f` [GHz] | `v_⊥` 25–50 ns | `v_⊥` 50–100 ns |
|---|---|---|
| 16.50 | 2.38432 | 0.99876 |
| 17.00 | 4.94765 | 2.14465 |
| 17.50 | 12.56961 | 5.76662 |
| **17.75** | **16.18337** | **7.09631** |
| 18.00 | 14.42991 | 6.03852 |
| 18.25 | 10.91722 | 4.59667 |
| 18.50 | 7.80953 | 3.36051 |
| 19.00 | 3.95357 | 1.76925 |
| 19.50 | 2.20086 | 1.01133 |

Fator **7** entre o pico e as asas. O ponto de 18.00 GHz vem do `E002`, mesma condição e mesma
janela — 8 corridas novas.

## 3. `EF-0` falhou como escrito, e a falha é minha
O `ADENDO-001 A1` definiu: contraste comparado com a **dispersão entre janelas**, e se o
contraste não exceder `5×` essa dispersão, `EF-1` fica indeterminado.

Medido: contraste `85.9 %`, "dispersão" `129.5 %`, razão **`0.66×`** → **`EF-1` INDETERMINADO**.

**Uma curva com fator 7 de contraste foi declarada plana.** Isso é absurdo na cara, e o
absurdo é do critério, não do dado.

### Diagnóstico — e ele NÃO repara o critério
A "dispersão entre janelas" que eu escolhi mede o **decaimento transiente**, que é sistemático
e **comum às nove frequências**: a razão `v(50–100)/v(25–50)` vale

`0.4189 · 0.4335 · 0.4588 · 0.4385 · 0.4185 · 0.4210 · 0.4303 · 0.4475 · 0.4595`

média `0.4363`, desvio `0.0152` — **dispersão de forma de 3.5 %**. As duas janelas medem a
**mesma curva**, escalada por um fator quase constante. Uma escala de ruído de 130 % sobre um
sinal que varia por fator 7 não é escala de ruído: é o transiente que o `L7.3` já registrava,
e que eu deveria ter normalizado.

Com a dispersão **de forma** (3.5 %), a razão seria `24.7×`, muito acima do critério de `5×`.
**Isto está registrado como diagnóstico do meu defeito, e explicitamente NÃO é usado para
converter o `EF-1` em aprovado** — mesma disciplina com que a leitura R2 do `PV-0` ficou como
hipótese e nunca como resgate.

O `σ(f_pico) = 0.2906 GHz` que reprovou o `EF-1` pela cláusula `A2` foi propagado **da mesma
dispersão defeituosa**. Os dois caminhos de indeterminação têm a mesma causa única.

## 4. O que sobreviveu

### A posição do pico convergiu — e é a grandeza discriminante
Aplicando a lição do `E003` (checar a convergência **da grandeza que decide**):

| janela | máximo na grade | `f_pico` ajustado |
|---|---|---|
| 25–50 ns | 17.75 GHz | **17.7933 GHz** |
| 50–100 ns | 17.75 GHz | **17.7642 GHz** |

Diferença `0.0291 GHz`, contra o critério de `0.125` do §3. **CONVERGIDA.** O transiente
**não desloca o pico** — escala a curva inteira, como a §3 pré-registrou que era o risco.

### `EF-3` — o remédio ao `EP-3` do `E002`, e ele funcionou
O `EP-3` tentou localizar ressonância com **dois** pontos e falhou. A curva explica por quê:
os dois pontos do `EP-3` (19.24 e 19.40 GHz) estavam **ambos na vizinhança do pico**, onde a
curva é localmente quadrática e portanto quase plana. Diferirem por `0.77 %` é o esperado, não
uma anomalia. **A "anomalia" do `EP-3` fica explicada.**

### Observação exploratória: o pico da propulsão parece ficar ABAIXO do de breathing
`17.78 GHz` contra os **`18.00 GHz`** que o `E001` mediu para o breathing SBM — `0.22 GHz`
abaixo. E o `E002` viu o mesmo sinal no ABM: `v(19.24) > v(19.40)`, com o breathing em
`19.35–19.40`. **Dois modos, duas medidas independentes, o mesmo sentido.**

**Exploratório, e frágil por três razões:** o `EF-1` está indeterminado e não posso alegar
esta comparação como testada; o `18.00` do `E001` tem resolução de `0.1 GHz`; e a curva foi
medida em janela **não estacionária**. Se a diferença for real, ela é interessante — o artigo
afirma que `v_sp` tem pico **na** ressonância do modo. **Não decidido.**

## 5. Gate
`G-E004 = (EF-0 medido) ∧ (f_pico convergida OU EF-0 declarar plana)`.
**PASSOU** — e passou pelos **dois** ramos do OU, o que torna a passagem pouco informativa. O
gate foi mal desenhado: ele não exigia que o `EF-1` tivesse veredito, e por isso passa numa
missão cuja pergunta central ficou sem resposta. **Sétima observação de desenho**, registrada.

## 6. Limites
- **`EF-1` INDETERMINADO. Esta missão NÃO testou a afirmação do artigo** de que `v_sp` tem pico
  na ressonância do modo. Nenhuma frase deste release pode ser lida como tendo testado isso.
- **`L-G` intocado.** Meu código, meu equilíbrio, minha régua, minha ressonância de referência.
- `v_⊥` absoluta é de janela **não estacionária** (`L7.3`); só `f_pico` é grandeza reportável.
- Um `α`, uma amplitude, um acoplamento, um modo. **Não é a Fig. 3**, é um corte dela.
- A referência de 18.00 GHz é minha, do `E001`, resolução `0.1 GHz`, e o `L6.2` já registra
  que "18" no artigo é valor redondo de texto corrido.
- Não toca `D-1`/`D-2`/`D-3`.

## 7. Execução não supervisionada — o que foi feito para protegê-la
Lote destacado (`setsid`), sobreviveu ao logout. `analyze4.py` **escrito antes do lote** e
selado com ele: nenhuma escolha de análise foi feita depois de ver o dado — e é por isso que o
defeito do `EF-0` aparece aqui como falha registrada, em vez de ter sido silenciosamente
corrigido. `STATE.md` atualizado **antes** do fim das corridas, com instruções de retomada a
frio. Provenance verificada por `grep`: zero referências a outras missões.

## 8. Custo
8 corridas de 100 ns, `1110–1180 s` cada. Total ≈ 2,5 h.

## 9. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar.
