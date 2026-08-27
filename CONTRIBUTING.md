# Como contribuir

Este projeto é um registro científico sob metodologia FPM. Uma contribuição não deve apagar
a ordem temporal entre hipótese, execução, resultado e decisão humana.

## Fluxo

1. Abra uma issue descrevendo a pergunta, o defeito ou a reprodução proposta.
2. Trabalhe em uma branch curta e envie um pull request para `main`.
3. Explique no PR o objetivo, os arquivos alterados, como validar e quais limites permanecem.
4. Aguarde os checks automáticos e a revisão do responsável indicado em `CODEOWNERS`.

## Imutabilidade científica

- `LAB/MISSIONS/`: um pré-registro executado não é reescrito; acrescente um adendo datado.
- `LAB/RELEASES/`: um resultado publicado não é reescrito; corrija por novo adendo.
- `LAB/DECISIONS/`: uma decisão não é reescrita; supere-a por novo writeback.
- `LAB/EVIDENCE/`: não substitua artefatos selados. Uma nova execução recebe novo diretório.
- `LAB/STATE.md`: é o único documento científico reescrito no lugar.

Passar um teste técnico não equivale a aceite científico. Aceite e freeze são decisões
separadas do mantenedor.

## Dados e dependências

Não envie binários, toolchains, PDFs de terceiros ou resultados volumosos ao Git normal.
Consulte `DATA.md`. Dependências devem ser identificadas por versão, origem e hash sempre que
possível.

## Verificação local

Antes do PR:

```bash
python3 scripts/check_repository.py
```

Não inclua credenciais, tokens, dados pessoais desnecessários ou material sem autorização de
redistribuição.

