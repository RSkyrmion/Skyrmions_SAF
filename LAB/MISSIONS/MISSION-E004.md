# MISSION-E004 — `v_sp(f)`: a autopropulsão tem pico na ressonância do modo?

Estado: **`AUTHORIZED`** por `WRITEBACK-013` · Data: 2026-08-25
Regime: extensão controlada · Fig. 3 do artigo

> **Pré-registro.** Escrito antes de qualquer corrida.

## 1. A afirmação testada
O artigo: *"vsp peaks at the resonance frequency of the corresponding breathing mode"*.
Isto é uma predição **quantitativa e falsificável** contra um número que **este laboratório já
mediu de forma independente da autopropulsão**: o `E001` pôs a ressonância de breathing SBM em
**18.00 GHz** (janela de 10 ns, resolução 0.1 GHz).

**Ela pode falhar.** O `EP-3` do `E002` já mostrou que a autopropulsão ABM é **plana a 0,77 %**
entre 19.24 e 19.40 GHz, o que não sustentou 19.40 como pico. Se `v_sp(f)` for plana ou tiver
pico deslocado no SBM, a afirmação do artigo não se reproduz aqui.

## 2. Ponto de operação e varredura
Idêntico ao `E002`/`E003`: `A_int = 0.02`, `K₀ = 0.6`, `α = 0.02`, `ΔK/K₀ = 0.005`, `T = 0`,
malha de 1 nm, caixa de 100 nm, PBC, **`θ_bond = 0°`**.

**`θ = 0°` é deliberado:** o `E003` mostrou que fora do eixo há artefato de comensurabilidade
(deriva espúria constante de `0.9 cm/s`, relaxação que não converge). A `θ = 0` a deriva
espúria decai para `7.1e−5 cm/s`. A varredura roda no ângulo **limpo**.

**Frequências (9 pontos, fixadas agora):**
`16.5, 17.0, 17.5, 17.75, 18.00, 18.25, 18.5, 19.0, 19.5 GHz`.
Espaçamento de `0.25 GHz` no núcleo e `0.5` nas asas. O ponto de `18.00 GHz` **já existe**
(`EVIDENCE/E002/prop_sbm_18.00GHz.dat`) e é reaproveitado na janela casada — 8 corridas novas.

## 3. O defeito que eu preciso evitar, e como
**O sistema não estaciona.** O `L7.3` registra que a `v_⊥` do SBM ainda decaía aos 200 ns.
Comparar `v_⊥` entre frequências numa janela fixa **confunde a resposta estacionária com o
transiente**, que pode ter constante de tempo diferente fora da ressonância. Ignorar isso seria
repetir a família de erros do `E002`.

**Mitigação pré-registrada:** a grandeza reportada **não é** `v_sp` absoluta, e sim a
**posição do pico** `f_pico` de `v_⊥(f)`. E ela é medida em **duas janelas independentes**,
`25–50 ns` e `50–100 ns`.
- Se `f_pico` for a mesma nas duas (a menos de meio passo, `0.125 GHz`), o transiente **não
  desloca o pico**, e `f_pico` é a grandeza reportada.
- Se diferirem por mais que isso, **`f_pico` é declarada não convergida**, a missão relata
  isso, e **as corridas NÃO são estendidas** — estender após ver o dado é escolher a janela
  pelo resultado (§6 do `E003`, defeito do `R002`).

É a mesma lição do `E003`: **checar a convergência da grandeza discriminante**, não de outra.

## 4. Critérios

### `EF-1` — PRIMÁRIO: o pico coincide com a ressonância do modo
`f_pico` de `v_⊥(f)`, por ajuste parabólico dos três pontos em torno do máximo.
**PASSA se `|f_pico − 18.00 GHz| ≤ 0.25 GHz`**, isto é um passo de grade.

**Checagem de poder, com a conta explícita — e desta vez conferida contra medida.**
No `E002` eu inflei uma banda por estimar mal a sensibilidade à dessintonia (errei por fator
~30). Aqui a estimativa é **calibrada pelo dado que já tenho**: a autopropulsão ABM caiu
`0.77 %` sob dessintonia de `0.16 GHz`. Extrapolando quadraticamente, `0.25 GHz` de dessintonia
custa ~`1.9 %` — **da ordem da variação que o ajuste parabólico precisa resolver.**
Consequência declarada: se a curva for **plana** neste intervalo, o ajuste parabólico **não
localiza pico algum**, e o `EF-1` fica **indeterminado, não aprovado**. A regra de morte está
no `EF-0`.

### `EF-0` — checagem de poder MEDIDA, antes de julgar o `EF-1`
Contraste da curva: `(v_max − v_min)/v_max` nos 9 pontos.
**Se o contraste for menor que `5 %`**, a curva é plana demais para o ajuste parabólico
significar coisa alguma, e **`EF-1` é declarado indeterminado** — não aprovado, não reprovado.
`5 %` porque a dispersão entre janelas do `E002`/`E003` na mesma quantidade é da ordem de 1 %,
logo abaixo de 5× isso o pico não se distingue de ruído de transiente.

### `EF-2` — SECUNDÁRIO: largura
FWHM da curva `v_⊥(f)`, comparada com a FWHM do espectro de breathing SBM do `E001`.
**Exploratório, sem banda:** o artigo não tabela largura para este ponto de operação.
Se `EF-0` declarar a curva plana, `EF-2` **não é medido**.

### `EF-3` — SECUNDÁRIO: o `EP-3` do `E002`, refeito com estatística
A varredura contém a resposta à pergunta que o `EP-3` falhou em responder com dois pontos.
Reportar a curva inteira. **Sem critério** — é o remédio para uma falha registrada, não um
teste novo.

## 5. Taxonomia de falha
| resultado | significado, decidido antes |
|---|---|
| `EF-0` < 5 % de contraste | curva plana; **`EF-1` indeterminado**. A afirmação do artigo **não é testável aqui** com este `α` e esta amplitude. É resultado, não fracasso |
| `f_pico` difere entre janelas | **não convergida**; sem veredito; **não estender** |
| `f_pico` dentro de 0.25 GHz de 18.00 | a afirmação do artigo **sobrevive** a um teste que podia refutá-la |
| `f_pico` fora | **discrepância real** entre a minha ressonância de breathing e a minha ressonância de autopropulsão. Relatar assim, sem resgate |

## 6. Limites que já viajam junto
- **`L-G` intocado.** Nada aqui é verificação independente.
- Um `α`, uma amplitude, um acoplamento, um modo (SBM). A Fig. 3 do artigo varre amplitudes e
  usa `α = 0.1`; **isto não é a Fig. 3**, é um corte dela.
- `v_⊥` absoluta continua **não estacionária** (`L7.3`); só a **posição do pico** é reportada.
- A ressonância de referência (18.00 GHz) é **minha**, do `E001`, com resolução de 0.1 GHz, e
  o `L6.2` já registra que "18" no artigo é valor redondo do texto corrido.

## 7. Provenance
Reusa `LAB/EVIDENCE/E003/saf_prop3` **sem alteração** (a frequência já é argumento de linha de
comando e `θ = 0` é o default). **Mas os caminhos de escrita dele apontam para `E003/`.**
Por isso: derivar `LAB/EVIDENCE/E004/saf_prop4.cu`, redirecionar, verificar por `grep`, e
**nunca** rodar o binário do `E003` para gerar dado do `E004` — é exatamente a regra §4 do
`CLAUDE.md`, e a cicatriz é o `R001`.

## 8. Gate
`G-E004` = (`EF-0` medido) ∧ (`f_pico` convergida entre janelas OU `EF-0` declarar plana).
Note que **`EF-1` indeterminado NÃO reprova o gate** — reprovaria a testabilidade da
afirmação. **Passar o gate não é aceite.**

---

# ADENDO-001 — 2026-08-25, escrito ANTES de qualquer corrida do `E004`

Rotulado e datado conforme `CLAUDE.md` §3. Corrige dois defeitos de desenho do texto acima,
**ambos detectados antes de existir qualquer dado do `E004`**.

## A1 — o piso de 5 % do `EF-0` era CIRCULAR
O §4 justifica o piso de contraste de 5 % assim: "a autopropulsão ABM caiu 0,77 % sob
dessintonia de 0,16 GHz". **Esse 0,77 % foi medido com o rastreador de CTC realimentado — o
mesmo instrumento que a `MISSION-I001` está testando neste momento.** Se o `IV-1` retornar
`C-tracker`, aquele número deixa de ser medida limpa de sensibilidade à dessintonia, e o piso
de 5 % fica sem a razão que o sustenta. Seria o erro do `E002` de novo: limiar cuja
justificativa evapora.

**O piso de 5 % fica SUSPENSO.** Em seu lugar, um critério **relativo**, calculado do próprio
dado do `E004`, sem importar número nenhum:

> **`EF-0` (revisto):** o contraste `(v_max − v_min)/v_max` da curva é comparado com a
> **dispersão entre janelas** (`25–50` vs `50–100 ns`) das mesmas 9 medidas, calculada dos
> mesmos arquivos. **Se o contraste não exceder `5×` essa dispersão medida, `EF-1` é declarado
> INDETERMINADO** — não aprovado, não reprovado.

O fator `5×` é razão sinal-ruído, não escala física importada: ele não depende de nenhum
número do `E002`, nem do rastreador, nem do artigo.

**Contingência registrada agora, para os dois desfechos do `I001`:**
- `IV-1 → C-real` (instrumento limpo): o `EF-0` revisto vale como escrito, e o `0.77 %` do
  `E002` volta a ser citável como contexto — **não** como limiar.
- `IV-1 → C-tracker`: o `EF-0` revisto **continua valendo sem alteração**, porque não usa
  aquele número. Mas então **toda medida de deriva deste laboratório fica sob suspeita**, e o
  `E004` passa a reportar `f_pico` com esse limite grudado.

## A2 — `EF-1` podia "passar" com um ajuste incapaz de distinguir 18,00 de 18,5
O ajuste parabólico de três pontos devolve **sempre** uma posição de pico, mesmo sobre uma
curva rasa. Com tolerância de `0.25 GHz` e diferenças ponto a ponto de 1–2 %, a **incerteza**
de `f_pico` pode facilmente exceder a própria tolerância — e aí "passou" não significa nada.

> **`EF-1` (revisto):** propagar a dispersão entre janelas de cada um dos três pontos do
> ajuste para uma incerteza `σ(f_pico)`. **`EF-1` só tem veredito se `σ(f_pico) < 0.25 GHz`.**
> Se `σ(f_pico) ≥ 0.25 GHz`, o resultado é **INDETERMINADO**, pela mesma razão do `EF-0`: o
> instrumento não separa as hipóteses.

## A3 — o que NÃO muda
Frequências, ponto de operação, `θ = 0°`, a regra de não estender corridas após ver o dado, a
taxonomia do §5 e o gate do §8 permanecem exatamente como escritos acima.
