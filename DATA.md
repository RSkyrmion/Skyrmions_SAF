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

## Integridade do conteúdo publicado

Execute:

```bash
python3 scripts/check_repository.py
```

O verificador confere os hashes de todos os artefatos presentes no clone. Entradas de hash
referentes a dados deliberadamente omitidos são informadas, não tratadas como corrupção.

