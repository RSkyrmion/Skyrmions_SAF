# RELEASE-AUDIT-002 — estimador cego independente

Data: 2026-08-24 · Autoridade: `WRITEBACK-008` · Regime `AUDIT`
Estado: **`TERMINAL_AWAITING_HUMAN`** · `human_acceptance: PENDING`

> Ataca `L3.4` — a camada que nenhuma auditoria anterior cobriu: **o estimador**.

---

## 1. Desenho
O auditor externo (`codex`, `gpt-5.6-sol`) recebeu **apenas** o artigo (texto + página 8 do
End Matter) e um `FORMAT.txt` com o layout de colunas de um arquivo de estado. Escreveu
`estimator.py` do zero, a partir da Eq. (1). **Não recebeu** o `saf.cu`, **não recebeu**
dados, **não recebeu** os valores-alvo. Depois **eu** rodei o código aqui, sobre a evidência
selada do R001.

O sentido do fluxo importa: o código veio de lá para cá. Nada meu saiu da máquina além do
artigo (já enviado no `AUDIT-001`) e do `FORMAT.txt`.

## 2. Cegueira — verificada
Varredura do `trace.jsonl` por `pesquisa/SAF | saf.cu | /LAB | MISSION- | RELEASE- |
WRITEBACK | EVIDENCE | 10.9x | 10.85 | mfinal | oommf`: única ocorrência é **`10.98`**, que é
o valor **publicado** na legenda da Fig. 2(a) e está no `paper.txt`. Nenhum dos meus valores
(`10.9529`, `10.9607`, `10.8500`) aparece.

## 3. Resultado — alvos pré-registrados desde `MISSION-A002` §3

| arquivo selado | `a` | alvo (`saf.cu`) | estimador cego | dif |
|---|---|---|---|---|
| `mfinal_weak.dat` | 1 nm | 10.9529 nm | **10.9530 nm** | +0.0001 nm (+0.0005 %) |
| `mfinal_weak_tight.dat` | 1 nm | 10.9607 nm | **10.9608 nm** | +0.0001 nm (+0.0006 %) |
| `mfinal_mesh05.dat` | 0.5 nm | 10.8500 nm | **10.8500 nm** | +0.0000 nm (+0.0003 %) |

`Q₁ = −1`, `Q₂ = +1` exatos nos três. **PASSOU.**

## 4. Por que o acordo não é trivial
O código do auditor faz escolhas **diferentes das minhas** em quatro pontos, e ainda assim
converge:
1. Arredonda `Q` ao inteiro e divide o primeiro momento pelo **inteiro**; eu divido pela
   soma bruta dos ângulos sólidos.
2. Enrola os baricentros dos triângulos na caixa periódica (`np.mod`); eu não enrolo.
3. Usa **imagem mínima** na separação; eu uso distância euclidiana direta.
4. Indexa `m[i,j]` (x-major); eu indexo `m[j,i]` (y-major).

Concordam em 0.0001 nm mesmo assim. Também **reproduz a diferença de 0.0078 nm** entre
`weak` e `weak_tight`, e o valor da malha refinada — não é acordo de um ponto.

## 5. O que isto fecha, e o que NÃO fecha
**Fecha `L3.4`** no que diz respeito ao estimador: a régua que produz `l` e `Q` a partir de um
estado está verificada por implementação independente e cega, derivada do artigo.

**NÃO fecha `L-G`.** O estimador mede **o meu estado final**. Ele valida a régua, não a
relaxação que produziu o estado. Continua sem verificação independente do **número** `l` no
sentido de outro solver chegar ao mesmo estado. Esta distinção é o ponto inteiro do release
e não deve ser suavizada.

**NÃO cobre** o resto de `L3.4`: relaxação, indexação de PBC no solver, e o campo efetivo
(que o `AUDIT-001` cobriu por derivação e o `A002` OV-2 cobriu num termo).

## 6. Força da evidência: `SOLID` para o que afirma
É a verificação mais forte do laboratório até aqui, por três motivos: implementação
independente (não derivação), cega verificada, e três alvos distintos incluindo um de malha
diferente. Limite residual: auditor e auditado continuam sendo LLMs, e uma leitura errada
compartilhada da Eq. (1) permaneceria invisível — mas as quatro divergências de convenção do
§4 tornam isso menos provável do que no `AUDIT-001`.

## 7. Artefatos (`LAB/EVIDENCE/AUDIT-002/`)
`prompt.txt`, `FORMAT.txt`, `estimator.py`, `response.md`, `trace.jsonl`, `stderr.log`,
`RUN-001.txt`, `SHA256SUMS.txt` — `sha256sum -c` passa nos 7.

## 8. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar **AUDIT-002**.
