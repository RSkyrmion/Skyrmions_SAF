# MISSION-A002 — Auditoria do `saf.cu` contra OOMMF (solver independente)

Estado: **`AUTHORIZED`** por `WRITEBACK-006` · Regime: `AUDIT` · Data: 2026-08-24

> **Este arquivo é pré-registro.** Escrito e congelado ANTES de qualquer execução do OOMMF.
> Os alvos numéricos abaixo vêm de logs do R001 já selados em `EVIDENCE/R001/`.

---

## 1. O que esta missão testa — e o que ela NÃO testa

**Testa a implementação, não a leitura.** O OOMMF fornece um caminho numérico independente:
estênceis, termos de energia, minimizador e — crucialmente — a conversão areal→volumétrica
do acoplamento entre camadas, tudo em código escrito por humanos e validado por uma
comunidade ao longo de duas décadas. Isso quebra a correlação que dois LLMs teriam.

**Não testa a leitura do artigo.** O arquivo MIF é escrito por mim. A minha tradução de
(A3)/(A4) para objetos do OOMMF é minha, e uma leitura errada se propaga igual nos dois
códigos. O `AUDIT-001` (derivação cega) testou a leitura; esta missão testa a implementação.
**Nenhuma das duas testa as duas coisas.** Isto está escrito aqui, antes dos resultados,
para não virar racionalização depois.

**O estimador é deliberadamente mantido fixo.** `l` e `Q` do estado final do OOMMF serão
computados com o **meu** estimador (Berg–Lüscher + centros de carga da Eq. 1), o mesmo do
`saf.cu`. Isso é de propósito: mantém o estimador constante para isolar a diferença no
*solver*. Consequência declarada: um erro do estimador é **invisível** a esta missão — é
exatamente o buraco que a proposta do estimador cego em Python atacaria, e ela não está
autorizada.

## 2. Tradução do modelo — decisões declaradas antes de rodar

| item do artigo | objeto OOMMF | valor / observação |
|---|---|---|
| grade 100×100 nm², célula 1×1 nm², PBC | `Oxs_PeriodicRectangularMesh`, periódico em `xy` | célula `1×1×0.4 nm` |
| espessura `d = 0.4 nm` | dimensão `z` da célula | **tem de ser exatamente `d`** (ver §2.1) |
| duas camadas, sem troca entre elas | 3 células em `z`: camada 1 / espaçador `Ms=0` / camada 2 | `Oxs_UniformExchange` é 6-vizinhos e acoplaria em `z` sem o espaçador |
| `A = 15 pJ/m` | `Oxs_UniformExchange` | |
| `K = K₀ = 0.6 MJ/m³`, eixo `z` | `Oxs_UniaxialAnisotropy` | |
| **sem demag** (QA-01: absorvido em `K₀`) | `Oxs_Demag` **omitido** | decisão registrada, não esquecimento |
| `D₁ = −D₂ = 3.05 mJ/m²` | `Oxs_DMExchange6Ngbr` por região | ver §2.2 |
| `H_int = A_int m₁·m₂`, areal | `Oxs_TwoSurfaceExchange` | **`sigma = −A_int`** (ver §2.1) |
| `B = 0` | sem Zeeman | |
| relaxação a `T = 0` | `Oxs_MinDriver` + `Oxs_CGEvolve` | |

### 2.1 Convenção de sinal e o peso `1/t_z` — lidos da fonte, não supostos
`app/oxs/ext/twosurfaceexchange.cc` documenta a densidade de energia como
`[sigma*(1 − mi·mj) + sigma2*(...)]/cellsize`. Comparando com `A_int m₁·m₂` do artigo, a
parte dependente de `m` casa com **`sigma = −A_int`**; sobra um offset constante `sigma`,
que não afeta campo nem equilíbrio mas **desloca energias absolutas**.
→ Por isso o OV-2 compara **diferenças** de energia entre dois estados, nunca absolutos.
Isso neutraliza de uma vez este offset e qualquer offset análogo na anisotropia.

O peso é `cellwgt = |Δ|/⟨Δ̂, celldims⟩ = 1/t_z`: o inverso da **espessura da célula** na
direção do link, independente do vão entre as superfícies. Daí a exigência `t_z = d`.

Resta indeterminado pela leitura da fonte um possível **fator 2** (a energia do link é
somada às duas células, e a soma final é multiplicada por `2·V_cell`). **Não vou resolver
isso lendo mais fonte** — o OV-2 mede. É o mesmo movimento que o VL-1/VL-2 fizeram.

### 2.2 DMI — verificado na fonte
`app/oxs/local/dmexchange6ngbr/DMexchange6ngbr.cc` acopla **apenas `x` e `y`** (o peso em
`z` está comentado, linha 193) e guarda todos os termos com `Ms_inverse[j]!=0`. É a DMI
interfacial da Eq. (A4), e o espaçador não vaza DMI entre camadas.

---

## 3. Escada de validação e **critérios pré-registrados**

### OV-1 — skyrmion único, acoplamento desligado
Camada 1 sozinha, `sigma = 0`, `D = 3.05 mJ/m²`, `K₀ = 0.6 MJ/m³`, fundo `+z`.
**PASSA se:** relaxa para `|Q| = 1` dentro de `0.05` e `mz` mínimo `< −0.9`.
Justificativa: `κ = D/D_c = 0.80 < 1` diz que isto *tem* de funcionar. Se falhar, a tradução
está errada — não a física.

### OV-2 — estados uniformes, só o termo interlayer *(o teste mais valioso da escada)*
Só `Oxs_TwoSurfaceExchange` ativo. Dois estados uniformes: `m₁=+z,m₂=+z` (paralelo) e
`m₁=+z,m₂=−z` (antiparalelo).

**Alvos pré-registrados** (`A_int = 0.02 mJ/m² = 2e−5 J/m²`, caixa `100×100 nm²`,
`A_box = 1e−14 m²`, `Ms = 0.58 MA/m`, `d = 0.4 nm`):

```
|E_paralelo − E_antiparalelo|  =  2·A_int·A_box  =  4.0000e-19 J
|Beff_int|                     =  A_int/(Ms·d)   =  0.086207 T
```

**PASSA se** ambos dentro de `1 %`.
Este é o `SL-2` — o fator `1/d` — medido por implementação humana independente. Já fechado
por três caminhos (FD interno, valor fechado interno, derivação cega externa); este seria o
quarto, e o primeiro por código independente.

### OV-3 — o par acoplado (o teste que discrimina)
`A_int = 0.02 mJ/m²`, `K₀ = 0.6 MJ/m³`, `B = 0`, dois skyrmions de cargas e quiralidades
opostas, separação inicial `10 nm`, ansatz de parede de domínio 360° (`R = 4 nm`, `w = 3 nm`),
o mesmo do `saf.cu`.

**Alvos pré-registrados, dos logs selados do R001:**

| referência | arquivo selado | `l` medido pelo `saf.cu` |
|---|---|---|
| tolerância padrão | `EVIDENCE/R001/mfinal_weak.dat` | **10.9529 nm** |
| tolerância apertada | `EVIDENCE/R001/mfinal_weak_tight.dat` | **10.9607 nm** |
| malha 0.5 nm | `EVIDENCE/R001/mfinal_mesh05.dat` | 10.8500 nm |
| publicado (Fig. 2a) | — | 10.98 nm |

**Critério PRIMÁRIO — PASSA se** `l` do OOMMF cai na banda **`[10.43, 11.53] nm`**, a mesma
banda que o R001 pré-registrou.
**Critério SECUNDÁRIO, declarado fraco de saída:** concordância com `10.95–10.96 nm` melhor
que `1 %`. Registrado como **não-discriminante para aceite**, porque a própria sensibilidade
à malha do R001 é de `1.0 %`. Vale como dado, não como resultado.
**Também exigido:** ramo não-coaxial (`l` não vai a zero), `Q₁ = −Q₂`, `|Q| ≈ 1`.

## 4. Taxonomia de falha — pré-registrada, para não escolher a explicação depois

- **OV-1 ou OV-2 falham** → é **erro de tradução meu** (`SL-A1`), não evidência contra o
  `saf.cu`. A missão não produz evidência sobre o R001 e o resultado do OV-3 é descartado.
- **OV-1 e OV-2 passam, OV-3 falha** → **discrepância real entre implementações**, material
  para o R001. Nenhum dos dois códigos fica automaticamente certo; a missão vira
  investigação, não veredito.
- **Tudo passa** → o limite "sem solver independente" cai. Continua de pé, intocado, o
  limite do estimador (§1) e o da leitura compartilhada.

## 5. Artefatos previstos
`EVIDENCE/A002/`: MIFs as-run, `.odt`, `.omf` finais, leitor de `.omf` + estimador, logs,
`SHA256SUMS.txt`, e o `saf.cu`/`saf` de referência por hash (não recopiados).

## 6. Gate
`G-A002` = OV-1 ∧ OV-2 ∧ (OV-3 primário). **Passar o gate não é aceite.**

---

# ADENDO DE PRÉ-REGISTRO — 2026-08-24, escrito APÓS OV-2 e ANTES do OV-1/OV-3

> Motivo: a escada revelou que **PBC é inviável** neste OOMMF para este modelo. Isto altera
> o §2 (tradução). O critério de mitigação abaixo é registrado **antes** de qualquer corrida
> do OV-1/OV-3, para não ser escolhido depois de ver o número.

## A. Calibração corrigida do acoplamento: `sigma = −A_int/2`
O §2.1 previa `sigma = −A_int` e deixava em aberto um "possível fator 2". O OV-2 mediu: o
fator 2 é real (energia somada às duas células × `2·Volume`, e `hcoef = 2/MU0`), e energia e
campo são mutuamente consistentes com `sigma_eff = 2·sigma`. Com `sigma = −A_int/2`:
`|ΔE| = 4.000000e−19 J` (alvo 4.0000e−19) e campo de torque `0.086207 T` (alvo 0.086207).
**OV-2 PASSA nos dois critérios pré-registrados.**

## B. PBC é inviável — dois bloqueios independentes, ambos documentados
1. **`Oxs_TwoSurfaceExchange` + `Oxs_PeriodicRectangularMesh`: bug silencioso.** 1164 de
   10000 células da interface perdem o link; energia 11.6 % curta; campo com 3 valores em vez
   de 1. Determinístico (idêntico com 1 e 4 threads). Evidência: `EVIDENCE/A002/OV2-FINDING.txt`.
2. **`Oxs_DMExchange6Ngbr` recusa PBC.** Erro explícito: *"Import mesh ... is not an
   Oxs_RectangularMesh object."* Recusa dura, não silenciosa. **Este é fatal.**
   `Oxs_DMI_C2v` aceita PBC, mas é simetria **C2v**, não **Cnv** interfacial — modelo errado.
   Contorná-lo exigiria compilar extensão nova: ação de sistema, fora do autorizado.

## C. Desvio declarado: fronteiras livres no lugar de PBC
OV-1 e OV-3 rodam com `Oxs_RectangularMesh`. O artigo usa PBC. Este é um desvio real de
modelo, não de implementação, e vai grudado em qualquer claim que sair daqui.

## D. Critério de mitigação — **PRÉ-REGISTRADO, antes de rodar**
Fronteiras livres com DMI produzem inclinação de borda (condição de Rohart–Thiaville) que
PBC não tem. Os skyrmions ficam no centro, a ~45 nm das bordas, então o efeito deve ser
pequeno — mas "deve ser" não é medida.

**Teste:** rodar o OV-3 em caixa de **100 nm** e em caixa de **140 nm**, tudo o mais igual.

- **Fronteira NÃO contamina** se `|l(140) − l(100)| / l(100) ≤ 1.0 %` — o mesmo 1.0 % da
  sensibilidade à malha já registrada no R001. Nesse caso o OV-3 vale como pré-registrado.
- **Se exceder 1.0 %**, o OV-3 é declarado **NÃO-CONCLUSIVO** quanto ao `saf.cu`: a diferença
  passa a ser dominada pelo desvio de fronteira, não por diferença entre implementações.
  Nesse caso não se reporta veredito sobre o R001.

Nenhum outro critério do §3 muda. A banda primária continua `[10.43, 11.53] nm` e o
secundário continua declarado não-discriminante.
