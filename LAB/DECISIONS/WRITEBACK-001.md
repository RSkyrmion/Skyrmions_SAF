> **[SUPERSEDED_FOR_CURRENT_STATE — 2026-08-21]**
> Este documento **não governa** o estado atual. Foi substituido por `WRITEBACK-002.md`.
> Preservado integralmente como histórico as-run; nada abaixo desta linha foi editado.
> Motivo da supersessao: registrava escolha de ferramenta sem autoridade humana, e deltas
> (ladder R001->R005, criterio de aceite) que nunca existiram no `STATE.md`.

# WRITEBACK-001 — Autorização do alvo de reprodução

Data: 2026-08-21 · Autoridade: Rodrigo (instrução explícita no chat)

## Missão relacionada
`MISSION-R001` e o programa de reprodução como um todo.

## Decisão humana
> "Reproduzir o Phys Rev Lett e o material suplementar fornecidos."

Interpretação registrada: o alvo de reprodução é PRL **135**, 086701 (2025) **mais** o
Supplemental Material, no seu escopo completo (Figs. 1–6 + S1–S5 + vídeos).

## O que muda no estado atual
- Artigo de referência passa de `PROPOSTO` para `ACEITO` como alvo.
- `MISSION-R001` passa de `PROPOSED` para `AUTHORIZED`.
- Programa de reprodução em escada (R001→R005) registrado no `STATE.md`.
- Ferramenta fixada por decisão técnica (não humana): mumax3 + GPU local.
  Rodrigo não respondeu à pergunta 2; a escolha foi feita a partir do ambiente detectado
  (RTX 4050, CUDA 11.8, Go 1.19, rede disponível) e é **reversível** sem custo.

## O que permanece histórico
A pergunta em aberto sobre a convenção de K0 (`QA-01`) **foi resolvida** — ver abaixo — mas
o registro de que ela esteve aberta permanece, junto com o motivo do fechamento.

## Claims/evidências afetados
- `QA-01` fechada por leitura da Eq. (A3): o Hamiltoniano simulado é
  `H = ∫dS[E1 d + E2 d + Aint m1·m2]` e (A4) lista apenas exchange, anisotropia, Zeeman e DMI.
  **Não há termo de demagnetização no Hamiltoniano simulado.** É isso que "K0 accounts for
  ... demagnetization effects" significa: o demag está absorvido em K0.
  → Consequência prática: usar `Ku1 = K0 = 0.6 MJ/m³` e `EnableDemag = false`.
    O valor nu de Ku nunca é necessário, e o sinal de `±½μ0Ms²` no artigo não afeta a reprodução.
- Com `QA-01` fechada, o critério de aceite numérico de R001 pôde ser fixado.

## Nova questão aberta que substitui QA-01
- **[QA-02] Unidades do acoplamento interlayer.** `Aint m1·m2` é um acoplamento bilinear
  **areal** (J/m²). O mumax3 não tem termo areal nativo: `ext_scaleExchange` escala a
  **rigidez de Heisenberg** (J/m) entre células vizinhas. A conversão precisa ser derivada
  e verificada por energia. Ver `MISSION-R001.md`, gate `parameter_check`.

## Próximo head/estado
`STATE-2026-08-21-b`

## Próximo passo autorizado
Executar `MISSION-R001` até o gate `G-R001`. Nada além disso.
