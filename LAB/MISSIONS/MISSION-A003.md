# MISSION-A003 — o `L-G`: um segundo solver mede `l`

Estado: **PROPOSTA — não autorizada.** Pré-registro escrito para leitura de Rodrigo.
Data: 2026-08-27 · Regime: auditoria por ferramenta independente (lineage `A001` → `A002`)

> **Pré-registro.** Escrito antes de qualquer corrida. Submetido à leitura de Rodrigo antes da
> execução (`CLAUDE.md` §2).
> **Fonte varrida:** texto principal, End Matter e suplementar (lição do `E005`), **mais** o
> fonte do mumax3 para as convenções.

## 1. O que está em jogo
Este é o ataque ao **`L-G`** — o limite acima de todos, intocado por catorze missões.
`10.9607 nm` é sustentado por um único código, o meu. O `mumax3 3.11.1` agora roda nesta
máquina (`TOOLS/`, `WRITEBACK-021`), com **DMI interfacial e PBC escritos pelos autores dele**.

**Mesmo o sucesso NÃO fecha o `L-G` inteiro.** O que o mumax3 verifica é a **numérica e as
expressões de campo**, *dada a minha leitura do modelo*. Quais termos entram, com que
parâmetros, e a Eq. (A4) do artigo — isso continua sendo leitura minha nos dois códigos. Uma
**leitura errada compartilhada sobrevive** (é a forma do `L3.3`).
Se esta missão passar, o `L-G` vira: *"o número é confirmado por um solver independente, dada
a minha leitura do modelo"*. É um degrau grande. **Não é a eliminação do limite.**

## 2. Escada de validação — o `A002` prova que ela é obrigatória
Sem escada, o `A002` teria rodado o par com **11,6 % do acoplamento faltando** e fabricado uma
discrepância falsa. A escada aqui é mais importante ainda, porque o veredito toca o `C-1`.

### `MV-0` — convenções do mumax3, LIDAS NA FONTE ou MEDIDAS. Nunca supostas.
Nada abaixo é assumido; cada item é um teste com número.
1. **Demag OFF.** O mumax3 calcula kernel de demag por padrão (visto no teste de fumaça). O
   nosso modelo não tem demag (`QA-01`). Desligar e **verificar** que a energia não muda ao
   variar `Msat` a campo nulo.
2. **Sinal do `Dind`.** O `AUDIT-001` identificou o sinal do DMI como **o risco discriminante**
   — o ponto onde o meu `pick_chirality` autocorrigiria um erro meu e o tornaria invisível.
   Medir: com `Dind = +3.05e−3`, qual quiralidade o mumax3 escolhe? Comparar com o `φ₀ = 0°`
   selado do `R001`. **Se divergir, é achado, não ajuste.**
3. **`Ku1` vs o nosso `K`.** Verificar por energia de estado uniforme inclinado.
4. **`QA-02` — o acoplamento interlayer. Este é o risco central.** O nosso termo é **areal**,
   `A_int·m₁·m₂` em J/m². O mumax3 oferece `ext_InterExchange(r1, r2, value)`, com `value` na
   convenção de troca dele. **A conversão tem de ser medida**, não deduzida: montar duas
   camadas uniformes antiparalelas e paralelas, e calibrar `value` até a **diferença de
   energia** bater com `ΔE = 2·A_int·Área` do nosso modelo.
   **Precedente que obriga isto:** no OOMMF, `sigma = −A_int/2` — **metade** do que a fonte
   sugeria (`A002`). Convenção de ferramenta se mede.

**`MV-0` PASSA quando os quatro itens tiverem número.** Se a `QA-02` não fechar — se o mumax3
não conseguir expressar o acoplamento areal com fidelidade — **a missão PARA aqui e relata
isso**. É desfecho legítimo, não fracasso.

### `MV-1` — skyrmion único, sem acoplamento (comparação, `R1`)
Mesmos parâmetros nos dois códigos, **com PBC** (o que o OOMMF não conseguiu, e foi o que matou
o `OV-1` do `A002` por inclinação de borda).
Grandeza: `Q` e o **raio** (`m_z = 0`).
**PASSA se** `|Q| = 1.0000` nos dois e os raios diferirem `< 2 %`.
Justificativa do 2 %: o `PV-0` do `E002` mediu que 3,2 % de diferença de tamanho é detectável
pelo tensor `𝒟`; 2 % é mais apertado que isso e ainda folgado para diferenças de discretização.
**Se `MV-1` falhar, o `MV-2` é DESCARTADO** — taxonomia do `A002` §4.

### `MV-2` — PRIMÁRIO: o par, e o número
mumax3 relaxa o par SAF no ponto do `C-1` (`A_int = 0.02`, `K₀ = 0.6`, malha 1 nm, caixa
100 nm, PBC, `T = 0`), a partir da mesma inicialização declarada no artigo.
`l` é medido **pelo estimador cego do `AUDIT-002`** aplicado à saída do mumax3 — não pelo meu
`ctc()`. Assim a régua também é independente do meu código.

**Critério, em forma de comparação:** `l_mumax3` contra `l_saf = 10.9607 nm`.

**Checagem de poder, ANTES do dado — e ela limita o que o sucesso vale.**
O `L1.1` do `C-1` mede sensibilidade de malha de **1,0 %**. Portanto:
- Acordo **melhor que 1 %** não distingue "os dois certos" de "os dois com o mesmo erro de
  leitura". Declarado agora: **o poder deste teste é para detectar erro GROSSO** — um fator,
  um sinal, um termo faltando — **não erro sutil**.
- **Desacordo > 1 %** é discrepância real e um dos dois códigos está errado. Aí o teste terá
  produzido a coisa mais valiosa que pode produzir.

**É por isso que este teste vale a pena mesmo com poder limitado: ele pode REFUTAR.**
Acordo será relatado como evidência **limitada**, com esta frase grudada.

## 3. Taxonomia de falha
| resultado | significado, decidido antes |
|---|---|
| `MV-0` item 4 não fecha | mumax3 não expressa o acoplamento areal. **Missão para**, e isso é resultado |
| `MV-0` item 2 diverge | sinal de DMI incompatível — toca o `AUDIT-001` e é **achado grave** |
| `MV-1` falha | física de um skyrmion difere. `MV-2` **descartado** |
| `\|Δl\|/l < 1 %` | `L-G` **reduzido, não eliminado**: número confirmado por solver independente, **dada a minha leitura do modelo** |
| `\|Δl\|/l > 1 %` | **discrepância real.** Um dos dois está errado, e descobrir qual vira missão |

## 4. Limites que já viajam junto
- **O `L-G` não é eliminado por esta missão**, no melhor caso. §1.
- A **leitura do modelo** é minha nos dois códigos. Leitura errada compartilhada sobrevive.
- mumax3 é `3.11.1` (o fonte arquivado), não o `3.12` do binário que não roda.
- Um ponto de parâmetros. Malha de 1 nm — e o `C-13` obriga a escalar `dt` se a malha mudar.
- Não toca `D-1`/`D-2`/`D-3`, `L2.3`, `L8.4`, `L9.1`, nem a dinâmica (`C-6`, `C-7`, `C-14`).

## 5. Provenance
`LAB/EVIDENCE/A003/` — scripts `.mx3`, saídas, log as-run, e o **hash do binário**
(`TOOLS/SHA256-mumax3-bin.txt`) copiado para dentro da evidência, porque a reprodutibilidade
depende dele. O binário do mumax3 **não escreve** em diretório de outra missão.

## 6. Custo estimado
mumax3 é rápido. `MV-0` ≈ 20 min · `MV-1` ≈ 15 min · `MV-2` ≈ 30–60 min. **Total < 2 h**,
dominado pelo trabalho de leitura de convenção, não por GPU.

## 7. Gate
`G-A003` = `MV-0` (quatro itens com número) ∧ `MV-1` ∧ **`MV-2` com veredito**.
**Passar o gate não é aceite. E o gate passar não fecha o `L-G`.**
