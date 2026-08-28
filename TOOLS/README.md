# TOOLS — dependências construídas, dentro do projeto

Categoria criada em 2026-08-27 (`WRITEBACK-021`). Existe por uma razão registrada:
o `ENVIRONMENT.md` nomeia como **fragilidade real** o fato de o OOMMF morar em outro projeto
(`pesquisa/kMC/`) — se aquele diretório mudar, o `A002` deixa de ser reproduzível.
**Não repetimos isso.** O mumax3 mora aqui dentro.

## `mumax3-bin` — segundo solver, independente
`mumax 3.11.1`, Go 1.22.6, CUDA 11.8, `cc=89` (RTX 4050). Hash em `SHA256-mumax3-bin.txt`.

Construído do **fonte** em `ARCHIVE/tools-mumax3-morto/mumax3-src`, copiado para `TOOLS/mumax3`
(o `ARCHIVE/` ficou intacto). Log completo em `BUILD-LOG.txt`; script em `build.sh`.

**O que precisou ser descoberto:** o Makefile força `-ccbin=/usr/bin/gcc`, e o gcc padrão aqui
é 12.2, que o CUDA 11.8 recusa. `gcc-11` está instalado; a correção é
`make CUDA_CC=89 NVCC_CCBIN=/usr/bin/gcc-11`. Está no `build.sh`.

**Por que ele e não o OOMMF:** o `A002` registrou que `Oxs_DMExchange6Ngbr` recusa malha
periódica e `Oxs_DMI_C2v` tem simetria errada — contornar exigiria eu **escrever** a extensão
de DMI Cnv com PBC, isto é, escrever o termo que o `AUDIT-001` identificou como o risco
discriminante. No mumax3 o DMI interfacial (`Dind`) e o PBC são **dos autores dele**:
`cuda/dmi.cu` trata `PBCx`/`PBCy` nativamente, e o binário cita Mulkers et al. PRB 95, 144401.

## Duas coisas a MEDIR antes de qualquer comparação, não supor
1. **Demag.** O mumax3 calcula kernel de demag por padrão. O nosso modelo **não tem demag**
   (`QA-01`: absorvido em `K₀`). Tem de ser desligado explicitamente e **verificado**.
2. **`QA-02` ressuscitou.** Como expressar o acoplamento interlayer **areal** `A_int·m₁·m₂` no
   mumax3 foi declarada "dissolvida, artefato da ferramenta abandonada". Volta, e a convenção
   tem de ser **lida na fonte ou medida** — foi assim que o `A002` descobriu `sigma = −A_int/2`
   no OOMMF, metade do que a fonte sugeria.

**Compilar não fecha o `L-G`.** Ele só se move quando um número independente existir e for
comparado. Isso é missão, com pré-registro próprio.
