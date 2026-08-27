# RELEASE-I001 — a deriva espúria é REAL; o rastreador está limpo

Missão: `MISSION-I001` · Autorizada por `WRITEBACK-013` · Execução: 2026-08-25
`human_acceptance: PENDING` · Evidência: `LAB/EVIDENCE/I001/`

## 1. Veredito: `C-real`. **Gate `G-I001` passou.**
A deriva espúria de `0.917 cm/s` que o `E003` mediu fora do eixo é **movimento real da
magnetização**, não viés do meu estimador. A **ressalva 1 do `E003` fecha.**

## 2. `IV-1` — rastreador sobre estado CONGELADO (o teste decisivo)
Magnetização **imóvel**, 10 001 chamadas ao rastreador, mesma cadência da corrida viva.
Qualquer deslocamento reportado seria 100 % do instrumento.

| localizador | `θ = 30°` | `θ = 0°` |
|---|---|---|
| (a) origem realimentada (o do `E002`/`E003`) | `2.01e−11 cm/s` | `2.77e−12` |
| (b) origem fixa | `5.00e−12` | `3.12e−12` |
| (c) centroide do núcleo (sem `ρ`) | `2.66e−12` | `6.30e−12` |

Deslocamento total acumulado: **`0.0000 pm`**. Razão congelado/vivo: **`2.2e−11`** —
**onze ordens de grandeza** abaixo do critério de 1 % registrado no §2.

**O controle a `θ = 0` importa tanto quanto:** ele exonera o rastreador **também** na condição
em que o `E002` rodou. A afirmação do `RELEASE-E003.md` §3 de que o `E002` não está
contaminado fica **reforçada por medida direta**, não só por decaimento.

## 3. `IV-2` — três localizadores na corrida viva
`θ = 30°`, sem excitação, janela de 10–20 ns:

| localizador | `\|v\|` | ângulo | realimenta? |
|---|---|---|---|
| (a) | `0.91745 cm/s` | `−153.875°` | sim |
| (b) origem fixa | `0.91745` | `−153.875°` | não |
| (c) centroide do núcleo | `0.91745` | `−153.875°` | não |

`(b)/(a) = 1.0000`, `(c)/(a) = 1.0000`.

### A concordância exata é DIAGNÓSTICA, não suspeita
Se o par transladar **rigidamente**, `m(r,t) = m₀(r − vt)`, então qualquer funcional do tipo
centroide satisfaz `C[m(·,t)] = C[m₀] + vt` **por identidade** — todos os localizadores dão
exatamente a mesma velocidade. A igualdade em quatro casas é, portanto, a assinatura de que o
movimento é **translação rígida**, sem deformação. Registro isto porque a leitura ingênua
("bom demais para ser verdade") levaria à conclusão errada.

O localizador **(c) não usa carga topológica nem Berg–Lüscher** — é outro funcional. Uma
leitura errada compartilhada entre (a) e (b) não sobreviveria a ele.

## 4. O que isto fecha, e o que não fecha
**Fecha:** a ressalva 1 do `E003`. O artefato fora do eixo é **de rede, não de régua**.
Nenhuma medida de posição deste laboratório está sob suspeita por este caminho.

**Não fecha:**
- **A causa física do movimento real continua conjectural.** Que seja força tipo Peierls
  convertida em deriva giroscópica é hipótese do `RELEASE-E003.md` §3, **não testada aqui**.
  `I001` mostrou *que* é real e *que* é rígido; não mostrou *por quê*.
- **`L-G` intocado.** Instrumento próprio testado contra si mesmo em outra condição. Não é
  verificação independente; o `AUDIT-002` continua sendo a única checagem cega da régua, e o
  `L5.3` dela (travessia de fronteira periódica não testada) **permanece aberto** — `I001` não
  o tocou.
- Um único estado, um ângulo, um acoplamento.

## 5. Efeito no `E004`
O piso do `EF-0` do `MISSION-E004` estava justificado por um número (`0.77 %` do `E002`)
medido com o rastreador aqui testado — circularidade detectada **antes** de qualquer corrida e
corrigida no `ADENDO-001` daquele pré-registro. Com `C-real`, aquele número volta a ser medida
limpa; ainda assim o `EF-0` revisto **não o usa**, por ser critério relativo ao próprio dado.

## 6. Custo
`66.5 s` (congelado, θ=30) + corrida viva de 20 ns + controle congelado θ=0. Total < 10 min.

## 7. Próxima decisão humana
Aceitar / aceitar-com-limitações / revisar / rejeitar. Nada congelado.
