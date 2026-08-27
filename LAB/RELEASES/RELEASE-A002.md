# RELEASE-A002 — as-run da auditoria contra OOMMF

Data: 2026-08-24 · Missão: `MISSION-A002` (`AUTHORIZED` por `WRITEBACK-006`) · Regime `AUDIT`
Estado: **`TERMINAL_AWAITING_HUMAN`** · `human_acceptance: PENDING`

> **Gate `G-A002` NÃO passou.** A missão não entregou seu objetivo principal. Entregou outras
> quatro coisas, uma delas mais valiosa que o objetivo. Este release diz as duas coisas.

---

## 1. Placar contra os critérios pré-registrados

| | resultado |
|---|---|
| **OV-1** (skyrmion único) | **FALHOU** — `Q = −0.9353`, fora da tolerância de 0.05 |
| **OV-2** (fator `1/d`) | **PASSOU** — os dois alvos, com 4 dígitos |
| **OV-3** (par acoplado) | **NÃO-CONCLUSIVO** — critério de mitigação falhou (2.29 % > 1.0 %) |
| `G-A002` | **não passou** |

## 2. OV-2 — passou, e é o resultado que sobrevive

`sigma = −A_int/2`, malha não periódica:

```
|E_par − E_anti| = 4.000000e-19 J   alvo 2·A_int·A_box = 4.0000e-19   ->  +0.0000 %
campo de torque  = 0.086207 T       alvo A_int/(Ms·d)  = 0.086207     ->  exato
campo uniforme: 1 valor distinto em 10000 células
```

**A calibração corrigiu o pré-registro.** O `MISSION-A002` §2.1 previa `sigma = −A_int` e
deixava em aberto "um possível fator 2, que o OV-2 mede". Mediu: o fator é real. A energia do
link é somada às **duas** células e a soma é multiplicada por `2·Volume`; o campo usa
`hcoef = 2/MU0`. Energia e campo são mutuamente consistentes com `sigma_eff = 2·sigma`.

**Este resultado não depende de fronteira** — estados uniformes não têm borda que os
distinga. É por isso que ele sobrevive ao naufrágio do OV-1/OV-3.

**Efeito: `SL-2` fecha por um quarto caminho** — FD interno (VL-1), valor fechado interno
(VL-2), derivação cega externa (`AUDIT-001`) e agora **código independente escrito por
humanos**. É o mais forte dos quatro, porque é o único que não é nem meu nem de um LLM.

## 3. PBC é inviável neste OOMMF — dois bloqueios

1. **`Oxs_TwoSurfaceExchange` + `Oxs_PeriodicRectangularMesh`: bug silencioso.**
   1164 de 10000 células da interface perdem o link. Campo com 3 valores distintos em vez de
   1; energia 11.6 % curta. Idêntico com 1 e 4 threads → determinístico, não é corrida.
   As células afetadas não formam borda: formam padrão espalhado.
   
   | malha | células fracas | valores distintos | `E_anti` |
   |---|---|---|---|
   | `Oxs_RectangularMesh` | 0 | 1 | `−8.0000000000000017e−19` (exato) |
   | `Oxs_PeriodicRectangularMesh` | 1164 | 3 | `−7.0746304987791074e−19` |

2. **`Oxs_DMExchange6Ngbr` recusa PBC** — erro explícito, *"is not an Oxs_RectangularMesh
   object"*. Recusa dura, não silenciosa. **Fatal.** `Oxs_DMI_C2v` aceita PBC mas é simetria
   C2v, não Cnv interfacial: modelo errado. Contornar exigiria compilar extensão nova — ação
   de sistema, não autorizada.

**Este achado, sozinho, justifica a escada.** Sem OV-2, o OV-3 teria rodado com 11.6 % do
acoplamento faltando, em posições espalhadas, e produzido uma **discrepância falsa** contra o
`saf.cu` — que eu teria reportado como diferença entre implementações.

## 4. Por que OV-1 falhou — o que isso descarta, e o que não acusa
Pela taxonomia pré-registrada (`MISSION-A002` §4), OV-1 falhar significa **erro de tradução
meu (`SL-A1`)**, e obriga a descartar o OV-3. Ambas as consequências são honradas aqui. O que
segue explica *qual* elemento da tradução falhou — e por que ele não acusa o `saf.cu`.

Fronteiras livres com DMI produzem inclinação de borda (Rohart–Thiaville). Medido:

```
Q (caixa 100×100)        = −0.9353      <- falha o critério
Q (janela central 60×60) = −1.0000      <- exato
|m_perp| na borda = 0.4647   |   no volume = 0.0878
núcleo do skyrmion: posto em x = 45 nm, relaxou para x = 49 nm
```

O skyrmion é um skyrmion legítimo, `|Q| = 1` exato longe da borda, `mz_min = −0.9928`. Todo o
déficit de carga (`+0.0647`) vem da borda. **E a borda exerce força real: o skyrmion migrou
4 nm.** O desvio de fronteira declarado no adendo §C não é benigno; é o efeito dominante.

## 5. OV-3 — não-conclusivo pelo critério que foi registrado antes

| | `l` caixa inteira | `l` janela central | `Q₁ / Q₂` (central) |
|---|---|---|---|
| L = 100 nm | 11.3896 nm | 10.7115 nm | −1.0000 / +1.0000 |
| L = 140 nm | 11.6505 nm | 10.9566 nm | −1.0000 / +1.0000 |
| **variação** | **2.29 %** | **2.29 %** | — |

O adendo §D registrou, **antes de rodar**: fronteira não contamina se `|l(140)−l(100)|/l(100)
≤ 1.0 %`; acima disso o OV-3 é **NÃO-CONCLUSIVO** quanto ao `saf.cu`. Deu **2.29 %**, e nas
duas leituras. Além disso `l` ainda **cresce** com a caixa — não convergiu.

**→ Nenhum veredito sobre o R001 sai daqui — por duas razões independentes.**
A primeira é a taxonomia pré-registrada no `MISSION-A002` §4: **OV-1 falhando já descarta o
OV-3**, sozinha, antes de qualquer consideração sobre os 2.29 %. A segunda é o próprio
critério de mitigação do adendo §D. Ter duas razões independentes é mais forte que ter uma.

### 5.2 Relaxação incompleta está DESCARTADA como causa
Suspeita legítima: OV-3 parou em ~2 000 iterações contra as 124 875 do `saf.cu`. Verificado
nos `.odt` — a unidade de `Max mxHxm` do OOMMF é **A/m**, não tesla:

| corrida | `Max mxHxm` | em tesla |
|---|---|---|
| OV-1 | 9.797e−05 A/m | 1.231e−10 T |
| OV-3 L=100 | 8.920e−05 A/m | 1.121e−10 T |
| OV-3 L=140 | 9.491e−05 A/m | 1.193e−10 T |
| `saf.cu` VL-4 (referência) | 7.955 A/m | 9.997e−06 T |

O OOMMF convergiu cerca de **90 000× mais apertado** que o critério do R001, e parou pelo
torque, não por teto de iteração. Os 2.29 % são fronteira, não relaxação inacabada.

### 5.1 O número que eu não vou usar
`l(140 nm, janela central) = 10.9566 nm` fica a **0.03 %** do `10.9529 nm` do `saf.cu`. É
tentador e **não conta**. O critério de mitigação foi registrado antes e falhou; usar este
número agora seria exatamente o movimento post-hoc que o método existe para impedir. Fica
registrado **como dado, não como resultado** — o mesmo tratamento que o `RELEASE-R002.md` §1
deu ao critério secundário.

## 6. Ativo colateral: estimador portado e verificado
`est.py` (Berg–Lüscher + centros de carga da Eq. 1) reproduz os três valores selados do R001:

```
mfinal_weak.dat        10.9530 nm   (selado 10.9529)   Q = ∓1.0000
mfinal_weak_tight.dat  10.9608 nm   (selado 10.9607)   Q = ∓1.0000
mfinal_mesh05.dat      10.8500 nm   (selado 10.8500)   Q = ∓1.0000
```
Erro máximo `0.0001 nm`. O estimador foi verificado contra resposta conhecida **antes** de
ser aplicado a dados novos. Fica disponível para missões futuras.

## 7. Força da evidência

- **OV-2: `SOLID` para o que afirma.** `SL-2` verificado por código independente
  humano-escrito. Não depende de fronteira, de ansatz, nem de estimador.
- **OV-3: `NONE`.** Não produz evidência sobre o R001, por critério pré-registrado.
- O limite **"sem solver independente" continua de pé.** O OOMMF verificou um *termo*, não o
  resultado. Não suavizar isto no aceite.

## 8. O que faria a missão terminar
Uma extensão de DMI **Cnv com suporte a PBC**. Isso significa compilar extensão nova para o
OOMMF — **ação de sistema, requer autorização**. Alternativa registrada: estudo de
convergência em caixa (180, 220 nm…) para extrapolar ao limite PBC, o que é uma missão nova,
com critério a pré-registrar, e não um conserto desta.

## 9. Artefatos (`LAB/EVIDENCE/A002/`)
MIFs as-run (`ov2*.mif`, `pair.mif`, `pbctest.mif`), `.odt`, `.ohf`, `.omf` finais,
`ovf.py` (leitor OVF), `est.py` (estimador), `OV2-FINDING.txt`, `OV13-RESULTS.txt`,
`SHA256SUMS.txt` — `sha256sum -c` passa nos 25.

## 10. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar **A002** — sabendo que o gate não
passou e que o valor está em OV-2 e nos achados de ferramenta, não em OV-3.
Continuam pendentes desde 21/08: **R001**, **R002**, **AUDIT-001**.
