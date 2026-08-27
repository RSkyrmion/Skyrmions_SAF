# WRITEBACK-010 — MISSION-E002 autorizada (autopropulsão)

Data: 2026-08-25 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Executemos E002"

## O que fica autorizado
**`MISSION-E002`** — autopropulsão do par de skyrmions sob excitação monocromática, no
regime de acoplamento fraco, a `T = 0`. Pré-registro em `LAB/MISSIONS/MISSION-E002.md`,
escrito **antes** de qualquer linha de código novo e antes de qualquer corrida.

Autoriza também, por serem consequência direta e **ação local**: derivar um binário novo a
partir do `saf_dyn.cu` selado, compilá-lo, e rodá-lo. Compilar código próprio não é ação de
sistema nem ação externa.

## Escopo lido — e o convite a corrigir
"E002" foi nomeada em `STATE.md` como *"autopropulsão sob ABM"*. O artigo, porém, tem **três**
camadas de autopropulsão, com custos muito diferentes. Registro qual eu li como autorizada:

| camada | está em | no escopo? |
|---|---|---|
| Fig. 2 — deriva a `T = 0`, acoplamento fraco, SBM e ABM, um ponto de parâmetros | Fig. 2(a)–(d) | **SIM** |
| Fig. 3 — curvas de ressonância `v_sp(f)` para várias amplitudes e `α = 0.1` | Fig. 3(a)–(e) | **NÃO** |
| Fig. 4 — LLG estocástica, `T = 1–7 K`, trajetórias de `Δt = 3.116 µs` | Fig. 4(a)–(d) | **NÃO** |

**Por que recortei assim.** A Fig. 4 exige capacidade nova (ruído térmico na LLG) e ~8,7 h de
GPU **por trajetória**, pelo custo medido no `E001` (1 ns ≈ 10 s). A Fig. 3 é um varrimento de
frequência em outro ponto de amortecimento. A Fig. 2 é o mecanismo em si — é o menor degrau
que ou reproduz a autopropulsão ou não reproduz.

**Se você quis as três camadas, corrija.** Elas ficam nomeadas como missões posteriores
(`E003` = ressonância, `E004` = térmico), **não propostas e não autorizadas**.

## O que este writeback NÃO faz
- **Não é aceite.** Passar o gate `G-E002` não é aceite; aceitar é ato seu.
- **Não autoriza** a etapa 2 do `AUDIT-001` (enviar o `saf.cu` a terceiro) nem nenhuma outra
  ação externa (INV-16).
- **Não autoriza** compilar extensão de DMI Cnv/PBC para o OOMMF (ação de sistema).
- **Não é freeze.**
- **Não fecha `L-G`.** O `E002` roda no meu código, a partir do meu estado de equilíbrio, com
  a minha régua. Ele adiciona um observável novo, não um verificador independente.

## Próximo head/estado
`STATE-2026-08-25-e`

## Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar o `E002`, **depois** do release.
