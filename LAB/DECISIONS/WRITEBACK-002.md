# WRITEBACK-002 — Ratificação do alvo, escopo e ferramenta

Data: 2026-08-21 · Autoridade: Rodrigo (instrução explícita no chat, em resposta às três
perguntas abertas do head `STATE-2026-08-21-a`)

## Missão relacionada
`MISSION-R001`

## Decisão humana (literal)
> "1 - PRL disponível na pasta é o artigo a ser reproduzido. 2 - Fazer a reprodução mais
> barata; 3 - Escreveremos um código em cuda para atacarmos o problema"

## O que muda no estado atual
1. **Alvo ratificado.** PRL **135**, 086701 (2025) (`c2y9-3cc9.pdf`) passa de `PROPOSTO`
   para `ACEITO` como artigo de referência do laboratório.
2. **Escopo fixado como o mais barato.** `MISSION-R001` permanece restrita a T = 0, sem
   excitação, acoplamento fraco, um único escalar de saída (l). Figs. 3–6, modos de
   breathing, temperatura finita e autopropulsão continuam **fora de escopo**.
3. **Ferramenta fixada por decisão humana:** código CUDA próprio. Isto **substitui** a
   escolha por mumax3, que havia sido feita sem autoridade humana (ver supersessão abaixo).
4. `MISSION-R001` passa de `PROPOSED` para `AUTHORIZED`.

## O que permanece histórico
- `WRITEBACK-001` é **SUPERSEDED_FOR_CURRENT_STATE** por este documento. Ele não é apagado
  nem corrigido. Motivo da supersessão: registrava como estado (a) uma escolha de ferramenta
  explicitamente marcada no próprio texto como *"decisão técnica (não humana)"*, (b) um
  programa R001→R005 que nunca existiu no `STATE.md`, e (c) uma ampliação do escopo para
  "Figs. 1–6 + S1–S5 + vídeos" que contradiz o escopo da própria missão.
- **A parte válida de `WRITEBACK-001` sobrevive por mérito próprio, não por herança:** o
  fechamento de `QA-01` é uma leitura verificável da Eq. (A4) e foi reconfirmado neste chat
  por extração direta do PDF. `K = K0 = 0.6 MJ/m³`, sem termo de demagnetização.
- `QA-02` (conversão de `Aint` areal para `ext_scaleExchange` do mumax3) fica **DISSOLVIDA**,
  não resolvida: era um artefato da ferramenta abandonada. Ver `MISSION-R001.md`.

## Claims/evidências afetados
Nenhuma evidência material existe ainda. `LAB/EVIDENCE/` está vazio. Nada a requalificar.

## O que este writeback NÃO contém
Derivações do executor (fator 1/d do campo interlayer, discretização 2D, tolerância numérica)
não estão aqui. Elas não são decisão humana; vivem no semantic lock de `MISSION-R001.md` e
respondem por evidência, não por autoridade.

## Próximo head/estado
`STATE-2026-08-21-b`

## Próximo passo autorizado
Executar `MISSION-R001` até o gate `G-R001`. Nada além disso.
