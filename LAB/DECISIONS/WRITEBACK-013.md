# WRITEBACK-013 — `MISSION-I001` e `MISSION-E004` autorizadas

Data: 2026-08-25 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Faça a ressalva 1 proposta e na sequencia implemente E004"

## O que fica autorizado, e a ordem
1. **`MISSION-I001`** — a "ressalva 1" do `E003`: separar **viés do rastreador de CTC** de
   **movimento real** na deriva espúria de `0.917 cm/s` medida fora do eixo.
2. **`MISSION-E004`** — varredura de frequência, `v_sp(f)` (Fig. 3), **na sequência**.

Ambas incluem derivar binário do código selado, compilar e rodar — ação local.

## Prefixo novo: `I` de instrumento
`I001` não é reprodução (`R`), extensão (`E`) nem auditoria por ferramenta independente
(`A`/`AUDIT`). Ela caracteriza **o meu próprio instrumento de medida**. O `AUDIT-002` validou a
régua contra um estimador cego, mas sobre **estados estáticos selados**; o `L5.3` registrou que
o comportamento dela em outras condições **não foi testado**. `I001` testa uma propriedade
**dinâmica** da régua que nenhuma missão cobriu: se ela deriva quando chamada repetidamente.

## Por que esta ordem importa
Se o `0.917 cm/s` for viés do estimador, o problema **não é do `E003`** — é da régua, e a régua
entra em tudo, inclusive no `C-1`. Por isso ela vem antes do `E004`.

## O que este writeback NÃO faz
- **Não é aceite** do `E003`, que segue `PENDING`.
- **Não autoriza** `E005` (estocástica), etapa 2 do `AUDIT-001`, nem extensão do OOMMF.
- **Não é freeze**, **não fecha `L-G`**, **não resolve** `D-1`/`D-2`/`D-3`.

## Próximo head/estado
`STATE-2026-08-25-h`
