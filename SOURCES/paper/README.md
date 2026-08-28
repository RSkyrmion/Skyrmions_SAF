# Fonte primária do laboratório

## Identificação verificável

C. C. de Souza Silva, M. V. Correia e J. C. Piña Velásquez, *Emergent Self-Propulsion of
Skyrmionic Matter in Synthetic Antiferromagnets*, **Physical Review Letters 135**, 086701
(2025), DOI [`10.1103/c2y9-3cc9`](https://doi.org/10.1103/c2y9-3cc9).

Arquivos locais:

- `c2y9-3cc9.pdf` — artigo, 9 páginas; o próprio metadata PDF contém título e DOI.
- `SupplementalMaterial.pdf` — suplemento, 6 páginas; título no conteúdo da página 1.
- `SHA256SUMS.txt` — identidade criptográfica dos dois arquivos locais.

Verificação local: `cd SOURCES/paper && sha256sum -c SHA256SUMS.txt`.

## Localizadores claim-bearing usados no laboratório

| assunto | fonte e local | uso no laboratório |
|---|---|---|
| modelo micromagnético e parâmetros | artigo, **Apêndice A**, pp. 8–9 do PDF, Eqs. `(A1)`–`(A4)` | tradução dos campos e riscos de sinal/fator |
| definição de `l`, dinâmica e propulsão | artigo, pp. 2–4, Eqs. `(1)`–`(4)`, Figs. 1–3 | estimador, modos e critérios de autopropulsão |
| região de estabilidade | artigo, p. 8, **Fig. 5** | alvos estruturais de `R002`/`A006` |
| espectro de breathing | artigo, p. 9, **Fig. 6** | identidade/ordem dos modos e `C-6` |
| indisponibilidade dos dados originais | artigo, p. 5, seção **Data availability** | classificar o trabalho como re-implementação, não reexecução |
| linha `K₀ = 0.65 − 2.5 A_int` | suplemento, p. 3 do PDF, Eq. `(S1)` e **Fig. S2** | comparação estrutural do `R002` |
| dissipação e acoplamento | suplemento, p. 4 do PDF, **Fig. S3** | contexto de `D-1` e regimes de acoplamento |
| resposta em baixa dissipação | suplemento, p. 5 do PDF, **Fig. S4(a–e)** | alvo de `E004`/`E005`; painel (c) usado no amolecimento |
| trajetórias térmicas | suplemento, p. 6 do PDF, **Fig. S5** | lacuna ainda não medida |

## Três verificações que não devem ser confundidas

1. **Metadados:** título, autores, periódico, ano e DOI identificam a obra. O DOI existir não
   demonstra nenhuma afirmação física.
2. **Conteúdo:** equação, texto ou legenda deve ser conferido na página indicada. Como
   `pdftotext` reencoda símbolos do PDF da APS, decisões sobre fórmula exigem também a página
   renderizada.
3. **Extração de figura:** pontos digitalizados são uma medição nossa do gráfico, não dados
   dos autores. Calibração, máscara, incerteza e alvo pré-selado pertencem à evidência da
   missão que fez a extração (`E002`, `E004`, `E005`).

## Papel epistêmico

Estes PDFs são **fonte científica primária** do modelo e das afirmações publicadas. Eles não
são evidência de que nossa implementação está correta. A fonte metodológica compartilhada no
`WRITEBACK-026` orienta o FPM e, por sua vez, não é evidência do fenômeno físico.
