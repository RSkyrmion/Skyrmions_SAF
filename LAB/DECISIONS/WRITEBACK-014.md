# WRITEBACK-014 — execução do `E004` sem aprovação intermediária

Data: 2026-08-25 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Preciso que as simulações E004 rodem na sequencia, sem minha aprovação, pois irei para casa
> e este computador está no locald e trabalho"

## O que isto autoriza — e o que NÃO autoriza
**Autoriza:** executar o lote inteiro do `E004` (8 corridas, ~2,6 h) **sem parar para relatar
entre corridas**, e escrever o `RELEASE-E004` ao final. A missão em si já estava autorizada por
`WRITEBACK-013`; o que se acrescenta aqui é a dispensa do relato intermediário.

**NÃO autoriza, e continua exigindo sim explícito e separado:**
- **Aceite** de `E003`, `I001` ou `E004`. Aceitar é ato exclusivamente humano (§2), e nenhum
  gate que passe substitui isso. Os três ficam `PENDING`.
- Missão nova além do `E004` (`E005` estocástica não está proposta).
- Ação externa (INV-16) e ação de sistema (compilar extensão do OOMMF).
- Freeze.
- Apagar qualquer coisa em `EVIDENCE/` ou `ARCHIVE/`.

**Leitura registrada:** "rodem na sequência, sem minha aprovação" é dispensa de **relato
intermediário de uma missão já autorizada**, não autorização em branco. Se você quis mais que
isso, corrija.

## Medidas tomadas por causa da ausência
1. **O lote roda destacado (`setsid`/`nohup`)**, para sobreviver ao encerramento da sessão e ao
   logout. Log em `LAB/EVIDENCE/E004/RUN-LOG.txt`.
2. **O script de análise foi escrito ANTES do lote** e está selado junto com o pré-registro.
   Nenhuma decisão de análise fica para depois de ver o dado.
3. **O `STATE.md` foi atualizado ANTES de o lote terminar**, declarando o `E004` como
   *em execução, não supervisionado*, com instruções de retomada a frio — para o caso de esta
   sessão terminar antes do fim das corridas.

## Próximo head/estado
`STATE-2026-08-25-i`

## Próxima decisão humana
Ao voltar: aceitar / aceitar-com-limitações / revisar / rejeitar `E003`, `I001` e `E004`.
E segue pendente a consulta externa aos autores (`QUERIES-AUTORES-001.md`).
