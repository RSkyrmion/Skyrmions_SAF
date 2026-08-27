# STATE.md — Laboratório SAF-Skyrmion

`head` atual: `STATE-2026-08-27-g` · `LAB_COMPLEXITY=MINIMAL` · `SCIENTIFIC_ASSURANCE=LIGHT`

> Este arquivo é a memória persistente do laboratório. Ele existe para que você — e
> qualquer LLM futura, sem acesso a este chat — consiga retomar a pesquisa a frio.
> Ordem de leitura a frio: este arquivo → `RELEASES/RELEASE-R001.md` →
> `RELEASES/RELEASE-R002.md` → `RELEASES/RELEASE-R002-ADDENDUM-001.md` →
> `RELEASES/WRITEBACK-004.md` → `RELEASES/WRITEBACK-005.md` →
> `RELEASES/RELEASE-AUDIT-001.md` → `RELEASES/WRITEBACK-006.md` →
> `RELEASES/RELEASE-A002.md` → **`RELEASES/WRITEBACK-007.md`** (o aceite; contém a versão
> canônica dos claims e dos limites — leia-o se só puder ler um arquivo além deste) →
> `RELEASES/WRITEBACK-008.md` → `RELEASES/RELEASE-AUDIT-002.md` → `RELEASES/RELEASE-E001.md`
> → `RELEASES/RELEASE-E001-ADDENDUM-001.md` → `RELEASES/RELEASE-E001-ADDENDUM-002.md` → `RELEASES/RELEASE-E001-ADDENDUM-003.md` → `RELEASES/RELEASE-E001-ADDENDUM-004.md` → `RELEASES/RELEASE-E001-ADDENDUM-005.md` →
> `DECISIONS/WRITEBACK-010.md` → `MISSIONS/MISSION-E002.md` → **`RELEASES/RELEASE-E002.md`** → `RELEASES/RELEASE-E002-ADDENDUM-001.md` → **`DECISIONS/WRITEBACK-011.md`** (o aceite do
> `E002`) → `QUERIES-AUTORES-001.md` (as três divergências em aberto) →
> `DECISIONS/WRITEBACK-012.md` → `MISSIONS/MISSION-E003.md` → **`RELEASES/RELEASE-E003.md`** → `RELEASES/RELEASE-E003-ADDENDUM-001.md` →
> `DECISIONS/WRITEBACK-013.md` → `MISSIONS/MISSION-I001.md` → `RELEASES/RELEASE-I001.md` →
> `MISSIONS/MISSION-E004.md` (**leia o `ADENDO-001` no fim dele**) → `DECISIONS/WRITEBACK-014.md`.
>
> **Regra de edição:** só este arquivo é reescrito no lugar. `RELEASE-*` e `WRITEBACK-*`
> nunca são editados — são complementados por adendo ou superados por writeback.

> **REGRAS:** `../CLAUDE.md` é lido automaticamente em toda sessão e traz as regras
> obrigatórias. **Sete** delas são aplicadas por **hooks** (`.claude/settings.json`), não por
> julgamento: aviso de `STATE.md` desatualizado; bloqueio de edição em `RELEASES/`,
> `DECISIONS/` e evidência selada; confirmação em `MISSIONS/`, ao invocar `codex` (ação
> externa) e ao apagar em `EVIDENCE/`/`ARCHIVE/`; e verificação de integridade a cada turno.
> Ver `CLAUDE.md` §9.
>
> **SÍNTESE:** `CONSOLIDATION-2026-08-24.md` resume a análise inicial inteira — o que ficou
> estabelecido, com que força, e o que não ficou. Comece por ele se quiser a história; use
> este arquivo para o estado formal.

## ESTADO GERAL — quinze missões, TODAS aceitas; **o `L-G` moveu-se** (2026-08-27)

> ### O `L-G`, depois do `A003` — e o que ele AINDA é
> Um segundo solver mediu o número. **`mumax3 3.11.1`** (troca, anisotropia, DMI interfacial,
> PBC e integrador escritos por **outras pessoas**, construído em `TOOLS/`), com o estado
> medido pelo **estimador cego do `AUDIT-002`**:
> **`l_mumax3 = 10.9279 nm` contra `l_saf.cu = 10.9607 nm` — `−0.30 %`.**
>
> **O que NÃO fecha, e não pode ser suavizado:**
> - **A leitura do modelo é minha nos dois códigos.** Quais termos, quais parâmetros, como li
>   a Eq. (A4). **Leitura errada compartilhada sobrevive** (`L3.3`).
> - **`0.30 %` está ABAIXO da sensibilidade de malha de `1.0 %`** (`L1.1`). O acordo **não
>   distingue "os dois certos" de "os dois com o mesmo erro"**. O poder é para erro **grosso**.
> - Podia refutar e não refutou — evidência **mais fraca** do que uma refutação teria sido.
> - **A dinâmica segue com um único código** (`C-6`, `C-7`, `C-14`).
>
> **`A003` ACEITO** (`WRITEBACK-023`, `C-15`), e a **redação nova do `L-G` foi aprovada por
> Rodrigo** e está no `CLAUDE.md` §7, datada.
>
> **O risco trocou de lado.** Antes, ao recontar, a tentação era omitir que não havia
> verificação. **Agora é exagerar que há** — dizer "foi verificado por solver independente" e
> parar aí. **Parar aí é falso.**

**Aceitas com limitações (quinze):** `R001`, `R002`, `AUDIT-001`, `A002` (`WRITEBACK-007`);
`AUDIT-002`, `E001` (`-009`); `E002` (`-011`); `E003`, `I001` (`-015`);
**`E004R`, `I002` (`-018`)**; **`I003` (`-019`)**; **`E004`, `E005` (`-021`)**; **`A003` (`-023`)**.
**`REVISION_REQUESTED`:** nenhuma. O `E004` saiu desse estado por `WB-021` — mas o registro
diz **como**: o critério primário dele nunca teve veredito, e a pergunta foi respondida
**pelo `E005`, não por ele**. O aceite é do material.
**`PENDING`: nenhuma.**

**Claims canônicos:** `C-1`..`C-4` (`WB-007`), `C-5`, `C-6` (`-009`), `C-7` (`-011`),
`C-8`, `C-9` (`-015`), **`C-10`, `C-11`, `C-12` (`-018`)**, **`C-13` (`-019`)**, **`C-14` (`-021`)**, **`C-15` (`-023`)**.

> **`C-11` supera o uso do `18.00 GHz`.** A ressonância de breathing SBM é
> **`17.9609 ± 0.0125 GHz`**. O `18.00` do `E001` era um **bin** de resolução `0.1 GHz`.
> Quem citar `18.00` daqui em diante está citando um bin, não uma linha.

> ### ⚠ O LIMITE ACIMA DE TODOS, DEPOIS DE DOZE MISSÕES
> **`L-G` está exatamente onde estava na primeira.** Seis camadas verificadas — leitura,
> estrutura, um termo, a régua, a dinâmica, a autopropulsão — e **nenhuma atacou o número**.
> `10.9607 nm` continua sustentado por **um único código, o meu**.
>
> Nenhuma simulação minha o move. Sair dele exige **ação de sistema** (compilar DMI Cnv com
> PBC no OOMMF) ou **ação externa** (etapa 2 do `AUDIT-001`). **Nenhuma autorizada.**
> Esta é a decisão estratégica na mesa de Rodrigo, e a minha recomendação é a primeira.

### Duas regras novas de processo, adotadas em 2026-08-26 (`WRITEBACK-017`)
1. **`CLAUDE.md` §6.1 — como se escreve um critério.** `R1` comparação, não limiar; `R2`
   convergência na saída; `R3` gate exige veredito. Vieram de **nove** defeitos de desenho
   entre `E002` e `E004R`, com o padrão sem exceção: **todo critério em forma de comparação
   funcionou; todo limiar absoluto falhou.**
2. **`CLAUDE.md` §2 + hook — o pré-registro vai a Rodrigo antes de executar.** Quatro dos nove
   defeitos foram pegos por revisão prévia; os cinco que passaram foram os que ninguém reviu.
   Aplicado pelo hook de `nvcc`; agora são **oito** regras no harness.

### Pendências que NÃO são resolvíveis por simulação minha
| | por quê |
|---|---|
| **`L-G`** | ação de sistema ou externa, não autorizadas |
| `D-1`, `D-2`, `D-3` | dependem dos autores; dossiê em `QUERIES-AUTORES-001.md`, **ação de Rodrigo** |
| `L2.3`, `L1.1` | outras físicas, missões próprias |
| `L8.4` | o `I002` refutou a própria premissa; não separável variando `K₀` |

## Onde as coisas estão (reorganizado em 2026-08-25)
```
SAF/  README.md · ENVIRONMENT.md
      LAB/       STATE.md · CONSOLIDATION-*.md · MISSIONS/ · DECISIONS/ · RELEASES/ · EVIDENCE/
      SOURCES/   paper/ · theory/ · fpm/
      ARCHIVE/   tools-mumax3-morto/
```
Quatro categorias, separadas de propósito: `MISSIONS/` é **promessa** (pré-registro),
`DECISIONS/` é **autoridade** (writebacks), `RELEASES/` é **o que aconteceu**, `EVIDENCE/` é
**o material**. Só este arquivo é reescrito no lugar.

### Mapeamento de caminhos antigos
`RELEASE-*`, `WRITEBACK-*` e `MISSION-*` **não foram editados** — um documento histórico
mantém os caminhos como foram escritos. Quem seguir uma referência antiga usa esta tabela:

| citado como | está agora em |
|---|---|
| `../c2y9-3cc9.pdf`, `../SupplementalMaterial.pdf` | `SOURCES/paper/` |
| `LAB/admensional_LLG.md` | `SOURCES/theory/admensional_LLG.md` |
| `instruções.md`, `FPM_GUIDED_RESEARCH_STARTER_*` | `SOURCES/fpm/` |
| `tools/…` (mumax3, go) | `ARCHIVE/tools-mumax3-morto/` |
| `LAB/RELEASES/WRITEBACK-*.md` | `LAB/DECISIONS/WRITEBACK-*.md` |
| `LAB/EVIDENCE/…` | inalterado |

## Pergunta/problema atual
Fase 1 (reprodução). Uma re-implementação independente do PRL 086701 relaxa para um par de
skyrmions não-coaxial com l compatível com 10.98 nm no acoplamento fraco, e reproduz a
estrutura da região de estabilidade no plano (A_int, K₀)?

## Área / tema
Skyrmions acoplados em antiferromagnetos sintéticos (SAF); dinâmica micromagnética (LLG),
modos de breathing, autopropulsão de par de skyrmions.

## Artigo de referência — **ACEITO** (WRITEBACK-002, decisão de Rodrigo)
C. C. de Souza Silva, M. V. Correia, J. C. Piña Velásquez,
*Emergent Self-Propulsion of Skyrmionic Matter in Synthetic Antiferromagnets*,
Phys. Rev. Lett. **135**, 086701 (2025). DOI: 10.1103/c2y9-3cc9

- Local: `../SOURCES/paper/c2y9-3cc9.pdf` e `../SOURCES/paper/SupplementalMaterial.pdf`
- Dados originais **não públicos** ("available from the authors upon reasonable request").
  → Isto é **re-implementação independente**, não re-execução. A força da evidência é
  limitada por isso, e o aceite final deve dizer isso explicitamente.

## Ferramenta — **FIXADA por decisão humana**
Código CUDA próprio (`saf.cu`, `saf_dyn.cu`). GPU RTX 4050 Laptop (sm_89), nvcc 11.8, driver
535.261 (CUDA 12.2). Não usamos mumax3: o binário pré-compilado foi feito para CUDA 12.9 e
**não roda** aqui (reverificado 2026-08-25). Ele foi movido para
`../ARCHIVE/tools-mumax3-morto/` — 1,1 GB de material morto, fora do caminho.
**Dependências externas completas em `../ENVIRONMENT.md`**, incluindo a fragilidade do OOMMF.

---

# Situação das missões

## `MISSION-R001` — **`ACCEPTED_WITH_LIMITATIONS`** (WRITEBACK-007)
Autorizada por `WRITEBACK-002`. Gate `G-R001` passou. `human_acceptance: PENDING` —
**passar o gate não é aceite.** Ver `RELEASES/RELEASE-R001.md`.

**Resultado (ainda NÃO aceito):** **l = 10.9607 nm** (malha de 1 nm, a mesma do artigo)
contra **10.98 nm** publicado → **−0.18 %**, dentro da banda pré-registrada [10.43, 11.53].
Ramo não-coaxial, Q₁ = −1.0000, Q₂ = +1.0000, torque 1e-6 T. Escada VL-1..VL-5 passou
inteira. `evidence_strength: BOUNDED`.

**Limite que precisa viajar junto com o número:** a sensibilidade à malha é de 1.0 %
(0.5 nm → 10.8500 nm), **maior que a discrepância de 0.18 %**. O acordo não é mais preciso
que o método. A claim proporcional é "consistente com o valor publicado dentro de 0.2 % num
único ponto de parâmetros", não "o artigo foi reproduzido".

Evidência: `EVIDENCE/R001/` (fonte CUDA, hashes, logs as-run de VL-1..VL-5, séries l(t),
magnetização final). `sha256sum -c` passa; o diretório é provenance selada e não muda.

## `MISSION-R002` — **`ACCEPTED_WITH_LIMITATIONS`** (WRITEBACK-007)
Reprodução **estrutural**: mapear a região de estabilidade no plano (A_int, K₀) e comparar
com a Eq. (S1) do suplementar, `K₀ = 0.65 − 2.5·A_int`. Ataca o limite que nenhuma troca de
solver conserta — a minha *leitura* do artigo.
Ver `RELEASES/RELEASE-R002.md` **e** `RELEASES/RELEASE-R002-ADDENDUM-001.md`.

### Resultado da varredura (165 pontos, 6 colunas de A_int)
- **PRIMÁRIO PASSOU** — ambos os pontos publicados, (0.02, 0.60) e (0.12, 0.35), caem dentro
  da região estável, ambos `NONCOAXIAL`. Este teste podia ter falhado e não falhou.
- **TERCIÁRIO PASSOU** — janelas descem monotonicamente em K₀.
- **SECUNDÁRIO NÃO-DISCRIMINANTE** — declarado morto na checagem de poder, **antes** dos
  dados. Não usado como evidência, apesar de inclinação −2.393 vs −2.5 e intercepto 0.655
  vs 0.65. **Nada no adendo o ressuscita.**
- **Defeito de protocolo registrado:** a regra de poder confundiu largura da janela com
  precisão do centro. Registrado como falha de desenho, **não reparado em aprovação**.
- **Achado estrutural:** o ramo coaxial estreita monotonicamente
  (0.125 → 0.100 → 0.075 → 0.025 → 0) e não é detectado em A_int = 0.12.

### O que o ADENDO-001 mudou (passo 1 de WRITEBACK-004)
1. **Hipótese de bacia REFUTADA.** Inicialização quase-coaxial (0.5 e 2.0 nm) em
   A_int = 0.12: tudo relaxa para não-coaxial. Controles em A_int = 0.02 respondem como
   esperado, inclusive l = 10.9529 nm idêntico à partida de 10 nm. `basin_test.csv`.
2. **A Fig. 5(c) foi extraída numericamente** (render a 500 dpi + limiar de cor,
   `extract_fig5c.py`). A Eq. (S1) é confirmada como a **linha de centro da própria figura**
   (centro medido: −2.499·A_int + 0.6546). O alvo escolhido no desenho do R002 estava certo.
3. **A comparação da fronteira virou quantitativa.** Minha fronteira coaxial↔não-coaxial vs
   a do artigo, em cinco colunas: diferenças ≤ 0.014, **meio passo da minha grade (0.025)**.
   Bordas da banda: viés constante de +0.024 na inferior (o viés esperado por quantização),
   e ≤ um passo na superior. Isto **supera** o limite nº 2 de `RELEASE-R002.md` §9.
4. **Ordem temporal preservada:** meus números foram escritos em `RELEASE-R002.md` **antes**
   da extração da figura. Predição precede medida. Risco residual de viés declarado, não
   negado.

### DISCREPÂNCIA ABERTA — reduzida, não eliminada (versão vigente)
Não é mais "não existe ramo coaxial vs o artigo diz que existe". É: **desacordo de largura
< 0.05 no ponto extremo A_int = 0.12**, onde o artigo prevê coaxial em K₀ ∈ [0.126, 0.144].
Varri 0.128/0.132/0.136/0.140/0.144 com duas inicializações — tudo não-coaxial
(`basin_test_fine.csv`). Nas outras cinco colunas as larguras são **consistentes** quando
lidas como limites.

Agravante que mantém o caso indecidido: nessa região a linha tracejada do artigo está
**extrapolada** — o último traço desenhado está em A_int = 0.1066. Leituras possíveis:
(i) desacordo real do meu modelo naquele canto; (ii) erro da minha extrapolação da figura;
(iii) largura real ainda menor que 0.017. **Não decidido. Não suavizar no aceite.**

## `MISSION-A001` — **SUPERSEDIDA na prática** por `MISSION-A002`
Era a auditoria cruzada desenhada para mumax3, com OOMMF apenas recomendado. O OOMMF estava
instalado; `WRITEBACK-006` autorizou `A002` diretamente. `A001` não foi executada e não
precisa mais ser.

## `MISSION-A002` — **`ACCEPTED_WITH_LIMITATIONS`**, apesar de o gate NÃO ter passado
Auditoria do `saf.cu` contra **OOMMF 2.0b0**. Autorizada por `WRITEBACK-006`.
Ver `RELEASES/RELEASE-A002.md`. Pré-registro (e seu adendo) em `MISSIONS/MISSION-A002.md`.

| | resultado |
|---|---|
| OV-1 (skyrmion único) | **FALHOU** — `Q = −0.9353`, tolerância era 0.05 |
| OV-2 (fator `1/d`) | **PASSOU** — os dois alvos, 4 dígitos |
| OV-3 (par acoplado) | **NÃO-CONCLUSIVO** — mitigação falhou, 2.29 % > 1.0 % |

### O que sobreviveu: OV-2
`sigma = −A_int/2` (o fator 2 previsto em aberto no §2.1 e **medido**, não suposto):
`|ΔE| = 4.000000e−19 J` (alvo 4.0000e−19) e campo de torque `0.086207 T` (alvo idem).
Não depende de fronteira, ansatz nem estimador — por isso sobrevive.
**`SL-2` fecha por um quarto caminho, o único nem meu nem de LLM.**

### PBC é inviável neste OOMMF — dois bloqueios
1. `Oxs_TwoSurfaceExchange` + malha periódica: **bug silencioso**, 1164/10000 células perdem
   o link, energia 11.6 % curta, campo com 3 valores em vez de 1. Determinístico.
2. `Oxs_DMExchange6Ngbr` **recusa** malha periódica (erro explícito). **Fatal.** `Oxs_DMI_C2v`
   aceita PBC mas é simetria errada (C2v, não Cnv). Contornar exige compilar extensão nova.

Sem a escada, o OV-3 teria rodado com 11.6 % do acoplamento faltando e fabricado uma
**discrepância falsa** contra o `saf.cu`.

### Por que OV-1 falhou — não acusa o `saf.cu`
Fronteira livre + DMI ⇒ inclinação de borda severa (`|m⊥| = 0.465` na borda vs `0.088` no
volume). `Q = −1.0000` **exato** na janela central 60×60; todo o déficit vem da borda. E a
borda empurra: o skyrmion migrou de x = 45 para x = 49 nm.

### OV-3 — e o número que NÃO conta
`l(100 nm) = 10.7115 nm`, `l(140 nm) = 10.9566 nm` (janela central), variação **2.29 %**,
e `l` ainda crescendo. O critério pré-registrado exigia ≤ 1.0 %. **Nenhum veredito sobre o
R001 sai daqui**, por duas razões independentes: a taxonomia do §4 já descartava o OV-3 pela
falha do OV-1, e o critério de mitigação falhou por conta própria.
Relaxação incompleta está **descartada**: o OOMMF parou em ~9e−05 A/m = 1.1e−10 T, cerca de
90 000× mais apertado que o critério de 1e−6 T do R001. O `10.9566` fica a 0.03 % do `10.9529` do `saf.cu` — **dado, não
resultado**; usá-lo depois de a mitigação falhar seria post-hoc.

### Ativo colateral
`EVIDENCE/A002/est.py` — estimador (Berg–Lüscher + Eq. 1) portado para Python e **verificado
contra os três valores selados do R001**, erro máximo `0.0001 nm`, antes de tocar dado novo.

### Limite que NÃO caiu
**"Sem solver independente" continua de pé.** O OOMMF verificou um *termo* (OV-2), não o
resultado. Não suavizar no aceite.

# `AUDIT-001` (auditoria externa cega via `codex`) — **`ACCEPTED_WITH_LIMITATIONS`**

**A pendência factual de `-g` está fechada.** Rodrigo (2026-08-24): *"O codex não terminou a
auditoria. Preciso iniciá-la do zero."* A etapa cega que o `WRITEBACK-004` dava como enviada
**não produziu resultado** — provavelmente por falta de `-o/--output-last-message` e/ou
estouro de tempo. Reexecutada do zero sob `WRITEBACK-005`.

**Etapa 1 (cega) — `TERMINAL_AWAITING_HUMAN`.** Ver `RELEASES/RELEASE-AUDIT-001.md`.
`codex-cli 0.149.1`, modelo `gpt-5.6-sol` fixado por `-m`, sandbox `read-only`, `exit=0`.
Diretório isolado com **apenas** o artigo (texto + página 8 a 200 dpi). Sem `saf.cu`, sem
arquivos do laboratório.

**Cegueira VERIFICADA, não declarada:** `-s read-only` restringe escrita, não leitura. O
`trace.jsonl` foi varrido por termos do laboratório → **zero ocorrências**; os dois únicos
comandos do agente foram `sed` e `rg` sobre `paper.txt` no diretório isolado.

## Resultado: 7 expressões comparadas, 7 acordos, 0 divergências
Normalização `−(1/(Ms a² d))∂H/∂m`, troca `2A/(Ms a²)`, anisotropia `2K/Ms`, Zeeman,
DMI `D/(Ms a)`, campo interlayer `−A_int m_j/(Ms d)` e energia interlayer areal `A_int a²`
— todos batem com o kernel do `saf.cu`. **Mas não são 7 testes independentes:** 2 são
discriminantes (`1/d` e sinal do DMI, riscos reais de leitura do artigo) e 5 são
confirmatórios (fixada a normalização areal, os prefatores seguem do micromagnetismo
padrão; pegam um fator perdido, não uma má leitura deste artigo).

- **`SL-2` (fator `1/d`) ganha um terceiro caminho, o primeiro externo e cego.**
- **O ponto cego do DMI foi iluminado e passou.** `pick_chirality` minimiza a energia DMI do
  ansatz e portanto **autocorrigiria** um erro de sinal meu, tornando-o invisível em `l`.
  O auditor derivou às cegas `cos χ = −p·sgn(D)`; isso prevê φ₀ = 0° para a camada 1
  (`p=−1, D=+3.05`). Os logs selados do R001 mostram φ₀ = 0°. **É UM teste, não dois:** a
  camada 2 é algebricamente forçada (com `p₂=−p₁` e `D₂=−D₁`, `cos χ₂ = cos χ₁`), e os logs
  confirmam energias DMI idênticas nas duas camadas.
- **Achado lateral:** a Eq. (A1) do artigo escreve `Beff = −Ms⁻¹ δH/δm`, que só fecha
  dimensionalmente se `δH/δm` for volumétrico, enquanto a Eq. (A3) é areal. Imprecisão de
  notação do artigo, encontrada de forma independente. Reforça `QA-01`/`SL-2`.

## Limites que precisam viajar junto (RELEASE-AUDIT-001 §5)
1. Acordo é evidência mais fraca do que um desacordo teria sido.
2. A cegueira é em relação ao **meu laboratório e ao meu código**, não ao artigo: o auditor
   é um LLM que provavelmente já viu este PRL e certamente viu a literatura de DMI/SAF.
3. Auditor e auditado são LLMs — uma leitura errada **compartilhada** da Eq. (A4) continua
   invisível.
4. Cobre só expressões de campo. **Não** cobre Berg–Lüscher, relaxação, PBC, `bond length`,
   nem número nenhum. Não toca 10.9607 nm.
5. A comparação código×derivação é **minha** e não é cega. Removê-la é exatamente o papel da
   etapa 2 — **não autorizada**.

**Efeito:** o limite "sem leitura independente do artigo" fica **rebaixado, não eliminado**.
Continua sem leitura independente do código e sem solver independente.

## Etapa 2 — **NÃO autorizada**
Enviar o `saf.cu` a terceiro. *"Iniciá-la do zero"* é ordem de reiniciar a auditoria, não de
escalar o que sai da máquina. Precisa de um sim próprio e explícito.

---

# Base física verificada (extração direta do PDF)
- Eq. (A3): `H = ∫dS[E1 d + E2 d + Aint m1·m2]` — integral **areal**. Duas redes 2D, sem eixo z.
- Eq. (A4): E_i tem exchange, anisotropia, Zeeman e DMI interfacial. **Sem termo de demag.**
- Parâmetros: d = 0.4 nm; A = 15 pJ/m; D1 = −D2 = 3.05 mJ/m²; Ms = 0.58 MA/m; grade
  100×100 nm², células 1×1 nm², PBC. Acoplamento fraco: A_int = 0.02 mJ/m², K₀ = 0.6 MJ/m³.
- Eq. (1): l = |R1−R2| com Ri = centro de carga topológica, (1/Qi)∫d²r r ϱi(r).
- Alvo do R001: **l = 10.98 nm** — legenda da Fig. 2(a), equilíbrio com excitação
  **desligada**. **Não usar** 10.39 nm: é um l̄ de regime estacionário **sob excitação**.
  **A atribuição de painel está EM QUESTÃO desde o `E002` (§5.1 do `RELEASE-E002`), não
  corrigida.** A Fig. 2(d) atribui 10.39 nm ao **ABM**; nas minhas corridas `l̄ = 10.3931 nm`
  é o do **SBM** e `10.9824 nm` o do ABM — os dois valores do artigo aparecem **trocados de
  painel**, com quatro dígitos. Duas leituras possíveis (legendas trocadas; ou a de (c)
  repetindo o valor de equilíbrio) e **nenhuma escolhida**. **O alvo do R001 não muda**: vem
  da Fig. 2(a), equilíbrio sem excitação.
- Sanidade: κ = D/Dc = 0.80 < 1 → regime correto para skyrmions metaestáveis.

## Questões fechadas
- **QA-01 (convenção de K₀): FECHADA.** Demag absorvido em K₀ → usar K = 0.6 MJ/m³, sem demag.
- **QA-02 (A_int no mumax3): DISSOLVIDA.** Artefato da ferramenta abandonada.

## Risco SL-2 — FECHADO por evidência
**Fator 1/d no campo interlayer.** `Beff_int,i = −A_int·mj/(Ms·d)`. Confirmado por **quatro**
caminhos: FD termo-a-termo (VL-1), valor fechado 0.086207 T (VL-2), derivação cega externa
(`AUDIT-001`) e **OOMMF** (`A002` OV-2, 4 dígitos) — o último é o único nem meu nem de LLM.

## Desvios de protocolo registrados
- `SL-7` (R001): estimador de carga topológica trocado (diferenças finitas → Berg-Lüscher)
  **durante** VL-3. Justificado por integralidade de Q, critério independente do alvo.
- `SL-B1` (R002): a região mapeada é a alcançável a partir da inicialização declarada no
  artigo. **Parcialmente fechado** pelo teste de bacia do ADENDO-001.
- Regra de poder mal especificada do R002 (§2 do release), não reparada em aprovação.

---

# Decisões humanas até agora
1. Montar o laboratório mínimo (prompt de inicialização v1.0).
2. `WRITEBACK-002` (2026-08-21): alvo ratificado; escopo = reprodução mais barata;
   ferramenta = código CUDA próprio; R001 autorizada.
3. `WRITEBACK-003` (2026-08-21): *"Aceito sua recomendação"* → `MISSION-R002` autorizada.
   Auditoria externa e instalação de solver explicitamente **não** autorizadas ali.
4. `WRITEBACK-004` (2026-08-21): *"Execute a sequência recomendada"* → passo 1 (teste de
   bacia) executado; passo 2 (codex) tratado como autorizado por interpretação, agora
   **em dúvida factual**; passo 3 (aceite) recusado por mim, porque aceite é ato humano.
5. `WRITEBACK-005` (2026-08-24): *"O codex não terminou a auditoria. Preciso iniciá-la do
   zero."* → etapa 1 (cega) de `AUDIT-001` autorizada e executada. Etapa 2 segue **não**
   autorizada.
6. `WRITEBACK-006` (2026-08-24): *"o OOMMF está instalado... Podemos usá-lo para executar os
   testes"* → `MISSION-A002` autorizada e executada. Leitura registrada como autorização;
   risco baixo porque rodar solver local não é ação externa.

## Histórico / supersessões
- `WRITEBACK-001` está `SUPERSEDED_FOR_CURRENT_STATE` por `WRITEBACK-002`. Preservado, não
  editado. Registrava escolha de ferramenta sem autoridade humana e deltas inexistentes.
  Sua parte válida (fechamento de QA-01) sobrevive por mérito próprio, reconfirmada do PDF.
- `RELEASE-R002.md` §4 e §9-limite-2 estão **corrigidos** por `RELEASE-R002-ADDENDUM-001.md`.
  Os textos originais permanecem como foram escritos.

---

# Fase 2 — executada em 2026-08-24, aguardando aceite

## `AUDIT-002` — estimador cego · **`ACCEPTED_WITH_LIMITATIONS`** (WRITEBACK-009)
O auditor externo escreveu, **sem ver o meu código nem os meus números**, um estimador
independente de `Q` e `l` a partir da Eq. (1); **eu rodei aqui** sobre a evidência selada.

| arquivo selado | alvo (`saf.cu`) | estimador cego | dif |
|---|---|---|---|
| `mfinal_weak.dat` | 10.9529 nm | **10.9530** | +0.0001 nm |
| `mfinal_weak_tight.dat` | 10.9607 nm | **10.9608** | +0.0001 nm |
| `mfinal_mesh05.dat` | 10.8500 nm | **10.8500** | +0.0000 nm |

`Q = ∓1` exato nos três. Faz **quatro escolhas de convenção diferentes das minhas** (arredonda
`Q` ao inteiro, enrola baricentros, imagem mínima, indexação x-major) e converge mesmo assim.

**Fecha `L3.4` na camada do estimador.** **NÃO fecha `L-G`:** o estimador mede o *meu* estado
final — valida a régua, não a relaxação que produziu o estado.

## `MISSION-E001` — dinâmica LLG e breathing · **`ACCEPTED_WITH_LIMITATIONS`** (WRITEBACK-009) · gate passou
Primeira missão da Fase 2. O `saf.cu` não tinha `γ` nem precessão; agora tem LLG com RK4.

| critério | resultado |
|---|---|
| EV-1 conservação (α=0, sem renorm) | **PASSOU** — deriva `1.06e−09`, `max‖m‖−1 = 3.36e−11` |
| EV-2 Larmor | **PASSOU** — `2.802494` vs `2.802494 GHz`, **+0.00000 %** |
| EV-3 primário (escala) | **PASSOU** — SBM `18.00 GHz` em `[14.4, 21.6]` |
| EV-3 secundário (ordem) | **PASSOU** — `f_ABM 19.40 > f_SBM 18.00` |
| EV-3 terciário | **não medido** (era exploratório) |

Frequências: **SBM 18.00 GHz** (publicado 18) e **ABM 19.40 GHz** (publicado 19.24, **+0.83 %**).
Identidade dos modos **medida, não rotulada**: `corr(δm_z0,δm_z1) = −1.0000` sob `ΔK` (em fase
= SBM) e `+0.9999` sob `B_z` (antifase = ABM).

**Não autoriza dizer** que os modos foram reproduzidos: a banda de ±20 % foi declarada antes
como teste de **escala**, e não separa 18 de 19.24. O acordo defensável é "ambos em ~18–19.5
GHz, na ordem certa".

### Defeitos — ambos CORRIGIDOS NA CAUSA (ver `RELEASE-E001-ADDENDUM-001.md`)
1. **Colisão de `argv`**: `ev3 <modo> <ns>` colidia com o `a_nm` do `main` e reduziu a grade a
   10×10 na primeira corrida. Pego na hora (`⟨m_z⟩_eq = ±1.000000000`). A correção do release
   cobria **só o `ev3`**; agora blinda o prefixo `ev*` inteiro.
2. **Provenance**: rodar `saf_dyn pair` reescrevia arquivos de `EVIDENCE/R001/`, que nunca
   tinham sido hasheados. Dano verificado **nulo** (saída do `estimator.py` de antes bate em
   17 dígitos com a de depois). Hashear dava **detecção**, não prevenção; a **causa** foi
   corrigida — os caminhos de escrita do `saf_dyn.cu` apontam para `E001`, e restam **zero**
   referências a `R001`. EV-3 refeito com o binário corrigido: **bit-idêntico**.

## Dívida do `1/(1+α²)` — **FECHADA**
Estava registrada como caminho não testado (com `α=0` o denominador vale 1). O `EV-2` foi
estendido para `α` arbitrário: na precessão amortecida `f = γB/(2π(1+α²))`, então ela mede o
denominador. `α = 0 / 0.02 / 0.30` → razão medida `1.00000000 / 0.99960016 / 0.91743119`
contra `1/(1+α²)` idêntico, desvio `≤ 3e−15`. `α=0.30` é efeito de 9 %, teste forte.

**Correção de raciocínio registrada:** eu havia escrito que omitir o fator faria o erro
**acumular** no `E002`. **Errado.** Na forma adimensional
`dS/dτ = −1/(1+α²)[S×H + α S×(S×H)]`, `t = t₀τ`, `t₀ = M_s a₀²/(2A_ex γ)`, o fator multiplica
o colchete **inteiro** — omiti-lo é exatamente `τ' = τ/(1+α²)`. Num sistema autônomo é pura
reetiquetagem do tempo: trajetória idêntica, taxas erradas por `0.04 %` **constante**,
independente da duração. Só num sistema **forçado** vira efeito real, como dessintonia de
`0.04 %` = **1/50** da largura de linha `α·f ≈ 2 %`. Desprezível, e não acumulativo.

Conferência de unidades: `t₀ = 0.1098 ps = 1/(γB₀)` com `B₀ = 2A_ex/(M_s a₀²) = 51.72 T`, que
é exatamente o prefator de troca do meu kernel. Passo RK4 de 10 fs = `0.091 t₀`.

## Forma adimensional — implementada e verificada (`ADENDO-002`)
A forma `dS/dτ = −1/(1+α²)[S×H + α S×(S×H)]`, `t = t₀τ`, `t₀ = M_s a₀²/(2A_ex γ)`, foi
**implementada no mesmo binário** (modo `ndcheck`) e comparada com a rota física em 20 000
passos RK4. Energias **idênticas em 16 dígitos** para `α = 0 / 0.02 / 0.30`; desvio de
configuração `~5e−14`, puro arredondamento. `γB₀t₀ = 1` exato.
A rota adimensional fica pronta para o `E002`, onde é melhor condicionada para ~3 µs.

### Unidade de energia (`ADENDO-003`) — cuidado com `d` vs `a₀`
Conjunto completo: `B₀ = 2A_ex/(M_s a₀²) = 51.724 T`, `t₀ = 1/(γB₀) = 0.1098 ps`,
`μ = M_s a₀² d`, e **`J_ex = μB₀ = 2 A_ex d = 1.20e−20 J`**.
A forma `J_ex = 2 a₀ A_ex = 3.00e−20 J` é a de **célula cúbica** e vale só se `d = a₀`;
aqui `a₀/d = 2.5`. Confirmado por dois caminhos: `μB₀`, e o coeficiente por ligação da troca
discreta `H_ex = 2A_ex d Σ(1−mᵢ·mⱼ)`.
**Assimetria a lembrar:** `t₀` e `B₀` **não** dependem de `d` (ele cancela contra `μ`), mas a
energia **depende**. Mesmo `d`-vs-`a₀` do risco `SL-2`. Não afeta resultado nenhum — o código
é SI puro — mas adimensionalizar energia com `2a₀A_ex` erraria por 2.5×.

### Reconciliação com `LAB/admensional_LLG.md` (`ADENDO-004`)
Fonte fornecida por Rodrigo. Confirma `ω₀ = γJ_cel/m_i = γB₀` (idêntico ao meu `t₀`) e traz a
identidade geral `J_cel = m_i B₀` — a mesma que usei. A diferença é só `m_i`: o documento usa
célula **cúbica** (`v_cel = a³`, logo `2aA`); este modelo é filme areal (`m_i = M_s a² d`, logo
`2Ad`). **Não há discordância** — é a mesma fórmula noutra geometria de célula.

**Verificação NOVA: comprimentos característicos** (`ADENDO-004` + **corrigido** no `-005`).
Três comprimentos, não um: troca magnetostático `√(2A/μ₀M_s²) = 8.424 nm`, DMI
`4A/(πD) = 6.262 nm`, parede `Δ = √(A/K) = 5.000 nm`. **Quem manda é o menor, `Δ`** — o
`ADENDO-004` usou só o de troca e anunciou folga de ~8×; a folga real é **5×**
(5 células por `Δ` na malha de 1 nm; 15.7 por parede completa). Todos satisfeitos, margem
aceitável e não confortável. Conferência: em `D=D_c` vale `l_D = Δ = 5.000 nm` exato,
confirmando `D_c = 4√(AK)/π` e `κ = 0.7985`.

**Isto dá causa física a `L1.1`:** a sensibilidade de malha de 1.0 % é o que se espera de uma
célula que resolve `Δ` apenas 5×. Extrapolações de Richardson a partir dos dois pontos
existentes apontam `l(a→0) ≈ 10.74–10.81 nm`, **afastando-se** do 10.98 publicado — mas isso é
**EXPLORATÓRIO** (sem critério pré-registrado, dois pontos não fixam a ordem) e **não altera
`C-1`**, porque o artigo também usa malha de 1 nm: a comparação do R001 é casada em malha, e o
contínuo é outra pergunta. Fecha, isso sim, qualquer leitura de `C-1` como afirmação sobre o
contínuo.

**Escopo do documento vs este modelo:** ele traz dipolar explícito (peso 0.00112) — que aqui
**não se usa**, por `QA-01` (demag absorvido em `K₀`); usá-lo seria dupla contagem. E traz STT
(`v_j`, `ξ`), ausente da Eq. (A1). Não traz DMI, anisotropia nem acoplamento interlayer. É o
esqueleto da adimensionalização, não o modelo completo.

---

## `MISSION-E002` — autopropulsão (Fig. 2, T = 0) · **`ACCEPTED_WITH_LIMITATIONS`** (WRITEBACK-011) · **gate NÃO passou**
Autorizada por `WRITEBACK-010` (*"Executemos E002"*). Escopo recortado ali: **Fig. 2 apenas**;
Fig. 3 e Fig. 4 ficaram de fora, nomeadas `E003`/`E004`, não propostas.
Ver `RELEASES/RELEASE-E002.md` **e o `-ADDENDUM-001`**. Evidência em `EVIDENCE/E002/` (23 arquivos selados).

### O que apareceu
**A autopropulsão apareceu, na direção certa e com a magnitude certa nos dois modos.**

| | meu `v_⊥` | alvo (extração da Fig. 2, feita ANTES de rodar) |
|---|---|---|
| SBM, `ΔK/K₀=0.005`, 18.00 GHz | **3.5400 cm/s** | 3.50 cm/s (1 px = 0.11) |
| ABM, `B₀=4 mT`, 19.24 GHz | **2.0322 cm/s** | 2.03 cm/s (1 px = 0.011) |

Também: pico de `l(t)` em `f_drive` sob SBM (`EP-4` passou; fecha o terciário `L6.3` do
`E001` **nesse ramo**). O ramo ABM mostra `2f_drive` no dado, mas está **`NÃO MEDIDA`** por
pré-registro — a condicional do `EP-4` foi disparada pela falha do `PV-1`, e não se converte
isso em resultado. Amplitudes de respiração 2.09 pm (SBM) e 0.13 pm (ABM), contra ≈2 e
≈0.1 pm da figura.

### O que falhou — e o gate
`G-E002 = PV-0 ∧ PV-1(SBM) ∧ PV-2 ∧ EP-1 ∧ EP-2(SBM)` → **NÃO PASSOU**.
- **`PV-0`** (𝒟 no equilíbrio) falhou: `19.4306e−15` contra `[13.5, 16.5]e−15`. **Não é
  unidade nem bug** — o estimador foi verificado contra a energia de troca validada por FD
  (razão 1.0177, só estêncil). Sobra ambiguidade sobre o eixo da Fig. 2(c), que omite o
  expoente; **provadamente não-propagante** (em `G/(α𝒟)` o prefator cancela).
- **`PV-1`** (piso de ruído) falhou nos dois ramos: `pp(l) = 0.868 pm`. **As Figs. 2(c)/(d)
  ficam declaradas mortas antes do dado** e não são relatadas.
- **`EP-3`** (dessintonia) falhou: `v(19.40) < v(19.24)`, ao contrário do previsto — **por
  0,77 %**. `v_sp` é plana a <1 % nesse intervalo, logo **não localiza a ressonância** e não
  sustenta `19.40` como pico. O `19.40` do `C-6` é um **bin** (centroide do espectro selado do
  `E001`: 19.348 GHz, FWHM 0.60).

### Duas coisas que precisam viajar junto
1. **`EP-1` passou por simetria, não por dinâmica.** `v_∥ = 0` **exato** é forçado pela
   simetria de troca-de-camadas da minha condição inicial. **O critério não podia falhar.**
   A afirmação do artigo — perpendicular *seja qual for* a orientação — **não foi testada**.
2. **Quatro dos meus critérios estavam mal desenhados** (`PV-0`, `PV-1`, a condicional do
   `EP-4`, a checagem de poder de `EP-2`/`EP-3`), sempre do mesmo jeito: limiar absoluto
   contra referência que não o sustentava. Registrados, **não reparados**.

### Três divergências ABERTAS — o aceite as declara, não as fecha (`L7.10`)
Detalhadas em **`LAB/QUERIES-AUTORES-001.md`**, com a pergunta exata e o dado mínimo que
resolveria cada uma:
- **`D-1`** o eixo 𝒟 da Fig. 2(c)/(d) não traz expoente; ou a forma do meu skyrmion difere em
  29,5 %, ou o rótulo omite um fator. Discriminante disponível: a amplitude **relativa** do
  ciclo, invariante ao prefator — eu meço **±3,78 %** contra **±4,0 %** da figura, o que pesa
  para o rótulo sem fechar.
- **`D-2`** os dois `l̄` aparecem trocados de painel (abaixo).
- **`D-3`** a forma do transiente da Fig. 2(a). Hipótese de "média corrida" **testada e
  rejeitada** (daria 12,2 cm/s aos 135 ns; a figura dá 3,5, e a minha taxa instantânea, 3,69).
  `v_⊥` e `l̄` decaem com **a mesma razão geométrica** (0,358 por janela de 25 ns): `D-2` e
  `D-3` são provavelmente **uma pergunta, não duas**.

### Achado exploratório: os dois `l̄` do artigo, trocados de painel
Meu SBM dá `l̄ = 10.3936 nm` (o valor que a Fig. 2d dá ao ABM); meu ABM dá `10.9824 nm` (o que
a Fig. 2c dá ao SBM). Quatro dígitos, cruzados — enquanto velocidade, simetria de excitação e
harmônico batem no painel certo. Ver correção na §Base física acima. **Não afeta `C-1`.**

### Limite acrescentado pelo `RELEASE-E002-ADDENDUM-001`
**A corrida SBM de 200 ns não atingiu o estacionário em `v_⊥`** — ainda decaía `0.042 cm/s`
por janela de 25 ns ao terminar. O `3.5400` pré-registrado é uma **travessia**, não um platô;
a extrapolação geométrica dá `3.498 cm/s` e é **exploratória**, não substitui o número. O
`EP-2` não muda (ambos dentro de `[2.45, 4.55]`). O artigo põe os *insets* em t ≈ 679 ns:
**eles rodaram muito mais longe que eu.** Já o `l̄` **está** convergido (resíduo 3e−4 nm),
e é isso que sustenta o achado dos painéis trocados.

### `L-G` intocado
O `E002` roda no meu código, do meu equilíbrio, com a minha régua. Acrescenta um observável,
**não** um verificador independente.

## `MISSION-E003` — a deriva segue a LIGAÇÃO, não a REDE · **gate passou** · aguardando aceite
Autorizada por `WRITEBACK-012`. Ver `RELEASES/RELEASE-E003.md` **e o `-ADDENDUM-001`, que
corrige a razão pela qual o gate passa**. Evidência em `EVIDENCE/E003/`
(12 arquivos selados). Custo: 48 min.

### Por que existiu
O `E002` deixou um **confundimento** no `C-7`: com a ligação em `x` e a deriva em `y`,
"perpendicular à ligação" e "ao longo de um eixo da malha" **preveem o mesmo resultado**. O
`L7.2` subestimava isso ao chamar de "teste fraco".

### Resultado — decisivo
Girando a ligação para `25.86°` e `18.09°`, a deriva foi para `123.57°` e `115.65°`:

| | previsão | medido |
|---|---|---|
| `H_ligação` | `dφ/dθ = +1` | **`+1.0201`** |
| `H_rede` | `dφ/dθ = 0` | — |

**O `L7.2` fecha.** O que fica testado é "a deriva acompanha a ligação em **dois** ângulos
além de zero", no modo **SBM** — não "em qualquer ângulo", como o artigo afirma.

**Por que o gate passa (`ADDENDUM-001`):** porque a grandeza discriminante **converge** —
`dφ/dθ` fica em `1.0073 / 1.0201 / 1.0258` em três janelas, variação `0.019` contra
separação `1.0` entre as hipóteses. **Não** porque a ambiguidade do §4.3 do pré-registro
deixasse espaço: o release original apoiou o gate na leitura favorável dessa ambiguidade,
o que é escolher a leitura depois do dado, e o adendo corrige isso. O que **não** converge é
o *offset*, por causa medida.

### Achado: artefato de comensurabilidade, novo
**Fora do eixo a relaxação NÃO converge** (2×10⁶ iterações, torque parado em `1.26e−5 T`
contra `1e−6` a `θ=0`), e o controle sem excitação mostra deriva espúria **constante** de
`0.917 cm/s` **ao longo da ligação** — ~23× a de `θ=0`, e **não decai**. Isso selecionou
`M-rede` pela regra registrada: a proteção que dá `v_∥ = 0` exato a `θ=0` **depende de a malha
ter um espelho ali**.

Essa contaminação prevê o desvio de perpendicularidade observado (`+7.7°`) por
`atan(v_espúria/|v|)` com razão **0.90 nas quatro medidas** (2 ângulos × 2 janelas) — usando
só números do controle, medidos **antes**. **Sobram ~10 % (0.8°) sem explicação**, registrados.
O teste de inclinação é **imune** a tudo isso.

**Não contamina o `E002`:** a `θ=0` (comensurável) a deriva espúria decai a `7.1e−5 cm/s` na
janela de ajuste, 0,002 % do sinal.

### `L-G` intocado
Removeu um confundimento **interno** do meu código. Não é verificação independente de nada.

## `MISSION-I001` — a deriva espúria é REAL, não é a régua · **gate passou** · aguardando aceite
Autorizada por `WRITEBACK-013`. Ver `RELEASES/RELEASE-I001.md`. Prefixo novo `I` = instrumento:
caracteriza **o meu próprio medidor** — não é reprodução, extensão nem auditoria externa.

**Veredito `C-real`.** Com a magnetização **congelada**, 10 001 chamadas ao rastreador dão
deriva de `2e−11 cm/s` e deslocamento acumulado de `0.0000 pm` — **onze ordens de grandeza**
abaixo dos `0.917 cm/s` medidos ao vivo. Na corrida viva, **três** localizadores concordam:
`(a)` realimentado, `(b)` origem fixa, `(c)` centroide do núcleo — este **sem carga topológica
nenhuma** — todos em `0.91745 cm/s` a `−153.875°`.

**A concordância exata é diagnóstica, não suspeita:** sob translação rígida
`m(r,t) = m₀(r−vt)`, todo funcional do tipo centroide dá a mesma velocidade **por identidade**.
O movimento é, portanto, **translação rígida**.

**Fecha** a ressalva 1 do `E003`: o artefato é **de rede, não de régua**. O controle a `θ = 0`
exonera o rastreador também na condição em que o `E002` rodou.
**Não fecha:** a causa física, o `L5.3`, e `L-G` — instrumento próprio testado contra si mesmo
em outra condição **não é** verificação independente.

## `MISSION-E004` — `v_sp(f)` tem pico na ressonância do modo? · **EM EXECUÇÃO**
Autorizada por `WRITEBACK-013`; execução não supervisionada por `WRITEBACK-014`.
Pré-registro em `MISSIONS/MISSION-E004.md` — **o `ADENDO-001` dele é obrigatório**: corrige
dois defeitos detectados **antes** do lote.
- O piso do `EF-0` era **circular** — vinha de um número medido com o rastreador que o `I001`
  estava testando naquele momento. Virou critério **relativo**: contraste vs dispersão entre
  janelas, calculado do próprio dado.
- O `EF-1` podia "passar" com um ajuste incapaz de distinguir 18,00 de 18,5. Agora exige
  `σ(f_pico) < 0.25 GHz` para ter veredito.

Testa *"vsp peaks at the resonance frequency of the corresponding breathing mode"* contra os
**18.00 GHz** que o `E001` mediu de forma independente da autopropulsão. Nove pontos de 16,5 a
19,5 GHz, `θ = 0°` (o ângulo limpo — fora do eixo há o artefato do `E003`).
**Pode falhar:** o `EP-3` do `E002` já achou autopropulsão plana a 0,77 % sob dessintonia.

## `MISSION-E004R` — **`ACCEPTED_WITH_LIMITATIONS`** (WB-018) · gate NÃO passou
Ver `RELEASES/RELEASE-E004R.md`.
**Fechou o `L5.3`:** par no centro `l = 10.960705784 nm`, par **na fronteira periódica**
`10.960705637` — `|Δl| = 1.5e−7 nm`, `Q` exato. A régua não tem buraco na travessia.
**Refinou o `C-6`:** `f_SBM = 17.9609 ± 0.0125 GHz` (janela de 40 ns). O `18.00` do `E001` era
um **bin** de resolução 0.1 GHz.
**Falhou no `RF-1`,** porque o `RF-0` checou a convergência da **entrada** (`v_⊥`) e não da
**saída** (`f_pico`) — o erro que virou a regra `R2` do §6.1. Exploratório e **não é veredito**:
`f_pico` converge a 6 MHz entre janelas e daria `17.8255` contra `f_SBM = 17.9609`.
**A afirmação do artigo sobre `v_sp` ter pico na ressonância segue NÃO TESTADA**, por duas
missões seguidas.

## `MISSION-I002` — a premissa caiu · **`ACCEPTED_WITH_LIMITATIONS`** (WB-018) · gate NÃO passou
Ver `RELEASES/RELEASE-I002.md`. Perguntava se os 11 % do `L8.4` vinham do **estado** ou da
**excitação**, variando `K₀` para mover `l`.

**`v_∥` não é função de `l`:** `K₀ = 0.65` e `0.70` dão o **mesmo** `l` (`11.5934` e `11.5875`)
e `v_∥` de `0.730` contra `0.432` — **41 % de diferença**. Os dois estados diferem `3.2 %` em
tamanho (`𝒟`). **A deriva de rede é hipersensível ao estado**, ~13× em amplificação.

**Este fracasso não é da família dos nove:** o critério estava bem-formado sob `R1`–`R3`, e
caiu porque a **premissa física** era falsa. É o tipo certo de fracasso.
**Predição minha errada, registrada:** eu previa `K₀` maior ⇒ `l` menor; `l` **sobe**
(`6.49 → 10.95 → 11.59`).

## `MISSION-I003` — era o passo de tempo · **`ACCEPTED_WITH_LIMITATIONS`** (WB-019) · gate passou
Primeiro pré-registro **revisado por Rodrigo antes da execução**, sob a regra nova.
**`H_dt` confirmado:** com `dt = 2.5 fs` (escalado por `a²`), `l = 10.8483 nm` **constante em
quatro casas** ao longo de 4 ns; com `10 fs`, o par se desliga (`10.85 → 12.39`). O `RF-4`
inválido do `E004R` foi **erro meu de passo de tempo, não física** — e o desfecho ruim
(`H_física`, que tocaria o `L1.1`) está descartado.

**Armadilha promovida ao `CLAUDE.md` §8:** `dt` tem de escalar com `a²`. Refinar malha em LLG
sem isso **produz física falsa que parece física**.

**Exploratório, não pré-registrado:** a deriva espúria cai `4.5×` ao refinar (`0.917 → 0.203`).
Era a predição do `RF-4`, mas dois pontos não fazem lei de escala. **`RF-4` e `L9.1` seguem
abertos.**

**Honestidade sobre o que vale:** conserta um erro **meu**. É higiene do registro, não avanço
sobre o artigo nem sobre o `L-G`.

## `MISSION-E005` — o amolecimento de amplitude reproduz · **`ACCEPTED_WITH_LIMITATIONS`** (WB-021)
Autorizada por `WRITEBACK-020`. Ver `RELEASES/RELEASE-E005.md`. Evidência: `EVIDENCE/E005/`
(23 arquivos selados). Figura: `LAB/FIGURES/F7_amolecimento_amplitude.png`. Custo: 13 h.

### Por que existiu — e o erro que a tornou necessária
Eu projetei o `E004` e o `E004R` para perguntar "o pico de `v_sp` coincide com a ressonância do
modo?" **sem ter lido o suplementar inteiro**. A **`Fig. S4(c)`** responde exatamente isso, no
nosso ponto de operação exato. Custou duas missões e ~8 h. **Não é defeito de critério** (a
família dos nove do `CLAUDE.md` §6.1): é **não ter varrido a fonte antes de desenhar**.

### `RA-1` PASSOU — o pico desce quando a amplitude sobe
Alvo extraído da `Fig. S4(c)` e **selado antes das corridas** (`RA-3`).

| `ΔK/K₀` | nosso `f_pico` | artigo |
|---|---|---|
| 0.002 | `17.9664 ± 0.0061` | `17.9176` |
| 0.005 | `17.8255 ± 0.0108` | *(interp. ~17.68)* |
| 0.008 | `17.5796 ± 0.0336` | `17.4649` |

Inclinação **`−64.470`** contra **`−74.807 GHz`/unidade** do artigo: razão **`0.862`**,
negativa e dentro da banda de fator 3. `H_fixo` previa ~0.

**Isto resolve a "discrepância" do `E004R`:** os `17.83` medidos lá a `ΔK/K₀ = 0.005` não eram
desacordo com `f_SBM = 17.96` — eram **amolecimento de amplitude**, e agora está estabelecido
por critério pré-registrado. **A afirmação do artigo sobreviveu a um teste que podia refutá-la.**

**`RA-0`** passou nas três: `f_pico` converge a 0.9–31 MHz enquanto `v_⊥` se move 0.9–2.8 %.
A **saída** converge quando as entradas não — a lição do `E003`, aplicada certo desta vez.

### Duas coisas que NÃO podem ser promovidas
- **`RA-2` é EXPLORATÓRIO**, e assim foi declarado antes. Ele observa que na menor amplitude
  `f_pico = 17.9664` e `f_SBM = 17.9609` coincidem a **`0.40 σ`**. Isso **não** é "a afirmação
  do artigo foi testada no limite linear". Quem fez o trabalho foi o `RA-1`.
- **Ressalva aberta:** os nossos picos ficam `+0.049` a `+0.115 GHz` **acima** dos do artigo, e
  o desvio cresce com a amplitude — o nosso amolecimento é **~14 % mais fraco**. Medido,
  registrado, **não explicado**. O `RA-1` era teste de sinal e escala, não de valor.

### `L-G` intocado
Décima quarta missão. O alvo é uma **figura**, não dados dos autores. Mesmo código, mesmo
equilíbrio, mesma régua.

## `MISSION-A003` — o segundo solver · **`ACCEPTED_WITH_LIMITATIONS`** (WB-023, `C-15`)
Autorizada por `WRITEBACK-022`. Ver `RELEASES/RELEASE-A003.md`. Evidência: `EVIDENCE/A003/`
(13 arquivos selados). Custo: **< 25 min**.

### A escada — e ela era obrigatória
| | medido | |
|---|---|---|
| `MV-0.1` demag OFF | `E_demag = 0`, `E_total` independente de `Msat` | PASSOU |
| `MV-0.3` `Ku1` | `−4.8000004e−18` vs `−Ku1·V = −4.8e−18` | PASSOU |
| `MV-0.4` **`QA-02`** | `A_inter = −A_int·Δz/2 = −4e−15 J/m` ⇒ `ΔE = 4.0000e−19 J` | PASSOU |
| `MV-0.2` **sinal do DMI** | quiralidade radial p/ FORA; a espelhada **colapsa** | PASSOU |
| `MV-1` skyrmion isolado | raio `7.3889` (mumax3) vs `7.3903 nm` (saf.cu) = **`−0.019 %`** | PASSOU |
| `MV-2` **o par** | `10.9279` vs `10.9607 nm` = **`−0.30 %`** | PASSOU |

### Dois fechamentos que valem por si
- **`QA-02` fechada** com `ΔE = 4.000000e−19 J` — **exatamente** o alvo do `OV-2` do `A002`,
  verificado contra o OOMMF. **Três ferramentas concordam no termo interlayer.**
- **O sinal do DMI, o risco discriminante do `AUDIT-001`, está verificado.** O meu
  `pick_chirality` autocorrigiria um erro meu e o tornaria invisível em `l`; o mumax3 escolhe
  sozinho e escolhe o mesmo. E medi no estado selado que **as duas camadas** são radiais para
  fora — a nota algébrica do `AUDIT-001` deixou de ser só álgebra.

### A checagem que evitou uma discrepância FALSA
O **`relax()` do mumax3 não converge este sistema**: dava `l = 10.3414 nm` (`−5.65 %`).
Após `minimize()`: `10.9276`, e `10.9279` numa segunda chamada. Sem o controle eu teria
relatado uma discrepância inexistente — mesma classe do bug de PBC do OOMMF no `A002`.
Armadilha promovida ao `CLAUDE.md` §8.

### O limite que sobra
A **inicialização** (separação de 10 nm, quiralidades) é a mesma nos dois códigos: **não** é
independente. Só o **solver** e a **régua** são.

# Glossário mínimo — termos que eu usei sem definir

**Freeze.** Preservar um estado aceito como **referência** do laboratório. Da spec:
*"Freeze significa preservar este estado aceito como referência; não significa declarar
verdade eterna — evidência futura ainda pode superseder o estado."* É **ortogonal** ao aceite
(`FPM_CORE_SPEC` §7: *"Freeze is orthogonal"*, *"No field implies another"*) e **não** autoriza
divulgar, submeter ou publicar. Congelar torna a supersessão **explícita e cara**: contradizer
um claim congelado exige writeback que nomeie o que está sendo superado.

**Estado atual: NÃO CONGELADO**, e recomendo manter assim até `L-G` fechar.
**Lacuna registrada:** este laboratório nunca adotou o bloco `mission_state` em YAML que a
spec recomenda; `freeze_status` aqui é prosa, não campo conferível. Adotá-lo é pré-requisito
para freeze significar algo.

**Selagem de material ≠ freeze.** São campos distintos na spec (`material_status` vs
`freeze_status`). O material **já está selado**: `SHA256SUMS.txt` em cada diretório de
evidência. É isso que protege o registro; freeze protege a interpretação.

---

# Próxima decisão humana necessária
1. **Nenhuma decisão de aceite pendente.** Quinze missões, todas aceitas com limitações.
2. **A decisão que importa: a direção.** Doze missões, `L-G` intocado. Atacar por dentro
   (**ação de sistema**: OOMMF com DMI Cnv + PBC), por fora (**ação externa**: etapa 2 do
   `AUDIT-001`), continuar estendendo, ou parar e consolidar. **Recomendo a primeira.**
3. **Levar o `QUERIES-AUTORES-001.md` aos autores** — ação de Rodrigo, parada desde 25/08.
**Nenhuma missão pendente.** Não há mais nada de rotina na mesa — resta a direção.

## Direções em aberto (nenhuma proposta, nenhuma autorizada)
- **`E005` — LLG estocástica (Fig. 4).** `T = 1–7 K`, trajetórias de 3,116 µs. Capacidade
  nova + ~8,7 h de GPU por trajetória. **Não proposta.**
- **A CAUSA FÍSICA do artefato de comensurabilidade** segue conjectural. O `I001` mostrou que
  o movimento é **real e rígido**; que seja força tipo Peierls virando deriva giroscópica é
  hipótese **não testada**. **Não proposta.**
- **`L5.3`** — a régua sob travessia da fronteira periódica segue **não testada**; o `I001`
  não a tocou. **Não proposta.**
- **Atacar `L-G`** — verificação independente do *resultado*. Exige DMI Cnv com PBC no OOMMF
  (**ação de sistema**: compilar) ou missão de convergência em caixa.
- **Fechar `L2.3`** — discrepância aberta em `A_int = 0.12`.
- **Etapa 2 do `AUDIT-001`** — enviar o `saf.cu` ao auditor externo (**ação externa**).
