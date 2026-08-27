# RELEASE-A005 — `AR-0` FALHOU. E a causa qualifica o `A003`.

Missão: `MISSION-A005` · Autorizada por `WRITEBACK-024` · Execução: 2026-08-27
`human_acceptance: PENDING` · Evidência: `LAB/EVIDENCE/A005/` · Custo: 4,6 min

## 1. Veredito
**`AR-0` FALHOU. Gate `G-A005` NÃO passou, e a `A007` fica BLOQUEADA** — como o pré-registro
mandava. **Mas a causa está identificada, e ela qualifica o `C-15` do `A003`.**

## 2. As medidas
| corrida | `θ_ligação` | `\|v\|` | `v_∥` | `v_⊥` | ângulo vs ligação |
|---|---|---|---|---|---|
| `AR-0` (`θ = 0°`) | `−180.000°` | `1.75489` | **`+0.00000`** | `+1.75489` | `+90.00°` |
| `AR-1` (`θ = 30°`) | `−150.196°` | `1.90013` | **`+0.82177`** | `+1.71323` | `+64.37°` |

`AR-0` exigia `|v| < 0.05 cm/s`. Mediu **`1.755`** — 35× o critério, e **25 000×** o que o
`saf.cu` dá na mesma condição (`7.1e−5 cm/s`, `E003`).

## 3. A causa: as duas relaxações NÃO estão casadas
O `MaxTorque` do mumax3 é declarado no fonte em **tesla** (`torque.go:24`, *"Maximum
torque/γ0"*) — **a mesma grandeza** do nosso critério de relaxação. E:

| | torque final |
|---|---|
| `saf.cu` (`relax`, tol pré-registrada) | `1.0e−6 T` |
| `mumax3` (`relax()` + `minimize()` ×2, **padrão**) | `4.5e−5 T` |

**O mumax3 para 45× mais frouxo.** E o `E003` já mediu que a deriva residual escala
**linearmente** com a tolerância: `tol = 1e−5` ⇒ `0.632 cm/s`; `tol = 1e−6` ⇒ `0.063` —
exatamente 10×. Extrapolando para `4.5e−5`: **~2.8 cm/s**. Medido: `1.755`. Mesma ordem.

**A deriva do `AR-0` é a resposta giroscópica ao torque residual**, fenômeno já caracterizado
no `E003` — não é falha do mumax3 nem física nova.

### O defeito é do meu pré-registro — o décimo, e de tipo novo
Os nove anteriores eram de **forma de critério**. Este é diferente: **eu nunca especifiquei
que a convergência das duas relaxações tinha de ser casada.** Comparar dois códigos deixando
cada um parar no seu próprio padrão não compara os códigos — compara os padrões.
Registrado, **não reparado**: o `AR-0` falhou como escrito.

## 4. `AR-1` — sem veredito formal, mas o dado decompõe-se sozinho
O gate caiu, logo o `AR-1` **não tem veredito**. Registro o que o dado mostra, com essa
etiqueta:

A componente **perpendicular** é praticamente a mesma nos dois ângulos (`1.755` e `1.713`) —
é a deriva residual, presente **independentemente do ângulo**. A componente **ao longo da
ligação** aparece **só fora do eixo**: `0` a `θ = 0°` e **`0.822`** a `θ = 30°`.

`0.822` contra os `0.917` do `saf.cu` na mesma condição: **razão `0.896`**.

Isto **aponta** para `H_comum` — o artefato de rede aparece nos dois códigos —, e a
decomposição é limpa porque a contaminação perpendicular é comum aos dois ângulos e sai da
comparação. **Mas é decomposição feita depois de ver o dado, e o critério pré-registrado está
sem veredito. Não é resultado.**

## 5. **O que isto qualifica no `A003`/`C-15`**
**O estado do `MV-2` foi relaxado com o mesmo padrão frouxo.** `l_mumax3 = 10.9279 nm` veio de
um estado **45× menos convergido** que o nosso `10.9607`.

E a direção do efeito é conhecida e medida: no `E003`, relaxação mais frouxa dá `l` **menor**
(`tol 1e−5` ⇒ `10.9529`; `tol 1e−6` ⇒ `10.9607`). O mumax3, a `4.5e−5`, daria `l` ainda menor.

**Portanto parte dos `−0.30 %` do `C-15` pode ser descasamento de convergência, não diferença
entre os códigos.** Isso **não invalida** o `C-15` — os `−0.30 %` estão medidos e o gate passou
—, mas muda a leitura: **o acordo verdadeiro pode ser melhor que `0.30 %`**, e o número atual
não separa "diferença de código" de "diferença de convergência".

**Recomendação de registro:** esta ressalva deve viajar com o `C-15` até ser resolvida, e a
redação do `L-G` no `CLAUDE.md` §7 **não muda** por causa dela — o `−0.30 %` continua sendo o
que foi medido, e a frase já diz que o acordo está abaixo da resolução do método.

## 6. O caminho para resolver — proposto, NÃO executado
O mumax3 expõe `RelaxTorqueThreshold` (`relax.go:17`). Casar a convergência é **uma linha**.
Mas escolher esse valor **depois** de ver a falha é escolher configuração por resultado.
Proponho, sem executar: uma missão que **pré-registre o casamento** (`RelaxTorqueThreshold =
1e−6`, o mesmo do `saf.cu`) e refaça **`AR-0`, `AR-1` e o `MV-2` do `A003`**. Custo ≈ 20 min.

## 7. Limites
- `AR-1` **sem veredito**. `L9.1` e `L8.4` seguem abertos.
- `L-G` intocado por esta missão; e o `C-15` fica com a ressalva do §5.
- Um ângulo por corrida, 20 ns, malha de 1 nm, `α = 0.02`.
- **Custo medido, corrigindo uma suposição minha:** o mumax3 faz 20 ns em `~139 s` = **7 s/ns**,
  contra `11.15 s/ns` do `saf.cu`. Eu havia dito que ele podia ser mais lento; é **1.6× mais
  rápido**. Isso melhora a perspectiva da `A007`.

## 8. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar. E decidir sobre a missão de casamento
de convergência do §6, que destrava a `A007` e resolve a ressalva do `C-15`.
