# MISSION-DATA-001 — higiene, catálogo e preservação verificável dos dados FPM

Estado: **`PROPOSED — NÃO AUTORIZADA`** · Data: 2026-08-27  
Tipo: missão metodológica de infraestrutura; **não produz nem promove claim científico**

> **Pré-registro.** Esta missão foi escrita depois da auditoria estrutural, mas antes de
> implementar qualquer correção. Criá-la não autoriza execução, remoção em `EVIDENCE/`,
> backup externo, depósito, mudança de licença, freeze ou aceite científico.

## 1. Problema

O FPM já separa promessa, decisão, ocorrido e evidência; sela arquivos com SHA-256 e preserva
falhas. A camada que falta é tornar a **estrutura dos dados** verificável por máquina, não só
legível por uma pessoa familiarizada com o laboratório.

A auditoria de 2026-08-27 encontrou:

1. `sha256sum -c` confirma os arquivos listados, mas não detecta **arquivos extras**. Há
   `LAB/EVIDENCE/A005/__pycache__/ovf.cpython-311.pyc`, criado depois do selo e ausente do
   manifesto. O payload hasheado não mudou; o diretório deixou de ter cobertura completa.
2. Existe a árvore vazia anômala `LAB/EVIDENCE/LAB/EVIDENCE/A005/`, sem missão nem selo.
3. **35 séries `.dat`** em `E004`, `E004R`, `E005`, `I002` e `I003` declaram
   `MISSION-E003` no cabeçalho por herança de código. Os releases e caminhos preservam a
   linhagem correta, mas o cabeçalho isolado é enganoso.
4. As tabelas geralmente trazem colunas e unidades em comentário, porém só `AUDIT-002` tem
   um `FORMAT.txt`; não há esquema validável comum, política uniforme de valores ausentes,
   tipos, precisão ou invariantes.
5. `ENVIRONMENT.md` não acompanha todas as missões mumax3 recentes. Comando, `cwd`, hash do
   solver, parâmetros, seed, tempos e códigos de saída aparecem de forma desigual nos logs.
6. O espelho público omite corretamente dados grandes, mas o depósito citável ainda é plano.
   Não há no repositório prova de segunda cópia integral, local distinto, teste de restauração
   ou prazo de retenção.

## 2. Objetivo

Construir uma camada mínima e validável que responda, para cada missão futura:

- **o que** existe e qual papel cada arquivo cumpre;
- **como, quando, onde e com quê** foi produzido;
- quais entradas, saídas, esquemas, unidades e relações de derivação existem;
- se o diretório está completo, íntegro e livre de artefatos transitórios;
- o que deve ser preservado, regenerado, descartado antes do selo ou exportado;
- qual pacote exato sustenta cada claim, release e futura citação.

## 3. Princípios externos absorvidos — e limite de uso

| fonte | delta adotado nesta missão |
|---|---|
| FAIR, DOI `10.1038/sdata.2016.18` | identificadores, metadados ricos, acesso declarado, interoperabilidade e reúso |
| NIST RDaF 2.0, DOI `10.6028/NIST.SP.1500-18r2` | ciclo planejar → gerar → analisar → compartilhar → preservar/descartar |
| W3C PROV | entidades, atividades e agentes; relações `used` e `wasGeneratedBy` |
| Frictionless Data Package / W3C CSVW | recurso + esquema tabular, tipos, unidades, dialeto e validação |
| RO-Crate 1.3 | pacote interoperável de objeto de pesquisa para exportação |
| BagIt, RFC 8493 | payload completo, manifest e tag manifest para transferência |
| DataCite Metadata Schema 4.7 | versão, direitos, formatos e relações entre artigo, software e dados |
| FORCE11 Data Citation Principles | granularidade, persistência, proveniência e fixidade do dado citado |
| RDA Data Versioning, DOI `10.15497/RDA00042` | identificar revisão e explicar significado da mudança |
| NDSA Levels of Digital Preservation 2.1 / TRUST | cópias, fixity, restauração, transparência e sustentabilidade |

Essas fontes orientam processo; não são evidência científica do SAF. O formato operacional
interno será JSON simples e validável. PROV/RO-Crate/BagIt entram como **mapeamento de
exportação**, não como burocracia diária.

## 4. Escopo e entregáveis

### `DH-0` — inventário basal sem mutação

Gerar em `/tmp` um inventário recursivo de diretórios, arquivos, bytes, hashes, symlinks,
extensões e cobertura. Registrar no release:

- 18 diretórios atualmente selados;
- a árvore vazia anômala;
- o `.pyc` extra em `A005`;
- os 35 cabeçalhos com missão divergente;
- duplicatas por conteúdo e os arquivos maiores.

O inventário não altera timestamp ou conteúdo de evidência.

### `DH-1` — verificador recursivo de evidência

Criar `scripts/check_evidence.py`, independente de Git, que para cada diretório:

1. compara **recursivamente** o conjunto real com as entradas do `SHA256SUMS.txt`;
2. reprova arquivo ausente, extra, duplicado no manifesto, hash inválido ou divergente;
3. reprova caminho absoluto, `..`, symlink e escape do diretório;
4. reprova artefatos transitórios (`__pycache__`, `*.pyc`, `*.tmp`, swap e backups de editor);
5. valida `AI-PROVENANCE.json` quando exigido;
6. distingue `UNSEALED`, `SEALED_VALID`, `SEALED_CONTAMINATED` e `SEALED_CORRUPT`;
7. produz saída humana curta e JSON opcional.

O hook e `check_repository.py` devem chamar esse verificador. Toda análise Python de
evidência deve usar `python3 -B` ou `PYTHONDONTWRITEBYTECODE=1`.

### `DH-2` — selo determinístico e seguro

Criar `scripts/seal_evidence.py` que opere somente em diretório ainda não selado e:

- valide manifestos, esquemas, caminhos e arquivos transitórios antes do selo;
- gere lista SHA-256 ordenada e recursiva, sem sobrescrever selo existente;
- recuse diretório vazio, symlink e arquivos que mudem durante o cálculo;
- grave um recibo com quantidade de arquivos, bytes e hash do próprio manifesto em
  `LAB/EVIDENCE-SEALS.jsonl`;
- termine tornando arquivos selados não graváveis quando suportado, sem impedir leitura e
  execução; falha dessa proteção deve ser declarada, não ocultada.

`EVIDENCE-SEALS.jsonl` é índice de fixity, não autoridade epistêmica. Em freeze/exportação,
seu estado será ancorado por release versionado e futuro depósito persistente.

### `DH-3` — manifesto funcional por missão futura

Definir `scripts/schemas/fpm-evidence-manifest.schema.json` e template correspondente.
Todo diretório novo terá `EVIDENCE-MANIFEST.json` antes do selo, contendo no mínimo:

- `schema_version`, `mission_id`, título, estado operacional e timestamps RFC 3339;
- cada recurso com caminho, papel (`INPUT`, `SOURCE`, `RAW`, `DERIVED`, `LOG`, `CODE`,
  `BINARY`, `FIGURE_TARGET`, `METADATA`), mídia/formato, bytes e SHA-256;
- relações `used`, `generated_by`, `derived_from`, `reused_from` e `supports_criterion`;
- comando/atividade produtora ou indicação explícita de origem manual/externa;
- política de acesso, direitos, retenção e sensibilidade;
- outputs esperados, produzidos, ausentes e motivo da ausência;
- links para missão, release, decisão e proveniência de IA.

Não fabricar manifestos funcionais retroativos. Para evidência histórica, o catálogo global
pode registrar apenas fatos documentados e marcar desconhecidos.

### `DH-4` — esquemas tabulares e qualidade

Definir esquemas reutilizáveis, inspirados em Table Schema/CSVW, para ao menos:

1. `trajectory-v1`: `t`, centros, `l`, cargas e tensor de dissipação;
2. `magnetization-grid-v1`: índices e componentes das duas camadas;
3. `phase-scan-v1`: parâmetros, classe, observáveis, iterações e torque;
4. `criterion-summary-v1`: critério, medida, unidade, estado e limite.

Cada coluna terá nome, descrição, tipo, unidade SI/canônica, nulabilidade e faixa/invariante
quando cientificamente válida. O validador verificará encoding UTF-8, número de colunas,
valores finitos, monotonicidade de tempo quando aplicável e enumerações; não imporá faixa
física escolhida depois do resultado.

Dados históricos permanecem imutáveis. Adaptadores de leitura podem mapear seus cabeçalhos
para os esquemas sem reescrever payload.

### `DH-5` — recibo de execução e ambiente por corrida

Definir `RUN-RECEIPT.json` validável com:

- missão/corrida, comando em vetor de argumentos e `cwd`;
- início/fim RFC 3339, duração, exit code, timeout e estado `COMPLETE/FAILED/INTERRUPTED`;
- hash do executável/código, solver e versões;
- hardware relevante, SO, driver, compilador e dependências;
- parâmetros, tolerâncias, seed e determinismo declarado;
- inputs, outputs e checkpoints por hash;
- agente executor e checkpoints humanos por referência, sem chain-of-thought ou segredo.

O runner deve escrever recibo parcial antes de executar e finalizá-lo mesmo em erro/timeout.
Isso impede que `LOTE COMPLETO` seja confundido com missão concluída.

### `DH-6` — catálogo e grafo claim→dado

Criar `LAB/DATA-CATALOG.json`, gerado e validado, com uma entrada por missão/evidência:

- estado do selo e do gate;
- release e decisão humana vigente;
- claims que usa ou sustenta, sem promover nenhum;
- esquema, tamanho, acesso, retenção e localização pública/privada;
- relações entre versões, revisões e reutilizações.

O catálogo é índice; em conflito, writeback, release e manifesto selado continuam sendo as
autoridades correspondentes.

### `DH-7` — retenção, backup e exportação

Atualizar `DATA.md` com classes:

- **PRESERVE:** input único, dados brutos claim-bearing, código/configuração, logs, recibos,
  checkpoints necessários e falhas informativas;
- **REGENERABLE:** derivados que têm input + código + comando + ambiente suficientes;
- **TRANSIENT:** cache, temporário e scratch — removidos **antes** do selo;
- **EXTERNAL:** material de terceiros, com direitos e origem;
- **RESTRICTED:** segredo, dado pessoal ou material não redistribuível.

Documentar objetivo mínimo de duas cópias integrais em locais distintos, verificação periódica
de fixity e teste de restauração. Nesta missão, backup pode ficar `UNVERIFIED`: **nenhuma
cópia para disco externo, nuvem ou repositório será feita sem destino e autorização próprios**.

Criar somente um exportador/dry-run local que produza em `/tmp`:

- pacote RO-Crate 1.3 com metadados e relações;
- bag BagIt SHA-256 para transferência;
- rascunho DataCite 4.7 com versão, direitos e related identifiers.

Nenhum DOI será criado e nenhum upload será realizado.

### `DH-8` — auditoria histórica sem reescrita

Criar `LAB/DATA-HYGIENE-AUDIT-2026-08-27.md` registrando as anomalias exatas e a fonte de
autoridade correta para cada uma. Não renomear nem editar os 35 `.dat` selados.

Duas correções físicas ficam **fora da autorização implícita desta missão**:

1. remover `LAB/EVIDENCE/A005/__pycache__/ovf.cpython-311.pyc`;
2. remover `LAB/EVIDENCE/LAB/` e sua árvore vazia.

Mesmo sendo artefatos acidentais, apagar dentro de `EVIDENCE/` exige autorização literal que
nomeie esses dois alvos. Se não houver autorização, o verificador deve continuar acusando-os
e o release registrar `SEALED_CONTAMINATED`/`UNSEALED_EMPTY`.

## 5. Critérios de aceitação

| critério | passa se |
|---|---|
| `DA-0` inventário | reproduz contagens e detecta as duas anomalias sem escrever em evidência |
| `DA-1` completude | fixture em `/tmp` passa limpa e falha separadamente para extra aninhado, ausente, duplicado, symlink e `../` |
| `DA-2` fixity | byte alterado reprova; manifesto anterior nunca é sobrescrito |
| `DA-3` manifesto | exemplo válido passa JSON Schema; ausência de campos, papel inválido e output esperado ausente sem motivo falham |
| `DA-4` tabelas | quatro famílias têm schema; fixtures válidas passam e coluna/tipo/unidade/NaN inválidos falham |
| `DA-5` recibo | sucesso, erro e timeout geram recibos distinguíveis, com comando, ambiente, hashes e outputs |
| `DA-6` catálogo | 18 selos e toda árvore de evidência aparecem; links inexistentes e promoção de claim sem writeback falham |
| `DA-7` não regressão | todos os arquivos cobertos pelos 18 selos conservam seus hashes anteriores |
| `DA-8` integração | hook, CI e verificador local usam a mesma regra recursiva e retornam código não zero para corrupção/contaminação |
| `DA-9` exportação | RO-Crate/BagIt/DataCite de fixture validam localmente; zero conexão ou escrita externa ocorre |
| `DA-10` escopo | nenhum claim, aceite, freeze, licença ou status científico muda |

## 6. Gate

`G-DATA-001 = DA-0 ∧ DA-1 ∧ ... ∧ DA-10`, todos com veredito. Se um critério ficar
indeterminado, o gate não passa. Passar o gate técnico não é aceite humano.

## 7. Taxonomia de falha

| classe | significado | ação pré-definida |
|---|---|---|
| `IMPLEMENTATION_ERROR` | fixture válida falha ou inválida passa | corrigir código; repetir toda suíte |
| `HISTORICAL_CONTAMINATION` | extra real fora do manifesto | registrar; não apagar sem autorização |
| `INSUFFICIENT_METADATA` | fato histórico não reconstruível | marcar `UNKNOWN`; nunca inventar |
| `SCHEMA_MISMATCH` | dado válido não cabe no schema | revisar schema antes de adotá-lo; não converter dado silenciosamente |
| `PRESERVATION_GAP` | cópia/restauração não demonstrada | manter `UNVERIFIED`; não alegar preservação redundante |
| `EXPORT_FAILURE` | pacote local não valida | não depositar nem criar identificador |
| `SCOPE_VIOLATION` | tentativa de mudar evidência/claim/autoridade | parar a missão |

## 8. Restrições de implementação

- Nenhum arquivo selado será editado, renomeado, movido ou recomprimido.
- Nenhuma proveniência histórica será fabricada.
- Testes que importem código de evidência usarão `-B` e escreverão somente em `/tmp`.
- Não adotar DVC, DataLad, banco de dados, PROV-O integral ou RO-Crate dentro de cada missão;
  o tamanho atual e o modelo imutável não justificam essas dependências.
- Não deduplicar evidência histórica por hardlink: identidade de conteúdo não substitui
  linhagem de missão.
- Licença e prazo de retenção são decisões humanas; o sistema apenas exige que o estado seja
  explícito (`UNDECIDED`, `RESTRICTED`, etc.).
- A missão pode produzir scripts, schemas, documentação, catálogo e fixtures. Não executa
  simulação científica.

## 9. Evidência e release da própria missão

Se autorizada, usar `LAB/EVIDENCE/DATA-001/` somente para fixtures, relatórios de validação,
inventário basal, hashes e `AI-PROVENANCE.json`. Nenhuma cópia dos 1,1 GiB históricos entra
ali. Publicar `LAB/RELEASES/RELEASE-DATA-001.md` com custo, critérios, falhas e limitações.

## 10. Orçamento e parada

- Orçamento: até **4 h de trabalho**, sem GPU e sem rede.
- Parar se qualquer teste escrever em diretório selado, se um script exigir privilégio de
  sistema ou se a solução demandar dependência externa não instalada.
- Dependência opcional não instalada vira proposta separada; não instalar nesta missão.

## 11. Próxima decisão humana

Rodrigo deve primeiro ler este pré-registro. Depois, separadamente:

1. autorizar ou não a execução de `DATA-001`;
2. autorizar ou não, de forma literal e nomeando os caminhos, a remoção dos dois artefatos em
   `EVIDENCE/` descritos no `DH-8`;
3. futuramente escolher destino de backup, licença e eventual depósito — decisões que esta
   missão não toma.

