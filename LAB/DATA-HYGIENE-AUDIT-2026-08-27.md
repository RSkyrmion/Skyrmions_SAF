# Auditoria de higiene de dados — 2026-08-27/28

Missão: `MISSION-DATA-001` + erratas/adendo · Autorização: `WRITEBACK-031`  
Escopo: leitura integral de `LAB/EVIDENCE/`, estrutura metodológica e ferramentas de validação  
Remoções executadas: **zero** · Escritas externas/uploads/DOIs: **zero**

## 1. Resultado executivo

O acervo científico consolidado permanece preservado, mas a árvore não pode ser declarada
integralmente saudável. Na fotografia da retomada há 21 diretórios de primeiro nível e 19
manifests SHA-256. Pela regra recursiva:

- 15 diretórios estão `SEALED_VALID`;
- `A003` e `A005` estão `SEALED_CONTAMINATED` por caches Python extras;
- `A005R` está `SEALED_CORRUPT` por cinco hashes divergentes e um arquivo extra;
- `A005R2` está `SEALED_CORRUPT` por ausência do manifesto funcional obrigatório, embora os
  hashes listados confiram;
- `DATA-001` ainda estava `UNSEALED` na fotografia porque seu próprio gate precede o selo;
- a árvore anômala `LAB/` está `UNSEALED`.

Após o selo de `DATA-001`, somente seu estado deve mudar para `SEALED_VALID`. A existência de
problemas históricos não foi convertida artificialmente em gate limpo.

## 2. Achados exatos e autoridade correta

### `H-01` — caches posteriores ao selo

- `A005/__pycache__/ovf.cpython-311.pyc`, criado em 2026-08-27 14:14:01 -03:00;
- `A003/__pycache__/ovf.cpython-311.pyc`, criado em 2026-08-27 16:10:20 -03:00, SHA-256
  `843eaf519d5b786ec0b551fbc18ecd93e3e7ee1ebc3fbfa4bc9194cb6b31d48f`.

Autoridade: os `SHA256SUMS.txt` originais e o conjunto recursivo real. Tratamento: manter
`SEALED_CONTAMINATED`; caches são `TRANSIENT`, mas nenhuma remoção foi autorizada.

### `H-02` — corrupção de `A005R`

Cinco arquivos cobertos não batem com o selo: `RUN-LOG.txt`, `ac1_theta0.mx3`,
`ac2_theta30.mx3`, `ac3_par.mx3` e `run_batch.sh`. `ac0_piso.mx3` é extra. O log foi
regravado ao menos duas vezes depois do selo; a observação mais recente é SHA-256
`6f9f0ae2731a40a994516ce63dd248041ac8f0d0b83c90948cc20929bc1683bb`, `mtime`
2026-08-27 16:07:39 -03:00.

Autoridade: os hashes esperados continuam sendo os do selo de 14:44:14. Sem cópia que bata
com eles, os payloads originais são `UNRECOVERED`. Recalcular o manifesto atual seria ocultar
o dano e é proibido.

### `H-03` — árvore anômala

`LAB/EVIDENCE/LAB/EVIDENCE/A005/ar1_fora_eixo.mx3` existe com zero byte, sem missão e sem
selo. Autoridade: nenhuma missão/release; estado `UNSEALED`. A remoção de
`LAB/EVIDENCE/LAB/` continua dependente de autorização literal separada.

### `H-04` — `A005R2`: autoridade e metadado

`A005R2` foi executada e selada durante a retomada. `RELEASE-A005R2.md` e
`AI-PROVENANCE.json` atribuem autorização ao `WRITEBACK-033`, mas esse writeback retoma apenas
`DATA-001` e diz que não amplia o escopo. A correção está em
`RELEASE-A005R2-ADDENDUM-001.md`/`WRITEBACK-034.md`. Além disso, o diretório novo não contém
`EVIDENCE-MANIFEST.json`, exigido por `DH-3`.

Autoridade: o texto literal do writeback prevalece sobre a referência incorreta do release.
O material permanece preservado, mas `PROCEDURALLY_UNAUTHORIZED`, sem promoção de claim.

### `H-05` — 35 cabeçalhos herdados

Os arquivos abaixo declaram `MISSION-E003` na primeira linha, embora pertençam a outras
missões. A autoridade correta é o diretório, a missão correspondente e seu release; o
cabeçalho não deve ser usado isoladamente. Os payloads selados não foram reescritos.

`E004` (8):
`prop_sbm_16.50GHz.dat`, `17.00`, `17.50`, `17.75`, `18.25`, `18.50`, `19.00` e `19.50`.

`E004R` (7):
`prop_rf4_mesh05_th30.dat`, `prop_rf4_mesh10_th30.dat`, `prop_sbm_17.00GHz.dat`,
`17.50`, `17.75`, `18.00` e `18.25`.

`E005` (14):
`prop_sbm_A0.002_{17.00,17.25,17.50,17.75,18.00,18.25,18.50}GHz.dat` e
`prop_sbm_A0.008_{17.00,17.25,17.50,17.75,18.00,18.25,18.50}GHz.dat`.

`I002` (4):
`prop_il_K0.55_th30.dat`, `prop_il_K0.60_th30.dat`, `prop_il_K0.65_th30.dat` e
`prop_il_K0.70_th30.dat`.

`I003` (2):
`prop_id1_mesh05_dt10fs.dat` e `prop_id1_mesh05_dt2.5fs.dat`.

### `H-06` — esquemas e ambiente históricos

Somente `AUDIT-002` tinha `FORMAT.txt`; tabelas anteriores não têm schema comum validável.
`ENVIRONMENT.md` também não cobria as missões mumax3 recentes. A correção adotada é
prospectiva: quatro schemas reutilizáveis, manifesto funcional e recibo de execução. Não se
fabricaram metadados históricos desconhecidos.

### `H-07` — preservação redundante não demonstrada

Não há prova local de duas cópias integrais em locais distintos, periodicidade de fixity ou
teste de restauração. Estado: `UNVERIFIED`. `DATA-001` fez apenas exportação de fixture em
`/tmp`; não realizou backup, upload ou depósito.

## 3. Classificação de tratamento

| conjunto | classificação | decisão operacional |
|---|---|---|
| payloads claim-bearing, inputs, fontes, logs, falhas e manifests | `PRESERVE` | conservar e verificar |
| catálogo, figuras e derivados reproduzíveis | `REGENERABLE` quando inputs/receita bastarem | manter índice; regenerar se necessário |
| `__pycache__`, `.pyc`, temporários e scratch | `TRANSIENT` | impedir antes de selar; remoção histórica depende de autorização |
| artigo e material de terceiro | `EXTERNAL` | manter origem/direitos; não redistribuir automaticamente |
| segredo/dado pessoal | `RESTRICTED` | nenhum foi identificado nesta auditoria; regra permanece preventiva |

Nenhum payload científico foi marcado para descarte automático. Duplicidade de hash não
autoriza hardlink ou eliminação porque linhagem de missão é parte da evidência.

## 4. Melhorias implementadas

- comparação recursiva exata, independente de Git, com estados separados;
- selo determinístico que recusa overwrite, symlink, vazio e transitório;
- manifesto funcional, quatro schemas tabulares e recibo finalizável em erro/timeout;
- catálogo claim→dado sem promoção silenciosa;
- hook e verificador do repositório integrados à mesma regra;
- retenção explícita e dry-run local RO-Crate 1.3 + BagIt + DataCite;
- fixtures positivas/negativas em `/tmp` e proveniência funcional.

Princípios de método usados: FAIR (`10.1038/sdata.2016.18`), NIST RDaF 2.0
(`10.6028/NIST.SP.1500-18r2`), W3C PROV, Frictionless/CSVW, RO-Crate 1.3, BagIt RFC 8493,
DataCite 4.7, FORCE11 Data Citation, RDA Data Versioning e NDSA/TRUST. Eles orientam processo;
não sustentam claim científico do SAF.

## 5. O que permanece para decisão humana

1. tratamento processual de `A005R2`;
2. eventual autorização literal para remover os caches e/ou `LAB/EVIDENCE/LAB/`;
3. destino e política de backup/restauração;
4. direitos/licença e eventual depósito citável.

Passar o gate técnico de `DATA-001` não resolve nenhum desses pontos e não é aceite humano.

