# ADENDO-001 a RELEASE-E001 — defeitos corrigidos e a dívida do `1/(1+α²)` fechada

Data: 2026-08-24 · Motivado por pergunta de Rodrigo
Missão: `MISSION-E001`, ainda `TERMINAL_AWAITING_HUMAN`

> `RELEASE-E001.md` **não foi editado**. Este adendo o complementa e, num ponto, **corrige um
> raciocínio errado meu** que estava registrado lá.

---

## 1. Defeito 1 (colisão de `argv`) — correção estava INCOMPLETA, agora ampliada
O `RELEASE-E001` §6.1 dizia "corrigido". Era verdade só para o `ev3`: `ev1` e `ev2` seguiam
expostos à mesma colisão, e não manifestavam por sorte de uso (eram chamados sem argumentos
extras). A blindagem agora é do prefixo inteiro:
`if(mode.rfind("ev",0)==0){ p.a=1e-9; p.nx=100; p.ny=100; }`

## 2. Defeito 2 (provenance) — a CAUSA não estava corrigida; agora está
O `RELEASE-E001` §6.2 registrava o dano como nulo e os arquivos como hasheados. Mas isso dava
**detecção**, não **prevenção**: o `saf_dyn pair` continuava escrevendo dentro de
`EVIDENCE/R001/`, e rodá-lo de novo reescreveria de novo.

**Corrigido na causa:** os 2 caminhos de escrita do `saf_dyn.cu` foram redirecionados de
`LAB/EVIDENCE/R001/` para `LAB/EVIDENCE/E001/`. Restam **zero** referências a `R001` no
código de dinâmica. Um binário de outra missão não escreve mais em evidência selada.

## 3. Reexecução após as correções — bit-idêntica
O binário mudou, então os espectros do EV-3 foram **refeitos** com o binário corrigido:
`max|diferença| = 0.000e+00` contra a série anterior. Picos e correlações inalterados.
A provenance do EV-3 fecha com o binário atual.

---

## 4. A dívida do `1/(1+α²)` — **FECHADA**, e o meu raciocínio estava errado

### 4.1 De onde o fator vem
Da inversão algébrica da forma de Gilbert (implícita) para a de Landau–Lifshitz (explícita):
`dm/dt = −γ m×B + α m×(dm/dt)` ⟹ `dm/dt = −γ/(1+α²)[m×B + α m×(m×B)]`.
Na forma adimensional que Rodrigo escreveu, ele **sobrevive explícito**, porque `α` é
adimensional:

```
dS_i/dτ = −1/(1+α²) [ S_i × H_i^eff + α S_i × (S_i × H_i^eff) ] ,
com  t = t₀ τ ,  t₀ = M_s a₀² / (2 A_ex γ)
```

### 4.2 As unidades batem com o meu código
```
t₀ = M_s a₀²/(2 A_ex γ) = 1.097949e−13 s = 0.1098 ps
B₀ = 2 A_ex/(M_s a₀²)   = 51.7241 T          e   t₀ = 1/(γ B₀)  (idêntico)
```
`B₀ = 51.72 T` é **exatamente** o prefator de troca `ce = 2A/(Ms a²)` do meu kernel. Meu passo
RK4 de 10 fs é `0.0911 t₀` — 11 passos por unidade natural de tempo.

### 4.3 CORREÇÃO: o erro NÃO acumularia
`MISSION-E001` §3.1 e `RELEASE-E001` §7.2 afirmam que omitir o fator faria o erro **acumular**
em trajetórias de ~3 µs no `E002`. **Isso está errado**, e a forma adimensional acima mostra
por quê: o fator multiplica o **colchete inteiro**. Omiti-lo é, exatamente, redefinir
`τ' = τ/(1+α²)`.

Para um sistema **autônomo** isso é uma pura reetiquetagem do eixo do tempo: a trajetória no
espaço de configurações é **idêntica**, e qualquer taxa fica errada por um fator constante
`(1+α²) = 1.0004` — **0.04 %, independente da duração**. Não acumula.

O único lugar onde não é reetiquetagem pura é num sistema **forçado**, porque a frequência de
excitação é fixa no tempo de laboratório: aí o descompasso vira **dessintonia** de 0.04 %.
Com `α = 0.02` a largura de linha da ressonância é `~α·f ≈ 2 %`, logo 0.04 % é **1/50 da
largura**. Real, mas desprezível — e também não acumulativo.

### 4.4 O fator agora está TESTADO, não só implementado
`RELEASE-E001` §7.2 registrava-o como caminho **não testado** (com `α = 0` o denominador vale
1). O `EV-2` foi estendido para `α` arbitrário: na precessão amortecida a frequência **é**
`γB/(2π(1+α²))`, então ela mede o denominador diretamente.

| `α` | `f` medido [GHz] | `γB/2π(1+α²)` | razão `f/f₀` | `1/(1+α²)` | desvio |
|---|---|---|---|---|---|
| 0.00 | 2.802494 | 2.802494 | 1.00000000 | 1.00000000 | `+8.9e−16` |
| 0.02 | 2.801374 | 2.801374 | 0.99960016 | 0.99960016 | `−2.0e−15` |
| 0.30 | 2.571096 | 2.571096 | 0.91743119 | 0.91743119 | `+3.1e−15` |

`α = 0.30` é o teste forte: efeito de **9 %**, impossível de confundir com ruído. Acordo em
precisão de máquina nos três.

**→ A dívida técnica registrada para o `E002` está FECHADA.** O fator está implementado e
verificado; e, mesmo que não estivesse, o efeito seria constante e de 0.04 %, não acumulativo.

## 5. Artefatos novos (`LAB/EVIDENCE/E001/`)
`ev2_precessao_a0.000.dat`, `ev2_precessao_a0.020.dat`, `ev2_precessao_a0.300.dat`,
`saf_dyn.cu`/`saf_dyn` corrigidos, séries EV-3 refeitas. `SHA256SUMS.txt` atualizado.

## 6. Efeito na decisão pendente
Nenhum critério pré-registrado muda; `G-E001` continua passado. O que muda é que dois
defeitos de execução estão de fato corrigidos na causa, uma dívida foi fechada por medida, e
um raciocínio errado meu foi corrigido no registro em vez de sobreviver nele.
