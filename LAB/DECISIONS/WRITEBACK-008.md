# WRITEBACK-008 — Fase 2 aberta e estimador cego autorizado

Data: 2026-08-24 · Autoridade: Rodrigo

## Decisão humana (literal)
> "Pode executar sua sugestão"

## A sugestão a que se refere (registrada como foi feita)
> "Se for para escolher uma: **Fase 2, a extensão controlada** — o candidato mais natural é a
> autopropulsão sob excitação ABM. Como acompanhamento barato, o **estimador cego em
> Python**: ataca `L3.4`, a camada que nenhuma auditoria cobriu, e nada meu sai da máquina."

## O que fica autorizado
1. **`AUDIT-002`** — estimador cego. O auditor externo (`codex`) escreve, **sem ver o meu
   código nem os meus números**, um estimador independente de `Q` e `l`; **eu rodo aqui**
   sobre a evidência selada do R001.
2. **Fase 2** — extensão controlada. Ver §Escopo.

## Ação externa — declarada, não escondida
O `AUDIT-002` é **ação externa (INV-16)**: sai da máquina o artigo (já enviado no
`AUDIT-001`, mesmo escopo) e um `FORMAT.txt` descrevendo o layout de colunas de um arquivo de
estado. **Não sai** o `saf.cu`, **não saem** dados, **não saem** os valores-alvo.

Registrado como custo real e não-nulo: a ordem das colunas revela o **emparelhamento de
polaridade das camadas** (camada 1 núcleo para baixo, camada 2 para cima), que é um dos
discriminantes do `AUDIT-001`. Aceitável porque `Q` e `l` são invariantes a inversão global e
porque o artigo já diz *"opposite magnetization background"* — mas não é envio inócuo.

**A etapa 2 do `AUDIT-001` (enviar o `saf.cu`) continua NÃO autorizada.** Isto aqui é outra
coisa: o código vem de lá para cá, não daqui para lá.

## Escopo da Fase 2 — recorte declarado, e por que ele é menor do que eu sugeri
Eu nomeei "autopropulsão sob excitação ABM". **Ela não é uma pequena extensão controlada.**
Exige dinâmica LLG real com o tempo — e o `saf.cu` hoje só faz descida amortecida em `T = 0`
(`SL-5` registrou que a trajetória não é evidência ali). Autopropulsão exige ainda muitos
ciclos de excitação e o rastreio da deriva do par.

Recorte: **`MISSION-E001` implementa e valida a dinâmica LLG** e mede o **espectro de modos
de breathing** (Apêndice B) contra o artigo. É o menor degrau que (i) adiciona capacidade
nova de verdade, (ii) tem alvo quantitativo publicado e (iii) é **pré-requisito** da
autopropulsão. A autopropulsão fica como `E002`, não proposta.

Se você quiser ir direto à autopropulsão assumindo o risco de pular a validação da dinâmica,
diga — é sua decisão, e eu registro o pulo como desvio.

## Próximo head/estado
`STATE-2026-08-24-k`
