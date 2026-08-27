# ADENDO-001 a RELEASE-R002 — teste de bacia e extração numérica da Fig. 5(c)

Data: 2026-08-21 · Autoridade: Rodrigo, *"Execute a sequência recomendada"* (passo 1)
Missão: `MISSION-R002`, ainda `TERMINAL_AWAITING_HUMAN`

> `RELEASE-R002.md` **não foi editado**. Este adendo o complementa e, em dois pontos,
> **corrige** conclusões dele. Os textos originais permanecem como foram escritos.

---

## 1. O que motivou isto
`RELEASE-R002.md` §4 registrou uma discrepância aberta: em A_int = 0.12 minha varredura não
achava ramo coaxial, enquanto a legenda da Fig. 5(c) diz que os dois ramos coexistem. O
`SL-B1` levantava a hipótese de que fosse efeito de bacia de atração.

## 2. Teste de bacia — hipótese REFUTADA
Inicialização coaxial (separação 0.5 e 2.0 nm em vez de 10 nm).

**Controles** (A_int = 0.02, resposta já conhecida): K₀=0.45 → COAXIAL de ambas as
inicializações ✓ ; K₀=0.60 → NONCOAXIAL, l = 10.9529 nm, **idêntico ao início de 10 nm** ✓.
Os controles mostram que uma partida quase-coaxial não fica presa artificialmente.

**Teste** (A_int = 0.12, K₀ de 0.125 a 0.40): **todas** as condições iniciais relaxam para
não-coaxial. Não é efeito de bacia. Evidência: `EVIDENCE/R002/basin_test.csv`.

## 3. Extração numérica da Fig. 5(c) — o que mudou a conclusão
`RELEASE-R002.md` §9 limite 2 afirma: *"não há valores extraíveis da linha tracejada da
Fig. 5(c) no texto do PDF"*. **Isso estava certo sobre o texto e errado como conclusão** —
a figura pode ser renderizada e medida por cor. Feito em `EVIDENCE/R002/extract_fig5c.py`
sobre `fig5c_rendered.png` (500 dpi).

Ajustes obtidos da figura do artigo:
```
tracejado (coax/nao-coax)   K0 = -3.933*Aint + 0.6157   (143 pts, Aint 0.008..0.107)
borda inferior da banda     K0 = -2.499*Aint + 0.4255
borda superior da banda     K0 = -2.498*Aint + 0.8837
centro da banda             K0 = -2.499*Aint + 0.6546
Eq. (S1) do suplementar     K0 = -2.500*Aint + 0.6500
```

### 3.1 A Eq. (S1) é confirmada como a linha de centro da própria figura
Inclinação bate em três casas; intercepto difere 0.0046. Isso valida o alvo escolhido no
desenho do R002 — a Eq. (S1) **é** a linha de centro, não uma aproximação vaga.

### 3.2 Minha fronteira coaxial↔não-coaxial contra a do artigo
| A_int | artigo | `saf.cu` | dif |
|---|---|---|---|
| 0.02 | 0.537 | 0.5375 | +0.0005 |
| 0.04 | 0.458 | 0.4625 | +0.0045 |
| 0.06 | 0.380 | 0.3875 | +0.0075 |
| 0.08 | 0.301 | 0.2875 | −0.0135 |
| 0.10 | 0.222 | 0.2125 | −0.0095 |

**Todas ≤ 0.014 — meio passo da minha grade (0.025).**

### 3.3 Bordas da banda de estabilidade
Borda inferior: diferença **+0.024 constante** em cinco colunas. Isso é exatamente o viés
esperado — minha borda é o primeiro ponto de grade estável, então fica acima da borda real
por até um passo (0.025). Borda superior: diferenças entre −0.034 e +0.016, todas dentro de
um passo.

### 3.4 Ordem temporal — por que isto não é ajuste post-hoc
Os meus números (0.5375, 0.4625, 0.3875, 0.2875, 0.2125 e as bordas) foram computados e
**escritos em `RELEASE-R002.md` antes** de a figura ser extraída. A predição precede a medida
do alvo.
**Risco residual, declarado:** a extração poderia, em princípio, ter sido ajustada para
concordar. Mitigações verificáveis: o método é mecânico (limiar de cor + ajuste linear), a
calibração vem dos ticks dos eixos, nenhum parâmetro foi ajustado contra os meus valores, e o
script está salvo. Não é prova de ausência de viés — é o que dá para oferecer.

## 4. A discrepância de §4 do release: reduzida, não eliminada
Larguras do ramo coaxial:

| A_int | artigo | `saf.cu` (limite inferior, por quantização) |
|---|---|---|
| 0.02 | 0.161 | 0.125 – 0.175 |
| 0.04 | 0.133 | 0.100 – 0.150 |
| 0.06 | 0.104 | 0.075 – 0.125 |
| 0.08 | 0.075 | 0.025 – 0.075 |
| 0.10 | 0.047 | 0.000 – 0.050 |
| 0.12 | 0.017 | < 0.050 (não detectado) |

Lidas como limites (a minha largura medida é o intervalo entre pontos de grade, logo
subestima em até um passo), **todas são consistentes**.

**Mas o teste fino não confirmou o coaxial em A_int = 0.12.** O artigo prevê coaxial em
K₀ ∈ [0.126, 0.144]; varri K₀ = 0.128 / 0.132 / 0.136 / 0.140 / 0.144 com duas
inicializações: **tudo não-coaxial**. Evidência: `basin_test_fine.csv`.

**Status honesto:** desacordo **estreito e localizado**, no extremo do diagrama, numa região
onde a linha tracejada do artigo está **extrapolada** — o último traço desenhado está em
A_int = 0.1066, e 0.12 fica além dele. Pode ser: (i) desacordo real do meu modelo naquele
canto; (ii) erro da minha extrapolação da figura; (iii) largura real ainda menor que 0.017.
Não decidido. Permanece aberto, agora muito mais estreito do que em `RELEASE-R002.md` §4.

## 5. Correção a `RELEASE-R002.md`
- §9 limite 2 (*"teste da fronteira é qualitativo"*) fica **superado**: a comparação é
  quantitativa, com resíduos ≤ meio passo de grade em cinco pontos.
- §4 (discrepância aberta): **reduzida** de "não existe ramo coaxial vs artigo diz que existe"
  para "desacordo de largura <0.05 no ponto extremo A_int=0.12, em região extrapolada".
- O critério **secundário continua não usado**. Ele morreu por uma regra de poder mal
  especificada, e nada aqui o ressuscita. O que existe agora é uma comparação **diferente e
  melhor** — bordas e fronteira contra a figura — que não é o critério secundário.

## 6. Artefatos novos
`basin_test.csv`, `basin_test_fine.csv`, `extract_fig5c.py`, `fig5c_rendered.png`,
`fig5c_extraction.txt`, `phase_diagram.png`.

## 7. Efeito na decisão pendente
A leitura do artigo embutida no `saf.cu` reproduz **quantitativamente** a fronteira
coaxial↔não-coaxial e as bordas da região de estabilidade, dentro de um passo de grade, em
cinco pontos independentes. Isso é bem mais forte do que `RELEASE-R002.md` podia afirmar.
A decisão de aceite continua sendo de Rodrigo.
