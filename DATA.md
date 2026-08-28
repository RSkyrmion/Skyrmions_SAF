# Política de dados e evidências

Este repositório é o espelho público e leve do laboratório. Ele versiona fontes, protocolos,
decisões, resultados textuais, manifests e hashes, mas não distribui automaticamente todo o
material local.

## O que está no GitHub

- fontes CUDA, Python, mumax3 e OOMMF necessárias para documentar as missões;
- pré-registros, decisões, releases e seus adendos;
- `SHA256SUMS.txt` dos diretórios de evidência;
- tabelas pequenas e figuras finais produzidas pelo projeto.

## O que não está no GitHub

- séries temporais e estados de simulação volumosos (`.dat`, `.omf`, `.ohf`, `.ovf`);
- executáveis compilados, toolchains e bibliotecas CUDA;
- PDFs do artigo de referência e outros materiais de terceiros;
- rastros internos de agentes e configurações específicas da máquina.

Os manifests preservam a identidade criptográfica dos arquivos omitidos. A ausência pública
de um arquivo não invalida seu hash, mas impede a reprodução integral apenas a partir deste
clone.

## Arquivamento citável

A estratégia prevista é depositar snapshots de dados aceitos em um repositório científico,
como o Zenodo, e registrar aqui o DOI e os hashes correspondentes. Até que esse depósito seja
feito, pedidos de acesso devem ser tratados pelo mantenedor do repositório.

## Classes de retenção

Todo manifesto novo declara uma das cinco classes. A classe descreve o tratamento; não concede
permissão para apagar, publicar ou mudar direitos.

| classe | conteúdo | tratamento |
|---|---|---|
| `PRESERVE` | input único, dado bruto claim-bearing, código/configuração, log, recibo, checkpoint necessário e falha informativa | conservar com fixity e proveniência |
| `REGENERABLE` | derivado cujo input, código, comando e ambiente são suficientes | pode ser regenerado; a decisão de descarte continua humana |
| `TRANSIENT` | cache, temporário, scratch, swap e backup de editor | excluir antes do selo; nunca aceitar dentro de evidência selada |
| `EXTERNAL` | material de terceiro | registrar origem, direitos, versão e acesso |
| `RESTRICTED` | segredo, dado pessoal ou material não redistribuível | não publicar; declarar controle de acesso |

Direitos e prazo de retenção são campos separados. Quando não decididos, usar `UNDECIDED` em
vez de inferir licença ou inventar prazo.

## Cópias, fixity e restauração

Objetivo mínimo: duas cópias integrais em locais distintos, verificação periódica de SHA-256
e teste documentado de restauração. O estado atual é **`UNVERIFIED`**: o repositório não contém
prova de segunda cópia integral nem de restauração. Isso deve permanecer explícito até uma
missão autorizada nomear destino, periodicidade e procedimento. `DATA-001` não realiza backup
externo.

## Pacote de transferência e citação

`scripts/export_data_package.py` produz somente em `/tmp` um dry-run com RO-Crate 1.3,
BagIt/SHA-256 e rascunho DataCite 4.7. O rascunho mantém direitos e autores indecididos e não
contém DOI. Exportar localmente não autoriza upload, depósito ou publicação.

Versionamento citável deve identificar a revisão e explicar seu significado. Um novo selo não
substitui silenciosamente um anterior, e corrupção histórica não é normalizada por recalcular
hashes.

## Integridade do conteúdo publicado

Execute:

```bash
python3 scripts/check_public_snapshot.py
```

Para a árvore local completa, execute também:

```bash
python3 -B scripts/check_evidence.py
```

O segundo comando é recursivo, independente de Git e reprova arquivo extra, ausente, symlink,
artefato transitório e hash divergente. O gate público executa a auditoria integral e tolera
somente as cinco divergências históricas de `A005R` declaradas em `WRITEBACK-035`; qualquer
erro adicional o faz falhar. Entradas deliberadamente omitidas continuam informadas, mas um
clone leve não demonstra a integridade do acervo local completo.
