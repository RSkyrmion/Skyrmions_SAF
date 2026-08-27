# WRITEBACK-015 — aceite de `E003` e `I001`; **revisão** de `E004`

Data: 2026-08-26 · Autoridade: Rodrigo

## Decisão humana (literal)
> "E003 aceito com limitações; I001 aceito com limitações; E004 é necessário responder ao
> questionamento apontado, portanrto gostaria de revisá-lo e todas pendências resolvidas"

## Efeito formal
| missão | antes | agora |
|---|---|---|
| `MISSION-E003` (+ `ADDENDUM-001`) | `PENDING` | **`ACCEPTED_WITH_LIMITATIONS`** |
| `MISSION-I001` | `PENDING` | **`ACCEPTED_WITH_LIMITATIONS`** |
| `MISSION-E004` (+ `ADENDO-001`) | `PENDING` | **`REVISION_REQUESTED`** |

`REVISION_REQUESTED` é estado novo neste laboratório. Significa: **o release fica como está**
(`RELEASE-E004.md` não se edita, §3), o material segue selado e citável, mas a missão **não
está aceita** e sua pergunta central segue **sem resposta**. Uma missão de revisão,
`MISSION-E004R`, a completa.

---

# Claims aceitos — continuação de `WRITEBACK-007`, `-009`, `-011`

## C-8 (de `MISSION-E003`) — a deriva segue a ligação
> A deriva de autopropulsão acompanha a **ligação**, não um eixo da malha:
> `dφ_drift/dθ_bond = +1.0201`, contra `+1` (`H_ligação`) e `0` (`H_rede`), medido em dois
> ângulos fora dos espelhos da rede quadrada.

**Limites:**
- **L8.1** Fecha o `L7.2` do `C-7`, mas o que fica testado é "acompanha a ligação em **dois**
  ângulos além de zero, no modo **SBM**" — **não** "em qualquer ângulo", como o artigo afirma.
- **L8.2** O gate passou **porque a grandeza discriminante converge** (`dφ/dθ` estável em
  `1.007–1.026` em três janelas), e **não** pela leitura favorável da ambiguidade do §4.3 do
  pré-registro. O release original apoiou o gate nessa leitura — escolher a leitura depois do
  dado — e o `ADDENDUM-001` corrigiu. A ambiguidade em si fica registrada, **não reparada**.
- **L8.3** **Artefato de comensurabilidade descoberto e não caracterizado:** fora do eixo a
  relaxação não converge (2×10⁶ iterações, torque em `1.26e−5 T`) e há deriva de `0.917 cm/s`
  ao longo da ligação. **Não contamina o `E002`**, que roda em `θ = 0`, comensurável.
- **L8.4** **~10 % do desvio de perpendicularidade (`0.8°`) sem explicação**, sistemático nas
  quatro medidas. Não arredondado para zero.
- **L8.5** `EO-0.1` comparou `l_eq` que, fora do eixo, **não é comprimento de equilíbrio**.
- **L8.6** `L-G` intocado: removeu confundimento **interno**, não verificou nada.

## C-9 (de `MISSION-I001`) — a régua está limpa
> A deriva espúria de `0.917 cm/s` é **movimento real e rígido** da magnetização, não viés do
> estimador: com a magnetização congelada, 10 001 chamadas dão `2e−11 cm/s` e deslocamento
> acumulado de `0.0000 pm`. Três localizadores independentes — um deles **sem carga
> topológica** — concordam em `0.91745 cm/s` na corrida viva.

**Limites:**
- **L9.1** A **causa física** do movimento segue conjectural. Força tipo Peierls virando deriva
  giroscópica é hipótese **não testada**.
- **L9.2** Um estado, um ângulo, um acoplamento. Não é caracterização geral da régua.
- **L9.3** **`L5.3` intocado:** a régua sob travessia da fronteira periódica segue **não
  testada**; o `I001` não chegou perto disso.
- **L9.4** `L-G` intocado. Instrumento próprio testado contra si mesmo em outra condição
  **não é** verificação independente. O `AUDIT-002` segue sendo a única checagem cega da régua.

**O que a concordância exata significa** (e é fácil errar ao recontar): sob translação rígida
`m(r,t) = m₀(r−vt)`, todo funcional do tipo centroide dá a mesma velocidade **por identidade**.
A igualdade em quatro casas é assinatura de **translação rígida**, não de sorte.

---

## `E004` — o que a revisão precisa responder
O `EF-0` declarou **plana** uma curva com fator 7 de contraste, porque a "dispersão entre
janelas" que escolhi mede o **decaimento transiente**, sistemático e comum às nove frequências
(razão `0.44` em todas; dispersão de **forma** real: `3.5 %`). Os dois caminhos de
indeterminação — `EF-0` e o `σ(f_pico)` da cláusula `A2` — vêm da **mesma causa única**.

Pré-registro da revisão em `LAB/MISSIONS/MISSION-E004R.md`.

## Escopo de "todas pendências resolvidas" — leitura registrada, e convite a corrigir
Nem todas as pendências deste laboratório são resolvíveis por simulação minha. Registro o
recorte que li, para você corrigir se for outro:

| pendência | na revisão? | por quê |
|---|---|---|
| `EF-1` indeterminado | **SIM** | é a pergunta central |
| `L7.3` — magnitude não estacionária | **SIM** | corridas de 300 ns resolvem, e removem a causa do defeito do `EF-0` |
| pico da propulsão (17.78) vs breathing (18.00) | **SIM** | exige remedir o breathing a `0.025 GHz` |
| `L5.3` — régua na travessia da fronteira PBC | **SIM** | teste barato, nunca feito |
| `L9.1` — causa do artefato de comensurabilidade | **PARCIAL** | refino de malha discrimina "força de rede"; não fecha a causa |
| `L8.4` — os 10 % (`0.8°`) do `E003` | **NÃO** | exigiria separar contaminação no estado *excitado*; não sei fazer barato |
| `L2.3` — ramo coaxial em `A_int = 0.12` | **NÃO** | outra física, outro ponto do diagrama; missão própria |
| `L1.1` — malha e o contínuo | **NÃO** | missão própria, custo alto |
| `D-1`, `D-2`, `D-3` | **NÃO** | dependem dos autores; **ação sua** |
| **`L-G`** | **NÃO** | exige **ação de sistema** (compilar DMI Cnv/PBC no OOMMF) ou **externa** (etapa 2 do `AUDIT-001`). Nenhuma autorizada |

**`L-G` continua sendo o limite acima de todos, e nenhuma simulação minha o move.**

## Próximo head/estado
`STATE-2026-08-26-a`
