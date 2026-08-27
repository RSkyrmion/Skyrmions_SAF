# MISSION-E003 — a deriva está presa à LIGAÇÃO ou à REDE?

Estado: **`AUTHORIZED`** por `WRITEBACK-012` · Data: 2026-08-25
Regime: teste de confundimento · Terceira missão da Fase 2

> **Pré-registro.** Escrito e congelado ANTES de escrever uma linha de código novo e ANTES de
> qualquer corrida.
>
> **Lição aplicada do `E002`:** quatro critérios daquela missão falharam por serem **limiares
> absolutos contra referências que não os sustentavam**. Aqui, os critérios são
> **comparações entre duas hipóteses**, e a escala de ruído vem de um **controle medido
> antes** de qualquer limiar ser escrito. Nenhum limiar absoluto é usado no critério primário.

---

## 1. A pergunta, e por que ela existe
No `E002` a ligação ficou ao longo de `x` e a deriva saiu ao longo de `y`. **Duas hipóteses
diferentes preveem exatamente isso:**

- **`H_ligação`** (o que o artigo afirma): a deriva é perpendicular à **ligação**,
  *"irrespective of the bond's orientation"*.
- **`H_rede`**: a deriva segue um eixo da **malha**, e a coincidência com a perpendicular à
  ligação é artefato do arranjo.

Os dados do `E002` **não separam as duas**. Isto é um confundimento no claim `C-7`, e o
`L7.2` o subestimava ao chamar de "teste fraco". Girar a ligação separa as hipóteses.

## 2. Ponto de operação
Idêntico ao `E002`, para que a comparação seja casada: `A_int = 0.02 mJ/m²`, `K₀ = 0.6 MJ/m³`,
`α = 0.02`, `T = 0`, grade 100×100 nm², células de 1 nm, PBC. Excitação **SBM**,
`K(t) = K₀[1 + 0.005 sin(ωt)]`, `f = 18.00 GHz` — o modo com maior sinal (3.5 cm/s) e com a
corrida de referência já selada (`EVIDENCE/E002/prop_sbm_18.00GHz.dat`, `θ = 0°`).

**Ângulos iniciais da ligação: `θ = 30°` e `θ = 22.5°.**
Escolha justificada: `45°` seria inútil, porque é **eixo de espelho da rede quadrada** tal
como `0°` e `90°`; qualquer proteção de simetria que exista a `0°` continuaria valendo lá.
`60°` seria `30°` refletido em torno da diagonal — consistência, não ponto independente.
`30°` e `22.5°` são distintos e ambos fora dos espelhos da rede.

## 3. Uma coisa que eu NÃO vou afirmar
Eu ia pré-registrar que, fora do eixo, a discretização **quebra** a simetria que força
`v_∥ = 0`, e usar isso para calibrar tolerância. **Não vou.** Tentei fechar analiticamente
qual operação protege `v_∥ = 0` a `θ = 0°` — troca de camadas combinada com reflexão ou com
`C2`, com a magnetização como vetor axial e o DMI mudando de sinal — e **não fecha limpo**.
Duas leituras seguem vivas:

- **`M-config`:** a proteção é da **configuração** (troca de camadas), independente da rede.
  Então `v_∥ ≈ 0` também fora do eixo, e um `v_∥` grande ali significaria física, não malha.
- **`M-rede`:** a proteção depende de a bissetriz perpendicular ser espelho da malha. Então
  fora do eixo `v_∥` cresce, e o valor é artefato de discretização.

**O `EO-0` decide isso por medida, antes de qualquer limiar.** Registro a ambiguidade agora
para não converter conjectura em critério — que é exatamente como o `PV-0` do `E002` estragou.

## 4. Escada — o controle vem PRIMEIRO

### `EO-0` — controle sem excitação, a `θ = 30°` e `θ = 22.5°`
Relaxar (`tol = 1e−6`, como no `E002`) e rodar **20 ns com a excitação DESLIGADA**.
Três coisas medidas, **antes** de qualquer corrida excitada:

1. **`θ_bond` após relaxação** — aprisionamento pela malha. Se a ligação girar de volta para
   um eixo/espelho da rede (`|θ_bond|` a menos de 5° de `0/45/90°`), o teste fora do eixo é
   **impossível como desenhado**: a missão relata **aprisionamento de malha** como achado e
   **não emite veredito sobre `EO-1`**.
2. **Magnitude e ângulo da deriva espúria.** Referência casada: a `θ = 0°` o `E002` mediu
   `v_⊥ = +7.1e−5 cm/s`, `v_∥ = 0.000000`.
   **Regra de leitura registrada agora:** se a deriva espúria fora do eixo ficar na mesma
   ordem de grandeza da de `θ = 0°`, adoto `M-config`; se subir ordens de grandeza, adoto
   `M-rede`. **Qualquer das duas é resultado**, e nenhuma altera o `EO-1`.
3. **Dispersão angular do controle** — a escala de ruído em graus que o `EO-1` usa como
   referência. Ela é **medida**, não estipulada.

### `EO-0.1` — sanidade do estado relaxado fora do eixo
`|Q₁| = |Q₂| = 1.0000` e `l` a menos de 1 % dos `10.9607 nm` de `θ = 0°`. Se o par não
relaxar para o mesmo ramo não-coaxial, o resto não é comparável e a missão para aqui.

## 5. Critério primário — `EO-1`, uma comparação, não um limiar

Medir o ângulo da deriva `φ_drift` e o ângulo da ligação `θ_bond` no estacionário. Reportar
o **resíduo** `R ≡ (φ_drift − θ_bond) − 90°`, em graus. As duas hipóteses preveem valores
**diferentes e exatos**:

| | previsão de `R` a `θ=30°` | a `θ=22.5°` |
|---|---|---|
| **`H_ligação`** | `0°` | `0°` |
| **`H_rede`** | `−30°` | `−22.5°` |

**Não há limiar a errar.** Reporto `R` com a dispersão angular do `EO-0` ao lado, e a
comparação com `−θ` é imediata do mesmo número.

**Dois ângulos tornam isto um teste de INCLINAÇÃO, não de ponto:** `H_rede` prevê
`R = −θ_bond` (inclinação `−1` contra `θ`), `H_ligação` prevê `R = 0` (inclinação `0`). Duas
hipóteses separadas por `7.5°` já entre os próprios pontos.

**Checagem de poder, antes do dado.** As hipóteses distam `30°` e `22.5°`. No `E002` o ângulo
de deriva saiu por duas rotas independentes (referencial fixo e projeção instantânea) que
concordaram em `<0.01 %`, logo a resolução angular é `≪ 1°`. **O poder é enorme** — três ordens
de grandeza de folga. É o oposto do problema do `EP-2`, cuja banda eu havia inflado por uma
estimativa de sensibilidade errada por fator ~30.

## 6. Janela e convergência — e a regra de o que fazer se falhar
Corridas de **100 ns**, ajuste nos **últimos 50 ns**. Justificativa: mede-se **direção**, que
no `E002` assentou muito antes da magnitude — que, aquela sim, ainda decaía aos 200 ns
(`L7.3`).

**Checagem interna, que faltou ao `E002`:** o ângulo de deriva é medido também em `25–50 ns` e
comparado com `50–100 ns`.

**Regra registrada AGORA para o caso de discordarem** (mais que a dispersão do `EO-0`):
a direção é declarada **não convergida** e a missão relata isso. **A corrida NÃO é estendida
depois de ver o dado** — estender seria escolher a janela em função do resultado, que é o
defeito que o `RELEASE-R002` registrou. Qualquer extensão vira missão nova, pré-registrada.

## 7. Critérios secundários
- **`EO-2`** — magnitude preservada sob rotação. `|v_⊥|` fora do eixo comparada com a de
  `θ = 0°` **na mesma janela de 50–100 ns** (não com o valor tardio), já que o `L7.3` diz que
  aquela corrida não estacionou. Exploratório: sem banda; a rotação não deveria mudar `|v_⊥|`
  no contínuo, e qualquer diferença mede anisotropia da malha.
- **`EO-3`** — `v_∥` no referencial da ligação, cujo significado é fixado pelo `EO-0` (§3).
  Sem limiar; é leitura, não critério.

## 8. Taxonomia de falha — pré-registrada
| o que acontece | o que significa, decidido antes |
|---|---|
| ligação gira para eixo/espelho da malha no `EO-0` | **aprisionamento de malha**; `EO-1` sem veredito; é achado, não fracasso |
| `EO-0.1` falha (`Q` ou `l` fora) | estado não comparável; missão para; nada é relatado sobre deriva |
| `R ≈ 0` nos dois ângulos | **`H_ligação`**: o `L7.2` fecha e a direção do `C-7` passa a estar testada |
| `R ≈ −θ` nos dois ângulos | **`H_rede`**: a perpendicularidade do `C-7` é artefato de malha, e **`C-7` tem de ser reescrito**. É o desfecho que dói, e é por isso que a missão existe |
| `R` entre os dois, ou inclinação ambígua | deriva parcialmente presa à malha; relatar como intermediário, **sem escolher lado** |
| janelas discordam | direção **não convergida**; sem veredito; não estender (§6) |

## 9. Limites que já viajam junto
- **`L-G` intocado.** Meu código, meu equilíbrio, minha régua. Esta missão **remove um
  confundimento interno**; não acrescenta verificador independente. Passe o que passar,
  nada aqui é verificação independente.
- Um único ponto de parâmetros, um único modo (SBM), malha de 1 nm, caixa de 100 nm.
- **Não** testa o ABM fora do eixo, **não** testa magnitude assintótica (`L7.3` continua de
  pé), **não** toca `D-1`/`D-2`/`D-3`.
- Se `H_ligação` passar, o que fica testado é "a deriva acompanha a ligação em **dois**
  ângulos além de zero" — não "em qualquer ângulo".

## 10. Provenance (§4 do `CLAUDE.md`)
Código novo em **`LAB/EVIDENCE/E003/saf_prop3.cu`**, derivado do `saf_prop.cu` **selado** do
`E002` (que não é editado). Todos os caminhos de escrita redirecionados para `E003/` **antes
da primeira execução**, verificado por `grep -n 'EVIDENCE/' saf_prop3.cu` mostrando **apenas**
`E003`. Selagem por `SHA256SUMS.txt` cobrindo todos os arquivos ao final.

## 11. Gate
`G-E003 = EO-0.1 ∧ (EO-0 concluído) ∧ (EO-1 com veredito, qualquer que seja)`.
Note que **`EO-1` apontar para `H_rede` NÃO reprova o gate** — reprovaria o `C-7`. O gate
falha se o estado não for comparável, ou se a direção não convergir.
**Passar o gate não é aceite.**
