# ADDENDUM-001 de MISSION-DATA-001 — retomada após atividade concorrente

Estado: **`EXECUTION_NOTE — missão autorizada por WB-031`** · Data: 2026-08-28

Na retomada de `DATA-001`, o filesystem não correspondia mais ao snapshot basal produzido em
2026-08-27. Este adendo preserva a separação temporal; não atribui autoria e não autoriza outra
missão.

## Mudanças observadas depois do snapshot basal

1. `LAB/EVIDENCE/A005R/RUN-LOG.txt` foi novamente regravado em 2026-08-27 16:07:39 -03:00.
   Seu SHA-256 observado passou a
   `6f9f0ae2731a40a994516ce63dd248041ac8f0d0b83c90948cc20929bc1683bb`; o hash selado
   continua `f9e34a925535691e6aff479842b66e9fe50d10f8b13707779b3c21e247015a16`.
2. `LAB/EVIDENCE/A003/__pycache__/ovf.cpython-311.pyc` surgiu em 2026-08-27 16:10:20 -03:00,
   fora do selo, com SHA-256
   `843eaf519d5b786ec0b551fbc18ecd93e3e7ee1ebc3fbfa4bc9194cb6b31d48f`.
3. `LAB/EVIDENCE/A005R2/` foi criado em 2026-08-28 com inputs, scripts, quatro checkpoints,
   log e proveniência, mas sem `SHA256SUMS.txt`, release ou writeback de autorização encontrado
   no ledger disponível. O diretório é classificado apenas como `UNSEALED`; seu mérito e sua
   autoridade científica não são avaliados por `DATA-001`.

## Baseline de retomada

Antes de selar `DATA-001`, a fotografia corrente tem 21 diretórios de primeiro nível, 18
manifests, 15 `SEALED_VALID`, 2 `SEALED_CONTAMINATED`, 1 `SEALED_CORRUPT` e 3 `UNSEALED`.
Depois do selo novo, `DATA-001` deve migrar de `UNSEALED` para `SEALED_VALID`, sem qualquer
outro estado mudar.

## Regra para a repetição do gate

A primeira avaliação `GATE-RESULTS.json` permanece `FAIL`: seu `DA-10` usou comparação textual
que ignorou a marcação Markdown do ledger. A repetição pode corrigir somente o avaliador e
deve ser registrada em arquivos novos `*-R1`, acompanhada de manifesto/proveniência aditivos.
Ela passa `DA-7` apenas se nenhum arquivo preexistente fora de `DATA-001` mudar durante a
repetição. O drift concorrente acima continua explícito e não é normalizado.

