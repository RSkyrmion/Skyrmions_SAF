# Consolidação epistêmica — auditoria de 2026-08-27

Escopo: revisar todo o ledger sob `CLAUDE.md` §6.2 e separar o que está consolidado, o que
precisa ser revisitado e o que deve ficar fora do corpo claim-bearing. Esta consolidação não
promove nem revoga claims: aceites continuam pertencendo aos writebacks humanos.

## Resultado da auditoria

- **17 diretórios de evidência já selados** foram conferidos, com cobertura completa de hash;
  todas as entradas verificaram. `A005R` foi formalizado e selado depois desta contagem,
  elevando o conjunto a 18.
- Os analisadores de `A004`, `A005`, `E002`, `E003`, `E004`, `E004R` e `E005` foram
  reexecutados e reproduziram exatamente os registros existentes.
- Nenhum arquivo de evidência previamente selado foi alterado.
- Os 15 claims aceitos permanecem aceitos. A auditoria altera **prioridade e condições de
  uso**, não autoridade humana passada.
- “Descartar” abaixo significa **não usar para sustentar claim**. Nada foi apagado: material
  histórico, falhas e exploração continuam preservados.

## Claims aceitos: força atual e ação recomendada

| claim | base aceita | independência relevante | classificação atual | limite / motivo para revisitar | ação |
|---|---|---|---|---|---|
| `C-1` | `R001`, `WB-007` | código próprio; depois confrontado por `C-15` | **consolidado no ponto medido** | sensibilidade de malha `1,0 %` maior que o acordo; não vale para o contínuo | `A008` |
| `C-2` | `R002`, `WB-007` | teste estrutural multiponto no mesmo código | **consolidado em cinco colunas** | `L2.3`: ramo coaxial ausente em `A_int=0.12` | `A006` |
| `C-3` | `AUDIT-001`, `WB-007` | derivação cega ao código, mas auditor e auditado são LLMs | **auxiliar válido** | não é leitura humana independente do modelo; possível erro compartilhado | manter rótulo |
| `C-4` | `A002`, `WB-007`; reforçado por `A003` | OOMMF e mumax3 confirmam o termo interlayer | **forte para `1/d`** | o gate do `A002` falhou e o teste não mede `l` | não ampliar |
| `C-5` | `AUDIT-002`, `WB-009` | estimador implementado às cegas | **consolidado nas condições testadas** | fronteira periódica não testada pelo estimador cego | controle cego barato |
| `C-6` | `E001`, `WB-009`; refinado por `C-11` | controles internos, um solver dinâmico | **consolidado internamente** | dinâmica sem segundo solver; `18.00 GHz` superado | `A007` |
| `C-7` | `E002`, `WB-011` | mesmo código e alvos extraídos de figura | **usável só com restrições fortes** | gate falhou; SBM não estacionou; magnitude tardia, não transiente | `A007` |
| `C-8` | `E003`, `WB-015` | discrimina ligação×rede dentro do mesmo solver | **apoiado em dois ângulos** | apenas SBM; estados fora do eixo não plenamente relaxados | segundo solver após convergência |
| `C-9` | `I001`, `WB-015` | três localizadores no mesmo estado | **forte exclusão instrumental** | exclui tracker, não identifica causa física | missão `L9.1` |
| `C-10` | `E004R`, `WB-018` | estimador próprio em centro×fronteira | **consolidado para esse estimador** | estimador cego não repetido; uma fronteira | controle cego |
| `C-11` | `E004R`, `WB-018` | espectro interno de maior resolução | **canônico** | um protocolo, um ponto | usar `17.9609 ± 0.0125` |
| `C-12` | `I002`, `WB-018` | comparação interna bem-formada | **informativo, revisitar** | quatro relaxações não convergiram plenamente | convergência de saída/estado |
| `C-13` | `I003`, `WB-019` | teste pareado de passo em uma malha | **regra numérica consolidada** | a redução `4,5×` da deriva não era critério | aplicar `dt∝a²`; missão própria para deriva |
| `C-14` | `E005`, `WB-021` | alvo extraído e selado antes; um solver | **sinal e escala consolidados** | amolecimento ~`14 %` mais fraco e não explicado | `A007`/modelo |
| `C-15` | `A003`, `WB-023` | solver e régua independentes; leitura e inicialização compartilhadas | **aceito, prioridade de revisão** | `−0,30 %` abaixo da malha; estado mumax parou `45×` mais frouxo | redesenho `A005R2` |

## Material que não deve sustentar claims

| origem | dado ou leitura | classificação e uso permitido |
|---|---|---|
| `R002` | inclinação/intercepto do critério secundário | **morto na checagem de poder**; apenas história do protocolo |
| `A002` | `OV-3`, inclusive `l(140 nm)=10.9566 nm` | **não conclusivo**; dado histórico, nunca resultado |
| `E001` | `18.00 GHz` como linha espectral | **superado por `C-11`**; pode aparecer apenas como bin de `0,1 GHz` |
| `E001-ADDENDUM-005` | extrapolação de contínuo `10.74–10.81 nm` | **exploratória**, só dois pontos e ordem desconhecida |
| `E002` | piso tardio `0.0005 pm`, `EP-3`, `EP-5`, atribuições de painéis `l̄`, `v∞≈3.498` | **exploratório/post-hoc ou não discriminante**; excluir do argumento principal |
| `E003` | `EO-2` | **não promotor**; conservar apenas no release |
| `E004` | `EF-1` como teste de ressonância | **sem veredito**; nunca dizer que testou o pico |
| `E004R` | `7,9σ` post-hoc, `RF-1`, `RF-4=1489` | respectivamente **post-hoc**, **sem veredito** e **inválido por passo de tempo** |
| `I003` | queda de deriva `0.917→0.203 cm/s` | **exploratória**; não fecha `L9.1` nem lei de malha |
| `E005` | coincidência `RA-2 = 0.40σ` | **exploratória**; não é teste do limite linear |
| `A005` | leitura `H_comum` a partir de `v∥=0.822` | **sugestiva pós-dado**, sem veredito formal |
| `A005R` | todas as três tentativas | **falha operacional**; nenhum observável científico foi produzido |

Esses valores podem ser citados ao explicar falhas, supersessões ou desenho de nova missão,
desde que o rótulo acima viaje junto. Não podem aparecer como suporte positivo de conclusão.

## Estado das missões ainda abertas

| missão | estado | gate | consequência |
|---|---|---|---|
| `A004` | `PENDING` de aceite humano | passou | resultado avaliável; recomendação técnica: aceitar com limitações |
| `A005` | `REVISION_REQUESTED` | falhou | `AR-1` não tem veredito; ressalva de convergência para `C-15` |
| `A005R` | `INCOMPLETE` | não avaliado | três timeouts em `relax()`, zero OVF; não desbloqueia `A007` |
| `A005R2` | `PROPOSED` | não executado | precisa de leitura e autorização literal novas |
| `A006` | autorizada | pré-registro ainda não lido | ataca `L2.3` |
| `A007` | autorizada, bloqueada | pré-registro ainda não lido | só depois de convergência comparável |
| `A008` | autorizada | pré-registro ainda não lido | ataca malha e contínuo |

## Reconstrução documental da proveniência histórica

Os diretórios anteriores à regra de 2026-08-27 estão isentos de manifesto retroativo. A
linhagem verificável disponível é a seguinte; isto **não** finge saber modelo, prompt ou papel
de IA que não foram registrados na época.

| grupo | promessa | material / ocorrido | autoridade |
|---|---|---|---|
| `R001`, `R002`, `A002` | `MISSIONS/MISSION-*.md` | `EVIDENCE/<id>/`, `RELEASES/RELEASE-*.md` | `WB-007` |
| `AUDIT-001` | protocolo no release/consolidação | `EVIDENCE/AUDIT-001/`, `RELEASE-AUDIT-001.md` | `WB-007`; ação externa em `WB-005` |
| `AUDIT-002`, `E001` | missão/release correspondente | evidência selada e releases/adendos | `WB-009` |
| `E002` | `MISSION-E002.md` | evidência + release/adendo | `WB-011` |
| `E003`, `I001` | missões correspondentes | evidência + releases/adendo | `WB-015` |
| `E004R`, `I002` | missões correspondentes | evidência + releases | `WB-018` |
| `I003` | `MISSION-I003.md` | evidência + release | `WB-019` |
| `E004`, `E005` | missões correspondentes | evidência + releases | `WB-021` |
| `A003` | `MISSION-A003.md` | evidência + release | `WB-023` |
| `A004`, `A005` | missões correspondentes | evidência + releases | autorização `WB-024`; aceite ainda não dado |
| `A005R` | `MISSION-A005R.md` | evidência + `RELEASE-A005R.md`; manifesto funcional local | autorização `WB-025`; sem aceite |

## Prioridade recomendada

1. Resolver documentalmente `A004` por decisão humana.
2. Revisar e, se aprovado, autorizar `A005R2`; só um teste avaliável pode rever a ressalva do
   `C-15` e o bloqueio de `A007`.
3. Executar a sequência científica `A006` → `A007` → `A008`, sempre após leitura do
   pré-registro específico; pular `A007` se continuar bloqueada.
4. Depois, criar missões próprias para estimador cego na fronteira, `L9.1` e `L8.4`.

## Regra de uso desta consolidação

Ela é um índice de força e prioridade. Quando houver conflito, a autoridade é o writeback
humano mais recente; a integridade material é o `SHA256SUMS.txt`; e o limite integral do claim
é o texto canônico do writeback que o aceitou.
