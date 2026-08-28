# MISSION-A005R2 — viabilidade e comparação por checkpoints de convergência

Estado: **`PROPOSED` — NÃO AUTORIZADA** · Data: 2026-08-27  
Regime: nova revisão após a interrupção operacional de `A005R`

> **Pré-registro.** Escrito depois de ver somente que as três chamadas monolíticas de
> `relax()` excederam 3600 s sem output. Nenhuma saída científica de `A005R` existiu. Este
> documento não herda a autorização do `WB-025` e não pode ser executado antes de leitura e
> autorização literal de Rodrigo.

## 1. Pergunta

É possível colocar mumax3 e `saf.cu` em estados de convergência **materialmente comparáveis**,
com progresso observável e recuperável, antes de reinterpretar a deriva do `A005` ou o
`−0,30 %` do `C-15`?

O defeito corrigido não é físico: `A005R` tornou `relax()` uma operação monolítica. Três
timeouts consumiram três horas sem torque final, checkpoint ou estado. Esta missão mede
primeiro a viabilidade; só executa dinâmica se a escada de convergência der veredito.

## 2. Hipóteses e desfechos permitidos

- **`H_full`:** mumax3 alcança `MaxTorque ≤ 1,0e−6 T`; comparação integral com o estado
  `saf.cu` canônico é possível.
- **`H_partial`:** mumax3 estabiliza num piso acima de `1,0e−6 T`, mas esse piso é mensurável
  e reproduzível; permite comparação casada auxiliar, não revisão definitiva de `C-15`.
- **`H_nonconvergent`:** não há progresso mensurável/repetível dentro do orçamento; a via
  mumax3 para este controle é operacionalmente inadequada.

Nenhum desses desfechos será renomeado depois de observar `l` ou velocidade.

## 3. Estágio V — instrumentos e poder, antes da corrida científica

1. Confirmar na fonte/localmente que `MaxTorque` e o critério do `saf.cu` estão na mesma
   grandeza (tesla), registrando arquivo e linha.
2. Copiar para `A005R2` — nunca sobrescrever — o último estado selado do `A003` como ponto de
   partida e medir seu `MaxTorque` antes de qualquer relaxação.
3. Verificar que cada processo escreve em diretório próprio e salva estado inicial.
4. Cronometrar e registrar cada degrau separadamente; não usar uma única chamada para vários
   critérios.

**Gate `V-0`:** unidade verificada + estado inicial legível + torque inicial impresso + hash
do input. Se falhar, parar sem corrida científica.

## 4. Estágio F — escada de viabilidade com checkpoints

Aplicar, nesta ordem fixa, alvos de `MaxTorque`: `2e−5`, `1e−5`, `3e−6`, `1e−6 T`. Cada degrau:

- inicia do último checkpoint bem-sucedido;
- roda em processo separado, com timeout de **900 s**;
- ao completar, imprime `MaxTorque`, `E_total`, tempo/iterações disponíveis, mede `l` e salva
  um novo checkpoint imutável;
- ao expirar, preserva todos os degraus anteriores e encerra a escada — não tenta alvos mais
  baixos na mesma execução.

**Orçamento do estágio:** máximo de quatro processos e `3600 s` de parede. Não aumentar o
timeout após ver `l`.

### Classificação mecânica

- **FULL:** um checkpoint mede `MaxTorque ≤ 1,0e−6 T`.
- **PARTIAL:** ao menos dois checkpoints melhoram monotonicamente o torque, mas o próximo
  degrau expira; repetir uma vez o último degrau completo deve reproduzir torque dentro de
  fator `1,2`. O melhor valor vira `T*`.
- **NONCONVERGENT:** menos de dois degraus completos, torque não melhora monotonicamente ou
  a repetição difere por mais de fator `1,2`.

Em `NONCONVERGENT`, a missão termina. Não há `AC-1`, `AC-2` ou `AC-3`.

## 5. Casamento permitido

- Em **FULL**, usar `1,0e−6 T` nos dois solvers.
- Em **PARTIAL**, produzir um novo estado `saf.cu` interrompido na faixa
  `[T*/1,2, 1,2·T*]`. Essa escolha depende **somente do torque**, antes de medir velocidade
  ou comparar `l`. O par parcial serve para diagnosticar sensibilidade; não substitui o
  estado canônico `saf.cu` a `1e−6 T`.

Se o `saf.cu` não puder parar nessa faixa de forma auditável, classificar o casamento como
**UNMATCHED** e não executar dinâmica comparativa.

## 6. Convergência da saída

Antes dos critérios físicos, comparar os dois últimos checkpoints bem-sucedidos:

- `l` é estável se variar `≤0,05 %`; esse poder é seis vezes menor que a discrepância de
  `0,30 %` que se quer interpretar;
- uma velocidade é estável se variar `≤10 %` entre duas janelas tardias iguais; isso é muito
  menor que a separação de fator `>2` das hipóteses do `AC-1`.

Falha de estabilidade da **saída** dá `NO_VERDICT`, mesmo que o torque de entrada atinja o
alvo. Não ajustar esses limites após os dados.

## 7. Critérios científicos condicionais

Só executar esta seção se o casamento for `FULL` ou `PARTIAL` e a saída relevante estiver
estável.

### `AC2-1` — deriva sem excitação, `θ=0°`

Mesma janela, duração, malha e torque nos dois códigos. Razão
`R0=|v_mumax3|/|v_saf.cu|`:

- `0,5 ≤ R0 ≤ 2`: apoia que a diferença do `A005` era convergência;
- `R0 > 2`: há resíduo específico de implementação/ferramenta;
- denominador compatível com zero ou saída não estável: `NO_VERDICT`.

### `AC2-2` — componente ao longo da ligação, `θ=30°`

Razão `R∥=|v∥,mumax3|/|v∥,saf.cu|`:

- `0,5 ≤ R∥ ≤ 2`: apoio a `H_comum`;
- `R∥ ≤ 0,1`: apoio a `H_nosso`;
- entre as bandas, sinal incompatível ou saída não estável: `NO_VERDICT`.

### `AC2-3` — comprimento do par e `C-15`

Medir cada checkpoint com o estimador cego do `AUDIT-002`.

- Em **FULL**, comparar diretamente com `10.9607 nm`: subir e reduzir `|Δl|` apoia efeito de
  convergência; ficar estável apoia diferença de código; descer refuta ambas as leituras.
- Em **PARTIAL**, relatar somente a curva `l(MaxTorque)` e sua estabilidade. Não promover
  extrapolação, não substituir `−0,30 %` e não declarar a ressalva do `C-15` resolvida.

## 8. Gate e efeito sobre `A007`

`G-A005R2` passa somente com: `V-0` + classificação FULL/PARTIAL + casamento auditável +
veredito em `AC2-1`, `AC2-2` e `AC2-3`.

**`A007` só pode ser desbloqueada por caminho FULL**, saída de velocidade estável e
`0,5≤R0≤2`. PARTIAL é informação útil, mas não demonstra piso residual baixo o suficiente
para dinâmica dirigida. Passar o gate não é aceite; desbloqueio e aceite continuam humanos.

## 9. Paradas e orçamento total

- Parar imediatamente em `V-0` falho ou `NONCONVERGENT`.
- Parar a dinâmica se o casamento for `UNMATCHED` ou a saída estática não convergir.
- Máximo total: **3 h de parede**, incluindo a escada, repetição, estado `saf.cu` e corridas
  dinâmicas. Ao atingir o teto, preservar checkpoints e publicar release incompleto.
- Proibido aumentar tempo, trocar tolerância, descartar checkpoint ou escolher janela depois
  de observar qual hipótese favorece.

## 10. Proveniência e limites

Novo diretório `LAB/EVIDENCE/A005R2/`, com `AI-PROVENANCE.json` antes do selo. Solver e régua
podem ser independentes; leitura do modelo e inicialização continuam compartilhadas. mumax3
é float32 e `saf.cu` double. Um ponto, uma malha, dois ângulos e `T=0`. Nenhuma ação externa,
aceite, freeze ou publicação é autorizada por este pré-registro.

