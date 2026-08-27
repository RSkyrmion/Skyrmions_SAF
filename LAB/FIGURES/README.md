# LAB/FIGURES — figuras do laboratório

Geradas por `make_figures.py`, que lê **apenas evidência selada** em `LAB/EVIDENCE/` e escreve
**apenas aqui**. Rodar da raiz do projeto: `python3 LAB/FIGURES/make_figures.py`.

## A regra de desenho, e por que ela existe
**Toda figura carrega no rodapé: a missão que a produziu, o que ela mostra, o limite que viaja
com ela, e o `L-G`.**

Uma figura viaja **sem** o release dela. É por figura que um trabalho é recontado, e o
`CLAUDE.md` §7 diz que o `L-G` é a primeira coisa que some ao recontar. Uma figura que se
parece com a do artigo e não diz o que **não** foi testado é exatamente o veículo desse
apagamento. Por isso o rodapé não é decoração: é a parte da figura que impede a leitura errada.

Nenhuma destas figuras é reprodução do artigo. Todas saem de um único código, o nosso.

## O que cada uma é — e o que ela NÃO é

| | análogo no artigo | o que mostra | o que **não** é |
|---|---|---|---|
| `F1_deriva_do_par` | Fig. 2(a),(b) | deriva sob SBM e ABM, com a curva do artigo extraída por cima | **o transiente não reproduz**; só o platô. E a corrida SBM não estacionou (`L7.3`) |
| `F2_ciclos_de_nado` | Fig. 2(c),(d) | ciclos `ℓ`–`𝒟` no estacionário | **exploratório**: o `PV-1` declarou estes painéis **mortos antes do dado** |
| `F3_ressonancia_autopropulsao` | Fig. 3(c) / **S4(c)** | `v_sp(f)`, duas janelas | `EF-1` e `RF-1` ficaram **sem veredito**; o pico **não foi testado** contra a ressonância |
| `F4_espectro_breathing` | Fig. 6 | espectro do breathing SBM, 10 ns vs 40 ns | o `18.00 GHz` do `E001` era um **bin**; o valor é `17.9609 ± 0.0125` (`C-11`) |
| `F5_regiao_estabilidade` | Fig. 5(c) | 165 pontos do `R002`, com a Eq. (S1) | `L2.3` **aberta**: em `A_int = 0.12` o artigo prevê coaxial e nós não encontramos |
| `F6_deriva_segue_ligacao` | *sem análogo* | `φ_deriva` vs `θ_ligação`, inclinação `+1.02` | testado em **dois** ângulos além de zero, só no SBM |

## O que ainda não tem figura porque não foi medido
Fig. 3 a `α = 0.1` · Fig. **S4** completa (o alvo publicado do `E004`, ver `E005`) ·
Fig. S2 / 5(b),(d) — potencial `E(R)` · Fig. S3 — tensor de dissipação fora do acoplamento
fraco · Fig. 5(a) — plano `(A_int, B)` · Fig. 4 e S5 — térmico.
Tudo o que fizemos, exceto o mapa do `R002`, foi em `A_int = 0.02`.

## Regeneração
As figuras **não são seladas**: são produto regenerável da evidência, que essa sim é selada.
Se um número mudar aqui sem que a evidência tenha mudado, o defeito é do script — o
`sha256sum -c` de `EVIDENCE/` é a autoridade.
