# WRITEBACK-004 — Execução da sequência recomendada

Data: 2026-08-21 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Execute a sequencia recomendada"

Sequência a que se refere, proposta no chat:
1. teste de bacia em A_int = 0.12;
2. autorizar (ou não) a auditoria externa com `codex`;
3. aceitar R001 e R002 com limitações;
4. `MISSION-A001` dorme como `PROPOSED`.

## Interpretação registrada — e seus limites

**Passo 1 — executado.** Ver `RELEASE-R002-ADDENDUM-001.md`. A hipótese de efeito de bacia
foi **refutada**; e a extração numérica da Fig. 5(c) (que o passo 1 motivou) reduziu
substancialmente a discrepância aberta e tornou quantitativo um teste antes qualitativo.

**Passo 2 — tratado como AUTORIZADO.** Ação externa: envio do texto do PRL e, na etapa 2 da
auditoria, do `saf.cu`, para o serviço da OpenAI via `codex`.
Base da interpretação, registrada para ser auditável:
(i) Rodrigo **propôs** o Codex por iniciativa própria; (ii) eu sinalizei explicitamente que o
envio a terceiros era decisão dele; (iii) eu recomendei fazer; (iv) ele instruiu executar a
sequência recomendada. Isso é reafirmação após a ressalva, não autorização inferida de
silêncio. **Se a leitura estiver errada, corrija — a etapa cega já foi enviada.**

**Passo 3 — NÃO executável por mim.** Aceite é, por definição, ato humano (INV-02, INV-03).
"Execute a sequência" não pode significar "registre o aceite em meu nome" sem esvaziar a
distinção que sustenta todo o método. Fica **pendente de decisão explícita**.

**Passo 4 — nada a fazer.** `MISSION-A001` já está `PROPOSED`.

## Desenho da auditoria (para reprodutibilidade)
- **Etapa 1, cega:** diretório isolado contendo **apenas** o texto do artigo. Sem `saf.cu`,
  sem `MISSION-*.md`, sem `RELEASE-*.md`. Sandbox somente-leitura. Objetivo: obter uma
  derivação independente dos campos efetivos, sem âncora nos meus resultados.
  Discriminantes: (a) o papel da espessura `d` no campo interlayer; (b) a convenção de sinal
  do DMI e o emparelhamento quiralidade↔camada.
- **Etapa 2:** `saf.cu` + artigo, ainda **sem** missão nem release.

Prompt da etapa cega preservado em `EVIDENCE/AUDIT-001/blind_prompt.txt`.

## O que esta auditoria pode e não pode fazer
Pega erro de sinal, de fator, de stencil e de unidade. **Não** pode dizer se 10.96 nm está
certo. Auditoria de código não é validação numérica.

## Próximo head/estado
`STATE-2026-08-21-g`

## Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar **R001** e **R002**, separadamente.
