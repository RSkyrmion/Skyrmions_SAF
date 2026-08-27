# RELEASE-E003-ADDENDUM-001 — a razão pela qual o gate passa

Data: 2026-08-25 · Corrige: `RELEASE-E003.md` §1 e §5
Origem: revisão que apontou que a afirmação "o gate passou" estava apoiada na leitura
**favorável** de uma ambiguidade que eu mesmo havia registrado.

## 1. O que estava errado no raciocínio, e não no dado
O `RELEASE-E003.md` §5 fez o seguinte: notou que o §4.3 do pré-registro diz "dispersão angular
do controle" **sem definir qual**, apontou as duas leituras possíveis (`0.04°` e `8.6°`), e
seguiu com a que faz a direção convergir.

**Isso é escolher a leitura depois de ver o dado.** É exatamente o movimento pelo qual a regra
de poder do `RELEASE-R002` §2 está registrada como defeito, e pelo qual recusei
`l(140 nm) = 10.9566` e a extrapolação de Richardson. O `§6` do pré-registro diz que direção
não convergida ⇒ **sem veredito**, e o gate exige veredito. Do jeito que estava escrito, o
gate estava apoiado numa conveniência.

O dado não muda. A **justificativa** muda, e ela precisava ser medida, não escolhida.

## 2. A medida que faltava: a inclinação converge
O `§6` pergunta se a **direção medida** converge, e eu respondi com o **offset** — que não
converge — para depois argumentar que quem importa é a inclinação. Faltou o óbvio: **checar se
a inclinação converge**, que é a única versão da pergunta que fala do critério de fato usado.

| janela | `θ_bond` (2 âng.) | `φ_drift` (2 âng.) | **`dφ/dθ`** |
|---|---|---|---|
| 25–50 ns | 25.9372 / 18.1682 | 119.2216 / 111.3962 | **`+1.0073`** |
| 50–100 ns | 25.8556 / 18.0881 | 123.5695 / 115.6454 | **`+1.0201`** |
| 75–100 ns | 25.8284 / 18.0614 | 125.2778 / 117.3103 | **`+1.0258`** |

**A inclinação varia `0.019` entre as três janelas.** As hipóteses distam `1.0`
(`H_ligação = +1`, `H_rede = 0`). Margem de **~50×**.

Enquanto isso o offset se move `4.4°`, por causa identificada e medida (a contaminação
constante do `EO-0` dividida por um sinal que decai).

## 3. O gate, com a razão correta
**`G-E003` PASSOU — porque a grandeza discriminante converge**, com `dφ/dθ` estável em
`1.007–1.026` em três janelas, e não porque a ambiguidade do §4.3 deixasse espaço.

Substitui a justificativa do `RELEASE-E003.md` §5. **O veredito `H_ligação` não muda**, e a
imprecisão do §4.3 continua registrada como quinta falha de desenho, **não reparada**.

## 4. Ressalva ao `EO-0.1`
O `EO-0.1` compara `l_eq` fora do eixo (`10.953118` e `10.956750 nm`) com o de `θ=0`
(`10.960706 nm`) e passa com folga no critério de 1 %. Mas os dois valores fora do eixo vêm de
uma relaxação que **bateu no teto de 2×10⁶ iterações com torque em `1.26e−5 T`** — não são
comprimentos de equilíbrio. **O critério passou como escrito; a grandeza que ele comparou não
é o que o nome dela sugere.** Registrado; não repara nem invalida o `EO-0.1`.

## 5. O que isto não muda
`L-G` intocado. O resíduo de 10 % (`0.8°`) segue sem explicação. O artefato de
comensurabilidade segue não caracterizado. A magnitude assintótica segue não medida.
