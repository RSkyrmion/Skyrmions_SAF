# WRITEBACK-034 — correção do `C-13` e autorização de escrever a `A008`

Data: 2026-08-28 · Autoridade: Rodrigo

## Decisões humanas (literais)
> "A questão do dt ser proporcional a a² é obvia: a relação entre o tempo real (medido em
> segundos) e o tempo admensional (tempo de integração em unidades reduzidas) é
> \delta t = \left(\frac{M_s a²}{2 \gamma A_{ex}}\right) \delta \tau, em que \delta t é o tempo
> em segundos e \delta \tau é o tempo admensional"

> "Concordo"

## 1. A observação de Rodrigo procede, e é mais forte que "óbvio"
A relação que ele escreve é **exatamente** `t₀ = M_s a₀²/(2 A_ex γ)`, que está registrada em
`RELEASE-E001-ADDENDUM-002.md` **linha 11**, implementada e conferida contra a rota física com
energias idênticas em 16 dígitos, em 2026-08-24.

Ou seja: quando o `I003` (2026-08-26) apresentou `dt ∝ a²` como achado empírico, ele estava
**redescobrindo por medida o que a evidência selada deste laboratório já dava analiticamente**,
dois dias antes.

## 2. Correção de proveniência do `C-13`
O `C-13` **continua aceito** (`WB-019`) e o seu conteúdo operacional continua correto.
O que muda é a **origem**:

> `dt ∝ a²` é **consequência analítica de `t₀`**, verificada no `E001-ADDENDUM-002`.
> O `I003` **confirmou por medida** e, adicionalmente, mostrou que o estado ligado sobrevive a
> `0.5 nm` quando o passo é corrigido — isto sim não segue da fórmula.

Registrado em `RELEASE-I003-ADDENDUM-001.md`; a entrada do `CLAUDE.md` §8 foi trocada de
"medido" para "analítico … confirmado por medida". O `RELEASE-I003.md` **não foi editado**.

Nenhum claim é revogado. `L13.1` (a redução de deriva `4.5×` é exploratória) segue valendo.

## 3. Autorizado: escrever o pré-registro da `A008`
"Concordo" refere-se à recomendação de **parar de investigar convergência** e atacar a
**malha**, mais o adendo do `C-13`.

**Interpretação registrada:** autoriza **escrever** o pré-registro da `MISSION-A008` e o adendo
acima. **Não autoriza executar** a `A008` — o `CLAUDE.md` §2 exige leitura do pré-registro por
Rodrigo antes da execução, e nada aqui dispensa isso. Se a intenção era autorizar também a
execução, corrija e este writeback será superado.

## 4. Registro de decisão negativa — o que fica explicitamente parado
- **A investigação de convergência (`A005R`/`A005R2`) encerra-se aqui.** O resíduo de `0,052 %`
  está ~20× abaixo da sensibilidade de malha de `1,01 %`, e a checagem de poder do `A003` já
  declarara, antes do dado, que acordo abaixo de `1 %` não separa "ambos certos" de "ambos com
  o mesmo erro". Mais precisão nesse eixo **não compra evidência**.
- **O portão da `A007` NÃO é reescrito.** Ele exige `MaxTorque ≤ 1e−6 T`, que o mumax3 não
  alcança (piso `1.7e−5`, float32) — logo a `A007` está bloqueada indefinidamente por um
  critério mal escolhido. **Eu apontei isso e deliberadamente não proponho mudá-lo**: alterar
  portão pré-registrado depois que ele me atrapalha é o movimento que o §6.2 proíbe ao
  executor. A iniciativa, se houver, é de Rodrigo.

## Próximo head/estado
`STATE-2026-08-28-b`
