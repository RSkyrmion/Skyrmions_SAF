# WRITEBACK-003 — Autorização da reprodução estrutural da Eq. (S1)

Data: 2026-08-21 · Autoridade: Rodrigo (instrução explícita no chat)

## Missão relacionada
`MISSION-R002` (nova). Impacta a decisão pendente sobre `MISSION-R001`.

## Decisão humana (literal)
> "Aceito sua recomendação"

Contexto da recomendação aceita: mapear a linha de centro da região de estabilidade no plano
(A_int, K₀) com o `saf.cu` já existente, comparando com a Eq. (S1) do material suplementar
(`K₀ = 0.65 − 2.5·A_int`), **antes** de instalar qualquer solver de terceiros.

## O que muda no estado atual
- `MISSION-R002` criada e passa direto a `AUTHORIZED`.
- `MISSION-A001` (auditoria com mumax3) permanece `PROPOSED` e **não autorizada**.
  Se ainda for desejada depois, a recomendação registrada é OOMMF no lugar do mumax3, pelo
  acoplamento de superfície areal nativo (`Oxs_TwoSurfaceExchange`, J/m²), que elimina o
  risco de tradução SL-A1.

## O que NÃO está autorizado por este writeback
- Auditoria do código com o `codex` (ou qualquer outro agente externo). Rodrigo perguntou
  *"o que acha?"* — isso é pedido de opinião, não autorização. Enviar o PDF do PRL e o
  `saf.cu` a um serviço de terceiros é **ação externa** (INV-16) e precisa de autorização
  explícita e separada. O desenho proposto está no chat, aguardando decisão.
- Instalar ou compilar qualquer solver.

## Claims/evidências afetados
Nenhuma evidência existente é invalidada. `RELEASE-R001.md` permanece íntegro e governante
para o que ele afirma.

**Ligação de impacto (Core §9):** R002 roda enquanto R001 está `TERMINAL_AWAITING_HUMAN`.
Se R002 revelar um erro de leitura do artigo, o resultado de R001 é **materialmente afetado**
e a decisão de aceite muda. É exatamente por isso que rodar R002 antes de aceitar R001 é
coerente, e não prematuro.

## Próximo head/estado
`STATE-2026-08-21-e`

## Próximo passo autorizado
Executar `MISSION-R002` até o gate `G-R002`. Nada além disso.
