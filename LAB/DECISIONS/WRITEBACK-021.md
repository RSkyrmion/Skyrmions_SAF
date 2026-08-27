# WRITEBACK-021 — aceite de `E005` e `E004`; **compilar o mumax3 autorizado**

Data: 2026-08-27 · Autoridade: Rodrigo

## Decisão humana (literal)
> "E005 e E004 aceito com limitações; autorizo compilar o mumax3"

## 1. Efeito formal
| missão | antes | agora |
|---|---|---|
| `MISSION-E005` | `PENDING` (gate passou) | **`ACCEPTED_WITH_LIMITATIONS`** |
| `MISSION-E004` | `REVISION_REQUESTED` (`WB-015`) | **`ACCEPTED_WITH_LIMITATIONS`** |

**Como o `E004` encerra, e isto precisa constar:** `REVISION_REQUESTED` significa "esta missão
deve trabalho". O trabalho foi feito — **pelo `E005`, não por ela**. O critério primário do
`E004` (`EF-1`) **nunca teve veredito**, e o `EF-0` dele declarou plana uma curva com fator 7
de contraste. O aceite é do **material**, não da resposta. Nada do `E004` pode ser citado como
tendo testado a afirmação do artigo.

O material do `E004R` **foi usado**: os `17.8255` a `ΔK/K₀ = 0.005` são o ponto central da
inclinação do `E005`.

---

## C-14 (de `MISSION-E005`) — o amolecimento de amplitude
> O pico de `v_sp` **desce quando a amplitude da excitação sobe**, com o sinal e a escala da
> `Fig. S4(c)` do suplementar: inclinação medida **`−64.470 GHz`** por unidade de `ΔK/K₀`
> contra **`−74.807`** extraída da figura e **selada antes das corridas** — razão **`0.862`**,
> dentro da banda de fator 3 pré-registrada. `f_pico` = `17.9664 / 17.8255 / 17.5796 GHz` para
> `ΔK/K₀` = `0.002 / 0.005 / 0.008`.

**Limites:**
- **L14.1** **Isto resolve a "discrepância" do `E004R`.** Os `17.83` medidos lá a `0.005` não
  eram desacordo com `f_SBM = 17.96`: eram amolecimento de amplitude. A afirmação do artigo
  sobreviveu a um teste que podia refutá-la — e sobreviver é evidência **mais fraca** do que um
  desacordo teria sido (`L3.1`).
- **L14.2 Ressalva aberta e não explicada:** os nossos picos ficam `+0.049` a `+0.115 GHz`
  **acima** dos do artigo, e o desvio cresce com a amplitude — o nosso amolecimento é
  **~14 % mais fraco**. O `RA-1` era teste de **sinal e escala**, não de valor; logo os 14 %
  não reprovam nada, mas **não somem**.
- **L14.3 O `RA-2` é EXPLORATÓRIO**, e foi declarado assim antes. Ele observa que na menor
  amplitude `f_pico` e `f_SBM` coincidem a `0.40 σ`. **Não** é "a afirmação do artigo foi
  testada no limite linear". Quem fez o trabalho foi o `RA-1`.
- **L14.4** O alvo é **extração de figura em eixo logarítmico**, não dado dos autores.
- **L14.5** Um acoplamento (`A_int = 0.02`), um modo (SBM), um `α`, três amplitudes. O ponto de
  `0.005` vem do `E004R`, com grade de 5 frequências contra 7 das outras duas.
- **L14.6** `L-G` intocado. Décima quarta missão.

---

## 2. **Ação de sistema autorizada: compilar o mumax3**
Primeira ação de sistema autorizada neste laboratório. `CLAUDE.md` §2 exigia sim explícito;
está dado, e literal.

### Por que o mumax3 e não o OOMMF — correção de uma recomendação minha repetida
Eu recomendei o OOMMF por vários turnos. **Estava errado.** O `A002` já registrava que
`Oxs_DMExchange6Ngbr` **recusa** malha periódica e que `Oxs_DMI_C2v` tem simetria errada;
contornar exige **escrever uma extensão nova de DMI Cnv com PBC**. Isto é: eu escreveria
justamente o termo que o `AUDIT-001` identificou como **o risco discriminante** — o sinal do
DMI, onde o meu próprio código esconderia um erro. Uma verificação cuja peça crítica é escrita
por mim **não é independente onde importa**.

O `ARCHIVE/tools-mumax3-morto/` tem o **código-fonte** do mumax3 e o Go 1.22.6 (que executa),
não só o binário CUDA 12.9 que não roda. Verificado na fonte, **não suposto**: `cuda/dmi.cu` é
o kernel de **DMI interfacial** e trata **PBC nativamente** (`PBCx`, `PBCy` nas quatro
vizinhanças).

Compilar dá um solver onde troca, anisotropia, DMI interfacial, integrador e PBC são **dos
autores do mumax3**. É isso que ataca o `L-G`.

### O que esta autorização NÃO é
- **Não é missão.** Compilar é infraestrutura. **Usar** o mumax3 para atacar o `L-G` é missão
  nova, com pré-registro próprio, que Rodrigo lê antes de executar (`CLAUDE.md` §2).
- **Não fecha o `L-G`.** Ele só se move quando um número independente existir e for comparado.
- **Não autoriza** ação externa, freeze, nem apagar nada.

### Risco declarado antes
Pode não compilar (versão de CUDA, dependências). É **build padrão de código estabelecido**,
não desenvolvimento — mas o resultado é incerto e será relatado como for.
E a **`QA-02` ressuscita**: como expressar o acoplamento interlayer areal `A_int·m₁·m₂` no
mumax3 foi declarada "dissolvida, artefato da ferramenta abandonada". Volta, e terá de ser
**lida na fonte ou medida**, como o `A002` ensinou.

## Próximo head/estado
`STATE-2026-08-27-c`
