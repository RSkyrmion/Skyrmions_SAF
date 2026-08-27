# MISSION-E001 — Fase 2: dinâmica LLG e espectro dos modos de breathing

Estado: **`AUTHORIZED`** por `WRITEBACK-008` · Data: 2026-08-24
Regime: extensão controlada (primeira missão da Fase 2)

> **Pré-registro.** Escrito e congelado ANTES de qualquer linha de código de dinâmica.

---

## 1. Por que esta missão, e não a autopropulsão
A autopropulsão sob ABM é o resultado central do artigo e foi o que eu sugeri. **Não é uma
pequena extensão controlada.** O `saf.cu` hoje faz **descida amortecida** — não tem `γ`, não
tem termo de precessão, e `SL-5` registrou explicitamente que a trajetória dele não é
evidência. Autopropulsão exige LLG real, muitos ciclos e rastreio de deriva.

Esta missão implementa e **valida** a dinâmica, e mede um observável com alvo publicado. É
pré-requisito da autopropulsão, que fica como `E002`, **não proposta**.

## 2. Protocolo do artigo (Apêndice B, extraído; imagem da p. 8 é a autoridade)
- `T = 0`. Amortecimento de Gilbert **α = 0.02**.
- Excitação em sinc: `sinc(x) = sin(πx)/πx`, corte `f_c = 100 GHz`.
- **`B_ext(t) = ẑ B₀ sinc(f_c t)`, `B₀ = 4 mT`** → excita o **ABM** (antissimétrico).
- **`K(t) = K₀ + ΔK sinc(f_c t)`, `ΔK = 0.004 K₀`** → excita o **SBM** (simétrico).
- Registrar `δm_z(t) = ⟨m_z(t)⟩ − ⟨m_z⟩_eq` por camada, a cada **2 ps**, por **Δt = 10 ns**.
- Modos identificados pelo espectro de potência.

Mapeamento SBM/ABM lido do texto principal, não suposto: a anisotropia é invariante por
reflexão especular, logo `ΔK` faz os dois skyrmions respirarem **em fase** (SBM); já `B_z`
quebra a simetria de inversão — sob `B_z > 0` o de cima contrai e o de baixo expande (ABM).

**Ponto de operação:** acoplamento fraco, `A_int = 0.02 mJ/m²`, `K₀ = 0.6 MJ/m³`, `B = 0`,
a partir do estado de equilíbrio já selado do R001.

## 3. Escada de validação e critérios pré-registrados

### EV-1 — a precessão é uma rotação (α = 0, sem excitação)
Com `α = 0` a LLG é conservativa. **PASSA se**, ao longo de 1 ns:
- deriva de energia `|ΔE|/|E| < 1e−4`;
- `max | |m| − 1 | < 1e−10`.

Justificativa: um termo de precessão com sinal, fator ou estêncil errado **não conserva
energia**. Este teste não pode ser passado por acidente.

### EV-2 — frequência de Larmor (alvo analítico, não do artigo)
Estado uniforme levemente inclinado, campo `B_z = 0.1 T`, `α = 0`, **sem** troca, DMI,
anisotropia ou acoplamento. A precessão tem de dar `f = γB/2π`.
Com `γ = 1.760859e11 rad s⁻¹ T⁻¹` → **`f = 2.8025 GHz`**.
**PASSA se** dentro de **0.5 %**. Calibra `γ` e o sinal, isolados de tudo mais.

**Convenção fixada, para o teste testar o que deve:** `γ` aqui é a razão giromagnética na
convenção **tesla**, `1.760859e11 rad s⁻¹ T⁻¹`, e **todo campo no `saf.cu` é em tesla** (o
código já imprime `Beff` e `Aint/(Ms·d)` em T). Muitos códigos micromagnéticos carregam
`γ₀ = μ₀γ = 2.2128e5 m A⁻¹ s⁻¹` e trabalham com campo em A/m; misturar as duas coisas insere
um `μ₀` silencioso. **Não introduzir A/m em lugar nenhum.**

### EV-3 — espectro de breathing (o teste com alvo publicado)

**Checagem de poder, feita ANTES dos dados** — aprendendo com o defeito registrado no
`RELEASE-R002` §2: o artigo dá SBM ≈ **18 GHz** e usa **19.24 GHz** para o ABM. Os dois
distam **7 %**. Portanto **qualquer banda de tolerância ≥ ±10 % é incapaz de distinguir SBM
de ABM**, e não pode ser usada para afirmar identidade de modo. Registro isto agora, não
depois.

- **PRIMÁRIO — escala do modo.** Pico do espectro sob excitação `ΔK` dentro de **±20 % de
  18 GHz**, isto é **[14.4, 21.6] GHz**.
  Declarado explicitamente: isto testa a **escala**, não a identidade. Um erro de fator 2 em
  `γ`, na normalização do campo ou no prefator da LLG **falha**. Uma confusão SBM↔ABM **não**
  falha, e por isso não será alegada com base neste critério.
- **SECUNDÁRIO — ordenamento, e este discrimina identidade.** Rodando as **duas** excitações
  com o mesmo código: **`f_ABM > f_SBM`**. O artigo afirma esta ordem; ela pode falhar.
- **TERCIÁRIO — assinatura no bond.** `l(t)` oscila a `ω` sob SBM e a `2ω` sob ABM.
  Declarado **exploratório**: sem alvo numérico pré-registrado, reportado como observação,
  nunca como resultado.

### EV-3.1 — janela de integração, registrada antes de rodar
A resolução em frequência é `1/Δt`: 0.1 GHz em 10 ns, 0.5 GHz em 2 ns. Contra uma banda de
±20 % (≈ ±3.6 GHz), **2 ns já é folgado**. O protocolo do artigo pede 10 ns.
**Regra registrada:** medir o custo com um trecho curto **antes** de comprometer a corrida
cheia. Se 10 ns for viável, usar 10 ns. Se não, usar a maior janela viável **≥ 2 ns**, e
declarar a janela usada junto com o resultado. A janela **não** será escolhida depois de ver
o espectro.

## 3.1 Caminho conhecido e NÃO testado por esta escada
O fator `1/(1+α²)` da Eq. (A1). Com `α = 0` (EV-1 e EV-2) o denominador vale exatamente 1,
logo **a escada não consegue detectar se ele foi implementado**. Com `α = 0.02` ele é uma
correção de 0.04 % na escala de tempo — invisível dentro da banda de ±20 % do EV-3, portanto
inofensivo **aqui**. Fica registrado como dívida: em `E002` (autopropulsão, trajetórias de
~3 µs) o erro acumula e passa a importar.

## 4. Taxonomia de falha — pré-registrada
- **EV-1 ou EV-2 falham** → a dinâmica está errada. `EV-3` é **descartado**, e a missão não
  produz afirmação alguma sobre modos.
- **EV-1/EV-2 passam, PRIMÁRIO falha** → discrepância real de escala entre a minha leitura e
  o artigo. Vira investigação, não veredito.
- **PRIMÁRIO passa, SECUNDÁRIO falha** → a escala está certa e a atribuição de simetria está
  errada. Reportar assim, sem suavizar.

## 5. Limites que já são conhecidos e vão viajar junto
- Nada aqui toca `L-G`: continua sem verificação independente do resultado por outro solver.
- Malha de 1 nm e caixa de 100 nm, não refinadas nesta missão.
- O estado inicial é o equilíbrio do **meu** código (agora com a régua verificada pelo
  `AUDIT-002`, mas o estado ainda é meu).

## 6. Gate
`G-E001` = EV-1 ∧ EV-2 ∧ (EV-3 primário). **Passar o gate não é aceite.**
