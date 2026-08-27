# MISSION-I001 — a deriva espúria é o rastreador ou é a magnetização?

Estado: **`AUTHORIZED`** por `WRITEBACK-013` · Data: 2026-08-25
Regime: caracterização de instrumento

> **Pré-registro.** Escrito antes de qualquer código novo e de qualquer corrida.

## 1. A pergunta
O `E003` mediu, **sem excitação alguma**, deriva de `0.917 cm/s` ao longo da ligação, fora do
eixo, **constante** (não decai). Duas causas possíveis, não separadas:

- **`C-tracker`** — viés do meu rastreador. O `track_update` usa como origem de desdobramento
  a CTC da **amostra anterior**. Se o mapa `origem → saída` não tiver ponto fixo local, o erro
  se **realimenta** e a posição acumulada anda sozinha, com a magnetização parada.
- **`C-real`** — movimento real. Força de rede (tipo Peierls) sobre um par incomensurável,
  convertida em deriva giroscópica ao longo da ligação por `Γ = G/α𝒟̄` alto.

## 2. `IV-1` — o teste decisivo: rastreador sobre estado CONGELADO
Relaxar a `θ = 30°` exatamente como no `E003`, **congelar a magnetização** (nenhum passo de
LLG) e chamar o rastreador **10 001 vezes**, a mesma cadência e o mesmo número de amostras da
corrida de controle do `E003`.

Com a magnetização imóvel, qualquer deslocamento reportado é **100 % do instrumento**.

**Critério, e ele é uma comparação, não um limiar:** a deriva reportada sobre estado congelado
é comparada com os `0.917 cm/s` medidos ao vivo.
- `≈ 0.917 cm/s` ⇒ **`C-tracker`**: a deriva é artefato do estimador.
- `≪ 0.917 cm/s` (menos de 1 %) ⇒ **`C-real`**: o instrumento está limpo e a magnetização
  move-se de fato.
- intermediário ⇒ as duas causas contribuem; reportar a partição, sem escolher lado.

## 3. `IV-2` — confirmação por localizadores sem realimentação
Na corrida **viva** de controle (excitação desligada, `θ = 30°`, 20 ns), medir a posição do par
por **três** localizadores simultâneos:

| | localizador | realimenta origem? |
|---|---|---|
| **(a)** | CTC com origem na amostra anterior (o do `E002`/`E003`) | **sim** |
| **(b)** | CTC de Berg–Lüscher com origem **fixa** no centro da caixa | não |
| **(c)** | centroide de `(1 − m_z·bg)/2`, origem fixa — **outro funcional**, sem `ρ` | não |

**Leitura registrada:** se (b) e (c) derivarem junto com (a), é `C-real`. Se só (a) derivar, é
`C-tracker`. Se (b) e (c) discordarem entre si, o problema é mais fundo que o rastreador e a
missão relata isso sem veredito.

O localizador (c) é deliberadamente **outro funcional**: não usa Berg–Lüscher, não usa carga
topológica. Uma leitura errada compartilhada entre (a) e (b) não sobrevive a ele.

## 4. Checagem de poder, antes do dado
A deriva a medir é `0.917 cm/s = 0.0092 nm/ns`; em 20 ns são **0.18 nm**, ou seja 18 % de uma
célula. Os localizadores (a) e (b) são de subcélula e no `E002` resolveram `l` a `1e−4 nm`.
O localizador (c) é de subcélula pelo mesmo argumento de primeiro momento. **Poder folgado:
três ordens de grandeza.** O que este teste **não** consegue é resolver derivas abaixo de
`~1e−3 cm/s`, e nada aqui depende disso.

## 5. Taxonomia de falha
| resultado | significado, decidido antes |
|---|---|
| `IV-1` ≈ 0.917 | **`C-tracker`**. Afeta o `E003` e **potencialmente toda medida de posição deste laboratório**. Vira limite novo e grave |
| `IV-1` ≪ 0.917 e (b),(c) derivam | **`C-real`**. A ressalva 1 do `E003` fecha: o artefato é físico-de-rede, não do instrumento |
| (b) e (c) discordam | sem veredito; problema mais fundo, relatar como tal |
| `IV-1` intermediário | partição relatada, sem escolher lado |

## 6. Limites
- Testa **um** estado (`θ = 30°`, relaxado, acoplamento fraco). Não é caracterização geral.
- **Não** testa travessia da fronteira periódica, que o `L5.3` já registra como não testada.
- `L-G` intocado.

## 7. Provenance
Código novo em `LAB/EVIDENCE/I001/saf_inst.cu`, derivado do `saf_prop3.cu` **selado**.
Caminhos de escrita redirecionados para `I001/` antes da primeira execução, verificado por
`grep`.

## 8. Gate
`G-I001` = `IV-1` conclusivo ∧ (b),(c) concordantes entre si. **Passar o gate não é aceite.**
