# WRITEBACK-024 — cinco missões autorizadas; os autores fora de alcance

Data: 2026-08-27 · Autoridade: Rodrigo

## Decisões humanas (literais)
> "Sobre os dados dos autores, está fora do meu alcance; O que podemos fazer sabendo que o
> Mumax está a disposição?"

> "Autorizo todos os testes discriminados acima"

## 1. O que muda com os autores fora de alcance
`D-1`, `D-2` e `D-3` deixam de estar **aguardando resposta** e passam a ser **ou atacados
daqui, ou abertos para sempre**. O `QUERIES-AUTORES-001.md` continua válido como registro do
que se perguntaria; deixa de ser um plano.

**Consequência de registro:** onde antes se lia "pendente da consulta aos autores", passa a
ler-se **"indecidível daqui, salvo pelo que o segundo solver alcançar"**.

## 2. As cinco missões, e a ordem
Ordenadas por **decisão por custo**, não por importância — as três primeiras são baratas e
cada uma fecha ou desloca alguma coisa; a quarta é a mais valiosa e por isso é a que mais
precisa de escada própria.

| | missão | ataca | custo |
|---|---|---|---|
| 1 | **`A004`** — 𝒟 do estado do mumax3 | `D-1` (o eixo sem expoente) | ~10 min, **sem corrida nova** |
| 2 | **`A005`** — deriva espúria fora do eixo no mumax3 | `L9.1`, `L8.4` | ~30 min |
| 3 | **`A006`** — ramo coaxial em `A_int = 0.12` | `L2.3` (a discrepância mais velha, aberta desde o `R002`) | ~1 h |
| 4 | **`A007`** — dinâmica dirigida | `D-2`, `D-3`, `L14.2` **e a lacuna de `C-6`/`C-7`/`C-14`** | a medir |
| 5 | **`A008`** — malha e contínuo | `L1.1` | horas |

Prefixo `A` em todas: são auditorias por ferramenta independente, linhagem `A002` → `A003`.

## 3. O que esta autorização NÃO dispensa
- **A regra do `CLAUDE.md` §2 continua valendo por missão:** cada pré-registro vai a Rodrigo
  **antes** da execução. "Autorizo todos os testes" autoriza as **missões**; não dispensa a
  leitura dos critérios. Se você quis dispensar também isso, corrija.
- **Aceite** de cada uma continua sendo ato seu.
- Não autoriza ação externa nem freeze.

## 4. Uma coisa que precisa ser dita sobre a `A007`
Ela é a mais valiosa e a mais perigosa. A dinâmica do mumax3 tem convenções que o `A003` **não**
tocou: `alpha`, excitação dependente do tempo, e **passo adaptativo** — diferença real, porque
o nosso RK4 é de passo fixo. Sem escada própria, arriscamos exatamente o que o `relax()` quase
nos fez no `A003`: artefato de ferramenta virando resultado. O pré-registro dela virá separado
e depois das três baratas, de propósito.

## Próximo head/estado
`STATE-2026-08-27-h`
