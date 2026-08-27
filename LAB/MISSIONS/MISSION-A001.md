# MISSION-A001 — Auditoria cruzada do solver R001 contra mumax3

```yaml
mission_state:
  lifecycle: PROPOSED           # NADA aqui esta autorizado. Nem o build.
  epistemic_regime: AUDIT       # M-C. NAO e' reproducao; nao substitui R001.
  scientific_verdict: NOT_APPLICABLE_YET
  evidence_strength: NOT_APPLICABLE_YET
  human_acceptance: PENDING
  freeze_status: NOT_FROZEN
  material_status: NO_ARTIFACTS_YET
  external_action_authorization: NOT_AUTHORIZED
```

## Origem
Pergunta de Rodrigo (2026-08-21): o mumax3 pode servir como solver independente para
checar o resultado do R001?

## Pergunta da missão
Um solver micromagnético escrito por terceiros e validado pela comunidade relaxa o mesmo
sistema para o mesmo comprimento de ligação que `saf.cu`?

## O que esta auditoria compra — e o que NÃO compra
**Compra (real):** validação da *numérica* — stencil de troca, discretização do DMI,
convergência ao mesmo ponto fixo, medida de Q. `saf.cu` nunca foi confrontado com código
independente; a escada VL-1..VL-5 testa consistência interna, o que é diferente.

**Não compra:** validação da minha *leitura do artigo*. Eu escrevo os dois decks de entrada.
Se eu errei a convenção de sinal de D, o ansatz de 360°, ou qual K entra, **os dois códigos
herdam o mesmo erro e concordam lindamente**. O limite nº 3 de `RELEASE-R001.md` ("nenhum
solver de terceiros validou este código") seria **rebaixado, não eliminado**.

**Introduz risco novo:** o mumax3 não tem termo de acoplamento interlayer areal. A tradução
para `ext_InterExchange` é uma superfície de falha que o meu código nunca teve — é a `QA-02`
voltando pela porta dos fundos. Ver SL-A1.

## Semantic lock — as duas checagens que decidem a missão

### SL-A1 — Tradução do acoplamento areal (J/m²) para Aex entre regiões (J/m)
mumax3, campo de troca na célula 1 vindo do vizinho em z:
`B = (2·A_eff/(Ms·cz²))·(m2 − m1)`. A parte `−m1` não gera torque (m×m = 0), então o que
importa é `(2·A_eff/(Ms·cz²))·m2`. Igualando ao alvo `−(Aint/(Ms·d))·m2`:

```
A_eff = −Aint·cz²/(2d)
com cz = d = 0.4 nm :   A_eff = −Aint·d/2 = −4.0e-15 J/m
```
API: `ext_InterExchange(1, 2, -4.0e-15)` (`engine/exchange.go:92`, valor em J/m, direto).

**Isto é derivação, não evidência.** A checagem que decide é o espelho de VL-2: estado
uniforme antiparalelo, verificar que o mumax3 reporta `|Beff_int| = 0.086207 T`. Se não bater,
a tradução está errada — e nada com skyrmion deve rodar antes disso.
Nota: `lex2` é `float32` no mumax3; o meu código é `double`. A comparação é single vs double.

### SL-A2 — Convenção de sinal do `Dind` vs Eq. (A4)   **[a checagem que se costuma pular]**
`saf.cu` escolhe a quiralidade por energia DMI (`pick_chirality`, linha 307), então ele
**se autocorrige** se a convenção de sinal for outra. O mumax3 **não**: `Dind` é setado
explicitamente. Se as convenções diferirem, o mumax3 relaxa a quiralidade oposta e a
divergência vai **parecer numérica sendo semântica**.

Fixar antes de comparar `l`: rodar um skyrmion único em cada código e comparar o **sentido de
rotação da magnetização no plano**, não só `|Q|`.

## Tolerância de concordância — **PRÉ-REGISTRADA**
**|l_mumax3 − l_saf| / l_saf ≤ 2 %.**

Justificativa escrita **antes** de rodar, para o número não ser engenharia reversa do
resultado: (i) mumax3 é precisão simples, `saf.cu` é dupla; (ii) o tratamento de fronteira do
DMI interfacial difere; (iii) `cz = 0.4 nm` deixa a ligação interlayer numericamente rígida;
(iv) as discretizações de troca e DMI não são idênticas. **Não** usar os 0.2 % que R001 obteve
contra o artigo: isso seria ajustar o deck até bater.

## Passos (nenhum autorizado)
1. **Compilar o mumax3 do fonte.** O binário em `tools/mumax3.12_linux_cuda12.9/` **não roda**
   (CUDA 12.9 vs driver 12.2). O tarball só traz essa build. Fonte: `tools/mumax3-src`
   (64 kernels .cu, sem PTX pré-gerado), com `nvcc` 11.8 e `tools/go` 1.22.6,
   `make CUDA_CC=89`. **Isto é ação de sistema e precisa da sua autorização explícita.**
2. SL-A1: espelho de VL-2 no mumax3 (estado uniforme).
3. SL-A2: skyrmion único, comparar quiralidade nos dois códigos.
4. Só então: par acoplado, mesmo problema, comparar `l`.

## Critério de falha / inconclusão
- SL-A1 falhando → tradução errada. Bloqueia tudo. Não é resultado científico.
- SL-A2 divergindo → problema semântico, **não** discordância física. Registrar e resolver.
- **Discordância acima de 2 % é um resultado, não um defeito a ser eliminado.** Significa que
  um dos dois códigos tem bug, ou que a tradução SL-A1 está errada. Nesse caso R001 **não**
  deve ser aceito sem investigação, e a discordância entra no ledger como conhecimento
  negativo (INV-09), não é apagada.

## Achado colateral que já vale para o R001 (sem custo, sem execução)
O mumax3 expõe `ext_topologicalchargelattice` — descrito no próprio fonte como
*"2D topological charge according to Berg and Lüscher"* (`engine/ext_topologicalchargelattice.go:11`).
Ou seja: o estimador que adotei em `SL-7` durante o VL-3 é o **padrão da comunidade**, não um
remendo ad-hoc meu. Isso fortalece o R001 **independentemente desta missão ser autorizada**.

## Relação com R001
R001 está `TERMINAL_AWAITING_HUMAN`. Rodrigo pode, coerentemente:
- **(a)** aceitar R001 primeiro (com o limite nº 3 explícito) e autorizar A001 depois; ou
- **(b)** autorizar A001 antes, como insumo para a decisão de aceite.
As duas são válidas. É decisão dele, não minha.
