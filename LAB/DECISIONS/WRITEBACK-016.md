# WRITEBACK-016 — `MISSION-I002` autorizada (o `L8.4`)

Data: 2026-08-26 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Podemos executar o teste sugerido?"

referindo-se ao teste que eu propus na mensagem anterior: variar `K₀` para obter estados de
equilíbrio com `l` diferente, e ver se a deriva espúria `v_∥` acompanha `l`.

## O que fica autorizado
`MISSION-I002`, pré-registro em `LAB/MISSIONS/MISSION-I002.md`. Prefixo `I` = instrumento /
artefato do meu próprio código, como o `I001`. Inclui derivar binário, compilar e rodar.

## Correção que originou esta missão
Eu havia dito que o `L8.4` "não sei fazer barato" e **estava errado**. Ao decompor a deriva no
referencial da ligação para explicar o que `L8.4` significa, apareceu que os 10 % não são ruído:
`v_∥` vale `0.917 cm/s` sem excitação e `0.817` com, enquanto `l` vai de `10.95` para
`10.42 nm`. Eu havia comparado a corrida excitada contra um controle medido **em outro estado**.

## O que NÃO fica autorizado
Aceite de nada; `E004R` segue `PENDING`, `E004` segue `REVISION_REQUESTED`. Missão nova além
desta. Ação externa (INV-16), ação de sistema, freeze.

## Próximo head/estado
`STATE-2026-08-26-b`
