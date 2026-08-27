# WRITEBACK-019 — ACEITE COM LIMITAÇÕES de `MISSION-I003`

Data: 2026-08-26 · Autoridade: Rodrigo

## Decisão humana (literal)
> "I003: Aceitar com limitações"

`human_acceptance` de `MISSION-I003` passa de `PENDING` a **`ACCEPTED_WITH_LIMITATIONS`**.
Gate `G-I003` **passou**. Primeiro pré-registro lido e liberado por Rodrigo **antes** da
execução, sob a regra do `CLAUDE.md` §2.

---

## C-13 (de `MISSION-I003`) — o desligamento em malha fina foi o passo de tempo
> Na malha de `0.5 nm`, o par de skyrmions **permanece ligado** quando o passo de tempo é
> escalado por `a²` (`dt = 2.5 fs`): `l = 10.8483 nm` **constante em quatro casas decimais**
> ao longo de 4 ns, `Q = ∓1.0000`. Com `dt = 10 fs` — o passo que serve à malha de `1 nm` — o
> par se desliga (`l: 10.85 → 12.39 nm`). O `RF-4` inválido do `E004R` foi **erro meu de passo
> de tempo, não física**.

**Limites:**
- **L13.1 NÃO fecha o `RF-4` nem o `L9.1`.** A redução de `4.5×` na deriva espúria ao refinar
  a malha (`0.91745 → 0.20265 cm/s`) é **exploratória e não pré-registrada** — o §6 do
  pré-registro declarou essa medida fora de escopo. Dois pontos de malha não estabelecem lei
  de escala, a janela é de 4 ns contra os 20 ns do `E003`, e o `C-12` mostrou que `v_∥` é
  hipersensível a coisas que o refino também move. **É consistência, não teste.**
- **L13.2** A relaxação a `0.5 nm` **não convergiu** (teto de `2×10⁶` iterações, torque
  `2.755e−6 T`). A comparação é casada — as duas corridas partem do mesmo estado — mas esse
  estado não é equilíbrio pleno.
- **L13.3** Um ângulo (`θ = 30°`), um acoplamento, 4 ns, duas malhas.
- **L13.4** `L-G` intocado.

**O que este claim vale, honestamente:** ele conserta um erro **meu**. Melhora o registro e
descarta o desfecho ruim — se `H_física` tivesse vencido, o estado ligado não sobreviveria a
`0.5 nm` sob LLG e o `L1.1` estaria em apuros. Mas **não é avanço sobre o artigo nem sobre o
`L-G`**. É higiene, e deve ser recontado como tal.

## Consequência de método, promovida ao `CLAUDE.md` §8
**`dt` tem de escalar com `a²`.** `B₀ = 2A/(M_s a₀²)` vai de `51.7` para `206.9 T` ao refinar
de `1.0` para `0.5 nm`. Nenhum resultado aceito está contaminado — nenhuma missão até aqui
refinou malha em **dinâmica** — mas qualquer ataque futuro ao `L1.1` com LLG cai nesta
armadilha. Escrito no §8 como armadilha **medida**, não suposta.

## Efeito no estado
**Doze missões aceitas com limitações.** `E004` segue `REVISION_REQUESTED`, e sua pergunta
segue sem resposta. **Nenhuma missão pendente.**

## Próximo head/estado
`STATE-2026-08-26-e`

## Próxima decisão humana
**A direção**, e é a única que resta. Doze missões, `L-G` exatamente onde estava na primeira.
E a consulta aos autores, que é ação de Rodrigo.
