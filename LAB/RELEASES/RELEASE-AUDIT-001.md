# RELEASE-AUDIT-001 — as-run da auditoria externa cega (etapa 1)

Data: 2026-08-24 · Autoridade: `WRITEBACK-005`
Estado: **`TERMINAL_AWAITING_HUMAN`** · `human_acceptance: PENDING`
Regime: `AUDIT` (não é missão de produção de resultado; é checagem de leitura)

> Auditoria de derivação não é validação numérica. Nada aqui diz que 10.9607 nm está certo.

---

## 1. Desenho e execução
Detalhes as-run completos em `EVIDENCE/AUDIT-001/RUN-001.txt`. Resumo:

- Ferramenta `codex-cli 0.149.1`, modelo **`gpt-5.6-sol`** fixado por `-m` (não herdado
  do `config.toml`, para o registro ser reproduzível). Sandbox `read-only`, `exit=0`.
- Diretório de trabalho isolado contendo **apenas** `paper.txt` (artigo inteiro, sem
  suplementar) e `endmatter_p8-8.png` (página 8 a 200 dpi, Eqs. A1–A4). Sem `saf.cu`,
  sem `MISSION-*`, `RELEASE-*`, `STATE.md`.
- Tarefa: derivar do zero a energia discreta e os campos efetivos termo a termo, com
  checagem dimensional; discriminantes pedidos (a) papel de `d` no campo interlayer e
  (b) convenção de sinal do DMI e quiralidade favorecida por camada.

## 2. Cegueira — **propriedade verificada, não declarada**
`-s read-only` restringe escrita, **não leitura**: o agente podia ter caminhado até
`/home/rodrigo/pesquisa/SAF`. O `trace.jsonl` foi varrido por
`pesquisa/SAF | saf.cu | /LAB | MISSION- | RELEASE- | WRITEBACK | STATE.md | EVIDENCE |
10.9607 | 10.9529 | mumax | OOMMF` → **zero ocorrências**. Os dois únicos comandos que o
agente executou foram um `sed` e um `rg` sobre o `paper.txt` dentro do diretório isolado.

## 3. Resultado: comparação termo a termo
Derivação cega do auditor × `saf.cu` (kernel de campo efetivo, linhas ~99–119).
A comparação é **minha**, feita depois; o que é cego é a derivação do auditor.

| termo | auditor (cego) | `saf.cu` | |
|---|---|---|---|
| normalização | `Beff = −(1/(Ms a² d)) ∂H/∂m` | idem (impresso no cabeçalho) | **bate** |
| troca | `2A/(Ms a²) · Δ_discreto` → `(2A/Ms)∇²m` | `ce = 2A/(Ms a²)`, laplaciano 5 pontos | **bate** |
| anisotropia | `(2K/Ms) m_z ẑ` | `bz += 2K·m_z/Ms` | **bate** |
| Zeeman | `B` | `bz += Bz` | **bate** |
| DMI | `D/(Ms a)` sobre diferenças centrais; contínuo `(2D/Ms)[∇m_z − (∂ₓmₓ+∂_ym_y)ẑ]` | `cd = D/(Ms a)`, mesmo estêncil | **bate** |
| interlayer | `−A_int m_j /(Ms d)` | `ci = −Aint/(Ms·d)` | **bate** |
| energia interlayer | `A_int a² m₁·m₂`, areal, sem `d`, sem ½ | `e += a²·Aint·(m₁·m₂)` | **bate** |

### 3.1 Discriminante (a) — o fator `1/d`: **fechado por terceiro caminho**
O auditor deriva `B_int,1 = −A_int m₂/(Ms d)` e dá a razão física: `A_int` já é energia por
área, então `d` não multiplica a energia — ele aparece no **denominador do campo** porque a
mesma energia interfacial faz torque sobre o momento contido em `a²d`.
O risco `SL-2` já estava fechado por dois caminhos internos (FD termo-a-termo em VL-1 e o
valor fechado 0.086207 T em VL-2). Este é o **primeiro caminho externo e cego**.

### 3.2 Discriminante (b) — DMI: **o ponto cego foi iluminado, e passou**
Este era o teste que importava. `pick_chirality` escolhe φ₀ ∈ {0, π} minimizando a energia
DMI do próprio ansatz — ou seja, **autocorrige um erro de sinal meu e portanto o torna
invisível em `l`**. Um sinal global trocado na minha energia DMI daria a imagem espelhada,
com o mesmo `l`.

O auditor derivou analiticamente, sem ver o código:
```
w_D = D·cos(χ)·[θ'(r) + sin θ cos θ / r]      ⇒      cos(χ) = −p·sgn(D)
```
com `p = m_z(0)` a polaridade do núcleo e `χ = 0` ↔ magnetização no plano radial para fora.

Predição × o que o meu código escolheu **empiricamente** (logs de R001, já selados):

| | polaridade `p` | `D` | previsto | `saf.cu` escolheu |
|---|---|---|---|---|
| camada 1 | `−1` (bg=+1, núcleo −z) | `+3.05` | `cos χ=+1` → **φ₀ = 0°** | **0°** (E(0)=−9.813e−20 J < E(π)) |
| camada 2 | `+1` (bg=−1, núcleo +z) | `−3.05` | `cos χ=+1` → **φ₀ = 0°** | **0°** (E(0)=−9.813e−20 J < E(π)) |

**Bate nas duas camadas — mas isto é UM teste, não dois.** Correção de dimensionamento,
registrada em vez de explorada: a camada 2 é **algebricamente forçada** pela própria fórmula
do auditor. Com `p₂=−p₁` e `D₂=−D₁`,
`cos χ₂ = −p₂·sgn(D₂) = −(−p₁)(−sgn D₁) = −p₁·sgn(D₁) = cos χ₁`.
Os meus logs confirmam o mecanismo: as energias DMI das duas camadas são **numericamente
idênticas** (−9.813e−20 / +9.813e−20 nas duas), porque inverter `bg` nega o integrando e
inverter `D` o nega de volta. O `pick_chirality` da camada 2 não tinha liberdade para
discordar depois que a camada 1 concordou.

Claim proporcional: **uma** checagem independente da convenção de sinal de `dmi_energy`
contra a Eq. (A4), replicada por simetria na segunda camada. Continua sendo exatamente o
discriminante que se queria, e continua tendo passado.

Separadamente — e isto é leitura de código, não teste — o `saf.cu` inverte polaridade e `D`
**juntos** (`bg=+1,D1` e `bg=-1,D2`, linhas 493/496), que é o que o artigo especifica. O
auditor destaca por conta própria a consequência não óbvia: as duas camadas acabam com a
**mesma** helicidade `χ`, isto é, as magnetizações de parede apontam localmente na mesma
direção, embora as cargas e os sentidos de giro sejam opostos.

### 3.3 Achado lateral: a notação do artigo é imprecisa
O auditor observa que a fórmula `Beff,i = −Ms⁻¹(δH/δm_i)` **como escrita na Eq. (A1)** só
fecha dimensionalmente se `δH/δm_i` for lido como densidade **volumétrica**; a Eq. (A3),
porém, é uma integral **areal**. O `saf.cu` usa `−(1/(Ms a² d))·∂H/∂m`, que é a leitura
consistente. Isto é um defeito de notação do artigo, achado de forma independente, e reforça
que `QA-01`/`SL-2` não eram preciosismo.

## 4. Divergências encontradas
**Nenhuma.** Sete expressões comparadas, sete acordos — mas **não são sete testes
independentes**, e a release não os conta como tal.

- **Dois acordos discriminantes**, que eram riscos reais de *leitura do artigo*: o `1/d` do
  campo interlayer (`A_int` areal sobre o volume `a²d`) e a convenção de sinal do DMI.
- **Cinco acordos confirmatórios**: fixada a normalização areal `−(1/(Ms a²d))∂H/∂m`, os
  prefatores de troca (`2A/(Ms a²)`), anisotropia (`2K/Ms`) e Zeeman seguem mecanicamente do
  micromagnetismo padrão. Pegariam um fator 2 ou um `a²` perdido no meu código — o que não é
  nada — mas não são riscos específicos deste artigo.

Isto é relevante para a decisão de aceite e é, ao mesmo tempo, o motivo do §5.

## 5. Força da evidência: `BOUNDED` — e por quê

1. **Acordo é evidência mais fraca do que desacordo teria sido.** Um único desacordo teria
   sido decisivo; a concordância só remove hipóteses de erro, não prova correção.
2. **A "independência" tem limite claro.** O auditor é um LLM que muito provavelmente já viu
   este PRL (publicado em ago/2025) e certamente viu a literatura padrão de DMI e SAF. A
   cegueira verificada é em relação **ao meu laboratório e ao meu código**, que é o que os
   discriminantes exigiam — **não** em relação ao artigo.
3. **Risco de erro correlacionado.** Auditor e auditado são modelos de linguagem. Uma
   leitura errada *compartilhada* da Eq. (A4) permanece invisível a este teste.
4. **Cobertura restrita a expressões de campo.** Não foram auditados: o estimador de carga
   topológica (Berg–Lüscher), a relaxação, a indexação de PBC, o estimador de `bond length`,
   nem qualquer número. Nada aqui toca 10.9607 nm.
5. **A comparação é minha e não é cega.** A etapa 2 do desenho (código contra artigo, pelo
   auditor) é justamente o que removeria este limite — e **não está autorizada**.

Claim proporcional: **"as expressões de campo efetivo do `saf.cu` sobrevivem a uma derivação
independente do artigo feita sem acesso ao código, inclusive no ponto onde o meu próprio
código esconderia um erro de sinal"** — e não "o `saf.cu` está correto".

## 6. Artefatos (`LAB/EVIDENCE/AUDIT-001/`)
`RUN-001.txt` (as-run), `blind_prompt_v2.txt` (prompt efetivo), `blind_prompt.txt` (desenho
original de WRITEBACK-004, preservado), `paper.txt`, `endmatter_p8-8.png`, `response.md`
(derivação do auditor), `trace.jsonl` (trace completo, base da verificação de cegueira),
`stderr.log`, `SHA256SUMS.txt` (`sha256sum -c` passa nos 8).

## 7. Ligação de impacto
`RELEASE-R001.md` §limites e `RELEASE-R002.md` §9.6 registram "sem leitura independente do
artigo". Esse limite fica **rebaixado, não eliminado**: existe agora uma leitura
independente do artigo, mas não uma leitura independente do código nem um solver
independente.

## 8. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar **AUDIT-001** — e, separadamente e
ainda pendentes desde 21/08, **R001** e **R002**.
Separadamente: autorizar ou não a **etapa 2** (enviar `saf.cu` ao auditor).
