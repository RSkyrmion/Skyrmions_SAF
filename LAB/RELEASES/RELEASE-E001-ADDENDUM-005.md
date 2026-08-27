# ADENDO-005 a RELEASE-E001 — os três comprimentos característicos e o que eles dizem sobre `L1.1`

Data: 2026-08-24 · Motivado por Rodrigo: *"Além do comprimento de troca devemos sempre
observar o comprimento característico da interação DM e o comprimento da parede de domínio"*

> Corrige uma conclusão do `ADENDO-004`: lá eu declarei folga de ~8× na discretização usando
> **só** o comprimento de troca magnetostático. Ele é o **mais folgado dos três**. A folga
> real é de 5×.

## 1. Os três comprimentos

| comprimento | fórmula | valor |
|---|---|---|
| troca magnetostático | `√(2A/μ₀M_s²)` | 8.424 nm |
| característico da DMI | `4A/(πD)` | **6.262 nm** |
| parâmetro de parede de domínio | `√(A/K)` | **5.000 nm** |
| parede completa | `π√(A/K)` | 15.708 nm |

**Conferência interna que fecha o esquema:** por construção, em `D = D_c` deve valer
`l_D = Δ`. Com `D_c = 4√(AK)/π = 3.8197 mJ/m²`, dá `l_D(D_c) = 5.000 nm = Δ` **exato**.
Isso confirma a convenção de `D_c` que o laboratório usa desde o R001: `κ = D/D_c = 0.7985`,
contra o `0.80` registrado no `STATE.md`.

## 2. Quem manda na malha
O critério é o **menor** dos comprimentos, que é `Δ = 5.000 nm` — não `λ_ms`.

| malha | `a/λ_ms` | `a/l_D` | `a/Δ` | células por `Δ` | células por parede |
|---|---|---|---|---|---|
| 1.00 nm | 0.119 | 0.160 | **0.200** | **5.0** | 15.7 |
| 0.50 nm | 0.059 | 0.080 | 0.100 | 10.0 | 31.4 |
| 0.25 nm | 0.030 | 0.040 | 0.050 | 20.0 | 62.8 |

Todos os três critérios são **satisfeitos** na malha de 1 nm, mas a margem é **5×**, não 8×.
Cinco células por `Δ` é aceitável e não é confortável.

## 3. Isto dá diagnóstico físico ao limite `L1.1`
`L1.1` (o limite que domina o claim `C-1`) registra que a sensibilidade à malha é de 1.0 %,
maior que a discrepância de 0.18 %. Até agora era um fato empírico sem explicação. Agora tem:
**a célula de 1 nm resolve `Δ` apenas 5×**, e é exatamente aí que um deslocamento de ~1 % em
`l` é esperado.

```
l(1.0 nm) = 10.9607 nm   (5 células por Δ)
l(0.5 nm) = 10.8500 nm   (10 células por Δ)
diferença = −1.01 %
```

## 4. **EXPLORATÓRIO — extrapolação, rotulada como tal e NÃO usada como resultado**
Com dois pontos é possível extrapolar, e o resultado é desconfortável:

| hipótese de ordem | `l(a→0)` | vs 10.98 publicado |
|---|---|---|
| segunda ordem em `a` | 10.8131 nm | **−1.52 %** |
| primeira ordem em `a` | 10.7393 nm | −2.19 % |

**Ambas se afastam do valor publicado, não se aproximam.**

Por que isto **não** é reportado como resultado, e não altera `C-1`:
1. **Não há critério pré-registrado.** É análise post-hoc de dados existentes. O `RELEASE-R002`
   §2 registrou o custo de confundir análise post-hoc com teste; não vou repetir.
2. **Dois pontos não estabelecem a ordem de convergência.** Escolher entre 1ª e 2ª ordem é
   suposição, e as duas dão respostas diferentes.
3. **E o mais importante — a comparação do R001 é casada em malha.** O artigo declara, no End
   Matter, células de `1 × 1 nm²`. Logo `10.98` publicado **também** é um número de malha de
   1 nm, não o limite do contínuo. Comparar meu 1 nm com o 1 nm deles é a comparação certa
   para reprodução; o limite do contínuo é **outra pergunta**.

O que isto de fato acrescenta a `L1.1`: nenhum dos dois números é o valor do contínuo, e há
indício de que o `l` físico esteja abaixo de ambos. Isso **não** enfraquece `C-1` como foi
escrito — `C-1` é explicitamente sobre um único ponto de parâmetros na malha do próprio
artigo — mas fecha a porta a qualquer leitura de `C-1` como afirmação sobre o contínuo.

## 5. Recomendação registrada (não é missão, não está autorizada)
Se você quiser decidir a questão do contínuo, o desenho seria uma missão de convergência com
**três** malhas (1.0, 0.5, 0.25 nm), critério de ordem pré-registrado antes de rodar, e
`l(a→0)` por ajuste e não por extrapolação de dois pontos. Custo: a malha de 0.25 nm é
400×400 = 160 000 células, 16× o trabalho do R001.

Sem isso, o correto é o que já está no registro: `C-1` vale na malha do artigo, com `L1.1`
grudado.

## 6. Efeito nos resultados
Nenhum claim muda. `G-E001` continua passado. O que muda é que `L1.1` deixa de ser um fato
solto e passa a ter causa identificada, e que a folga de discretização anunciada no
`ADENDO-004` fica corrigida de ~8× para 5×.
