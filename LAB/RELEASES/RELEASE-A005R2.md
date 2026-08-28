# RELEASE-A005R2 — a saída convergiu; a escada, pela letra, **NÃO**

Missão: `MISSION-A005R2` · Autorizada por `WRITEBACK-033` · Execução: 2026-08-28, 09:26–09:40
`human_acceptance: PENDING` · Evidência: `LAB/EVIDENCE/A005R2/` · Parede: **~8 min** de 3 h

## 1. Veredito
**Classificação da escada: `NONCONVERGENT`, pela letra do §4.**
**Gate `G-A005R2` NÃO passou. `AC2-1`, `AC2-2` e `AC2-3` NÃO foram executados.**
**`A007` permanece BLOQUEADA** — o §8 só a desbloqueia por caminho `FULL`.

E, ao mesmo tempo: **`l` convergiu e travou em `10.9551 nm`**, com variação de `0.0000 %`
entre os dois últimos checkpoints. As duas coisas são verdadeiras e não se cancelam.

## 2. `V-0` — PASSOU
| item do §3 | resultado |
|---|---|
| unidade na fonte | `TOOLS/mumax3/engine/torque.go:24` → `maxTorque`, unidade **`T`**; `saf_prop4r.cu:1062` → `tol` em **`[T]`**. Mesma grandeza |
| estado de partida copiado, nunca sobrescrito | `A003/mfinal_par_mumax3.dat` → `input_A003_mfinal_par.dat`, hash `7fa7b1ea…` **idêntico ao manifesto selado do `A003`** |
| torque inicial, antes de qualquer relaxação | **`4.8334e−5 T`** — igual ao valor final do `A003`, confirmando round-trip exato |
| hash do input | `INPUT-HASH.txt` |

## 3. Estágio `F` — a escada
Quatro processos separados, timeout de 900 s cada, cada degrau partindo do checkpoint anterior.

| degrau | alvo | torque de entrada | torque de saída | parede |
|---|---|---|---|---|
| `F1` | `2e−5` | `4.8334e−5` | **`2.2918e−5`** | 3.88 s |
| `F2` | `1e−5` | `2.2631e−5` | **`1.7119e−5`** | 1.56 s |
| `F3` | `3e−6` | `1.9252e−5` | `1.9252e−5` | 0.06 s |
| `F4` | `1e−6` | `1.7119e−5` | `1.7119e−5` | 53.3 s |
| repetição de `F4` | — | `1.7119e−5` | `1.7119e−5` | 390.7 s |

**Nenhum alvo foi atingido.** O melhor torque é `1.7119e−5 T`, ~17× acima do `1e−6` do `saf.cu`.

### O achado instrumental: o checkpoint tem mais ruído que a melhoria
Compare o **torque de saída** de um degrau com o **torque de entrada** do seguinte, que carrega
o mesmo arquivo: `F2` salvou `1.7119e−5`; `F3` releu `1.9252e−5`. `F3` salvou `1.9252e−5`;
`F4` releu `1.7119e−5`.

**O ida-e-volta pelo OVF em float32 desloca `MaxTorque` em ~12 %** — mais que a melhoria que os
degraus 3 e 4 tentavam obter. O mecanismo de checkpoint está no piso de precisão da ferramenta.

### Reprodutibilidade: perfeita
A repetição do último degrau completo devolveu `1.711853057346851e-05` — **os mesmos 16
dígitos**. Fator `1.000`, contra o limite de `1.2` do §4.

## 4. A classificação, aplicada pela letra
| classe (§4) | condição | verificação |
|---|---|---|
| **FULL** | um checkpoint com `MaxTorque ≤ 1.0e−6 T` | **não** — melhor `1.71e−5` |
| **PARTIAL** | ≥2 checkpoints melhoram monotonicamente **e o próximo degrau expira**; repetição dentro de fator 1.2 | melhora ✔ (`4.83→2.29→1.71`), repetição ✔ (`1.000`), **mas `F3` NÃO expirou — completou sem progresso** ✘ |
| **NONCONVERGENT** | <2 degraus completos, **ou torque não melhora monotonicamente**, ou repetição fora de 1.2 | **torque não é monótono**: `2.29 → 1.71 → 1.93 → 1.71` ✔ |

**`NONCONVERGENT`.** O §4 é explícito: *"Em `NONCONVERGENT`, a missão termina. Não há `AC-1`,
`AC-2` ou `AC-3`."*

### Registro de desenho — e ele não é meu
A taxonomia do §4 não previu **"degrau completa sem progredir"**: ela só contempla "expira".
E trata não-monotonicidade como fracasso mesmo quando a não-monotonicidade é **inteiramente o
ruído de float32 do próprio mecanismo de checkpoint**, não comportamento do minimizador.

Registro isto como lacuna de desenho do pré-registro, **sem reparar**. O `CLAUDE.md` §6.2 é
explícito: o executor não pode redefinir teste e meta depois de ver a saída. O pré-registro foi
escrito por outro agente; eu o executei. **A separação executor–projetista funcionou aqui: eu
não podia acomodar a regra, e não acomodei.**

## 5. O que a escada mediu, e o que isso NÃO é
O §4 manda cada degrau medir `l`. Pelo **estimador cego do `AUDIT-002`**:

| checkpoint | `MaxTorque` | `l` [nm] | vs `saf.cu` `10.9607` |
|---|---|---|---|
| input (`A003`) | `4.8334e−5` | `10.9279` | `−0.299 %` |
| `ck1` | `2.2918e−5` | `10.9526` | `−0.074 %` |
| `ck2` | `1.7119e−5` | **`10.9551`** | **`−0.051 %`** |
| `ck3` | `1.9252e−5` | `10.9551` | `−0.051 %` |
| `ck4` | `1.7119e−5` | `10.9551` | `−0.051 %` |

Estabilidade da saída (§6): **`0.0000 %`** entre os dois últimos, contra o limite de `0.05 %`.
**A saída converge mesmo com a entrada em platô** — e isso é o oposto do erro que o `RF-0` do
`E004R` cometeu, que checou a entrada.

**Estes números são medida de degrau da escada, NÃO veredito do `AC2-3`**, que não foi
executado. Portanto:
- **NÃO revisam o `C-15`.** O `−0,30 %` permanece canônico com a ressalva de torque frouxo.
- **NÃO fecham a ressalva** do `RELEASE-A005` §5.
- O §7 do pré-registro é explícito: em ausência de `FULL`, "não promover extrapolação, não
  substituir `−0,30 %` e não declarar a ressalva do `C-15` resolvida".

## 6. Relação com a execução não autorizada de 2026-08-27
O `WRITEBACK-033` registra que executei, sem autorização e sem saber, o equivalente a esta
missão. Aquela execução mediu piso `1.4903e−5 T` e `l = 10.9552 nm`.

Esta execução, autorizada e limpa, mede piso `1.7119e−5 T` e `l = 10.9551 nm`.

**`l` coincide em quatro casas; o piso difere `~15 %`** (caminho diferente até ele). Isto é
**coincidência confirmatória**, e **não valida retroativamente** a execução irregular. O
material daquela continua rotulado como artefato no `WB-033`.

## 7. Limites
- `L-G` **intocado**. Leitura do modelo e inicialização seguem compartilhadas.
- mumax3 é float32; `saf.cu` é double — e este release mostra que essa diferença **não é
  cosmética**: ela põe o piso de torque 17× acima e injeta 12 % de ruído no checkpoint.
- Um ponto de parâmetros, uma malha, `T = 0`, estática. Nenhuma dinâmica foi executada.
- `A007` segue bloqueada. `AC2-1` e `AC2-2` não têm dado: `L9.1` e `L8.4` seguem abertos.
- Proveniência em `AI-PROVENANCE.json`, validada por `scripts/check_ai_provenance.py`.

## 8. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar. E, se quiser o caminho `FULL`, ele
**não existe com este mecanismo**: o piso é da ferramenta, não da escada. Alternativa seria
comparar em torque casado *no outro sentido* — parar o `saf.cu` em `~1.7e−5 T` —, o que o §5
do pré-registro prevê para `PARTIAL` e que esta classificação **não autoriza**.
