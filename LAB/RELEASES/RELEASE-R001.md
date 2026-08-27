# RELEASE-R001 — as-run da reprodução do par não-coaxial em T=0

Data: 2026-08-21 · Missão: `MISSION-R001` (`AUTHORIZED` por `WRITEBACK-002`)
Estado desta release: **`TERMINAL_AWAITING_HUMAN`**

> Isto é um registro as-run. O gate `G-R001` passou. **Passar o gate não é aceite.**
> `human_acceptance: PENDING`. Nada aqui está congelado nem autoriza R002.

## Resultado

| grandeza | valor |
|---|---|
| **l reproduzido (malha 1 nm — a mesma do artigo)** | **10.9607 nm** |
| l publicado (Fig. 2(a), equilíbrio, excitação desligada) | 10.98 nm |
| **diferença** | **−0.019 nm = −0.18 %** |
| banda de aceite pré-registrada | [10.43, 11.53] nm → **dentro** |
| Q₁ , Q₂ | −1.0000 , +1.0000 |
| ramo | **não-coaxial** (l parte de 10 nm e cresce; não colapsa) |
| torque final | 9.996e-07 T (convergido) |
| energia total | −4.785440e-18 J |

**Comparador:** o valor governante é o de malha de **1 nm**, porque é a malha que o
Apêndice A do artigo declara (`cells of size 1 × 1 nm²`). VL-5 (0.5 nm) é robustez, **não**
uma correção: trocar o comparador para a malha fina mudaria silenciosamente o que está sendo
comparado com o quê.

## Escada de verificação — as-run (binário final, log `EVIDENCE/R001/vl123_final_binary.log`)

| gate | resultado |
|---|---|
| VL-1 FD campo-vs-energia, termo a termo | **PASSA** — pior erro relativo 5e-8 (troca, anisotropia, DMI, interlayer, Zeeman, tudo junto) |
| VL-2 estado uniforme | **PASSA** — `H_int = ±Aint·Área` com erro relativo 1e-16; `\|Beff_int\| = 0.086207 T = Aint/(Ms·d)` exato |
| VL-3 skyrmion único | **PASSA** — `Q = −1.0000`, mz mínimo −0.9929, convergido |
| VL-4 par acoplado | **PASSA** — ver tabela acima |
| VL-5 malha 0.5 nm | **PASSA** — `l = 10.8500 nm`, mesmo ramo, `Q₁=−1, Q₂=+1`, E = −4.785820e-18 J |

**SL-2 (fator 1/d) fica confirmado por dois caminhos independentes:** FD em VL-1 e o valor
fechado `Aint/(Ms·d) = 0.086207 T` em VL-2.

## Sensibilidade à malha (VL-5)
1.0 nm → 10.9607 nm · 0.5 nm → 10.8500 nm · Δ = −0.11 nm (**−1.0 %**).
A malha é uma fonte de erro sistemático **maior que a discrepância com o artigo (0.18 %)**.
Isso deve constar em qualquer claim: o acordo de 0.18 % não é mais preciso que o método.
Como o artigo usa 1 nm, ambos carregam o mesmo viés de malha — que é o que uma reprodução
fiel deve mostrar.

## Nota de convergência (honesta)
A primeira execução de VL-4 parou em `l = 10.9529 nm` com tolerância de torque 1e-5 T, com
`l` ainda subindo. Os incrementos decaíam geometricamente (razão 0.983); a extrapolação dava
10.962 nm. Reexecutado com tolerância 1e-6 T: **10.9607 nm**, confirmando a extrapolação. O
valor governante é o de 1e-6 T. A execução de 1e-5 T fica no histórico
(`EVIDENCE/R001/vl4_weak.log`), não apagada.

## Desvio de protocolo registrado durante a execução
`SL-7` — o estimador de carga topológica foi trocado de diferenças finitas para Berg-Lüscher
**durante** VL-3, porque o primeiro dava `|Q| = 0.984` num estado relaxado saudável.
Justificativa e a razão de isto não ser INV-05 estão em `MISSIONS/MISSION-R001.md`, §SL-7.
Resumo: o critério que forçou a troca é a integralidade de Q, conhecida a priori e
independente do alvo de 10.98 nm; a energia relaxada é idêntica antes e depois.

## Força da evidência: `BOUNDED`
A claim proporcional é: **"uma re-implementação independente é consistente com o
comprimento de ligação de equilíbrio publicado, dentro de 0.2 %, num único ponto de
parâmetros"** — e **não** "o artigo foi reproduzido".

O que limita a força:
1. **Um único escalar**, num **único ponto de parâmetros** (acoplamento fraco, T=0, B=0).
2. O alvo foi lido de uma **legenda de figura**, com 4 algarismos significativos e sem barra
   de erro publicada.
3. **Sem acesso aos dados originais** (não públicos) → re-implementação, não re-execução.
   Nenhum solver de referência de terceiros validou este código.
4. **Sensibilidade à malha (1.0 %) excede a discrepância (0.18 %)** — ver acima.
5. O estimador de Q foi **trocado durante a execução** (SL-7).
6. Auto-interação por PBC numa caixa de 100 nm com l ≈ 11 nm não foi quantificada.
7. Nada foi testado sobre dinâmica, temperatura finita, modos de breathing ou autopropulsão.

## Artefatos materiais (`LAB/EVIDENCE/R001/`)
| arquivo | papel |
|---|---|
| `saf.cu` | fonte CUDA (energia discreta + campos por derivada dela) |
| `SHA256SUMS.txt` | identidade de bytes do fonte e do binário |
| `vl123_final_binary.log` | VL-1/2/3 as-run, **binário final** |
| `vl4_weak.log`, `l_of_t_weak.dat` | VL-4 primeira execução (tol 1e-5), histórico |
| `vl4_tight.log`, `l_of_t_weak_tight.dat` | **VL-4 governante** (tol 1e-6) |
| `vl5_mesh05.log`, `l_of_t_mesh05.dat` | VL-5 malha 0.5 nm |
| `mfinal_*.dat` | magnetização final das duas camadas |

Reprodução: `nvcc -O2 -arch=sm_89 -o saf saf.cu` e `./saf pair 1e-6 1.0 weak_tight`
(executar a partir de `/home/rodrigo/pesquisa/SAF`).

## Próxima decisão humana
Rodrigo aceita, aceita-com-limitações, pede revisão ou rejeita `MISSION-R001`.
**R002 não está autorizada** e não deve começar antes disso.
