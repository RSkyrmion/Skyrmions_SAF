# CONSOLIDAÇÃO — Fase 1 e primeira missão da Fase 2

Data: 2026-08-24 · atualizado 2026-08-25 · `head` do estado: `STATE-2026-08-25-a`
Pedido de Rodrigo: *"Quero concluir nossa análise inicial"*

> Este documento é a **síntese**, não a autoridade. A autoridade dos claims é o
> `WRITEBACK-007`; a de cada resultado, seu `RELEASE-*`. Ele existe para que a análise possa
> ser retomada, contada ou defendida sem reler dezessete arquivos.

---

## 1. A pergunta

Uma re-implementação **independente** do modelo de
C. C. de Souza Silva, M. V. Correia, J. C. Piña Velásquez,
*Emergent Self-Propulsion of Skyrmionic Matter in Synthetic Antiferromagnets*,
**PRL 135, 086701 (2025)**, reproduz o par de skyrmions acoplados daquele artigo?

Os dados originais **não são públicos**. Isto é re-implementação, não re-execução — e essa
limitação é estrutural, não corrigível por esforço.

---

## 2. O que ficou estabelecido, do mais forte para o mais fraco

### 2.1 O estimador — `SOLID` (`AUDIT-002`)
Um auditor externo escreveu, **cego** ao meu código e aos meus números, um estimador de `Q` e
`l` a partir da Eq. (1). Rodando sobre a evidência selada:

| arquivo | meu valor | estimador cego | dif |
|---|---|---|---|
| `mfinal_weak.dat` | 10.9529 nm | 10.9530 | +0.0001 |
| `mfinal_weak_tight.dat` | 10.9607 nm | 10.9608 | +0.0001 |
| `mfinal_mesh05.dat` | 10.8500 nm | 10.8500 | +0.0000 |

Faz **quatro escolhas de convenção diferentes** das minhas e converge assim mesmo.
Cegueira verificada por varredura do trace.

### 2.2 O fator `1/d` (`SL-2`) — fechado por **quatro** caminhos
`B_int,i = −A_int m_j/(M_s d)`. Confirmado por: (i) diferenças finitas internas (VL-1),
(ii) valor fechado `0.086207 T` interno (VL-2), (iii) **derivação cega externa**
(`AUDIT-001`), (iv) **OOMMF**, código humano independente, 4 dígitos (`A002` OV-2).
O quarto é o único que não é nem meu nem de um LLM.

### 2.3 A leitura do artigo — `BOUNDED` (`AUDIT-001`)
Derivação cega das expressões de campo: **7 comparadas, 7 acordos, 0 divergências** — mas
**2 discriminantes** (o `1/d` e o sinal do DMI) e **5 confirmatórias**.
O discriminante que importava: `pick_chirality` **autocorrigiria** um erro de sinal meu,
tornando-o invisível em `l`. O auditor derivou às cegas `cos χ = −p·sgn(D)`, que prevê
`φ₀ = 0°`; os logs selados mostram `φ₀ = 0°`. **Passou.**
Achado lateral: a Eq. (A1) do artigo é dimensionalmente imprecisa — só fecha se `δH/δm` for
volumétrico, enquanto a Eq. (A3) é areal.

### 2.4 A estrutura — `BOUNDED` (`R002` + adendo)
Fronteira coaxial↔não-coaxial contra a extraída da Fig. 5(c): **cinco colunas, resíduo
≤ meio passo de grade**. Eq. (S1) confirmada como a **linha de centro da própria figura**.
Os dois pontos publicados caem na região estável. Predição escrita **antes** da extração.

### 2.5 A dinâmica — `BOUNDED` (`E001`, aceita com restrições)
LLG implementada e validada: energia conservada a `1.06e−09` com `α=0` **sem renormalizar**;
Larmor exata (`+0.00000 %`); fator `1/(1+α²)` medido a `3e−15` com `α` até 0.30; forma
adimensional implementada e conferida contra a física (energias idênticas em 16 dígitos).
Modos de breathing: **SBM 18.00 GHz** (publicado 18), **ABM 19.40 GHz** (publicado 19.24,
`+0.83 %`), na ordem certa. Identidade dos modos **medida** (`corr = −1.0000` vs `+0.9999`),
não rotulada.

### 2.6 O número — `BOUNDED`, e é o mais frágil do lote (`R001`)
`l = 10.9607 nm` contra `10.98 nm` publicado → `−0.18 %`, dentro da banda pré-registrada.
**Mas a sensibilidade à malha é `1.0 %`** — cinco vezes a discrepância. O acordo **não é mais
preciso que o método**.

---

## 3. O que NÃO ficou estabelecido

### 3.1 `L-G` — o limite que sobrevive a tudo
**Não há verificação independente do resultado `l`.** Três instrumentos atacaram três camadas
— leitura (`AUDIT-001`), estrutura (`R002`), um termo isolado (`A002` OV-2) — e um quarto
verificou a régua (`AUDIT-002`). **Nenhum atacou o número.** O que sustenta `10.9607 nm`
continua sendo um único código, o meu.

A tentativa de fechá-lo falhou por motivo de ferramenta, não de física: o OOMMF não tem DMI
Cnv com PBC nesta instalação (ver §5).

### 3.2 `L2.3` — discrepância aberta em `A_int = 0.12`
O artigo prevê ramo coaxial em `K₀ ∈ [0.126, 0.144]`; varri cinco valores com duas
inicializações e não encontro. Estreita, localizada, em região onde a linha do artigo está
**extrapolada** (último traço em 0.1066). **Aberta.**

### 3.3 O limite do contínuo
Os três comprimentos característicos: troca `8.424 nm`, DMI `6.262 nm`, parede
**`Δ = 5.000 nm`**. Manda o menor: a malha de 1 nm resolve `Δ` apenas **5×**. Isso dá causa
física a `L1.1`.
Extrapolação exploratória dos dois pontos aponta `l(a→0) ≈ 10.74–10.81 nm`, **afastando-se**
do publicado. **Não é resultado** — sem critério pré-registrado, dois pontos não fixam a
ordem, e o artigo também usa malha de 1 nm, então a comparação do R001 é casada em malha.

---

## 4. O claim proporcional, em uma frase
> Uma re-implementação independente, cuja **leitura** do artigo sobreviveu a auditoria cega,
> cuja **régua** foi reproduzida por código independente, e cujo **termo de acoplamento** foi
> confirmado por solver humano, produz um par não-coaxial com `l` consistente com o valor
> publicado dentro de `0.2 %` **num único ponto de parâmetros e na malha do próprio artigo**,
> e reproduz a estrutura da região de estabilidade dentro de meio passo de grade.
> **O resultado em si permanece sem verificação independente.**

Não é "o artigo foi reproduzido".

---

## 5. Achados de ferramenta (subprodutos de valor próprio)
1. **`Oxs_TwoSurfaceExchange` + malha periódica: bug silencioso.** 1164 de 10000 células da
   interface perdem o link; energia 11.6 % curta. Determinístico. Sem a escada de validação,
   teria fabricado uma discrepância falsa contra o meu próprio código.
2. **`Oxs_DMExchange6Ngbr` recusa malha periódica.** Recusa dura. `Oxs_DMI_C2v` aceita mas é
   simetria errada. **Não há DMI interfacial com PBC** nesta instalação.
3. **`sigma = −A_int/2`**, não `−A_int`: a energia do link é somada às duas células e o campo
   usa `hcoef = 2/μ₀`.
4. **Notação da Eq. (A1) do artigo é imprecisa** (§2.3).

## 6. Achados de método
- As escadas de validação pegaram **três** coisas que teriam virado resultado falso: o bug de
  PBC do OOMMF, o colapso do par por colisão de `argv`, e a contaminação de fronteira livre.
- O pré-registro **matou dois números tentadores**: `l(140 nm) = 10.9566` (a 0.03 % do meu) e a
  extrapolação de Richardson. Os dois estão no registro como dado, nenhum como resultado.
- Dois defeitos meus, pegos e corrigidos na causa: colisão de `argv` e reescrita de evidência
  selada do R001 (dano verificado nulo por comparação de 17 dígitos).
- Uma regra de poder mal especificada (`R002` §2), registrada e **não reparada em aprovação**.

## 7. Unidades e escalas (referência rápida)
```
B₀ = 2A/(M_s a₀²)        = 51.7241 T          (= prefator de troca do kernel)
t₀ = 1/(γB₀)             = 0.1098 ps
μ  = M_s a₀² d           = 2.32e−22 A m²
J  = μB₀ = 2 A d         = 1.20e−20 J         (célula cúbica daria 2a₀A = 3.00e−20)
λ_ms = √(2A/μ₀M_s²) = 8.424 nm | l_D = 4A/(πD) = 6.262 nm | Δ = √(A/K) = 5.000 nm
D_c = 4√(AK)/π = 3.8197 mJ/m²   ->   κ = 0.7985
```

---

## 8. Estado formal
| item | estado |
|---|---|
| `R001`, `R002`, `AUDIT-001`, `A002` | **`ACCEPTED_WITH_LIMITATIONS`** (`WRITEBACK-007`) |
| `AUDIT-002`, `E001` + 5 adendos | **`ACCEPTED_WITH_LIMITATIONS`** (`WRITEBACK-009`, 25/08) |
| `E002` (autopropulsão) | não proposta |
| Freeze | **não pedido, não feito** |

**Análise inicial ENCERRADA com aceite.** As seis missões executadas estão aceitas com
limitações. Nenhuma decisão humana pendente.

**O aceite de `AUDIT-002` e `E001` aumentou o número de camadas verificadas de três para
cinco — e não moveu `L-G` um milímetro.** É a distinção mais fácil de perder ao recontar o
trabalho, e por isso está registrada em `WRITEBACK-009` §L-G.

## 9. Se a pesquisa continuar
1. **`E002` — autopropulsão sob ABM.** O resultado central do artigo. A dinâmica existe e está
   validada; a dívida do `1/(1+α²)` está paga; a rota adimensional está pronta.
2. **Atacar `L-G`.** Exige compilar uma extensão de DMI Cnv com PBC para o OOMMF (**ação de
   sistema**) — é o único caminho que fecha o limite que sobrou.
3. **Missão de convergência** em três malhas (1.0 / 0.5 / 0.25 nm), ordem pré-registrada.
4. **Fechar `L2.3`.**
5. **Etapa 2 do `AUDIT-001`** — enviar o `saf.cu` ao auditor externo (**ação externa**).
