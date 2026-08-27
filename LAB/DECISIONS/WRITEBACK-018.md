# WRITEBACK-018 — ACEITE COM LIMITAÇÕES de `E004R` e `I002`

Data: 2026-08-26 · Autoridade: Rodrigo

## Decisão humana (literal)
> "E004R e I002 — aceito com limitações"

`human_acceptance` de `MISSION-E004R` e `MISSION-I002` passa de `PENDING` a
**`ACCEPTED_WITH_LIMITATIONS`**. Os `RELEASE-*` não foram editados.

**Aceite dado apesar de os dois gates NÃO terem passado.** Como no `A002` e no `E002`, o
aceite é dos itens que sobreviveram, não da missão como desenhada.

## O que este aceite explicitamente NÃO faz
- **NÃO responde o `RF-1`.** A afirmação do artigo de que `v_sp` tem pico na ressonância do
  modo continua **NÃO TESTADA** neste laboratório, agora por duas missões seguidas. Nenhum
  número do `E004R` pode ser citado como tendo testado isso.
- **NÃO resolve o `L8.4`.** O `I002` refutou a própria premissa; a pergunta segue aberta.
- **NÃO fecha `L-G`**, não é freeze, não autoriza missão nova.

---

# Claims aceitos — continuação de `WB-007`, `-009`, `-011`, `-015`

## C-10 (de `E004R`, `RF-3`) — a régua atravessa a fronteira periódica
> O estimador de `l` e `Q` dá o **mesmo** resultado com o par no centro da caixa e com o par
> **centrado na fronteira periódica**: `10.960705784` contra `10.960705637 nm`,
> `|Δl| = 1.5e−7 nm`, `Q = ∓1.0000` exato nos dois.

**Limites:**
- **L10.1** Fecha o `L5.3` **só para o meu código**. O estimador cego do `AUDIT-002` **não foi
  reexecutado** nesta condição; para ele o `L5.3` continua aberto.
- **L10.2** Um estado, um acoplamento, uma malha. A fronteira testada é a de `x`.
- **L10.3** `L-G` intocado.

## C-11 (de `E004R`, `RF-2`) — a ressonância de breathing SBM, medida com precisão suficiente
> `f_SBM = 17.9609 ± 0.0125 GHz` (janela sinc de 40 ns, resolução `0.025 GHz`, centroide acima
> de meia altura), FWHM `0.65 GHz`.

**Limites:**
- **L11.1 Isto REFINA `C-6` e supera o uso do `18.00 GHz`.** Aquele valor era um **bin** de
  resolução `0.1 GHz`; o `L6.2` já registrava que o acerto contra o "18" do artigo era "mais
  bonito do que é forte". **Daqui em diante, `f_SBM = 17.96`, e quem citar `18.00` está citando
  um bin.** Não contradiz o artigo, que cita valor redondo em texto corrido.
- **L11.2** Protocolo sinc, `α = 0.02`, um ponto de parâmetros.

## C-12 (de `I002`) — a deriva de rede é hipersensível ao estado, e `l` não a parametriza
> A deriva espúria `v_∥` **não é função de `l`**: dois estados de equilíbrio com o **mesmo**
> comprimento de ligação (`11.5934` e `11.5875 nm`, `0.05 %` de diferença) têm
> `v_∥ = 0.730` e `0.432 cm/s` — **41 %**. Os dois diferem `3.2 %` em tamanho de skyrmion
> (`𝒟 = 18.74` contra `18.14e−15 N·s/m`): **amplificação de ~13×**.

**Limites:**
- **L12.1 O `L8.4` CONTINUA ABERTO.** Este claim é o que **refuta a premissa** do teste, não a
  resposta dele. Se os 11 % vêm do estado ou da excitação **segue sem resposta**, e agora com
  uma razão medida para ser difícil: não é separável variando `K₀`.
- **L12.2** A **causa** da força de rede (`L9.1`) segue sem teste. Hipersensibilidade é
  *consistente* com comensurabilidade; consistência não é teste.
- **L12.3** Quatro pontos, um ângulo, 20 ns, e as quatro relaxações **não convergiram**
  (teto de `2×10⁶` iterações). Os `v_∥` são estáveis a `0.02 %`, mas partem de estados não
  plenamente relaxados.
- **L12.4** `L-G` intocado.

---

## Registro de método — por que o `I002` merece aceite tendo falhado o gate
O critério do `I002` estava **bem-formado sob as regras `R1`–`R3`** do `CLAUDE.md` §6.1:
comparação entre duas hipóteses prevendo valores diferentes da mesma grandeza, sem limiar
absoluto, poder medido (`~100×`), convergência checada na **saída**. Ele não deu veredito
porque a **premissa física** era falsa.

**Este é o tipo certo de fracasso**, e distingui-lo dos nove defeitos de desenho é o que evita
que a regra nova vire desculpa para nunca arriscar. Um pré-registro bom não impede que a física
surpreenda — é para isso que ele existe.

## Efeito no estado
Onze missões aceitas com limitações. `E004` segue `REVISION_REQUESTED` **e sua pergunta segue
sem resposta**. `I003` em execução.

## Próximo head/estado
`STATE-2026-08-26-d`

## Próxima decisão humana
**A direção** (`STATE.md` §Próxima decisão, item 2). Doze missões, `L-G` intocado.
E a consulta aos autores, que é ação de Rodrigo.
