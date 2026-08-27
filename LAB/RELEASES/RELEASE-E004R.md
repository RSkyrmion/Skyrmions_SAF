# RELEASE-E004R — `RF-3` fecha o `L5.3`; o `RF-1` fica sem veredito pelo MESMO erro meu

Missão: `MISSION-E004R` · Autorizada por `WRITEBACK-015` · Execução: 2026-08-26, 06:55–12:02
`human_acceptance: PENDING` · Evidência: `LAB/EVIDENCE/E004R/`

## 1. Veredito
- **`RF-3` PASSOU e fecha o `L5.3`** — limite aberto desde o `AUDIT-002`.
- **`RF-2` entregou** `f_SBM = 17.9609 ± 0.0125 GHz`, e mostrou que o `18.00` do `E001` era um
  **bin**, não uma linha.
- **`RF-0` reprovou 3 das 5 frequências ⇒ `RF-1` SEM VEREDITO.**
- **`RF-4` INVÁLIDO** — o par se desligou na malha fina.
- **Gate `G-E004R` NÃO passou** (exige `RF-1` com veredito).

**A revisão não respondeu a pergunta que ela existia para responder.**

## 2. `RF-3` — a régua na travessia da fronteira periódica (`L5.3`)
| | `l` | `Q₁` / `Q₂` | relaxação |
|---|---|---|---|
| par no centro | `10.960705784 nm` | `−1.000000` / `+1.000000` | 189 825 it, `1.0e−6 T`, convergiu |
| par **na fronteira** (`x = 0`) | `10.960705637 nm` | `−1.000000` / `+1.000000` | 189 850 it, `1.0e−6 T`, convergiu |

`|Δl| = 1.47e−7 nm`, critério `< 1e−3`. **PASSOU.**
O `L5.3` do `C-5` — *"o comportamento sob travessia da fronteira periódica não foi testado em
nenhum dos dois códigos"* — **fecha para o meu código**. Continua não testado para o estimador
cego do `AUDIT-002`, que não foi reexecutado aqui.

## 3. `RF-2` — a ressonância de breathing, remedida
Janela de 40 ns, resolução `0.025 GHz` (4× melhor que o `E001`):
**`f_SBM = 17.9609 GHz`** (centroide acima de meia altura), pico em `17.9491`, FWHM `0.65 GHz`,
`σ(f_SBM) = 0.0125 GHz`.

**O `18.00 GHz` do `E001` era um bin de resolução `0.1 GHz`.** O `L6.2` já registrava que
aquele acerto contra o "18" do artigo era "mais bonito do que é forte"; agora está medido:
`17.96`. Isso **não** contradiz o artigo (que cita valor redondo em texto corrido), mas
**refina `C-6`** e deve viajar junto com ele daqui em diante.

## 4. `RF-0` reprovou — e o defeito é a TERCEIRA repetição do mesmo erro

| `f` [GHz] | `v` 150–225 ns | `v` 225–300 ns | `\|razão−1\|` | critério < 1 % |
|---|---|---|---|---|
| 17.00 | 1.16351 | 1.14790 | 1.342 % | **FALHOU** |
| 17.50 | 2.94251 | 2.87532 | 2.283 % | **FALHOU** |
| 17.75 | 3.76173 | 3.70388 | 1.538 % | **FALHOU** |
| 18.00 | 3.52654 | 3.49936 | 0.771 % | passou |
| 18.25 | 2.81475 | 2.79791 | 0.598 % | passou |

Duas de cinco. O §4 exige ≥ 3 ⇒ **`RF-1` sem veredito**, e o gate cai.

### O defeito, nomeado sem atenuação
**O `RF-0` checa a convergência da grandeza ERRADA.** Ele exige que cada `v_⊥` esteja
estacionária — a **entrada** — quando o que decide o `RF-1` é a **posição do pico**, a saída.

Isto é **exatamente** o erro que o `RELEASE-E003-ADDENDUM-001` diagnosticou e corrigiu:
*"você respondeu com o offset, que não converge, e nunca checou se a inclinação converge —
a única versão da pergunta que fala do critério de fato usado."* Eu escrevi aquele adendo, e
**repeti o erro na missão seguinte**. É a terceira ocorrência da mesma família (o `EF-0` do
`E004` foi a segunda) e a nona desta linha de trabalho.

Agravante: o próprio limiar de `1 %` foi escolhido **sem medida que o sustentasse** — o mesmo
vício dos `PV-0`, `PV-1` e `EF-0`.

## 5. O que o dado mostra — EXPLORATÓRIO, e explicitamente NÃO é o `RF-1`
Registro os números porque escondê-los seria pior, e com a etiqueta que eles merecem.

Aplicando a checagem que eu **deveria** ter pré-registrado — convergência de `f_pico`:

| janela | `f_pico` |
|---|---|
| 150–225 ns | `17.8192 GHz` |
| 225–300 ns | `17.8255 GHz` |

**Diferença de `6.3 MHz`**, enquanto as velocidades individuais se movem `0.6–2.3 %`.
`σ(f_pico) = 0.0118 GHz` por Monte Carlo com `σ_rel = 1.31 %` (a escala de ruído genuína do
`RF-0.1`; no `E004` a mesma quantidade dava `129.5 %` porque media o transiente).

Com isso, `|f_pico − f_SBM| = 0.1354 GHz` contra `2σ_comb = 0.0344` — **7.9 σ**.

**ISTO NÃO É O `RF-1`, E NÃO PODE SER CITADO COMO SE FOSSE.** O critério pré-registrado
está sem veredito, e nenhum número calculado depois de ver o dado o substitui. É a mesma
disciplina que manteve a leitura R2 do `PV-0` como hipótese e recusou `l(140) = 10.9566`.

Registro também que o `f_pico` **se deslocou** de `17.7642` (100 ns, `E004`) para `17.8255`
(300 ns): `61 MHz`. A predição do §4 do pré-registro era que um deslocamento material
significaria contaminação transiente no número do `E004` — e `61 MHz` é maior que os `29 MHz`
de convergência entre janelas que o `E004` reportava.

## 6. `RF-4` — inválido, não "aumentou 1600×"
Na malha de `0.5 nm` o par **desligou-se**: `l` foi de `10.848` a `28.466 nm` e o par percorreu
`295 nm` numa caixa de `100`. `Q` permaneceu `∓1`, então os skyrmions sobreviveram, mas o
estado ligado não. **Comparar deriva espúria entre um par ligado e um par desfeito não mede
nada**, e o número bruto (`1489 cm/s`) não é relatável como resultado.

Causa candidata **não verificada**: o passo de tempo. `B₀ = 2A/(M_s a²)` vai de `51.7` para
`206.9 T` ao refinar de 1 para 0.5 nm, e os `10 fs` que servem a 1 nm ficam marginais. **Eu não
escalei `dt` com a malha e não pré-registrei checagem de preservação de estado** — oitavo
defeito de desenho. O `RF-4` era exploratório e não gateia nada.

Deliberadamente **não refiz** a corrida com `dt` corrigido: escolher `dt` depois de ver o
resultado é decisão que merece ser explícita, e o teste que decidiria (2 ns a 0.5 nm com
`dt = 2.5 fs`, ~7 min) fica **proposto, não executado**.

## 7. Gate
`G-E004R = RF-0(≥3) ∧ RF-2 ∧ RF-1 com veredito` → **NÃO PASSOU**.
Ao menos o gate desta vez **exigia** veredito do critério primário — o defeito do `G-E004`,
que passava sem resposta, estava corrigido. O gate funcionou: ele reprovou uma missão que não
respondeu.

## 8. Limites
- **`L-G` intocado.** Nona missão, nenhuma verificação independente do número.
- `RF-1` sem veredito: **a afirmação do artigo sobre `v_sp` ter pico na ressonância do modo
  segue NÃO TESTADA** neste laboratório, agora por duas missões seguidas.
- `L5.3` fecha **só para o meu código**.
- `RF-4` inválido; a causa do artefato de comensurabilidade segue sem teste.
- Um `α`, uma amplitude, um acoplamento, um modo, cinco frequências.
- `D-1`/`D-2`/`D-3` intocadas — dependem dos autores.

## 9. Custo
`RF-3` 11 s · `RF-2` 431 s · `RF-4` 993 + 276 s · varredura 5 × ~3335 s. Total ≈ 5,1 h.

## 10. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar.
