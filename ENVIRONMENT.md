# ENVIRONMENT.md — dependências externas deste laboratório

Verificado em **2026-08-25**. Cada resultado aceito depende de algum item desta lista; se um
deles mudar, o resultado correspondente pode deixar de ser reproduzível.

## Máquina
| item | valor |
|---|---|
| GPU | NVIDIA GeForce RTX 4050 Laptop (`sm_89`) |
| driver | 535.261.03 (CUDA 12.2) |
| `nvcc` | release 11.8, V11.8.89 |
| Python / numpy | 3.x / numpy 1.24.2 |
| SO | Linux 6.1.0 (Debian) |

## Ferramentas por missão

| missão | ferramenta | onde | risco |
|---|---|---|---|
| `R001`, `R002`, `E001` | código CUDA próprio (`saf.cu`, `saf_dyn.cu`) | `LAB/EVIDENCE/<missão>/` | nenhum — selado com hash |
| `AUDIT-001`, `AUDIT-002` | `codex-cli 0.149.1`, modelo `gpt-5.6-sol` | `~/.nvm/.../bin/codex` | serviço externo; versão e modelo registrados nos releases |
| `A002` | **OOMMF 2.0b0** | ⚠ `/home/rodrigo/pesquisa/kMC/micromag/oommf_work/oommf` | **fragilidade real — ver abaixo** |

### ⚠ Fragilidade conhecida: o OOMMF mora em outro projeto
O OOMMF que produziu o `RELEASE-A002` **não está dentro do `SAF/`**. Ele está no projeto
`kMC`. Se aquele diretório for movido, renomeado ou limpo, o `A002` deixa de ser reproduzível
— e o `A002` é o único resultado com solver independente.

Extensões locais necessárias, **compiladas** naquele binário:
`Oxs_TwoSurfaceExchange` (estoque), `Oxs_DMExchange6Ngbr` (extensão local),
`Oxs_PeriodicRectangularMesh`, `Oxs_CGEvolve`/`Oxs_MinDriver`.

Recompilar do zero não é trivial: o `DMExchange6Ngbr` é extensão de terceiros que precisa ser
colocada em `app/oxs/local/` e o OOMMF reconstruído.

**Mitigação recomendada, não executada** (mover ou copiar toca outro projeto e não foi
autorizado): copiar a árvore do OOMMF para `SAF/ARCHIVE/oommf-2.0b0/`, ou ao menos registrar
o hash do binário `oxs`.

## Como rodar (diretório de trabalho importa)
Os binários deste laboratório escrevem em **caminhos relativos**. Rode sempre a partir da raiz
do projeto:

```
cd /home/rodrigo/pesquisa/SAF
./LAB/EVIDENCE/E001/saf_dyn ev1
./LAB/EVIDENCE/E001/saf_dyn ev3 sbm 10
./LAB/EVIDENCE/R002/saf classify <Aint_mJm2> <K0_MJm3>
```

Rodar de outro diretório grava em lugar errado ou falha em silêncio. Isto **não** foi
corrigido no código de propósito: `saf_dyn.cu` está em evidência aceita e hasheada, e não se
edita evidência aceita por conveniência.

## Serviços externos (INV-16)
Qualquer uso do `codex` envia dados para a OpenAI e exige **autorização explícita e separada**
de Rodrigo. Autorizações concedidas até hoje: `WRITEBACK-005` (artigo, etapa cega) e
`WRITEBACK-008` (artigo + descrição de formato). A **etapa 2** — enviar o `saf.cu` — continua
**não autorizada**.
