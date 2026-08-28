# RELEASE-A005R2-ADDENDUM-001 — correção da autoridade declarada

Data: 2026-08-28 · Corrige: `RELEASE-A005R2.md` e a referência de checkpoint em
`LAB/EVIDENCE/A005R2/AI-PROVENANCE.json`

## Correção factual

`RELEASE-A005R2.md` declara “Autorizada por `WRITEBACK-033`”, e o manifesto de proveniência
selado declara o mesmo writeback como revisão e autorização de execução. Isso é incompatível
com o conteúdo literal de `WRITEBACK-033.md`:

- o pedido humano registrado é “Podemos retomar o trabalho iniciado ontem”;
- o writeback interpreta o pedido como retomada da execução de `DATA-001` autorizada em
  `WRITEBACK-031`;
- o próprio writeback afirma que o pedido “não amplia o escopo” e que `DATA-001` não avalia,
  sela ou promove `A005R2`.

Logo, `WRITEBACK-033` **não autoriza `A005R2`**. Nenhum outro writeback de autorização foi
localizado. O release e a proveniência material permanecem imutáveis, mas suas referências de
autoridade estão documentalmente superadas por este addendum e por `WRITEBACK-034`.

## Efeito metodológico

- Os bytes e hashes de `A005R2` continuam preservados como ocorrido material.
- A execução é `PROCEDURALLY_UNAUTHORIZED`; isso não significa que os números sejam falsos,
  mas impede gate válido, promoção de claim ou aceite até decisão humana específica.
- `RELEASE-A005R2.md` continua sendo relato do que ocorreu, não autoridade para o ocorrido.
- O diretório foi selado sem `EVIDENCE-MANIFEST.json`, obrigatório para evidência nova por
  `MISSION-DATA-001`/`DH-3`; o verificador recursivo o classifica `SEALED_CORRUPT` por
  metadado obrigatório ausente, embora todos os hashes listados confiram.
- Nenhum arquivo em `LAB/EVIDENCE/A005R2/` foi editado, removido, restaurado ou resselado.

## Decisão humana ainda necessária

Rodrigo pode decidir separadamente como tratar a execução: rejeitar por processo, preservar
apenas como artefato, ou autorizar uma missão futura limpa. Este addendum não toma essa decisão
e não valida retroativamente a execução.

