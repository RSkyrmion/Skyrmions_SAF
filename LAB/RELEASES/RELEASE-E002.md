# RELEASE-E002 — autopropulsão do par de skyrmions (Fig. 2, T = 0)

Missão: `MISSION-E002` · Autorizada por `WRITEBACK-010` (2026-08-25, *"Executemos E002"*)
Execução: 2026-08-25 · `human_acceptance: PENDING`
Evidência: `LAB/EVIDENCE/E002/` (selada por `SHA256SUMS.txt`)

> **Este é o as-run, incluindo o que falhou.** Dois dos cinco pré-testes falharam, o gate
> **não passou**, e três dos critérios que passaram passaram por motivos mais fracos do que
> parecem. Nada disso foi reparado em aprovação.

---

## 1. Veredito de uma linha
**A autopropulsão apareceu, na direção certa e com a magnitude certa nos dois modos** — mas o
**gate `G-E002` NÃO passou**, porque `PV-0` e `PV-1` falharam, ambos por defeito de desenho
dos meus próprios critérios.

## 2. Tabela dos critérios pré-registrados

### Pré-testes (escada, `MISSION-E002.md` §5)
| | medido | critério | |
|---|---|---|---|
| **`PV-0`** 𝒟 no equilíbrio | `19.4306e−15 N·s/m` | `[13.5, 16.5]e−15` | **FALHOU** |
| | `\|𝒟_xx−𝒟_yy\|/𝒟_xx = 0.0021` | `< 0.05` | passou |
| | `\|𝒟_xy\|/𝒟_xx = 0.0000` | `< 0.05` | passou |
| **`PV-1`** piso, pp(`l`), 200 ns | **`0.8680 pm`** | `< 0.40 pm` (Fig. 2c) | **FALHOU** |
| | | `< 0.02 pm` (Fig. 2d) | **FALHOU** |
| **`PV-2`** passo de tempo | `dif = 0.000 %` | `< 2 %` | **PASSOU** |
| | `max‖m‖−1 = 2.220e−16` | `< 1e−9` | **PASSOU** |
| **`PV-3`** custo | `11.15 s/ns` medido antes | — | cumprido |

### Critérios (`MISSION-E002.md` §6)
| | SBM 18.00 GHz | ABM 19.24 GHz | ABM 19.40 GHz |
|---|---|---|---|
| **`EP-1`** `\|v_∥\|/\|v_⊥\|` | `0.0000` **PASSOU** | `0.0000` **PASSOU** | `0.0000` **PASSOU** |
| **`EP-2`** `\|v_⊥\|` | **`3.5400`** cm/s (alvo 3.50) **PASSOU** | **`2.0322`** cm/s (alvo 2.03) **PASSOU** | — |
| **`EP-3`** dessintonia | — | \| `v(19.40) < v(19.24)`, razão `0.9923` → **FALHOU** ||
| **`EP-4`** harmônico de `l` | `17.9993 GHz = f_d` **PASSOU** | `38.4785 = 2f_d` **NÃO MEDIDA** | `38.7984 = 2f_d` **NÃO MEDIDA** |
| **`EP-5`** Eq. (4) | razão `1.10` (exploratório) | razão `0.006` (exploratório) | razão `0.006` |

**`EP-4` no ABM está "NÃO MEDIDA", não "passou".** O pré-registro condicionou o ramo ABM ao
`PV-1`, que o matou. O pico limpo em `2f_drive` existe no dado e é relatado abaixo como
observação, **não** como critério cumprido.

### Gate
`G-E002 = PV-0 ∧ PV-1(SBM) ∧ PV-2 ∧ EP-1 ∧ EP-2(SBM)` → **NÃO PASSOU** (dois termos falharam).

---

## 3. O que passou, e o que isso vale

### `EP-2` — a magnitude da autopropulsão, nos dois modos
| | meu `v_⊥` | alvo extraído da Fig. 2 | desvio |
|---|---|---|---|
| SBM, `ΔK/K₀ = 0.005`, 18.00 GHz | **3.5400 cm/s** | 3.50 cm/s | **+1.1 %** |
| ABM, `B₀ = 4 mT`, 19.24 GHz | **2.0322 cm/s** | 2.03 cm/s | **+0.1 %** |

**Não alegue 1,1 % nem 0,1 %.** Os alvos vêm de extração de figura: 1 px = 0.11 cm/s no
painel (a) e 0.011 cm/s no (b), e o platô do painel (a) está sobre uma única linha de pixels.
O acordo defensável é **"dentro da precisão de leitura do alvo"**, ~3 % no SBM e ~0,5 % no
ABM, contra uma banda pré-registrada de ±30 %/±50 % que era, e continua sendo, **teste de
escala**. O transiente **não** concorda: aos 5 ns eu dou 43 cm/s onde a figura dá ~17, e só
convirjo ao platô por volta de 130 ns. É o platô que bate, não a curva.

### `EP-1` — a deriva é perpendicular, mas o teste é mais fraco do que parece
`v_∥ = 0.000000 cm/s` **exato** nas três corridas, ângulo de deriva `−90.000°`, por duas rotas
independentes (referencial fixo e projeção instantânea, que concordam em `<0.01 %`).

**O zero exato não é resultado dinâmico, é simetria.** Trocar as duas camadas e inverter em
torno da bissetriz da ligação é simetria da minha condição inicial; sob `ΔK` ela é exata, e
sob `B_z` ela é exata a menos de meio período. Ela **força** `v_∥ = 0`. É o mesmo argumento
que o artigo faz ("the skyrmions mirror each other's dynamics"), mas significa que, no meu
arranjo, **o `EP-1` não podia falhar**. O teste que o artigo de fato propõe — deriva
perpendicular *seja qual for* a orientação da ligação — exige inicialização fora do eixo de
simetria e **não foi feito**. `EP-1` é, portanto, verificação de consistência, não teste.

### `EP-4` (SBM) — a assinatura `ω`, medida
Pico do espectro de `l(t)` no estacionário em `17.9993 GHz`, contra `f_drive = 18.0000`.
Promovido do terciário **não medido** do `E001` (`L6.3`), que fica assim **fechado no ramo
SBM**. O ramo ABM está morto por pré-registro (§2 acima), apesar de o dado mostrar
`38.4785` e `38.7984 GHz` contra `2f_drive = 38.48` e `38.80`.

---

## 4. O que falhou

### `PV-0` — 𝒟 fora da banda por +29,5 %
Detalhe completo em `EVIDENCE/E002/PV0-VEREDITO.md`. Resumo:
- **Não é unidade, não é `d`, não é bug.** O estimador foi verificado contra a energia de
  troca (validada por FD desde a `VL-1`): as duas rotas dão `3.886e−14` e `3.955e−14`,
  razão `1.0177` — **só a diferença de estêncil** (avançada vs centrada), prevista em ~2,5 %.
  Reproduzido em CUDA e em numpy com os mesmos dígitos, e idêntico nos três estados selados
  do `R001`.
- **Defeito de desenho registrado:** o critério comparou um 𝒟 **absoluto** contra um eixo de
  figura **cujo expoente está ausente do rótulo**. Ele não distingue "a minha forma difere"
  de "o rótulo omite um expoente". Mal pré-registrado, **não reparado**.
- Duas leituras do eixo, ambas exigindo expoente omitido: **R1** (`10⁻¹⁵ N·s/m`, a única
  dimensionalmente consistente) ⇒ diferença real de forma de +29,5 %; **R2** (autores usaram
  `γ₀ = μ₀γ` e rotularam N·s/m) ⇒ +3,1 %. **R2 é hipótese post-hoc e não resgata o `PV-0`.**
- **A ambiguidade é provadamente não-propagante:** em `G/(α𝒟)` o prefator `M_s d/γ` cancela,
  logo `EP-5` não depende de qual leitura é a certa, e `EP-1..EP-4` não usam 𝒟.

### `PV-1` — piso de ruído fora do limite nos dois ramos
`pp(l)` na corrida de 200 ns sem excitação = **0.8680 pm**, contra 0.40 (Fig. 2c) e 0.02
(Fig. 2d). **Ambos os painéis de ciclo de nado ficam declarados mortos antes do dado**, e
não são relatados como resultado.

**Segundo defeito de desenho, do mesmo tipo:** "pico-a-pico ao longo da corrida inteira" mede
a **aproximação lenta e monótona ao equilíbrio**, não o poder de resolver um sinal cíclico em
`f_drive`. O piso sem tendência nos últimos 50 ns é `0.0005 pm` — 4 000× abaixo da amplitude
SBM e 100× abaixo da ABM — mas esse número é **exploratório e não repara o critério**.
A deriva espúria residual na janela de ajuste é `+7.1e−5 cm/s`, isto é 0,002 % do alvo.

### `EP-3` — a dessintonia, e a minha checagem de poder errada
`v(19.40) = 2.0166` contra `v(19.24) = 2.0322 cm/s`. A predição registrada era
`v(19.40) > v(19.24)`; saiu o contrário. **FALHOU** — por **0,77 %**.

**Terceiro defeito de desenho, e este contamina o `EP-2`.** Eu pré-registrei banda de ±50 %
no ABM argumentando que 0,16 GHz de dessintonia custaria 15–40 % em `v_sp`. O medido é
**0,77 %**: superestimei a sensibilidade por um fator ~30, e a banda saiu larga demais por
raciocínio meu. O `EP-2` ABM passou a +0,1 % de qualquer modo, mas a **justificativa** que
sustentava a largura da banda estava errada, e isso fica registrado.

Consequência científica de `EP-3`, com dois pontos só: `v_sp` é **plana a <1 %** entre 19,24 e
19,40 GHz. Ela **não localiza** a ressonância e **não sustenta** 19,40 como pico de
autopropulsão. Reexaminei o espectro selado do `E001` com o `spectra.py` dele: o pico está em
19,40, mas 19,30 está a 0,993, o centroide acima de meia altura é **19,348 GHz** e a
FWHM é 0,60 GHz. O `19.40` do `C-6` é um **bin**, não uma linha resolvida.

---

## 5. Observações exploratórias — não são critério e não são resultado

### 5.1 Os dois `l̄` do artigo aparecem trocados de painel
| | meu `l̄` no estacionário | o artigo reporta |
|---|---|---|
| excitação `ΔK` (SBM), 18.00 GHz | **10.3936 nm** | Fig. 2(d), ABM: **10.39 nm** |
| excitação `B_z` (ABM), 19.24 GHz | **10.9824 nm** | Fig. 2(c), SBM: **10.98 nm** |

Quatro dígitos, cruzados. Em **todo o resto** os meus rótulos concordam com o artigo:
`ΔK` é invariante por reflexão e responde em `ω`; `B_z` quebra inversão e responde em `2ω`;
e as **velocidades** batem no painel certo. Só `l̄` sai trocado.

Duas leituras, e **não escolho uma**: (i) as legendas (c)/(d) trocaram os dois valores;
(ii) a legenda de (c) repetiu o valor de **equilíbrio** — 10,98 nm é o que a Fig. 2(a) dá para
o par relaxado, e é o alvo do `C-1`.

**Não afeta `C-1`:** o alvo do `R001` vem da legenda da Fig. 2(a), equilíbrio com excitação
desligada. **Afeta uma nota de leitura do `STATE.md`**, que atribui o 10,39 nm ao regime ABM;
pelos meus dados ele é o do SBM.

### 5.2 Amplitudes de respiração
`pp(l)` no estacionário: **2.087 pm** sob SBM (Fig. 2c mostra ≈ 2 pm) e **0.1259/0.1268 pm**
sob ABM (Fig. 2d mostra ≈ 0.1 pm). Como a amplitude relativa é invariante ao prefator de 𝒟,
isto é a única evidência disponível sobre a ambiguidade R1/R2 do `PV-0` — e pesa a favor de
R2. **Não repara o `PV-0`.**

### 5.3 A Eq. (4)
SBM: `|v_sp|` pela Eq. (4) = 3.91 cm/s contra 3.54 pela CTC, razão **1.10**, estável a 0,55 %
sob metade dos ciclos. ABM: razão **0.006** — a Eq. (4) não descreve o ABM, que é exatamente
o que o artigo diz ("Eq. (4) becomes insufficient"). Ambos usam `|Q|`, logo comparam
**magnitude apenas**. E são consistência interna do meu código: **não tocam `L-G`**.

---

## 6. Defeitos de execução, corrigidos na causa antes da produção
1. **Banner com `argv` colidido.** `prop none 18.0 2.0` fazia o cabeçalho anunciar
   `6x6 células de 18 nm` enquanto a corrida usava 100×100 (o `l_eq` batia com o valor selado
   do `R001`). A corrida estava certa; o **cabeçalho errado iria para dentro da evidência**.
   É o defeito do `RELEASE-E001` §6.1 reaparecendo no *print*. Blindagem movida para antes do
   banner.
2. **Transiente de relaxação residual.** A `tol = 1e−5` sobrava uma deriva de `−0.71 cm/s`
   — 18 % do alvo — decaindo com `τ ≈ 25 ns`. Apertar para `1e−6` reduz por exatamente 10×
   (`−0.063 cm/s`) e leva o equilíbrio ao valor canônico do `C-1`, `l = 10.960706 nm`.
   Toda a produção parte daí.
3. **Provenance (§4 do `CLAUDE.md`).** `saf_prop.cu` é arquivo **novo**, derivado do
   `saf_dyn.cu` selado (que não foi editado). Todos os caminhos de escrita redirecionados
   **antes da primeira execução**, verificado por `grep -n 'EVIDENCE/' saf_prop.cu` → só
   `E002`. Zero referências a `E001` ou `R001`.

## 7. Limites — os mesmos do pré-registro, mais o que a execução acrescentou
- **`L-G` INTOCADO.** Isto é o meu código, partindo do meu equilíbrio, medido pela minha
  régua. O `E002` acrescenta um observável novo; **não** acrescenta verificador independente.
  Nenhuma frase deste release é verificação independente de coisa alguma.
- **`EP-1` é simetria, não teste** (§3). A afirmação "perpendicular seja qual for a
  orientação" **não foi testada**.
- Os alvos são **extrações de figura**, com a precisão de leitura declarada, não valores
  tabelados pelos autores.
- **O transiente não reproduz a Fig. 2(a)**; só o platô reproduz.
- Um único ponto de parâmetros, malha de 1 nm, caixa de 100 nm. A causa física de `L1.1` (a
  malha resolve `Δ = 5 nm` apenas 5×) vale aqui igual.
- **Quatro dos meus critérios estavam mal desenhados** (`PV-0`, `PV-1`, a condicional do
  `EP-4`, a checagem de poder do `EP-2`/`EP-3`), sempre do mesmo jeito: limiar absoluto contra
  uma referência que não o sustentava. Registrado, **não reparado**.
- Fig. 3 (ressonância) e Fig. 4 (estocástica, 3,116 µs) estão fora de escopo por
  `WRITEBACK-010`.

## 8. Custo
`11.15 s/ns` medido antes de comprometer as corridas. Quatro corridas de 200 ns
(2233–2237 s cada) mais o controle de 20 ns a 5 fs (442 s). Total ≈ 2,6 h de GPU.

## 9. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar. **O gate não passou** — como no `A002`,
a recomendação de aceite, se houver, é dos itens que sobreviveram, não da missão como
desenhada. Nada está congelado.
