# WRITEBACK-007 — ACEITE COM LIMITAÇÕES de R001, R002, AUDIT-001 e A002

Data: 2026-08-24 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Aceito com limitações"

## Escopo desta leitura — e o convite a corrigir
Registro que interpretei isto como cobrindo **as quatro** decisões que estavam sobre a mesa
na mensagem imediatamente anterior, na ordem em que foram apresentadas:
`MISSION-R001`, `MISSION-R002`, `AUDIT-001` (etapa 1) e `MISSION-A002`.

**Se você quis aceitar menos que as quatro, corrija** — em particular o `A002`, cujo gate
**não passou** e cuja recomendação de aceite foi feita em base diferente das outras três.

`human_acceptance` de cada uma passa de `PENDING` a **`ACCEPTED_WITH_LIMITATIONS`**.
Os arquivos `RELEASE-*.md` **não foram editados** e continuam dizendo `PENDING` no corpo,
como foram escritos. Este writeback é a autoridade que supersede aquele campo.

## O que o aceite NÃO faz
- **Não é freeze.** Nada aqui está congelado. Freeze é ato separado e não foi pedido.
- **Não autoriza** a etapa 2 do `AUDIT-001` (enviar o `saf.cu` a terceiro).
- **Não autoriza** compilar extensão de DMI Cnv/PBC para o OOMMF, nem o estimador cego em
  Python, nem missão nova alguma.
- **Não apaga** nenhuma discrepância aberta. Aceitar com limitações significa que os limites
  viajam junto **para sempre**, não que foram resolvidos.

---

# Claims aceitos, com seus limites — versão canônica

## C-1 (de R001) — o número
> Uma re-implementação independente do PRL 135, 086701 relaxa para um par de skyrmions
> **não-coaxial** com `l = 10.9607 nm`, **consistente com o valor publicado de 10.98 nm dentro
> de 0.2 %, num único ponto de parâmetros**.

**Limites que viajam junto, obrigatoriamente:**
- **L1.1** A sensibilidade à malha é de **1.0 %** (0.5 nm → 10.8500 nm) — **maior que a
  discrepância de 0.18 %**. O acordo **não é mais preciso que o método**. É proibido dizer
  "o artigo foi reproduzido".
- **L1.2** Um único ponto de parâmetros. Não é reprodução da figura, nem do artigo.
- **L1.3** Os dados originais não são públicos. Isto é **re-implementação**, não
  re-execução. A evidência é estruturalmente mais fraca que uma replicação de dados.
- **L1.4** Desvio de protocolo `SL-7` registrado (estimador de carga trocado durante VL-3).

## C-2 (de R002) — a estrutura
> A leitura do artigo embutida no `saf.cu` **sobreviveu a um teste estrutural multiponto que
> poderia tê-la refutado**: os dois pontos publicados caem na região estável, e a fronteira
> coaxial↔não-coaxial reproduz a do artigo em cinco colunas com resíduo ≤ meio passo de grade.

**Limites:**
- **L2.1** É "sobreviveu a um teste", **não** "a Eq. (S1) foi reproduzida". O critério que
  testaria a Eq. (S1) quantitativamente morreu na checagem de poder, e nada o ressuscitou.
- **L2.2** Defeito de protocolo registrado e **não reparado**: a regra de poder confundiu
  largura da janela com precisão do centro.
- **L2.3** **DISCREPÂNCIA AINDA ABERTA**: em `A_int = 0.12` o artigo prevê ramo coaxial em
  `K₀ ∈ [0.126, 0.144]` e eu não o encontro. Estreita e localizada, em região onde a linha
  do artigo está extrapolada (último traço em 0.1066), mas **aberta**. O aceite não a fecha.
- **L2.4** `SL-B1`: região alcançável a partir da inicialização declarada, não "a região de
  estabilidade" em abstrato.
- **L2.5** Malha 1 nm, caixa 100 nm, resolução em `K₀` de 0.025 — não refinadas.

## C-3 (de AUDIT-001) — a leitura
> As expressões de campo efetivo do `saf.cu` sobrevivem a uma **derivação independente do
> artigo feita sem acesso ao código**, inclusive no ponto (sinal do DMI) onde o meu próprio
> código esconderia um erro.

**Limites:**
- **L3.1** Acordo é evidência mais fraca do que um desacordo teria sido.
- **L3.2** A cegueira é em relação **ao meu laboratório e ao meu código**, não ao artigo: o
  auditor provavelmente já viu este PRL.
- **L3.3** Auditor e auditado são LLMs. Uma **leitura errada compartilhada** da Eq. (A4)
  continua invisível.
- **L3.4** Cobre expressões de campo. **Não** cobre Berg–Lüscher, relaxação, PBC, estimador
  de `bond length`, nem número algum.
- **L3.5** A comparação código×derivação é **minha** e não é cega.

## C-4 (de A002) — o termo, e a ferramenta
> O fator `1/d` do campo interlayer (`SL-2`) está verificado por **código independente escrito
> por humanos** (OOMMF), com quatro dígitos de acordo em energia e campo.
> E: `Oxs_TwoSurfaceExchange` tem **bug silencioso com malha periódica** que teria fabricado
> uma discrepância falsa.

**Limites:**
- **L4.1** **O gate `G-A002` NÃO passou.** Este aceite é do OV-2 e dos achados de ferramenta,
  não da missão como desenhada.
- **L4.2** OV-3 é **não-conclusivo**, por duas razões independentes (taxonomia do §4 pela
  falha do OV-1; e o critério de mitigação, 2.29 % > 1.0 %). `l(140) = 10.9566 nm` é
  **dado, não resultado** — usá-lo seria post-hoc.
- **L4.3** **"Sem solver independente" CONTINUA DE PÉ.** O OOMMF verificou um *termo*, não o
  resultado. Este é o limite mais importante do lote e não pode ser suavizado.

## Limite global, acima de todos
**L-G:** Continua sem verificação independente do **resultado** `l`. Três instrumentos
diferentes atacaram três camadas — leitura (AUDIT-001), estrutura (R002) e um termo isolado
(A002 OV-2) — e nenhum atacou o número. O que sustenta `10.9607 nm` continua sendo um único
código, o meu.

---

## Efeito no estado
Fase 1 (reprodução) **encerrada com aceite**. Fase 2 (extensão controlada) fica **aberta**,
sem missão proposta e sem direção escolhida — decisão sua.

## Próximo head/estado
`STATE-2026-08-24-j`

## Próxima decisão humana
Nenhuma pendente. O laboratório está em repouso consistente pela primeira vez desde 21/08.
Quando quiser seguir, as direções em aberto estão em `STATE.md`.
