# WRITEBACK-012 — `MISSION-E003` autorizada (deriva presa à ligação ou à rede?)

Data: 2026-08-25 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Autorizado MISSION-E003"

seguida da desambiguação, quando perguntei qual das duas eu havia colidido sob esse nome:
> "As duas, nesta ordem"

## A colisão de nomes, e como fica
**O embaraço foi meu:** usei "E003" para duas missões diferentes na mesma mensagem — na tabela
de alternativas era a varredura de frequência (como o `STATE.md` também chamava), e no
parágrafo final era a minha recomendação principal, o teste fora do eixo. Perguntei antes de
escrever o pré-registro, porque pré-registro não se edita depois.

Numeração fixada pela resposta *"as duas, nesta ordem"*:

| | missão | estado |
|---|---|---|
| **`E003`** | deriva presa à **ligação** ou à **rede**? (teste fora do eixo) | **AUTORIZADA aqui** |
| `E004` | varredura de frequência, `v_sp(f)` (Fig. 3) | **não autorizada** — precisa de sim próprio quando chegar a vez |
| `E005` | LLG estocástica, `T > 0` (Fig. 4) | não proposta |

Isto **renumera** o que o `STATE.md` chamava de `E003`/`E004`; corrigido lá.
**`E004` não está autorizada por esta ordem.** A opção escolhida dizia, no próprio texto, que
a segunda precisaria de autorização própria — e o §2 do `CLAUDE.md` diz que missão terminada
não autoriza a seguinte. Se você quis autorizar as duas de uma vez, corrija.

## O que fica autorizado
`MISSION-E003`, pré-registro em `LAB/MISSIONS/MISSION-E003.md`, escrito **antes** de qualquer
código novo e de qualquer corrida. Inclui derivar binário novo do `saf_prop.cu` selado,
compilá-lo e rodá-lo — ação local, não é ação de sistema nem externa.

## Por que esta missão
Ao escrever o `RELEASE-E002` eu registrei que o `EP-1` passou por simetria. Revendo, o
problema é **pior**: nas três corridas a ligação ficou ao longo de `x` e a deriva saiu ao
longo de `y`, de modo que os dados **não distinguem "perpendicular à ligação" de "ao longo de
um eixo da rede"**. As duas hipóteses preveem o mesmo resultado naquele arranjo. Isso é um
**confundimento no `C-7`**, não apenas um teste fraco, e o `L7.2` subestimava.

## O que este writeback NÃO faz
- **Não é aceite** de nada; passar gate não é aceite.
- **Não autoriza** `E004`, `E005`, a etapa 2 do `AUDIT-001`, nem compilar extensão do OOMMF.
- **Não é freeze**, e **não fecha `L-G`** — nenhuma corrida minha fecha.
- **Não resolve** `D-1`/`D-2`/`D-3`, que seguem pendentes da sua consulta aos autores.

## Próximo head/estado
`STATE-2026-08-25-g`

## Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar o `E003`, depois do release.
