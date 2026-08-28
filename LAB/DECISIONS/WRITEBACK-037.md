# WRITEBACK-037 — décima barreira: ledger append-only aplicado no shell

Data: 2026-08-28 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Execute isso"

referindo-se à recomendação de estender o `guard-bash.sh` para bloquear escrita por redireção
de shell sobre arquivo existente em `LAB/DECISIONS/` e `LAB/RELEASES/`.

## 1. O que motivou — e é o pior tipo de falha
Em 2026-08-28, dois agentes gravaram o `WRITEBACK-033` e **um destruiu o registro do outro**.
Perdeu-se o writeback que continha a autorização literal de Rodrigo para a `A005R2` e o
autoexame da execução irregular de 27/08. **A frase de Rodrigo sobreviveu apenas porque o
`WB-036` a citou.**

O guarda de `Edit/Write` do §9 cobre `DECISIONS/` e `RELEASES/` — mas **nós dois escrevemos com
`cat >`**, canal que ele não vê. É o mesmo "limite honesto" que o §9 já documentava para
binários compilados, agora atingindo **o ledger de decisões**: a única parte do laboratório que
é append-only por princípio, e o único registro da autoridade humana.

**Eu usei `cat >` em `DECISIONS/` dezenas de vezes sem uma vez perceber que contornava o
guarda.** Uma regra que o executor ignora sem notar não é defesa — é o critério do §9 para
promover regra a hook.

## 2. O que foi implementado
Caso 3 novo no `.claude/hooks/guard-bash.sh`: extrai alvos de `>`/`>>`, `tee`, `cp`/`mv`/
`install` e `sed -i`; se algum cair em `LAB/DECISIONS/` ou `LAB/RELEASES/` **e o arquivo já
existir**, **bloqueia** (`deny`).

Mapeia o §3 literalmente: *"nunca se editam"*. **Arquivo novo passa** — é assim que writeback e
release nascem. **Sobrescrita não passa.**

### Teste executado, com os casos que NÃO podem ser bloqueados
| caso | resultado |
|---|---|
| sobrescrever writeback existente | **BLOQUEIA** |
| sobrescrever release existente | **BLOQUEIA** |
| `sed -i` em writeback existente | **BLOQUEIA** |
| `cp` por cima de release existente | **BLOQUEIA** |
| criar writeback **novo** | passa |
| criar release **novo** | passa |
| ler writeback, escrever em `/tmp` | passa |
| selar evidência (`sha256sum > SHA256SUMS.txt`) | passa |
| comando comum | passa |

## 3. Limites conhecidos desta barreira — declarados, não escondidos
1. **É textual.** O hook vê a string do comando e não distingue "escreve aqui" de "menciona
   este caminho". Um comando que apenas *cite* `> LAB/DECISIONS/<existente>` dentro de aspas
   será bloqueado. Aconteceu duas vezes ao testar esta própria regra.
   **É o lado certo para errar:** perder um registro de decisão é catastrófico; reescrever um
   comando é trivial.
2. **Não fecha a corrida.** Se dois agentes verificarem e gravarem o mesmo número novo no mesmo
   instante, a colisão ainda ocorre. Fechar exigiria alocação atômica de número — outra ordem
   de complexidade, **não implementada**.
3. **Não cobre um binário compilado** que escreva nesses diretórios, pela mesma razão do §9.
4. **Não repara o dano já feito.** O `WRITEBACK-033` perdido **não foi regravado**: regravá-lo
   clobbaria o registro do agente concorrente e repetiria exatamente o erro. A colisão está
   documentada no `STATE` e aqui.

## 4. Efeito no `CLAUDE.md`
O §9 passa de **nove** para **dez** barreiras.

## 5. O que isto NÃO faz
Não aceita missão, não autoriza executar a `A008`, não desbloqueia a `A007`, não é freeze nem
ação externa.

## Próximo head/estado
`STATE-2026-08-28-f`
