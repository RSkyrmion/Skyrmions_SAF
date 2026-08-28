# MISSION-STORAGE-001 — reduzir o acervo sem apagar evidência nem história de falha

Estado: **`PROPOSED — NÃO AUTORIZADA A EXECUTAR`** · Data: 2026-08-28  
Origem: proposta de redução do acervo após `DATA-001`, revisada por Rodrigo em seis pontos.  
Regime: migração de representação, sem mudança de claim científico.

> **Pré-registro.** Este texto precisa ser lido por Rodrigo antes de qualquer empacotamento,
> restauração de teste ou validação (`CLAUDE.md` §2). A autorização da execução técnica não
> autoriza desincorporação. Apagar, mover, substituir, restaurar ou normalizar qualquer alvo
> em `LAB/EVIDENCE/` exige um segundo writeback, posterior aos resultados, com lista literal
> dos alvos e exceção estreita aos `WRITEBACK-031` e `WRITEBACK-035`.

## 1. Pergunta e resultado permitido

**Pergunta:** quanto do acervo pode ser representado em forma fria, comprimida sem perdas,
mantendo identidade criptográfica, restauração verificável, reprodução das análises e os
registros deliberados de falha?

A missão pode concluir somente uma destas formas:

1. `MIGRATION_READY`: existem pacotes íntegros, restauração independente e uma lista de
   candidatos à desincorporação, ainda sem apagar nada;
2. `COLD_COPY_ONLY`: os pacotes são íntegros, mas falta cópia independente, reprodução ou
   autoridade para remover os originais;
3. `NOT_SAFE_TO_MIGRATE`: algum gate material falhou.

Nenhum resultado desta missão promove, rebaixa ou reinterpreta `C-1`–`C-15`, releases,
falhas ou selos históricos.

## 2. Baseline conhecido antes da execução

O levantamento somente leitura de 2026-08-28 encontrou em `LAB/EVIDENCE/`:

- `1.095.981.271` bytes físicos e `1.095.874.775` bytes de arquivos;
- 275 arquivos em 21 diretórios de primeiro nível;
- 70 `.dat`, totalizando `1.072.454.958` bytes (`~97,8 %` dos bytes de arquivos);
- duplicatas exatas com economia potencial aproximada de apenas `6,3 MB`;
- ensaio integral em `/tmp`: `.dat` comprimidos por Zstandard de `1.072.454.958` para
  `278.690.230` bytes, redução de `74,01 %`, sem tocar o acervo.

Esses números serão recalculados antes da execução. Divergência não será corrigida: será
registrada como mudança de baseline e interromperá a missão até avaliação.

## 3. Autoridades de integridade — selo interno e pacote externo

É proibido comprimir arquivos **dentro** de um diretório selado ou substituir um payload por
`*.zst`. Isso alteraria o conjunto de caminhos/bytes coberto por `SHA256SUMS.txt`.

Cada pacote frio será produzido fora de `LAB/EVIDENCE/` e conterá uma cópia lógica do
diretório elegível, preservando caminhos relativos, bytes, permissões e tempos registrados.
Haverá duas autoridades, com papéis distintos:

1. o `SHA256SUMS.txt` histórico continua sendo a autoridade sobre os payloads restaurados;
2. um `ARCHIVE-MANIFEST.json` novo registra SHA-256 e tamanho do pacote comprimido, ferramenta,
   versão, argumentos, conteúdo, hashes históricos esperados e proveniência.

O selo histórico nunca será recalculado para acomodar compressão. Depois da restauração, seu
`SHA256SUMS.txt` original precisa passar sem edição. O manifesto externo não normaliza selo
corrupto nem substitui autoridade epistêmica.

Formato candidato: um `tar.zst` por diretório de evidência, com Zstandard sem perdas. O uso
efetivo de `ARCHIVE/` ou de outro destino persistente depende de destino nomeado e autorização;
ensaios anteriores à decisão escrevem exclusivamente em diretório novo sob `/tmp`.

## 4. `PERMANENT-FAILURE-HOLD` — quarentena nomeada e permanente

Os seguintes objetos ficam fora de compressão, migração, remoção, movimentação, substituição,
normalização e resselo:

1. `LAB/EVIDENCE/A005R/` inteiro — inclui os cinco payloads divergentes
   (`RUN-LOG.txt`, `ac1_theta0.mx3`, `ac2_theta30.mx3`, `ac3_par.mx3`, `run_batch.sh`), o extra
   `ac0_piso.mx3` e seu contexto de corrupção;
2. `LAB/EVIDENCE/A003/` inteiro — preserva em contexto
   `__pycache__/ovf.cpython-311.pyc` e o estado `SEALED_CONTAMINATED`;
3. `LAB/EVIDENCE/A005/` inteiro — preserva em contexto
   `__pycache__/ovf.cpython-311.pyc` e o estado `SEALED_CONTAMINATED`;
4. `LAB/EVIDENCE/LAB/` inteiro — árvore anômala `UNSEALED`, incluindo
   `EVIDENCE/A005/ar1_fora_eixo.mx3` de zero byte.

O congelamento do diretório inteiro, e não apenas do arquivo anômalo, preserva relações,
ausências e contexto. Esses alvos não contam como dívida de limpeza nem como economia perdida.

Novos objetos podem entrar no hold somente por adendo prévio à execução ou por interrupção da
missão; nunca são retirados em resposta ao tamanho observado.

## 5. Classificação em dois eixos

O inventário de decisão terá uma linha por arquivo e dois eixos independentes:

### Papel epistêmico

- `CLAIM_BEARING`: sustenta claim, número, figura ou critério;
- `CONTEXT_ONLY`: necessário para interpretar proveniência, configuração ou ambiente;
- `FAILURE_RECORD`: registra contaminação, corrupção, resultado negativo, timeout ou falha;
- `NON_CLAIM`: não sustenta claim, sem que isso implique descarte.

### Ação de retenção

- `ACTIVE`: continua no caminho de trabalho;
- `COLD_PRESERVE`: pode ganhar cópia comprimida, mas não ser descartado;
- `PERMANENT_HOLD`: §4;
- `REGENERABLE_CANDIDATE`: somente derivado com cadeia completa e testável;
- `TRANSIENT`: somente material futuro ainda não selado; material transitório histórico
  dentro de evidência nunca herda autorização automática de remoção.

`CLAIM_BEARING` e `FAILURE_RECORD` são inelegíveis à desincorporação. `NON_CLAIM` não implica
`REGENERABLE_CANDIDATE`. A classificação deve citar missão, release, writeback, manifesto,
script consumidor e output associado; ausência de prova resolve para preservação.

## 6. Fases e separação de autoridade

### `ST-0` — baseline somente leitura

1. inventariar caminhos, tipos, bytes, inode, modo, mtime, SHA-256 e estado de selo;
2. executar os verificadores vigentes e registrar também as falhas esperadas;
3. confirmar literalmente todos os alvos do `PERMANENT-FAILURE-HOLD`;
4. mapear `analyze*.py`, entradas consumidas, comandos e outputs arquivados;
5. produzir o inventário dos dois eixos do §5.

Se qualquer alvo protegido faltar, mudar ou deixar de apresentar sua anomalia conhecida, a
missão para como `BASELINE_DRIFT`; nada é reparado.

### `ST-1` — empacotamento sem escrita em evidência

Para cada diretório elegível, o `PACKAGER`:

1. lê `LAB/EVIDENCE/` e escreve apenas em destino novo autorizado;
2. cria pacote sem perdas e `ARCHIVE-MANIFEST.json`;
3. registra hashes de cada payload original e do pacote;
4. registra comando em vetor de argumentos, versões e `RUN-RECEIPT.json`;
5. não segue symlinks e reprova caminhos absolutos, `..`, duplicados ou colisões;
6. não escreve, toca, renomeia ou res sela qualquer origem.

### `ST-2` — restauração por linhagem compensatória

O `RESTORE_VALIDATOR` deve ser distinto do `PACKAGER` em implementação e percurso de
validação. Outro agente com o mesmo código não basta. Ele recebe pacote, manifesto e critérios,
mas não importa o código do empacotador. Deve:

1. verificar o frame Zstandard com ferramenta independente;
2. verificar o hash externo do pacote;
3. restaurar em diretório novo sob `/tmp`;
4. rejeitar path traversal, symlink e arquivo inesperado;
5. comparar conjunto de caminhos, bytes, modos e metadados registrados;
6. executar o `SHA256SUMS.txt` histórico dentro da árvore restaurada.

Se a mesma linhagem empacotar e validar, o resultado obrigatório é `SELF_VALIDATION` e
`ST-2 = UNEVALUATED`; testes automáticos não promovem o gate sozinhos.

### `ST-3` — reprodução bit-idêntica das análises

Antes de rodar, `ST-0` gera uma matriz fechada com, para cada candidato:

- `analyze*.py` selado aplicável e seu SHA-256;
- comando exato, `cwd`, interpretador e ambiente;
- inputs restaurados;
- outputs arquivados designados e seus SHA-256;
- ou motivo documentado para `NO_ANALYZER`/`NO_ARCHIVED_OUTPUT`.

O critério é comparação, não limiar: reexecutar cada analisador aplicável sobre o dado
restaurado e exigir saída designada **bit-idêntica** à arquivada. Timestamp, caminho temporário
ou outro campo volátil só pode ser excluído se identificado no pré-run da matriz e se não fizer
parte do produto científico; a exclusão fica explícita e não pode ser criada após divergência.

Um candidato com `NO_ANALYZER`, `NO_ARCHIVED_OUTPUT`, ambiente insuficiente ou saída diferente
pode receber `COLD_PRESERVE`, mas é inelegível à desincorporação.

### `ST-4` — duas cópias e teste de restauração

Antes de propor remoção deve haver:

1. duas cópias integrais verificadas em locais de falha distintos;
2. SHA-256 externo idêntico nas duas cópias;
3. restauração completa a partir da segunda cópia;
4. recibo que nomeie dispositivos/destinos, datas e executor.

Duas pastas no mesmo filesystem não satisfazem este critério. Enquanto o segundo destino não
for nomeado e autorizado, `ST-4 = UNEVALUATED`.

### `ST-5` — proposta de desincorporação, sem executá-la

Gerar relatório com lista literal de cada alvo, bytes, papel epistêmico, classe de retenção,
pacotes/cópias correspondentes, resultados de `ST-2`/`ST-3`, economia líquida e comando
proposto. Excluir da lista:

- todo `CLAIM_BEARING`;
- todo `FAILURE_RECORD`;
- todo `PERMANENT_HOLD`;
- qualquer objeto sem restauração independente e reprodução bit-idêntica aplicável.

O relatório termina pedindo decisão humana. Não contém comando autoexecutável nem autorização
implícita.

### `ST-6` — desincorporação condicional, missão suspensa

Esta fase nasce **suspensa**. Só pode existir após novo writeback que:

1. cite a lista de `ST-5` e nomeie literalmente cada alvo;
2. abra exceção estreita aos `WB-031` e `WB-035`;
3. declare o efeito sobre a regra de imutabilidade do `CLAUDE.md` §3–§4;
4. autorize remover — não editar, normalizar ou resselar — somente esses originais;
5. mantenha o `PERMANENT-FAILURE-HOLD` intocado;
6. determine o recibo/tombstone append-only e o procedimento de recuperação.

Sem esse writeback, `ST-6 = NOT_AUTHORIZED`, mesmo que todos os gates técnicos passem.

## 7. Critérios de aceitação

| critério | passa se |
|---|---|
| `SC-0` escopo | nenhum byte em `LAB/EVIDENCE/` muda durante `ST-0`–`ST-5` |
| `SC-1` hold | os quatro objetos do §4 permanecem presentes e bit-idênticos |
| `SC-2` classificação | todo arquivo tem dois eixos, fonte e justificativa; dúvida preserva |
| `SC-3` pacote | pacote e manifesto externo validam; selo histórico não é recalculado |
| `SC-4` restauração | linhagem compensatória restaura conjunto e bytes idênticos |
| `SC-5` análise | todo candidato à remoção reproduz outputs designados bit a bit |
| `SC-6` cópias | duas cópias em locais de falha distintos e uma restauração da segunda |
| `SC-7` proposta | lista literal exclui claim, falha, hold e todo item `UNEVALUATED` |
| `SC-8` autoridade | nenhum original é removido sem writeback posterior e específico |
| `SC-9` ciência | nenhum claim, release, aceite, selo histórico ou limite muda |

`G-STORAGE = SC-0 ∧ SC-1 ∧ ... ∧ SC-9`, todos com veredito. Qualquer `UNEVALUATED` impede
`MIGRATION_READY`. `ST-6` não faz parte deste gate e continua dependendo de decisão posterior.

## 8. Taxonomia de falha

| ocorrência | classificação e ação pré-decidida |
|---|---|
| origem muda durante leitura | `SOURCE_DRIFT`; parar, preservar ambos os registros |
| selo válido não passa após restauração | `RESTORE_MISMATCH`; pacote rejeitado |
| selo historicamente corrupto aparece válido | `NORMALIZATION_BUG`; parar imediatamente |
| pacote passa, análise diverge | `SEMANTIC_REPRODUCTION_FAIL`; preservar original ativo |
| analisador/output ausente | `UNEVALUATED`; somente `COLD_PRESERVE` |
| mesma linhagem empacota e valida | `SELF_VALIDATION`; `SC-4` não passa |
| só existe uma localização física | `SINGLE_COPY`; nenhuma desincorporação proposta |
| alvo protegido aparece como candidato | `SCOPE_VIOLATION`; gate falha integralmente |
| autorização genérica sem lista literal | `AUTHORITY_INSUFFICIENT`; `ST-6` não executa |

Falha desta missão é dado metodológico e deve ser registrada; nunca vira permissão para limpar
o material que a revelou.

## 9. Artefatos previstos

Somente após autorização de execução, criar diretório novo `LAB/EVIDENCE/STORAGE-001/` com:

- `AI-PROVENANCE.json` criado antes dos demais artefatos;
- `BASELINE-INVENTORY.json` e `PERMANENT-FAILURE-HOLD.json`;
- `EPISTEMIC-RETENTION-MATRIX.json`;
- `ANALYSIS-REPRODUCTION-MATRIX.json`;
- `PACKAGE-INDEX.json` e manifests externos copiados como evidência;
- recibos de empacotamento e validação;
- `RESTORE-RESULTS.json`, `ANALYSIS-RESULTS.json`, `COPY-AUDIT.json`;
- `DEACCESSION-CANDIDATES.json`, obrigatoriamente não executado em `ST-0`–`ST-5`;
- `GATE-RESULTS.json`, `SHA256SUMS.txt` e manifesto funcional.

Pacotes volumosos não entram em `STORAGE-001/`; ficam no destino frio autorizado e são
referenciados por localização, tamanho e SHA-256. Nenhum upload, DOI, publicação, licença,
simulação científica ou ação externa é autorizado por esta missão.

## 10. Autorizações ainda necessárias

1. **Para executar `ST-0`–`ST-5`:** Rodrigo lê este pré-registro e autoriza literalmente
   `MISSION-STORAGE-001`; precisa também nomear qualquer destino persistente além de `/tmp`.
2. **Para satisfazer `ST-2`:** uma linhagem compensatória distinta precisa ser nomeada ou
   aceita, com independência declarada por eixo.
3. **Para satisfazer `ST-4`:** destino da segunda cópia, em local de falha distinto, precisa
   ser nomeado e autorizado.
4. **Para executar `ST-6`:** novo writeback posterior aos resultados, com os alvos literais e
   a exceção normativa descrita no §6.

Até lá, o estado correto é `PROPOSED — NÃO AUTORIZADA A EXECUTAR`.
