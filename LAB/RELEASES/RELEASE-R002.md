# RELEASE-R002 — as-run da reprodução estrutural (região de estabilidade)

Data: 2026-08-21 · Missão: `MISSION-R002` (`AUTHORIZED` por `WRITEBACK-003`)
Estado desta release: **`TERMINAL_AWAITING_HUMAN`** · `human_acceptance: PENDING`

> Gate `G-R002` passou. **Passar o gate não é aceite.** Nada aqui está congelado.

---

## 1. Resultado contra os critérios pré-registrados

### PRIMÁRIO — **PASSOU** (é este que discrimina)
Os dois pontos publicados caem dentro da região `STABLE`:

| ponto | classe | l |
|---|---|---|
| (A_int=0.02, K₀=0.60) | NONCOAXIAL | 10.9529 nm |
| (A_int=0.12, K₀=0.35) | NONCOAXIAL | 15.0060 nm |

Este teste **podia ter falhado**. Uma leitura errada de D, de K ou do ansatz colocaria
plausivelmente um dos dois fora da região estável. Não colocou.

### TERCIÁRIO — **PASSOU**
Centros das janelas descem monotonicamente com A_int:
0.613 → 0.550 → 0.512 → 0.463 → 0.425 → 0.362.

### SECUNDÁRIO — **NÃO-DISCRIMINANTE, não usado como evidência**
Declarado morto na checagem de poder (passo 1 do protocolo), **antes** das demais colunas,
porque as semi-larguras das janelas (média 0.217) excedem o limiar pré-registrado de ±0.15.

Para registro, **como dado e não como resultado**: inclinação −2.393 (S1: −2.5),
intercepto 0.655 (S1: 0.65). Estes números **não** são reportados como sucesso.

---

## 2. Defeito de protocolo — registrado, não reparado

**A minha regra de poder estava mal especificada.** Ela usou a largura da janela como proxy da
capacidade de discriminação, e isso confunde duas coisas diferentes:

- as **bordas** da janela são determinadas a ±0.0125 (meio passo de grade), logo o **centro**
  também é — a precisão da estimativa é boa;
- a largura governa outra coisa: quão frouxamente "linha de centro" mapeia no que a Eq. (S1)
  quer dizer.

Classe de falha: **governança / desenho** (Core §9). Consequência: o critério secundário
permanece **não usado**. Não estou convertendo o defeito em aprovação depois de ver os dados —
seria exatamente a inversão que a regra existia para impedir.

**Deliberadamente não feito:** montar uma análise de poder contra a alternativa `QA-01` para
resgatar o critério. `QA-01` já foi fechada por leitura direta da Eq. (A4); demonstrar poder
contra uma alternativa já refutada não é demonstrar poder, e apresentá-la logo após declarar
o critério morto seria o resgate disfarçado.

---

## 3. Observação que fica pendente de teste próprio

Resíduos do centro observado contra a Eq. (S1):

| A_int | centro | S1 prevê | resíduo |
|---|---|---|---|
| 0.02 | 0.613 | 0.600 | +0.013 |
| 0.04 | 0.550 | 0.550 | 0.000 |
| 0.06 | 0.512 | 0.500 | +0.012 |
| 0.08 | 0.463 | 0.450 | +0.013 |
| 0.10 | 0.425 | 0.400 | +0.025 |
| 0.12 | 0.362 | 0.350 | +0.012 |

**Todos ≤ 0.025 = um passo de grade, e todos do mesmo sinal.** É uma afirmação bem mais forte
que o ajuste de inclinação, e o viés sistematicamente positivo é informativo por si (um
deslocamento de meio passo de discretização produziria exatamente isso).

**Status epistemológico: `CLAIM_CANDIDATE`.** Não `SUPPORTED_WITHIN_SCOPE`. Precisa do seu
próprio teste pré-registrado — o critério sob o qual ele contaria foi declarado morto antes
dos dados, e não pode ser ressuscitado por eles.

---

## 4. Achado estrutural mais forte: o ramo coaxial colapsa

| A_int | ramo coaxial | largura |
|---|---|---|
| 0.02 | [0.400, 0.525] | 0.125 |
| 0.04 | [0.350, 0.450] | 0.100 |
| 0.06 | [0.300, 0.375] | 0.075 |
| 0.08 | [0.250, 0.275] | 0.025 |
| 0.10 | ponto único em 0.200 | 0.000 |
| 0.12 | **ausente** | — |

Monótono em cinco colunas, sem parâmetro livre. Fronteira coaxial↔não-coaxial em
0.5375 / 0.4625 / 0.3875 / 0.2875 / 0.2125, inclinação **−4.125** — distinta da inclinação
−2.393 da linha de centro, ou seja, **as duas observáveis não são redundantes**.

### DISCREPÂNCIA EM ABERTO — não é rodapé
A legenda da Fig. 5(c) diz que a região de estabilidade *"features both possibilities, coaxial
and noncoaxial"*. Em **A_int = 0.12** — que é o ponto de acoplamento forte que o próprio
artigo usa — a minha varredura **não encontra ramo coaxial algum**.

Duas leituras possíveis, e **não consigo decidir entre elas pelo texto**:
1. a legenda descreve a região genericamente, não a cada A_int; ou
2. a minha leitura diverge do artigo nesse regime.

Fica registrado como discrepância aberta. Não deve ser suavizado no aceite.

---

## 5. Predição não verificável (rotulada como tal)
`l = 15.0060 nm` em (0.12, 0.35). O texto principal diz apenas *"the size of the skyrmion pair
is ∼10 nm"*, num contexto de estimativa de comprimentos-de-corpo que cobre os dois regimes.
Isso é consistente em ordem de grandeza mas **não é alvo quantitativo**. Este valor é
**predição do meu código, não corroboração**. Não deve ser contado como acordo com o artigo.

---

## 6. SL-B2 validado empiricamente
Os 8 estados `EXPLODE` da coluna A_int=0.02 têm **|Q| = 1.0000 exato**. Classificação apenas
por Q teria rotulado os 8 como estáveis. O critério conjunto (Q, área) era necessário.
Limiar de área (10 %) calibrado do estado ligado do R001 (1.10 %), não arbitrado.

## 7. Ponto ambíguo — resolvido pelo protocolo, não reclassificado
Um único `AMBIGUOUS` em 165 pontos: (0.08, 0.30), não convergido no orçamento padrão.
Reexecutado com orçamento 8× → `NONCOAXIAL`, l = 2.3019 nm, convergido em 1 215 575 iterações.
`scan_full.csv` **não foi reescrito** (INV-07); a resolução vive em `ambiguous_resolved.csv` e
é sobreposta pela análise, que imprime a mudança.

## 8. Provenance — dois binários, declarados
| binário | hash do fonte | produziu |
|---|---|---|
| A | `2dff5804…8a67` | `scan_full.csv` (165 linhas) |
| B | `f6eb9775…601b` | `ambiguous_resolved.csv`; hash atual em `SHA256SUMS.txt` |

B difere de A **apenas** por argumentos opcionais de linha de comando (tolerância, orçamento),
com os mesmos defaults. Verificado empiricamente, não afirmado: três pontos da varredura
reexecutados com B devolvem valores **bit-idênticos** ao CSV —
(0.02,0.60)→10.9529, (0.06,0.40)→9.6739, (0.12,0.35)→15.0060.

`EVIDENCE/R001/` permanece byte-idêntico; `sha256sum -c` passa. O `saf.cu` do R002 é cópia,
não edição do arquivo do R001.

## 9. Força da evidência: `BOUNDED`
Claim proporcional: **"a leitura do artigo embutida no `saf.cu` sobreviveu a um teste
estrutural multiponto que poderia tê-la refutado"** — e não "a Eq. (S1) foi reproduzida".

Limites:
1. O critério que testaria a Eq. (S1) quantitativamente foi declarado não-discriminante.
2. O teste da fronteira coaxial é **qualitativo**: não há valores extraíveis da linha tracejada
   da Fig. 5(c) no texto do PDF.
3. `SL-B1` — a região mapeada é a alcançável **a partir da inicialização declarada no artigo**,
   não "a região de estabilidade" em abstrato. Colapsos são ambíguos entre instabilidade real e
   saída de bacia.
4. Discrepância aberta em A_int = 0.12 (§4).
5. Malha de 1 nm, caixa de 100 nm, resolução em K₀ de 0.025 — não refinadas nesta missão.
6. Continua sem solver independente e sem leitura independente do artigo.

## 10. Ligação de impacto com R001
O critério primário passar significa que **a leitura do artigo usada no R001 sobreviveu a um
teste que poderia tê-la derrubado**. Isso **fortalece** o R001 sem aceitá-lo. Se o primário
tivesse falhado, `RELEASE-R001.md` estaria materialmente afetado.

As duas decisões de aceite continuam com Rodrigo, e são separadas.

## 11. Artefatos (`LAB/EVIDENCE/R002/`)
`saf.cu`, `saf`, `SHA256SUMS.txt`, `power_check_aint0.02.csv` (29 pts),
`scan_full.csv` (165 pts), `ambiguous_resolved.csv`, `analyse.py`, `analysis_output.txt`.

Reprodução: `nvcc -O2 -arch=sm_89 -o saf saf.cu`, depois
`./saf classify <Aint_mJm2> <K0_MJm3>` e `python3 analyse.py scan_full.csv`.

## 12. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar **R001** e **R002** (decisões separadas).
Continuam não autorizados: `MISSION-A001` (mumax3, com OOMMF recomendado no lugar) e a
auditoria externa com `codex`.
