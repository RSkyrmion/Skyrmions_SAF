# WRITEBACK-011 — ACEITE COM RESSALVAS de `MISSION-E002`

Data: 2026-08-25 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Peço que aceite com ressalvas e deixe registrado os motivos que levaram a divergência dos
> dados para posteriormente eu verificar junto aos autores do trabalho a maneira correta de
> interpretar os dados ou solicitar os dados que geraram o gráfico"

`human_acceptance` de `MISSION-E002` passa de `PENDING` a **`ACCEPTED_WITH_LIMITATIONS`**.
Cobre `RELEASE-E002.md` e o `RELEASE-E002-ADDENDUM-001.md`. Os `RELEASE-*` não foram editados
e continuam dizendo `PENDING` no corpo; este writeback é a autoridade que supersede.

**Aceite dado apesar de o gate `G-E002` NÃO ter passado**, como no `A002`. O aceite é dos
itens que sobreviveram, não da missão como desenhada.

## Ação decorrente, e de quem é
A segunda metade da instrução é uma tarefa: registrar as divergências de forma que Rodrigo
possa levá-las aos autores. Feito em **`LAB/QUERIES-AUTORES-001.md`**.

**Consultar os autores é ação de Rodrigo, não minha.** Escrever a qualquer pessoa ou serviço
fora desta máquina é ação externa (INV-16) e continua **não autorizada** — a instrução diz
*"eu verificar junto aos autores"*, e eu a leio literalmente. Preparei o dossiê; não enviei
nada e não vou enviar.

## O que este aceite NÃO faz
- **Não é freeze.** Nada está congelado.
- **Não fecha `L-G`.**
- **Não repara** nenhum dos quatro critérios mal desenhados. Eles seguem falhados no registro.
- **Não resolve** as divergências `D-1`, `D-2` e `D-3`; ao contrário, o aceite as declara
  **abertas e pendentes de consulta externa**.
- **Não autoriza** missão nova (`E003`, `E004`, o teste fora do eixo de simetria), nem a
  etapa 2 do `AUDIT-001`, nem compilar extensão para o OOMMF.

---

# Claim aceito, com seus limites — continuação de `WRITEBACK-007` e `-009`

## C-7 (de `MISSION-E002`) — a autopropulsão
> Uma re-implementação independente do PRL 135, 086701 **produz a autopropulsão do par de
> skyrmions** no acoplamento fraco: deriva perpendicular à ligação sob os dois modos, com
> `v_sp = 3.54 cm/s` sob SBM e `2.03 cm/s` sob ABM, contra alvos de `3.50` e `2.03 cm/s`
> extraídos da Fig. 2 **antes de qualquer corrida**; e com a assinatura harmônica `ω` do modo
> SBM **medida** no espectro de `l(t)`.

**Limites que viajam junto, obrigatoriamente:**
- **L7.1 O gate NÃO passou.** `PV-0` (tensor 𝒟) e `PV-1` (piso de ruído) falharam. Este
  aceite é dos itens que sobreviveram.
- **L7.2 `EP-1` passou por SIMETRIA, não por dinâmica.** `v_∥ = 0` exato é **forçado** pela
  simetria de troca-de-camadas da condição inicial: o critério **não podia falhar**. A
  afirmação do artigo — deriva perpendicular *seja qual for* a orientação da ligação — **não
  foi testada**. É o limite mais fácil de perder ao recontar este resultado.
- **L7.3 A corrida SBM não atingiu o estacionário** em `v_⊥` (ainda decaía `0.042 cm/s` por
  janela de 25 ns aos 200 ns). O `3.54` é uma **travessia**, não um platô medido. A
  extrapolação geométrica (`3.498`) é **exploratória** e não substitui o número.
- **L7.4 Os alvos são extrações de figura**, pelo procedimento declarado no §2 do
  pré-registro, com 1 px = `0.11` e `0.011 cm/s`. **Não** são valores tabelados pelos autores.
  O acordo defensável é "dentro da precisão de leitura do alvo", não os 1,1 % / 0,1 % brutos.
- **L7.5 `EP-4` no ABM está `NÃO MEDIDA`**, por condicional do próprio pré-registro. O pico
  limpo em `2f_drive` existe no dado e é **observação**, não critério cumprido.
- **L7.6 Quatro dos critérios estavam mal desenhados** (`PV-0`, `PV-1`, a condicional do
  `EP-4`, a checagem de poder de `EP-2`/`EP-3`), sempre do mesmo modo: limiar absoluto contra
  referência que não o sustentava. Registrados, **não reparados**.
- **L7.7 O transiente NÃO reproduz a Fig. 2(a).** Só o valor tardio se aproxima. Ver `D-3`.
- **L7.8** Um único ponto de parâmetros, malha de 1 nm, caixa de 100 nm. A causa física de
  `L1.1` (a malha resolve `Δ = 5 nm` apenas 5×) vale aqui igual.
- **L7.9 `L-G` INTOCADO.** Meu código, meu equilíbrio, minha régua. O `E002` acrescenta um
  observável; **não** acrescenta verificador independente. Sexta camada verificada, `L-G` no
  mesmo lugar.
- **L7.10 Três divergências ficam ABERTAS** e explicitamente **não resolvidas por este
  aceite**: `D-1` (fator do eixo 𝒟), `D-2` (os `l̄` trocados de painel), `D-3` (a forma do
  transiente). Dossiê em `LAB/QUERIES-AUTORES-001.md`.

## Efeito no estado
Sete missões executadas, todas `ACCEPTED_WITH_LIMITATIONS`. Fase 2 segue aberta.
**Nova pendência que não é decisão minha nem missão:** a consulta de Rodrigo aos autores.
Enquanto ela não voltar, `D-1`, `D-2` e `D-3` são **indecidíveis daqui** e assim ficam
declaradas.

## Próximo head/estado
`STATE-2026-08-25-f`

## Próxima decisão humana
Nenhuma pendente **neste laboratório**. A ação pendente é externa e é de Rodrigo: levar
`QUERIES-AUTORES-001` aos autores. O que voltar de lá entra por writeback novo.
