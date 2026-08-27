# WRITEBACK-005 — Reinício da auditoria externa cega (AUDIT-001)

Data: 2026-08-24 · Autoridade: Rodrigo

## Decisão humana (literal)
> "O codex não terminou a auditoria. Preciso iniciá-la do zero."

## O que isto resolve
Fecha a pendência factual aberta em `STATE-2026-08-21-g`: a etapa cega registrada como
*"já enviada"* no `WRITEBACK-004` **não produziu resultado**. O `EVIDENCE/AUDIT-001/` tinha
só o `blind_prompt.txt` porque não havia resposta para guardar.

**Causa mais provável, registrada:** a corrida original não passou `-o/--output-last-message`
e/ou estourou o tempo da chamada. Nesta corrida ambos foram corrigidos: `-o` para a resposta
final, `--json` para o trace, e teto de 10 min.

## O que fica autorizado por este writeback
**Somente a etapa 1 (cega)** de `AUDIT-001`: enviar o **artigo publicado** (texto extraído
+ imagem da página do End Matter) ao serviço da OpenAI via `codex`. Executada; ver
`RELEASE-AUDIT-001.md`.

## O que continua NÃO autorizado
- **Etapa 2** — enviar o `saf.cu` a terceiro. *"Iniciá-la do zero"* é ordem de reiniciar a
  auditoria, não de escalar o que sai da máquina. Código é ação externa materialmente maior
  que artigo publicado, e precisa do seu próprio sim.
- `MISSION-A001` (solver independente; OOMMF recomendado no lugar do mumax3).
- Envio do material suplementar.

## Desvio de desenho em relação ao WRITEBACK-004 — declarado
O desenho original mandava só `paper.txt`. Acrescentei a imagem da página 8 (End Matter),
porque a extração do PDF reencodifica e desloca glifos matemáticos: a PRL codifica ∫→`Z`,
=→`¼`, +→`þ`, parênteses→`ð…Þ`, e na saída em duas colunas o `∫` da Eq. (A3) cai uma linha
acima do resto da equação. Auditar uma derivação sobre equações assim é auditar outra coisa.
O prompt declara que, em conflito entre texto e imagem, **a imagem manda**.
Escopo do que saiu da máquina: inalterado — só o artigo.

## Próximo head/estado
`STATE-2026-08-24-h`

## Próxima decisão humana
Inalterada e ainda pendente: aceitar / aceitar-com-limitações / revisar / rejeitar **R001**
e **R002**, separadamente. `AUDIT-001` etapa 1 é insumo para essa decisão, não substituto.
Separadamente: autorizar ou não a etapa 2.
