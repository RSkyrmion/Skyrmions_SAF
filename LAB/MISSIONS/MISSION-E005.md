# MISSION-E005 — `Fig. S4(c)`: o pico de `v_sp` contra o alvo PUBLICADO

Estado: **`AUTHORIZED`** por `WRITEBACK-020` · Data: 2026-08-26
Regime: extensão controlada. Completa o que `E004` e `E004R` não responderam.

> **Pré-registro.** Escrito antes de qualquer código novo e de qualquer corrida.
> **Submetido à leitura de Rodrigo antes da execução** (`CLAUDE.md` §2).
> **Fonte varrida:** texto principal, End Matter **e suplementar inteiro** — foi a falta desta
> varredura que custou o `E004` e o `E004R`.

## 1. O alvo, que existe e eu não tinha visto
A **`Fig. S4(c)`** do suplementar é `v_sp` contra frequência para **SBM, acoplamento fraco
(`A_int = 0.02`, `K₀ = 0.6`), `α = 0.02`** — o nosso ponto exato — em três amplitudes
`ΔK/K₀ = 0.002, 0.004, 0.008`, com a linha de ressonância marcada em **18 GHz** e eixo de
14 a 23 GHz.

Lendo a figura: os picos das três curvas caem **à esquerda** da linha tracejada, e deslocam-se
**mais para a esquerda conforme a amplitude cresce**. Nós medimos `17.83` a `ΔK/K₀ = 0.005`.

## 2. A pergunta, na forma que funciona (`R1`)
Não "o meu pico bate com a minha ressonância?" — foi essa forma que morreu duas vezes.
A pergunta é: **o deslocamento do pico com a amplitude reproduz o do artigo?**

- **`H_amplitude`** — o pico é função da amplitude (amolecimento não-linear), e `f_pico(ΔK)`
  desce quando `ΔK` sobe, como na `Fig. S4(c)`.
- **`H_fixo`** — o pico não depende da amplitude; o deslocamento que li na figura é erro de
  leitura minha.

Duas previsões **diferentes da mesma grandeza** — o sinal e o tamanho de `df_pico/dΔK` —
medidas no mesmo instrumento. **Sem limiar absoluto.**

## 3. Corridas
`θ = 0°` (o ângulo comensurável, limpo — fora dele há o artefato do `E003`/`C-12`).
`dt = 10 fs` (malha de 1 nm; o `C-13` só obriga a escalar `dt` se a malha mudar, e não muda).

**Duas amplitudes: `ΔK/K₀ = 0.002` e `0.008`** — as extremas da figura, que maximizam o
contraste em `df_pico/dΔK`. Sete frequências cada:
`17.00, 17.25, 17.50, 17.75, 18.00, 18.25, 18.50 GHz`.
Janela de **300 ns** (o `RF-0` do `E004R` mostrou que 100 ns não basta), ajuste em `225–300`.
**14 corridas ≈ 13 h.**

O `ΔK/K₀ = 0.005` já medido (`E004R`) entra como **terceiro ponto**, não como alvo.

## 4. Critérios

### `RA-0` — convergência, checada na SAÍDA (`R2`)
`f_pico` de cada amplitude, comparado entre `150–225` e `225–300 ns`.
**PASSA se diferirem por `≤ 0.125 GHz`** (meio passo). Foi o erro do `RF-0` checar `v_⊥`, a
entrada; aqui é `f_pico`, que é o que o critério consome.
Amplitude que não convergir é **excluída** e relatada; **não se estende corrida** depois do dado.

### `RA-1` — PRIMÁRIO: o sinal e a escala de `df_pico/dΔK`
Com `f_pico(0.002)`, `f_pico(0.005)` e `f_pico(0.008)`:
- **`H_amplitude`** prevê `f_pico` **decrescente** com `ΔK`, e a inclinação da figura é de
  ordem `−0.5 GHz` por unidade de `ΔK/K₀ = 0.006` (pico indo de ~18 a ~17.5).
- **`H_fixo`** prevê inclinação **zero** dentro de `σ`.

**PASSA para `H_amplitude` se** a inclinação for **negativa** e sua magnitude estiver
**dentro de um fator 3** da lida na figura. Fator 3 e não um limiar apertado porque a leitura
da figura é em escala log e por olho — declarado **antes**, como teste de **escala e sinal**,
não de valor.

`σ(f_pico)` por Monte Carlo (semente `20260827`) da dispersão entre janelas do `RA-0`.
**`RA-1` só tem veredito se `σ < 0.10 GHz`.**

### `RA-2` — SECUNDÁRIO: o pico contra a ressonância, com o alvo certo
Agora com alvo publicado: a `Fig. S4(c)` marca a ressonância em **18 GHz** e mostra os picos
**abaixo** dela. Comparar `f_pico(0.002)` (a amplitude mais baixa, onde o amolecimento é
menor) com o nosso `f_SBM = 17.9609 ± 0.0125` (`C-11`).
**Exploratório, sem limiar:** é a pergunta do `E004`, e ela só terá veredito quando o `RA-1`
disser se o amolecimento existe. Relatado como observação.

### `RA-3` — extração do alvo, ANTES das corridas
Extrair `f_pico` das três curvas da `Fig. S4(c)` pelo procedimento do `E002` §2 (render a
200 dpi, calibrar pelos ticks, traçar por máscara de cor), e **selar antes de rodar**.

## 5. Taxonomia de falha
| resultado | significado, decidido antes |
|---|---|
| inclinação negativa, dentro do fator 3 | **`H_amplitude`**: o amolecimento não-linear reproduz. O "deslocamento" que reportei no `E004R` deixa de ser candidato a discrepância |
| inclinação ~zero | **`H_fixo`**: eu li a figura errado, e o deslocamento do `E004R` volta a ser **discrepância aberta** |
| inclinação negativa mas fora do fator 3 | discrepância de **escala** do amolecimento. Relatar assim |
| `σ ≥ 0.10 GHz` ou `RA-0` reprova | **INDETERMINADO**; sem veredito, sem estender |

## 6. Limites que já viajam junto
- **`L-G` intocado.** Décima quarta missão.
- Duas amplitudes novas mais uma já medida; sete frequências; um acoplamento; um modo; `α`
  único; malha de 1 nm; caixa de 100 nm.
- O alvo é **extração de figura em escala log**, lida por olho na posição do pico. É por isso
  que o `RA-1` é teste de **sinal e escala**, e está declarado assim.
- **Não** reproduz a `Fig. S4` inteira (faltam ABM, acoplamento forte, e o painel (e) `v_sp`
  vs `α`).
- `D-1`, `D-2`, `D-3`, `L2.3`, `L1.1`, `L8.4`, `L9.1` **intocados**.

## 7. Provenance
`LAB/EVIDENCE/E005/saf_amp.cu`, derivado do `saf_prop4r.cu` **selado**, com `ΔK/K₀` virando
argumento de linha de comando. Caminhos redirecionados **antes** da primeira execução e
verificados por `grep`. §4 do `CLAUDE.md`; a cicatriz é o `R001`.

## 8. Gate
`G-E005` = `RA-3` (alvo selado antes) ∧ `RA-0` (≥2 amplitudes) ∧ **`RA-1` com veredito**.
O gate exige veredito do primário (`R3`). **Passar o gate não é aceite.**
