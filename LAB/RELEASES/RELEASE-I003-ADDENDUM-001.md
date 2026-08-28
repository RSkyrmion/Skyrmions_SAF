# RELEASE-I003-ADDENDUM-001 — a proveniência do `dt ∝ a²` estava errada

Data: 2026-08-28 · Corrige: `RELEASE-I003.md` §1, §4 e a entrada correspondente do
`CLAUDE.md` §8 · Origem: observação de Rodrigo em 2026-08-28.

## 1. O que estava errado
O `RELEASE-I003.md` apresenta `dt ∝ a²` como **achado empírico** ("a causa é a que eu havia
conjecturado e não testado"), e a entrada que dele foi promovida ao `CLAUDE.md` §8 diz
"**medido**". O `RELEASE-A005` §6 chama a causa de "candidata **não verificada**".

**Nada disso era verdade.** A relação já estava **verificada e registrada neste laboratório**,
em `RELEASE-E001-ADDENDUM-002.md`, **linha 11**:

```
t = t₀ τ ,     t₀ = M_s a₀² / (2 A_ex γ)
```

Ali ela foi implementada no mesmo binário (modo `ndcheck`) e conferida contra a rota física
com energias **idênticas em 16 dígitos**, em 2026-08-24 — **dois dias antes do `I003`**.

O `a²` está explícito na fórmula. A conclusão sai em uma linha:

| malha | `t₀` | `dt = 10 fs` equivale a |
|---|---|---|
| 1,0 nm | `0.10979 ps` | `0.0911 t₀` |
| 0,5 nm | `0.02745 ps` | **`0.3643 t₀`** |

Quatro vezes mais grosseiro, exatamente `(1/0.5)²`.

## 2. O que o `I003` legitimamente acrescentou — e é mais estreito
`t₀` diz que o passo estava grosseiro. **Não** diz que corrigi-lo restaura o estado ligado.
Essa era a hipótese `H_física` do pré-registro, que teria tocado o `L1.1`, e ela **precisava**
de medida. O `I003` mostrou que `l` fica em `10.8483 nm`, constante em quatro casas, com
`dt = 2.5 fs`.

Mas essa medida só foi necessária **porque eu já havia rodado errado e reportado**. Com a
fórmula aplicada de início, o `RF-4` do `E004R` não teria falhado.

## 3. O que muda e o que não muda
**Não muda:** o conteúdo operacional. `dt` **tem** de escalar com `a²`, e refinar malha em LLG
sem isso produz física falsa que parece física. A entrada do §8 continua valendo.

**Muda:** a proveniência. Passa a ser **consequência analítica de `t₀`, registrada no
`E001-ADDENDUM-002`**, e não achado empírico do `I003`. A palavra "medido" no §8 é substituída
por "analítico, verificado no `E001-ADDENDUM-002`; confirmado por medida no `I003`".

**Não muda:** o `C-13` continua aceito (`WB-019`) e a redução de deriva de `4.5×` continua
**exploratória** (`L13.1`).

## 4. A lição de método, que é a parte que importa
Gastei 19 min de GPU e uma missão inteira para confirmar o que a evidência selada deste
laboratório já entregava de graça. O `CLAUDE.md` §1 manda reler o estado a cada sessão; ele
não diz explicitamente "releia os adendos técnicos antes de propor um teste numérico", e este
caso mostra que deveria.

**Proposta, não autorizada:** acrescentar ao §1 a obrigação de varrer os adendos de release
antes de desenhar missão numérica — do mesmo modo que o `E005` passou a exigir varrer a fonte
inteira antes de desenhar missão científica.
