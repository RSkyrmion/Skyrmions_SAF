# MISSION-R002 — Reprodução estrutural: linha de centro da Eq. (S1)

```yaml
mission_state:
  lifecycle: TERMINAL_AWAITING_HUMAN   # gate G-R002 passou; ver RELEASES/RELEASE-R002.md
  epistemic_regime: REPRODUCTION
  scientific_verdict: PARTIAL_PASS   # primario+terciario passaram; secundario nao-discriminante
  evidence_strength: BOUNDED
  human_acceptance: PENDING
  freeze_status: NOT_FROZEN
  material_status: RELEASE_SEALED
  external_action_authorization: NOT_AUTHORIZED
```

## Por que esta missão existe
R001 comparou **um escalar** contra **um número publicado**. O limite que nenhuma troca de
solver conserta é a minha *leitura* do artigo: se eu errei a convenção de sinal de D, o
ansatz, ou qual K entra, qualquer segundo solver alimentado pelo meu mesmo deck concorda
comigo e não nota nada.

Um erro de leitura normalmente **quebra uma tendência**, não desloca um número só. Daí esta
missão: reproduzir uma previsão **estrutural, multiponto**, com o código que já existe.

## Alvo publicado
Material suplementar, Eq. (S1):
```
K0 = 0.65 − 2.5·Aint          (K0 em MJ/m³, Aint em mJ/m²)
```
descrita como *"traça aproximadamente a linha de centro da região de estabilidade"*.

Consistência já verificada por leitura (sem simulação): a relação bate **exatamente** nos
dois regimes do texto principal — Aint=0.02 → K0=0.60 ✓ ; Aint=0.12 → K0=0.35 ✓.

## Pergunta
A região de estabilidade do par produzida pelo `saf.cu`, no plano (Aint, K0), tem linha de
centro compatível com `K0 = 0.65 − 2.5·Aint`?

## Semantic lock

### SL-B1 — A região mapeada é dependente da inicialização
A Fig. 5(c) mostra ramos coaxial e não-coaxial **coexistindo**: o resultado depende da bacia
de atração. Com uma inicialização fixa (separação 10 nm, ansatz de 360°, quiralidade escolhida
por energia DMI) eu traço **a região de estabilidade alcançável a partir do protocolo
declarado no artigo**, e não "a região de estabilidade" em abstrato.

Consequência que precisa ser carregada: um colapso em algum K0 é **ambíguo** entre "o par é
instável ali" e "esta inicialização saiu da bacia". Não interpretar como o primeiro sem
evidência adicional.

### SL-B2 — Classificação por (Q, área), nunca por Q sozinho
**Um skyrmion em explosão continua com |Q| = 1** — a topologia se conserva enquanto o domínio
cresce. Classificar só por Q rotularia estados explodidos como estáveis, que é justamente o
modo de falha que `MISSION-R001.md` já nomeia.

Regra de classificação, por camada, ao fim da relaxação:
| classe | critério |
|---|---|
| `COLLAPSE` | \|Q\| < 0.5 (skyrmion desapareceu) |
| `EXPLODE` | \|Q\| ≥ 0.5 **e** área revertida > 10 % das células |
| `STABLE` | \|Q\| ∈ [0.95, 1.05] **e** área revertida ≤ 10 % |
| `AMBIGUOUS` | qualquer outro caso, ou relaxação não convergida no orçamento |

Sub-classificação de `STABLE`: `COAXIAL` se l < 1 nm, `NONCOAXIAL` caso contrário.

**Limiar de área calibrado da evidência do R001, não inventado:** o estado ligado de
`EVIDENCE/R001/mfinal_weak_tight.dat` usa **1.10 %** das células (110 de 10000, raio efetivo
5.92 nm). O limiar de 10 % é ~9× isso — folga confortável, e muito abaixo do ~50 % de um
estado em faixa/espiral.

### SL-B3 — Região de estabilidade inclui os dois ramos
A Eq. (S1) traça a linha de centro da *região de estabilidade do par*, que segundo a
Fig. 5(c) contém **tanto** o ramo coaxial **quanto** o não-coaxial. Logo `STABLE` = par
sobrevive, independentemente do ramo. Não restringir a `NONCOAXIAL`.

## Protocolo
1. **Checagem de poder do teste (antes de gastar a varredura inteira).** Varrer uma coluna
   só: `Aint = 0.02`, `K0` de 0.15 a 0.85. Medir a **largura da janela de estabilidade**.
   - Janela estreita (≲ ±0.05 MJ/m³) → a linha de centro é bem determinada, o teste discrimina.
   - Janela larga (≳ ±0.15 MJ/m³) → a linha de centro é mal determinada e **o critério
     secundário passaria com quase qualquer leitura, certa ou errada**. Nesse caso o teste é
     não-discriminante e isso deve ser **reportado como tal**, não maquiado.
2. Só então varrer `Aint ∈ {0.02, 0.04, 0.06, 0.08, 0.10, 0.12}` mJ/m².
3. Para cada Aint: janela `[K0_min, K0_max]` de `STABLE`; centro = ponto médio.
4. Ajuste linear do centro vs Aint; comparar com (inclinação −2.5, intercepto 0.65).

## Critério de aceite — **PRÉ-REGISTRADO, antes de qualquer execução**

**Primário (binário, é este que discrimina):**
Os dois pontos publicados devem cair **dentro** da minha região `STABLE`:
`(Aint, K0) = (0.02, 0.60)` e `(0.12, 0.35)`.
Se uma leitura minha estiver errada, é muito provável que um destes caia fora.

**Secundário (fraco por construção — declarado fraco aqui, não depois):**
Ajuste da linha de centro em Aint ∈ [0.02, 0.12] com
inclinação em **[−3.125, −1.875]** (−2.5 ± 25 %) e intercepto em **[0.57, 0.73]** (0.65 ± 0.08).

Tolerâncias largas de propósito: o próprio SM chama a Eq. (S1) de *empírica* e diz
*"aproximadamente"*, e **não define** como o centro foi obtido. Um critério apertado aqui
seria fingir precisão que a fonte não oferece.

**Terciário (qualitativo, robusto):** a janela de estabilidade deve **descer** em K0 de forma
monótona conforme Aint cresce. Inclinação positiva ou não-monotonicidade refuta a estrutura
independentemente de qualquer ajuste.

**Regressão grátis:** o ponto (0.02, 0.60) deve devolver `l = 10.96 nm`. Se não devolver, a
cópia do código em R002 divergiu da de R001 e eu descubro na hora.

## Critério de falha / inconclusão
- Ponto publicado fora da região `STABLE` → **erro de leitura provável**. R001 fica
  materialmente afetado e **não deve ser aceito** sem investigação.
- Janela larga demais (passo 1) → teste **não-discriminante**. Reportar como inconclusivo;
  não usar o critério secundário como se tivesse passado.
- Muitos `AMBIGUOUS` perto das bordas → refinar orçamento de relaxação, não reclassificar.

## Provenance / integridade
`saf.cu` é **copiado** para `EVIDENCE/R002/`, não editado em `EVIDENCE/R001/`. O hash do
R001 em `EVIDENCE/R001/SHA256SUMS.txt` é provenance as-run selada (INV-07) e não pode mudar
por causa de uma missão posterior. R002 tem o seu próprio hash.

## Gate final
`G-R002`: passa se o critério **primário** passar e o terciário não for violado. O secundário
é informativo, e o seu resultado deve ser reportado com a ressalva de fraqueza acima.

## Stop rules
- Não instalar nem compilar solver algum nesta missão.
- Não enviar código nem PDF a agente/serviço externo sem autorização explícita e separada.
- `MISSION-A001` continua `PROPOSED`.

---

## RESULTADO DA CHECAGEM DE PODER (passo 1) — registrado ANTES de rodar o resto

Coluna `Aint = 0.02`, K0 de 0.15 a 0.85, passo 0.025 (29 pontos).
Evidência: `EVIDENCE/R002/power_check_aint0.02.csv`.

| K0 (MJ/m³) | desfecho |
|---|---|
| ≤ 0.375 | EXPLODE (área revertida 13–45 %) |
| 0.400 – 0.525 | COAXIAL |
| 0.550 – 0.825 | NONCOAXIAL |
| 0.850 | COLLAPSE |

**Janela de estabilidade = [0.400, 0.825] → semi-largura ±0.21 MJ/m³.**

### Veredicto do critério secundário: **NÃO-DISCRIMINANTE**
O protocolo pré-registrado diz: janela ≳ ±0.15 → linha de centro mal determinada, o critério
secundário passaria com quase qualquer leitura, e isso deve ser reportado como tal.
±0.21 > ±0.15. Portanto **o critério secundário está morto e não será usado como evidência**,
independentemente do valor que o ajuste devolver.

Para registro, e explicitamente **não** como sucesso: centro observado = 0.6125 contra 0.60
previsto pela Eq. (S1). Com janela de ±0.21, esse acordo não carrega informação.

### SL-B2 validado empiricamente
Todos os 8 estados classificados `EXPLODE` têm `|Q| = 1.0000` **exato**. Classificação só por
Q teria rotulado os 8 como estáveis. O critério conjunto (Q, área) era necessário, não zelo.

### Critério primário: continua vivo
`(0.02, 0.60)` → `NONCOAXIAL`, dentro da região estável. ✓
Falta `(0.12, 0.35)`.

---

## TESTE NOVO — fronteira coaxial↔não-coaxial   **[origem post-hoc, declarada]**

**Origem honesta:** esta observável não estava no desenho original. Eu a encontrei *olhando*
os dados da coluna Aint=0.02. Usá-la como se fosse o teste pré-registrado seria INV-05
(descoberta virando confirmação). Está registrada aqui **antes** de eu rodar as demais
colunas, e o seu estado epistemológico é:

```
DISCOVERY_ONLY em Aint=0.02  →  CLAIM_CANDIDATE se confirmada nas demais colunas
```

**Por que vale mais que a linha de centro:** a transição coaxial→não-coaxial em Aint=0.02 cai
entre K0=0.525 e K0=0.550 — determinada com resolução de 0.025, ~10× melhor que a
semi-largura de ±0.21 da janela de estabilidade.

**Alvo publicado:** a Fig. 5(c) mostra essa fronteira como linha tracejada separando os ramos
coaxial e não-coaxial dentro da região estável.

**Critério pré-registrado agora, para as colunas ainda não executadas
(Aint = 0.04, 0.06, 0.08, 0.10, 0.12):**
1. A fronteira deve **existir** em cada coluna (os dois ramos coexistem) — estrutura da Fig. 5(c).
2. O ramo não-coaxial deve estar **acima** em K0 e o coaxial **abaixo**, como em Aint=0.02.
3. A fronteira deve **descer** em K0 de forma monótona conforme Aint cresce.

**Limitação que não pode ser omitida:** eu não consigo extrair valores numéricos da linha
tracejada da Fig. 5(c) a partir do texto do PDF. Portanto este teste é **estrutural e
qualitativo**, não quantitativo. Ele pode refutar a minha leitura; não pode confirmá-la com
precisão numérica.
