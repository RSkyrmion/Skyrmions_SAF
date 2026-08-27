# RELEASE-E001 — as-run da Fase 2: dinâmica LLG e modos de breathing

Data: 2026-08-24 · Missão: `MISSION-E001` (`AUTHORIZED` por `WRITEBACK-008`)
Estado: **`TERMINAL_AWAITING_HUMAN`** · `human_acceptance: PENDING`
**Gate `G-E001` PASSOU.** Passar o gate não é aceite.

---

## 1. Placar contra os critérios pré-registrados

| | resultado |
|---|---|
| **EV-1** conservação (α=0) | **PASSOU** — deriva `1.06e−09` (crit. `<1e−4`), `max\|\|m\|−1\| = 3.36e−11` (crit. `<1e−10`) |
| **EV-2** Larmor | **PASSOU** — `2.802494 GHz` vs alvo `2.802494 GHz`, desvio **+0.00000 %** |
| **EV-3 primário** escala do modo | **PASSOU** — SBM `18.00 GHz` na banda `[14.4, 21.6]` |
| **EV-3 secundário** ordenamento | **PASSOU** — `f_ABM = 19.40 > f_SBM = 18.00 GHz` |
| **EV-3 terciário** `l(t)` a ω vs 2ω | **NÃO MEDIDO** (era declarado exploratório) |

## 2. EV-1 — a precessão é uma rotação de verdade
`α = 0`, 1 ns, `dt = 10 fs`, RK4, **sem renormalização**. Deriva relativa de energia
`1.062e−09`, cinco ordens de margem. `max\|\|m\|−1\| = 3.355e−11` **sem renormalizar** — ou
seja, `dm/dt ⊥ m` emerge do kernel, não de uma correção forçada. Um sinal, fator ou estêncil
errado no termo de precessão não conserva energia; este teste não passa por acidente.

## 3. EV-2 — `γ` e o sinal, calibrados contra alvo analítico
`B = 0.1 T`, sem troca/DMI/anisotropia/acoplamento. Fase perfeitamente linear (resíduo máximo
do ajuste `9.06e−14 rad`), exatamente `2.000` voltas, `m_z` constante.
`f = 2.802494 GHz` contra `γB/2π = 2.802494 GHz`. **Desvio +0.00000 %.**

Observação registrada: o sentido sai **anti-horário** (ω>0), que é o que a Eq. (A1) como
escrita produz para `γ>0` e `B` em `+z`. Implementei a equação do artigo, não uma convenção
de livro-texto. Irrelevante para um espectro de potência, mas registrado.

## 4. EV-3 — o espectro, e como a identidade do modo foi estabelecida

Protocolo do Apêndice B: `α = 0.02`, sinc com `f_c = 100 GHz`, `B₀ = 4 mT` (ABM),
`ΔK = 0.004 K₀` (SBM), `δm_z` a cada 2 ps, **janela de 10 ns** (resolução 0.1 GHz).
A regra registrada mandava medir o custo antes de escolher a janela: 1 ns ≈ 10 s, logo os
10 ns do artigo eram viáveis e foram usados.

### 4.1 O mapeamento de canal foi MEDIDO, não suposto
As duas camadas têm fundos opostos (`⟨m_z⟩_eq = +0.9698` e `−0.9698`). Se ambos os skyrmions
expandem (SBM), `⟨m_z⟩` da camada 1 cai e o da camada 2 sobe — os sinais **anticorrelacionam**.
Logo o SBM vive em `δm_z0 − δm_z1` e o ABM em `δm_z0 + δm_z1`. Confirmado nos dados:

| excitação | `corr(δm_z0, δm_z1)` | leitura |
|---|---|---|
| `ΔK` | **−1.0000** | respiram **em fase** → SBM |
| `B_z` | **+0.9999** | **antifase** → ABM |

Isto é exatamente o que o texto principal afirma (anisotropia é invariante por reflexão
especular → SBM; `B_z` quebra inversão → ABM), obtido por medida e não por rótulo.

### 4.2 Frequências

| modo | medido | publicado | dif |
|---|---|---|---|
| SBM (canal `δm_z0−δm_z1`, excitação `ΔK`) | **18.00 GHz** | 18 GHz | — |
| ABM (canal `δm_z0+δm_z1`, excitação `B_z`) | **19.40 GHz** | 19.24 GHz | **+0.83 %** |

## 5. O que este acordo NÃO autoriza dizer
- **A banda de ±20 % foi declarada, antes dos dados, como teste de ESCALA e não de
  identidade.** Ela não separa 18 de 19.24 (distam 7 %). A identidade dos modos repousa no
  critério secundário e no §4.1, não nela.
- **`18.00` batendo em `18` é mais bonito do que é forte.** O artigo cita "18 GHz" como número
  redondo no texto corrido; a minha resolução é 0.1 GHz. O acordo real e defensável é
  "ambos os modos caem em ~18–19.5 GHz, na ordem certa", não "coincidência em quatro dígitos".
- O ABM em `+0.83 %` é o número mais informativo do par, porque `19.24` é citado com três
  algarismos.

## 6. Defeitos de execução registrados
1. **Colisão de argumentos.** O `main` herdado lê `argv[3]` como `a_nm`; o meu `ev3 <modo>
   <ns>` fez `10` (nanosegundos) virar **célula de 10 nm**, reduzindo a grade a 10×10. O par
   colapsou e a primeira corrida saiu com `⟨m_z⟩_eq = ±1.000000000` — obviamente errado, e
   por isso pego de imediato. Corrigido restaurando a grade explicitamente no despacho.
   Os arquivos da corrida ruim foram apagados, não reaproveitados.
2. **Defeito de provenance no R001 — mais sério, e meu.** Rodar `saf_dyn pair` como
   diagnóstico **reescreveu** `EVIDENCE/R001/mfinal_weak.dat` e `l_of_t_weak.dat`. O
   `SHA256SUMS.txt` do R001 cobria **apenas** `saf.cu` e `saf`: os arquivos de dados nunca
   foram hasheados, então `sha256sum -c` passava sem verificar nada.
   **Verificação do dano:** o `estimator.py` do `AUDIT-002` rodou sobre o arquivo **antes** da
   reescrita e sua saída está gravada em `EVIDENCE/AUDIT-002/RUN-001.txt`. Rodando depois,
   `R1`, `R2` e `l` batem em **todos os 17 dígitos**. O conteúdo é reproduzível e o dano é
   nulo — mas isso foi sorte de determinismo, não desenho.
   **Corrigido:** os 12 arquivos de `EVIDENCE/R001/` estão agora hasheados.

## 7. Força da evidência: `BOUNDED`
Claim proporcional: **"a dinâmica LLG implementada reproduz a Larmor analítica exatamente,
conserva energia, e produz dois modos de breathing na faixa e na ordem que o artigo reporta,
com a simetria de cada modo confirmada por medida"** — e não "os modos de breathing foram
reproduzidos".

Limites:
1. `L-G` intocado: continua sem verificação independente do resultado por outro solver.
2. O fator `1/(1+α²)` **não é testado** por esta escada (com `α=0` vale 1). Registrado em
   `MISSION-E001` §3.1 como dívida que importa em `E002`.
3. Malha 1 nm, caixa 100 nm, um único ponto de parâmetros.
4. Terciário não medido — `l(t)` não foi registrado durante a dinâmica.
5. O estado inicial é o equilíbrio do meu código (régua verificada pelo `AUDIT-002`, estado
   ainda meu).

## 8. Artefatos (`LAB/EVIDENCE/E001/`)
`saf_dyn.cu`, `saf_dyn`, `ev2_precessao.dat`, `ev3_sbm_10ns.dat`, `ev3_abm_10ns.dat`,
`spectra.py`, `EV3-RESULTS.txt`, `SHA256SUMS.txt` — `sha256sum -c` passa nos 7.
Reprodução: `nvcc -O2 -arch=sm_89 -o saf_dyn saf_dyn.cu`, depois `./saf_dyn ev1`,
`./saf_dyn ev2`, `./saf_dyn ev3 sbm 10`, `./saf_dyn ev3 abm 10`.

## 9. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar **E001** e **AUDIT-002**.
`E002` (autopropulsão) continua **não proposta** e não autorizada.
