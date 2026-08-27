# RELEASE-E003 — a deriva está presa à LIGAÇÃO, não à REDE

Missão: `MISSION-E003` · Autorizada por `WRITEBACK-012` (2026-08-25, *"Autorizado MISSION-E003"*)
Execução: 2026-08-25 · `human_acceptance: PENDING`
Evidência: `LAB/EVIDENCE/E003/` (selada por `SHA256SUMS.txt`)

---

## 1. Veredito
**`H_ligação`, e por margem decisiva.** O confundimento que o `E002` deixou no `C-7` está
removido: a deriva acompanha a **ligação**, não um eixo da malha.

O discriminante pré-registrado era a **inclinação** de `φ_drift` contra `θ_bond`, medida em
dois ângulos:

|  | previsão | medido |
|---|---|---|
| **`H_ligação`** | `dφ_drift/dθ_bond = +1` | **`+1.0201`** |
| **`H_rede`** | `dφ_drift/dθ_bond = 0` | — |

Girei a ligação para `25.86°` e `18.09°` (após relaxar) e a direção da deriva foi para
`123.57°` e `115.65°`: as duas diferenças são `+7.77°` e `+7.92°`. **A deriva girou junto com
a ligação, quase exatamente 1:1.**

**O gate `G-E003` passou.** Não é aceite.

## 2. Como o teste foi construído para não poder ser resgatado
Nenhum limiar absoluto entra no critério primário — foi a lição das quatro regras mal
desenhadas do `E002`. As duas hipóteses fazem previsões **exatas e diferentes** (`+1` e `0`),
e o número medido cai sobre uma delas. `45°` foi descartado no pré-registro por ser **eixo de
espelho da rede quadrada**, onde qualquer proteção de simetria existente a `0°` continuaria
valendo; `60°` foi descartado por ser `30°` refletido.

## 3. O defeito que apareceu, e que é um achado
**Fora do eixo, a relaxação do meu código NÃO converge.** A `θ = 0` ela chega a
`torque = 1e−6 T` em 189 825 iterações; a `30°` e `22.5°` ela **bate no teto de 2×10⁶
iterações com o torque parado em `1.26e−5 T`**.

A consequência foi medida no controle `EO-0`, **sem excitação alguma**:

| | deriva espúria | direção | decai? |
|---|---|---|---|
| `θ = 0°` (E002 `PV-1`) | `3.99e−2 cm/s` em 10–20 ns | — | **sim**, para `7.1e−5` em 150–200 ns |
| `θ = 30°` | **`0.91745 cm/s`** | `+0.140°` da ligação — **ao longo dela** | **não**, constante em 20 ns |
| `θ = 22.5°` | **`0.90379 cm/s`** | `+0.138°` da ligação | **não** |

São **~23×** a deriva espúria de `θ = 0` na mesma janela, e ela **não decai**. Pela regra
registrada em §4.2 do pré-registro, isto seleciona **`M-rede`**: a proteção que mantém
`v_∥ = 0` exatamente a `θ = 0` **depende de a malha ter um espelho ali**, e não é propriedade
só da configuração. A ambiguidade que eu me recusei a resolver por conjectura no pré-registro
foi resolvida **por medida**.

**Interpretação física, conjectural:** a `Γ = G/α𝒟̄` alto, uma força de rede (tipo Peierls)
perpendicular à ligação produz deriva **giroscópica ao longo** dela. Explica a direção
(`+0.14°` da ligação) e o caráter não-decadente. **Não testado.**

### Este defeito NÃO contamina o `E002`
A `θ = 0` a deriva espúria decai para `7.1e−5 cm/s` na janela de ajuste (150–200 ns), isto é
0,002 % do sinal. O `θ = 0` é **comensurável** com a malha, e é por isso que o `E002` nunca
viu este artefato. `C-7` não muda por causa disto.

## 4. O que a contaminação explica — e o que não explica
O desvio da perpendicularidade **não é zero**: é `+7.71°` e `+7.56°` na janela de 50–100 ns.
A contaminação medida **independentemente no `EO-0`** prevê exatamente esse desvio, por
`atan(v_espúria/|v|)`:

| θ | janela | `\|v\|` [cm/s] | desvio medido | previsto pela `EO-0` | razão |
|---|---|---|---|---|---|
| 30.0 | 25–50 ns | 14.4490 | `+3.2844°` | `+3.6332°` | 0.904 |
| 30.0 | 50–100 ns | 6.0841 | `+7.7138°` | `+8.5754°` | 0.900 |
| 22.5 | 25–50 ns | 14.4565 | `+3.2280°` | `+3.5773°` | 0.902 |
| 22.5 | 50–100 ns | 6.0869 | `+7.5573°` | `+8.4456°` | 0.895 |

**Razão 0.90 nas quatro** — dois ângulos × duas janelas. A previsão usa só números do
controle, medidos **antes** das corridas excitadas, e o pré-registro (§4.3) já dizia que a
escala do `EO-0` é a referência do `EO-1`.

**O que ela não explica:** ~10 %, isto é `0.8°` na janela tardia. Sistemático, presente nas
quatro medidas, **sem explicação**. Fica registrado como resíduo aberto, não arredondado para
zero. Note que o *teste de inclinação* é **imune** a tudo isto: a contaminação é ao longo da
ligação nos dois ângulos, logo desloca o offset e não a inclinação.

## 5. Convergência da direção — e a regra que eu não violei
As janelas de 25–50 e 50–100 ns dão desvios diferentes: `4.43°` e `4.33°` de diferença.
Pela regra do §6 isso seria "direção não convergida" — **e eu não estendi a corrida**, porque
estender depois de ver o dado é escolher a janela pelo resultado.

Mas a diferença **não é ruído nem deriva de convergência**: é a contaminação **constante**
dividida por um sinal que **decai** (14.4 → 6.1 cm/s). O valor previsto por essa conta é
`4.94°`; o medido é `4.43°` e `4.33°`. O que não converge é o *offset*, por uma causa
identificada e medida — não a **inclinação**, que é o critério.

**Imprecisão do meu pré-registro, registrada:** o §4.3 diz "dispersão angular do controle" sem
definir qual. Há duas leituras — a dispersão do próprio ângulo do controle (`0.04°`) ou a
escala angular que a contaminação impõe ao `EO-1` (`8.6°`). Sob a primeira, a direção não
converge; sob a segunda, converge. **Quinta imprecisão de desenho desta linha de trabalho**,
registrada e não reparada. O veredito não depende dela: a inclinação decide sozinha.

## 6. Secundários
- **`EO-0.1` PASSOU.** `Q₁ = −1.0000`, `Q₂ = +1.0000`; `l_eq` = `10.953118` (θ=30°) e
  `10.956750 nm` (θ=22.5°) contra `10.960706` a θ=0° — `−0.069 %` e `−0.036 %`, critério < 1 %.
  Sem aprisionamento em eixo: a ligação girou `−3.98°` e `−4.25°` e parou longe de 0/45/90°.
- **`EO-2`** (exploratório): `|v|` na janela casada de 50–100 ns dá `6.0385` (θ=0°),
  `6.0841` (+0.75 %) e `6.0869 cm/s` (+0.80 %). Parte disso é a própria contaminação somada
  em quadratura. Não é critério e não é resultado.
- **Regressão verificada antes de tudo:** a `θ = 0` o `saf_prop3` reproduz o
  `prop_sbm_18.00GHz.dat` do `E002` **bit a bit** nas 2501 amostras dos primeiros 5 ns.

## 7. Efeito sobre o `C-7`
O `L7.2` dizia que a perpendicularidade não estava testada, porque `v_∥ = 0` era forçado por
simetria e porque ligação e deriva coincidiam com eixos da malha. **Isso deixa de valer**: a
deriva acompanha a ligação com inclinação `1.02` em dois ângulos fora dos espelhos da rede.

O que fica testado é **"a deriva acompanha a ligação em dois ângulos além de zero"** — não
"em qualquer ângulo", como o artigo afirma. E fica testado **só no modo SBM**.

## 8. Limites
- **`L-G` INTOCADO.** Esta missão **removeu um confundimento interno** do meu próprio código.
  Não é verificação independente de nada. Nenhuma camada nova foi verificada por terceiro.
- Um ponto de parâmetros, um modo (SBM), dois ângulos, malha de 1 nm, caixa de 100 nm.
- **A magnitude assintótica continua não medida** (`L7.3`): estas corridas são de 100 ns, mais
  curtas que as de 200 ns do `E002`, que já não haviam estacionado.
- **Artefato de comensurabilidade novo e não caracterizado:** fora do eixo a relaxação não
  converge e há deriva espúria constante de ~0.9 cm/s. Quanto disso é força de rede e quanto é
  viés do rastreador de CTC **não foi separado**.
- Resíduo de 10 % (`0.8°`) na explicação do desvio, **sem causa identificada**.
- Não toca `D-1`/`D-2`/`D-3`, que seguem pendentes da consulta aos autores.

## 9. Custo
`279 s` cada controle de 20 ns; `1175 s` cada corrida excitada de 100 ns. Total ≈ 48 min.

## 10. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar. Nada está congelado.
