# SAF-Skyrmion — re-implementação independente do PRL 135, 086701 (2025)

Laboratório de pesquisa sob metodologia **FPM**. Não é um repositório de código: é um
registro de decisões, evidência selada e claims com limites explícitos.

> **Espelho público leve.** O GitHub contém fontes, protocolos, decisões, resultados
> textuais, manifests e figuras finais. Dados brutos, executáveis, toolchains, PDFs de
> terceiros e rastros internos não são publicados aqui. Consulte [`DATA.md`](DATA.md).

## Por onde começar

| se você quer… | leia |
|---|---|
| o estado atual, para retomar o trabalho | **`LAB/STATE.md`** |
| a história e o que se sabe, em uma sentada | `LAB/CONSOLIDATION-2026-08-24.md` |
| os claims canônicos com seus limites | `LAB/DECISIONS/WRITEBACK-007.md` e `-009.md` |
| saber do que isto depende para rodar | `ENVIRONMENT.md` |

## O mapa

```
SAF/
├── README.md            você está aqui
├── ENVIRONMENT.md       dependências externas, versões, fragilidades
├── LAB/                 o laboratório
│   ├── STATE.md             estado atual — a porta de entrada
│   ├── CONSOLIDATION-*.md   síntese da análise
│   ├── MISSIONS/            pré-registros (escritos ANTES de executar)
│   ├── DECISIONS/           writebacks — decisões humanas e autoridade
│   ├── RELEASES/            resultados as-run e seus adendos
│   └── EVIDENCE/            artefatos selados por hash, um dir por missão
├── SOURCES/             insumos, não produtos
│   ├── paper/               o artigo e o suplementar
│   ├── theory/              notas teóricas fornecidas por Rodrigo
│   └── fpm/                 o pacote de inicialização da metodologia
└── ARCHIVE/             material morto, preservado e fora do caminho
```

## As quatro categorias, e por que estão separadas

- **`MISSIONS/` é promessa.** Critérios escritos antes de haver dados. Não se editam — um
  critério ajustado depois do resultado não é critério.
- **`DECISIONS/` é autoridade.** O que Rodrigo decidiu, com a citação literal. Só ele pode
  autorizar missão, aceitar resultado ou permitir ação externa.
- **`RELEASES/` é o que aconteceu.** As-run, incluindo o que falhou. Não se editam: corrigem-se
  por adendo.
- **`EVIDENCE/` é o material.** Código, dados, logs, com `SHA256SUMS.txt` em cada diretório.

Só o `STATE.md` é reescrito no lugar.

## Verificar a integridade

```
python3 scripts/check_repository.py
```

No laboratório completo, `sha256sum -c` continua sendo a autoridade. No espelho público, o
script confere todos os artefatos presentes e informa quantas entradas pertencem aos dados
deliberadamente omitidos.

## Referência

C. C. de Souza Silva, M. V. Correia e J. C. Piña Velásquez, *Emergent Self-Propulsion of
Skyrmionic Matter in Synthetic Antiferromagnets*, Physical Review Letters **135**, 086701
(2025), [doi:10.1103/c2y9-3cc9](https://doi.org/10.1103/c2y9-3cc9).

Os metadados para citar esta implementação estão em [`CITATION.cff`](CITATION.cff).

## Licenciamento

Esta publicação inicial é conservadora: todos os direitos sobre o material original estão
reservados até que licenças explícitas de código e dados sejam escolhidas. Material de
terceiros conserva seus próprios direitos. Consulte [`LICENSE`](LICENSE).

## Estado, em uma linha
O estado vivo está em [`LAB/STATE.md`](LAB/STATE.md). Como decisões e releases são
acrescentados sem reescrever a história, confira também documentos posteriores ao `head`
registrado ali. Nada está congelado.
