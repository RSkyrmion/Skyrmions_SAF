# WRITEBACK-023 — ACEITE de `A003` e **nova redação do `L-G`**

Data: 2026-08-27 · Autoridade: Rodrigo

## Decisão humana (literal)
> "A003 aceito com limitações; aprovo a redação sugerida do L-G"

`human_acceptance` de `MISSION-A003` passa de `PENDING` a **`ACCEPTED_WITH_LIMITATIONS`**.
Gate `G-A003` passou. **E o `CLAUDE.md` §7 é reescrito** — primeira vez desde a fundação do
laboratório. A mudança é ato humano e está aqui pela citação literal.

---

## C-15 (de `MISSION-A003`) — o número, por um segundo solver
> Um solver independente — **`mumax3 3.11.1`**, com troca, anisotropia, DMI interfacial, PBC e
> integrador escritos por **outras pessoas** — relaxa o par SAF no ponto do `C-1` e dá
> **`l = 10.9279 nm`** contra os `10.9607 nm` do `saf.cu`: **`−0.30 %`**.
> O estado foi medido pelo **estimador cego do `AUDIT-002`**: nem o solver nem a régua são
> meus. `Q₁ = −1`, `Q₂ = +1`.

**Limites — e o `L15.2` é o que não pode ser suavizado:**
- **L15.1** A **leitura do modelo é minha nos dois códigos**: quais termos entram, com que
  parâmetros, e como li a Eq. (A4). **Uma leitura errada compartilhada sobrevive** (`L3.3`).
- **L15.2** **Os `0.30 %` estão ABAIXO da sensibilidade de malha de `1.0 %`** (`L1.1`).
  Declarado **antes do dado**: acordo neste nível **não distingue "os dois certos" de "os dois
  com o mesmo erro de leitura"**. O poder deste teste é para erro **grosso** — um fator, um
  sinal, um termo faltando. Ele **podia** refutar e não refutou; isso é evidência **mais fraca**
  do que uma refutação teria sido (`L3.1`).
- **L15.3** A **inicialização é a mesma** nos dois códigos (separação de 10 nm, quiralidades
  medidas do estado selado). **Só o solver e a régua são independentes.**
- **L15.4** **A dinâmica NÃO foi tocada.** `C-6`, `C-7` e `C-14` seguem com um único código.
- **L15.5** Um ponto de parâmetros, estática, `T = 0`, malha de 1 nm, caixa de 100 nm.
  mumax3 é float32; o `saf.cu` é double.

**Fechamentos que valem por si, independentes do número:**
- **`QA-02` FECHADA.** `A_inter = −A_int·Δz/2 = −4e−15 J/m` ⇒ `ΔE = 4.000000e−19 J` — o
  **mesmo** alvo que o `OV-2` do `A002` verificou contra o OOMMF. **Três ferramentas
  independentes concordam no termo interlayer.**
- **O sinal do DMI está verificado.** O `AUDIT-001` registrou que o meu `pick_chirality`
  escolhe por energia e **autocorrigiria um erro de sinal meu, tornando-o invisível em `l`**.
  O mumax3 escolhe sozinho e escolhe o mesmo; a quiralidade espelhada **colapsa**.

**Armadilha medida, promovida ao `CLAUDE.md` §8:** o **`relax()` do mumax3 não converge** este
sistema (`l = 10.3414 nm`, `−5.65 %`). Só após `minimize()` — e confirmado por uma segunda
chamada — o valor assenta em `10.9279`. **Sem o controle de convergência, este release teria
anunciado uma discrepância que não existe.**

---

## A nova redação do `L-G` — aprovada literalmente
Substitui o `CLAUDE.md` §7. O texto anterior dizia *"não há verificação independente do
resultado `l` ... o que sustenta `10.9607 nm` é um único código"*, e era verdade até hoje.

**O risco mudou de lado.** Antes, a tentação ao recontar era **omitir** que não havia
verificação. Agora é **exagerar** que há — dizer "foi verificado independentemente" e parar
aí. O §7 novo guarda contra isso, e é por isso que ele nomeia as três coisas que continuam
sem verificação: a leitura do modelo, a resolução do acordo, e a dinâmica.

## Efeito no estado
**Quinze missões, todas `ACCEPTED_WITH_LIMITATIONS`. Nenhuma pendente.**

## Próximo head/estado
`STATE-2026-08-27-g`
