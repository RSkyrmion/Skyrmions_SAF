# RELEASE-A008 — `l` cai com o refino; o critério, porém, ficou INCONCLUSIVO

Missão: `MISSION-A008` (+ `ADENDO-001`) · Autorizada por `WRITEBACK-039` · Execução: 2026-08-28
`human_acceptance: PENDING` · Evidência: `LAB/EVIDENCE/A008/` · Parede: **~9 min**

## 1. Veredito
**`AM-1`: INCONCLUSIVO.** As duas razões de refino disponíveis discordam: o triplo grosso cai
sobre `H_converge`, o triplo fino cai **entre as bandas**. Pela taxonomia do §8, isso é
"inconclusivo; relatar sem escolher lado".
**`AM-2` NÃO FOI EXECUTADO** — o §7 o condiciona a `AM-1` classificar `H_converge`.
**Gate `G-A008` passou**, porque exige `AM-1` **com veredito**, e "inconclusivo" é um dos
vereditos previstos. Passar o gate não é aceite, e aqui o gate passar não significa resposta.

## 2. `AM-0` — passou inteiro
| | |
|---|---|
| `AM-0.1` custo medido antes | 44 s em `a = 0.5 nm`; as quatro malhas couberam |
| `AM-0.2` estado comparável | `\|Q₁\| = \|Q₂\| = 1.0000`, par não coaxial, **em todas** |
| `AM-0.3` convergência da **saída** | `\|Δl\|` entre rodadas = **`0.000000 nm`** em todas |
| `AM-0.4` regressão a 1 nm | `10.955154` vs `10.9551` do `A005R2/ck4` → **`5.4e−5 nm`** (critério `< 0.005`) |

O `AM-0.3` merece destaque: a convergência foi checada em **`l`**, não no torque — a regra
`R2` do §6.1 que a linha `A005R` violou. E ela foi **exata**: `Δl = 0` entre rodadas nas quatro
malhas, com `MinimizerStop = 1e−8`.

## 3. A série medida — e ela é o resultado
Estimador **cego** do `AUDIT-002`, com `a` passado como argumento em cada malha.

| `a` [nm] | `l` [nm] | vs `10.98` publicado | vs `C-1` (`10.9607`) |
|---|---|---|---|
| 2.00 | `11.490846` | `+4.65 %` | `+4.84 %` |
| 1.00 | `10.955154` | `−0.23 %` | `−0.05 %` |
| 0.50 | `10.832353` | `−1.34 %` | `−1.17 %` |
| 0.25 | **`10.763929`** | **`−1.97 %`** | `−1.80 %` |

**`l` cai monotonicamente com o refino, e a partir de 1 nm fica sempre ABAIXO do valor
publicado.** Isto **não é extrapolação** — são quatro pontos medidos, cada um convergido em
`l` e verificado por régua cega.

### Checagem cruzada com o `saf.cu` selado
| malha | `saf.cu` (selado) | mumax3 | |
|---|---|---|---|
| 1.0 nm | `10.9607` (tol `1e−6`) | `10.9552` | `−0.051 %` |
| 0.5 nm | `10.8500` (`R001`) | `10.8324` | `−0.163 %` |

Os dois códigos concordam na **tendência** e no **valor** dentro do resíduo de convergência já
caracterizado no `A005R2`.

## 4. `AM-1` — por que ficou inconclusivo
| triplo | `r` | ordem implicada |
|---|---|---|
| 2.0 / 1.0 / 0.5 | `0.2292` | `p = 2.125` |
| 1.0 / 0.5 / 0.25 | **`0.5572`** | `p = 0.844` |

`H_converge` previa `r ≈ 0.25`; `H_nao_converge` previa `r ≳ 0.7`. O triplo grosso acerta
`H_converge` quase exatamente. **O triplo fino cai no meio**, e é ele que governa o
comportamento assintótico.

**Não escolho lado**, como a taxonomia manda. Registro as leituras possíveis, sem promover
nenhuma:
- a ordem efetiva **degrada** ao refinar, o que aconteceria se algo além da discretização no
  plano passasse a limitar — a **caixa fixa de 100 nm** e suas imagens periódicas são candidatas
  declaradas no §9 do pré-registro;
- ou o **float32** do mumax3 degrada em `0.25 nm`, onde o campo de troca é 16× o de 1 nm — risco
  também declarado no §9. O `AM-0.3` mostra que o **estado** está convergido em cada malha, mas
  não exclui viés sistemático da precisão;
- ou o esquema simplesmente não está em regime assintótico nesta faixa.

**Nenhuma foi testada.** Distinguir exigiria variar a caixa, ou um solver em precisão dupla.

## 5. O que isto faz — e o que NÃO faz — ao `C-1`
**Não revoga o `C-1`.** Ele é comparação **casada em malha**: nós, o mumax3 e o artigo usamos
1 nm, e a 1 nm o acordo é `−0.23 %` contra o publicado. Isso continua valendo.

**Fecha, por MEDIDA, a leitura do `C-1` como afirmação sobre o contínuo.** O
`E001-ADDENDUM-005` já a fechava parcialmente com dois pontos e extrapolação exploratória;
agora são **quatro pontos medidos** mostrando queda monotônica, sem precisar de extrapolação
alguma.

**Limite novo, que passa a viajar com o `C-1`:**
> O acordo de `C-1` com `10.98 nm` é **específico da malha de 1 nm**. Refinando para `0.5` e
> `0.25 nm`, `l` cai para `10.83` e `10.76 nm` — `−1.3 %` e `−2.0 %` do publicado. O limite do
> contínuo **não foi determinado**: o `AM-1` ficou inconclusivo e o `AM-2` não foi executado.

## 6. Limites
- **`AM-2` não executado.** Uma extrapolação calculada fora de critério daria `~10.68 nm`; ela
  **não é resultado, não é `AM-2`**, e não pode ser citada como limite do contínuo.
- **Caixa fixa em 100 nm.** Refinar a malha **não** afasta as imagens periódicas; um efeito de
  caixa apareceria em todas as malhas e é **indistinguível daqui**.
- **float32** no mumax3, com o piso já medido no `A005R2` (`1.7e−5 T`).
- Um ponto de parâmetros, estática, `T = 0`, um único solver para a série (o `saf.cu` entra só
  como checagem cruzada em duas malhas).
- **`L-G` intocado.** Leitura do modelo e inicialização seguem compartilhadas.

## 7. Proveniência
`AI-PROVENANCE.json`, `EVIDENCE-MANIFEST.json` e **`RUN-RECEIPT.json` por processo** (8 recibos),
conforme o `ADENDO-001` — primeira missão deste laboratório a nascer completa nesse padrão.

## 8. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar. E decidir se o limite do §5 passa a
viajar com o `C-1` — isso é promoção de limite e exige writeback seu.
