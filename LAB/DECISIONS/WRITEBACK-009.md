# WRITEBACK-009 — ACEITE COM RESTRIÇÕES de AUDIT-002 e E001

Data: 2026-08-25 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Audit-002 e E001 aceito com restrições"

`human_acceptance` de `AUDIT-002` e `MISSION-E001` passa de `PENDING` a
**`ACCEPTED_WITH_LIMITATIONS`**. Os `RELEASE-*.md` não foram editados e continuam dizendo
`PENDING` no corpo; este writeback é a autoridade que supersede aquele campo, como o
`WRITEBACK-007` fez para as quatro primeiras missões.

**Cobertura:** `RELEASE-E001.md` mais os seus cinco adendos (`ADENDUM-001` a `-005`), que são
parte do mesmo resultado.

## O que este aceite NÃO faz
- **Não é freeze.** Nada está congelado. Freeze continua não pedido.
- **Não autoriza** `E002` (autopropulsão), que segue **não proposta**.
- **Não autoriza** compilar extensão de DMI Cnv/PBC para o OOMMF, nem a etapa 2 do
  `AUDIT-001` (enviar o `saf.cu` a terceiro), nem missão de convergência.
- **Não fecha `L-G`.** Ver §C-5.1 — este é o ponto que mais corre risco de ser suavizado.

---

# Claims aceitos, com seus limites — continuação da versão canônica do `WRITEBACK-007`

## C-5 (de `AUDIT-002`) — a régua
> O estimador que produz `l` e `Q` a partir de um estado foi **reproduzido por implementação
> independente, escrita às cegas a partir da Eq. (1)**, com erro máximo de `0.0001 nm` nos
> três valores selados e `Q = ∓1` exato.

**Limites:**
- **L5.1 — o mais importante.** O estimador mede **o meu estado final**. Ele valida a
  **régua**, não a relaxação que produziu o estado. **`L-G` continua intocado.** Dizer que
  "um código independente confirmou 10,96 nm" seria falso: um código independente confirmou
  que, *dado o meu estado*, a régua lê 10,96 nm.
- **L5.2** Auditor e auditado são LLMs. Uma leitura errada **compartilhada** da Eq. (1)
  permanece invisível. Mitigado — não eliminado — pelas quatro divergências de convenção
  entre os dois códigos (arredondamento de `Q`, enrolamento de baricentros, imagem mínima,
  ordem de indexação).
- **L5.3** Testado apenas com o par **próximo ao centro** da caixa, condição declarada no
  `FORMAT.txt`. O comportamento sob travessia da fronteira periódica — onde o primeiro momento
  da Eq. (1) é mal definido — **não foi testado** em nenhum dos dois códigos.
- **L5.4** Acordo é evidência mais fraca do que um desacordo teria sido.

## C-6 (de `MISSION-E001` + adendos) — a dinâmica
> A dinâmica LLG implementada conserva energia sem renormalização, reproduz a precessão de
> Larmor exatamente, e produz **dois modos de breathing na faixa e na ordem que o artigo
> reporta**, com a simetria de cada modo **medida** e não rotulada.

**Limites:**
- **L6.1** A banda de `±20 %` do critério primário foi declarada, **antes dos dados**, como
  teste de **escala** e não de identidade: ela não separa 18 de 19,24 GHz, que distam 7 %.
  A identidade dos modos repousa no critério secundário (ordenamento) e na correlação
  medida — **não** na banda.
- **L6.2** `SBM = 18.00 GHz` bater em "18 GHz" é **mais bonito do que é forte**: o artigo cita
  o valor redondo no texto corrido e a minha resolução é 0,1 GHz. O número defensável do par é
  o **ABM, `19.40` contra `19.24`, `+0.83 %`**, porque `19.24` vem com três algarismos.
- **L6.3** Critério terciário (`l(t)` a `ω` sob SBM e `2ω` sob ABM) **não foi medido**.
- **L6.4** Malha de 1 nm, caixa de 100 nm, **um único ponto de parâmetros**.
- **L6.5** O estado inicial é o equilíbrio do **meu** código. A régua está verificada
  (`C-5`), o estado não.
- **L6.6** `L-G` intocado, de novo.

**Dívidas que este aceite fecha (não são mais limites):**
- O fator `1/(1+α²)` estava registrado como caminho não testado. Foi **medido** por Larmor
  amortecida a `3e−15` com `α` até 0,30 (`ADENDUM-001`), e o raciocínio errado de que ele
  "acumularia" em `E002` foi **corrigido no registro**: é reescala uniforme de tempo.
- A forma adimensional foi **implementada e conferida** contra a física: energias idênticas em
  16 dígitos (`ADENDUM-002`).

## Refinamento de `L1.1` (claim `C-1`, já aceito em `WRITEBACK-007`)
O `ADENDUM-005` **não altera** `C-1`, mas dá causa e acrescenta uma ressalva que passa a
viajar junto:
- **Causa física identificada:** dos três comprimentos característicos — troca `8.424 nm`,
  DMI `6.262 nm`, parede `Δ = 5.000 nm` — manda o **menor**, e a malha de 1 nm resolve `Δ`
  apenas **5×**. É daí que sai a sensibilidade de 1,0 %.
- **Ressalva nova:** extrapolação exploratória dos dois pontos aponta `l(a→0) ≈ 10.74–10.81 nm`,
  **afastando-se** do publicado. Não é resultado (sem critério pré-registrado, dois pontos não
  fixam a ordem, e o artigo também usa malha de 1 nm). Mas **fecha** qualquer leitura de `C-1`
  como afirmação sobre o contínuo.

---

## Limite global — inalterado e reafirmado
**L-G:** continua **sem verificação independente do resultado `l`**. Cinco instrumentos
atacaram cinco camadas — leitura (`AUDIT-001`), estrutura (`R002`), um termo isolado
(`A002` OV-2), a régua (`AUDIT-002`) e a dinâmica (`E001`) — e **nenhum atacou o número**.

Este aceite **aumenta** o número de camadas verificadas sem mover `L-G` um milímetro. Essa
distinção é a coisa mais fácil de perder ao recontar o trabalho.

## Efeito no estado
**Análise inicial ENCERRADA com aceite.** Todas as seis missões executadas estão
`ACCEPTED_WITH_LIMITATIONS`. **Nenhuma decisão humana pendente.** O laboratório entra em
repouso consistente e completo pela primeira vez.

## Próximo head/estado
`STATE-2026-08-25-a`

## Próxima decisão humana
**Nenhuma.** As direções em aberto estão em `STATE.md` §Direções e em
`CONSOLIDATION-2026-08-24.md` §9. Nenhuma proposta, nenhuma autorizada.
