# RELEASE-A003 — um segundo solver mede `l`. **`−0.30 %`.**

Missão: `MISSION-A003` · Autorizada por `WRITEBACK-022` · Execução: 2026-08-27
`human_acceptance: PENDING` · Evidência: `LAB/EVIDENCE/A003/`

> Pré-registro **lido e liberado por Rodrigo antes da execução** (`CLAUDE.md` §2).
> Solver: `mumax3 3.11.1` construído em `TOOLS/` (`WB-021`), hash em `SHA256-mumax3-bin.txt`.

## 1. Veredito
**`MV-2`: `l_mumax3 = 10.9279 nm` contra `l_saf.cu = 10.9607 nm` — `−0.30 %`**, dentro do
critério pré-registrado de 1 %. **Gate `G-A003` passou.**

**O `L-G` MOVE-SE PELA PRIMEIRA VEZ EM QUATORZE MISSÕES — e NÃO se fecha.** Ver §6.

## 2. `MV-0` — convenções do mumax3, medidas e não supostas

| item | medido | veredito |
|---|---|---|
| **MV-0.1** demag OFF | `E_demag = 0`; `E_total` independente de `Msat` | PASSOU |
| **MV-0.3** `Ku1` | `E_anis = −4.8000004e−18` vs `−Ku1·V = −4.8e−18` (8 algarismos) | PASSOU |
| **MV-0.4** `QA-02` | `A_inter = −4e−15 J/m` ⇒ `ΔE = 4.0000e−19 J` | PASSOU |
| **MV-0.2** sinal do DMI | quiralidade radial **para fora**; a espelhada **colapsa** | PASSOU |

### `QA-02` fechada — e pelo mesmo número que o OOMMF já confirmara
O nosso termo é **areal** (`A_int·m₁·m₂`, J/m²); o mumax3 usa rigidez de troca (J/m).
Derivei `A_inter = −A_int·Δz/2 = −4e−15 J/m` e **medi**: com camadas uniformes,
`ΔE = E_∥ − E_∦ = 4.0000e−19 J`, linear (o dobro de `A_inter` dá o dobro), e zero quando
desacopladas. **`4.000000e−19 J` é exatamente o alvo do `OV-2` do `A002`**, verificado contra
o OOMMF. **Três ferramentas independentes concordam no termo interlayer.**
O campo também fecha analiticamente: `2A_inter/(M_s Δz²) = −A_int/(M_s d)`, o nosso `SL-2`.

### O sinal do DMI — o risco discriminante do `AUDIT-001`, agora verificado
O `AUDIT-001` registrou que o meu `pick_chirality` escolhe quiralidade **por energia** e
portanto **autocorrigiria um erro de sinal meu, tornando-o invisível em `l`**. O mumax3 escolhe
sozinho: com `Dind = +3.05e−3`, a quiralidade radial **para fora** sobrevive
(`⟨mz⟩ = 0.9565`) e a espelhada **colapsa** para uniforme (`⟨mz⟩ = 1.0`). Isso é
`φ₀ = 0` — o valor selado do `R001`.
Medi também no estado selado que **as duas camadas** são radiais para fora, confirmando a nota
algébrica do `AUDIT-001` (`p₂=−p₁`, `D₂=−D₁` ⇒ `cos χ₂ = cos χ₁`) — que até aqui era álgebra.

## 3. `MV-1` — skyrmion isolado, comparação casada
| | `Q` | raio (`m_z = 0`) |
|---|---|---|
| mumax3 | `−1.000000` | `7.3889 nm` |
| saf.cu (`Aint=0`, tol `1e−6`) | `−1.000000` | `7.3903 nm` |

**Diferença `−0.019 %`**, contra critério de 2 %. Cem vezes melhor que o exigido. **PASSOU.**

## 4. `MV-2` — o par, e o número
Convenções todas do `MV-0`. Estado medido pelo **estimador cego do `AUDIT-002`** — nem o
solver nem a régua são meus. `Q1 = −1`, `Q2 = +1`.

### O controle de convergência que evitou uma discrepância falsa
| estágio | `maxTorque` | `l` |
|---|---|---|
| após `relax()` | `7.07e−4` | **10.3414 nm** |
| após `minimize()` | `4.84e−5` | **10.9276 nm** |
| após `minimize()` de novo | `4.83e−5` | **10.9279 nm** |

**O `relax()` do mumax3 NÃO converge este sistema.** Sem esta checagem eu teria relatado
`−5.65 %` de discrepância — que **não existe**. É a mesma classe do bug de PBC do OOMMF, que a
escada do `A002` pegou: um artefato de ferramenta que fabricaria um resultado falso.
Armadilha promovida ao `CLAUDE.md` §8.

### O resultado
`l_mumax3 = 10.9279 nm` · `l_saf.cu = 10.9607 nm` · **`Δ = −0.30 %`** · critério `< 1 %`.

## 5. `MV-2` na taxonomia pré-registrada
`|Δl|/l < 1 %` ⇒ *"`L-G` **reduzido, não eliminado**: número confirmado por solver
independente, **dada a minha leitura do modelo**"*. É o que se aplica.

## 6. O que isto faz — e o que NÃO faz — ao `L-G`

**Antes:** não havia verificação independente do resultado. `10.9607 nm` era sustentado por um
único código, o meu.

**Agora, se aceito:** o número é confirmado por **`mumax3 3.11.1`** — troca, anisotropia, DMI
interfacial, PBC e integrador escritos por **outras pessoas** — e medido pelo **estimador cego
do `AUDIT-002`**, a `0.30 %`.

**O que NÃO fecha, e não pode ser suavizado:**
- **A leitura do modelo é minha nos dois códigos.** Quais termos entram, com que parâmetros,
  e como li a Eq. (A4) — tudo meu. **Uma leitura errada compartilhada sobrevive** (`L3.3`).
- **A checagem de poder, declarada antes, limita o que o acordo vale.** A sensibilidade de
  malha do `C-1` é `1.0 %` (`L1.1`); os `0.30 %` estão **abaixo** dela. Acordo neste nível
  **não distingue "os dois certos" de "os dois com o mesmo erro de leitura"**. O poder deste
  teste é para erro **grosso** — um fator, um sinal, um termo faltando. Ele **podia** refutar
  e não refutou; isso é evidência **mais fraca** do que uma refutação teria sido (`L3.1`).
- **Não toca a dinâmica.** `C-6`, `C-7`, `C-14` seguem com um único código.

**Redação sugerida para o `CLAUDE.md` §7 e o `STATE.md`, SE Rodrigo aceitar** — a mudança é
dele, porque altera a narrativa central do laboratório:
> `L-G`: o resultado `l` tem verificação por **um** solver independente (`mumax3`, `A003`,
> `−0.30 %`), medido por estimador cego. **Não** tem verificação independente da **leitura do
> modelo**: quais termos e quais parâmetros são meus nos dois códigos. E o acordo está
> **abaixo** da sensibilidade de malha, logo não separa "ambos certos" de "ambos com o mesmo
> erro". Nunca escrever "o artigo foi reproduzido".

## 7. Limites
- Um ponto de parâmetros (o do `C-1`), malha de 1 nm, caixa de 100 nm, `T = 0`, estática.
- mumax3 `3.11.1` (o fonte arquivado), float32 — o `saf.cu` é double.
- A inicialização (separação de 10 nm, quiralidades) é a mesma nos dois: **não** é
  independente. Só o solver e a régua são.
- `D-1`, `D-2`, `D-3`, `L2.3`, `L8.4`, `L9.1`, `L14.2` **intocados**.

## 8. Custo
`MV-0` ≈ 6 min · `MV-1` ≈ 4 min · `MV-2` + convergência ≈ 10 min. **Total < 25 min.**

## 9. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar. E, se aceitar, decidir a nova redação
do `L-G` no `CLAUDE.md` §7 — que é a coisa mais importante deste release.
