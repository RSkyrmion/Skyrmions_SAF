# WRITEBACK-020 — rotina de figuras; e `MISSION-E005` (Fig. S4(c)) autorizada

Data: 2026-08-26 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Adicionalmente eu quero que vc crie uma rotina para reproduzir nossas figuras, semelhantes
> as do artigo. Depois disso, aceito sua proposta e desejo executar as simulações necessárias"

## 1. Rotina de figuras — FEITA
`LAB/FIGURES/make_figures.py` + `README.md`. Seis figuras a partir de evidência **selada**.
Categoria nova `LAB/FIGURES/` registrada no `CLAUDE.md` §5.

**Decisão de desenho, e a razão dela:** toda figura carrega no rodapé a missão, o que mostra,
o limite, e o `L-G`. Uma figura **viaja sem o release dela** — é por figura que um trabalho é
recontado, e o §7 diz que o `L-G` é a primeira coisa que some. O rodapé não é decoração: é a
parte que impede a leitura errada. As figuras **não são seladas**: são produto regenerável;
quem manda é o `sha256sum` da evidência.

## 2. `MISSION-E005` autorizada — e por que ela existe
"Aceito sua proposta" = reproduzir a **`Fig. S4(c)`** do suplementar: `v_sp(f)` no acoplamento
fraco, `α = 0.02`, SBM, em três amplitudes.

**Registro do erro que a torna necessária.** Eu projetei o `E004` e o `E004R` para responder
"o pico de `v_sp` coincide com a ressonância do modo?" **sem ter lido o suplementar inteiro**.
A `Fig. S4(c)` responde exatamente isso, no nosso ponto de operação exato, e eu só a encontrei
depois — duas missões e ~8 h de GPU. **Não é defeito de critério** (a família dos nove do
§6.1): é **não ter lido a fonte inteira antes de desenhar**.

Proposta de processo decorrente, **não autorizada**: exigir no pré-registro uma linha
declarando que a fonte inteira — suplementar incluído — foi varrida à procura do alvo.

## O que NÃO fica autorizado
Aceite de nada. `E004` segue `REVISION_REQUESTED`. Ação externa, ação de sistema, freeze.

## Próximo head/estado
`STATE-2026-08-26-f`
