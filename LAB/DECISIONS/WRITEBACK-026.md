# WRITEBACK-026 — hardening de agência verificável no FPM

Data: 2026-08-27 · Autoridade: Rodrigo

## Pedido humano (literal)

> "Meu amigo junto com sua ia criou o seguinte regras [...]. Consigos copiar e aprimorar
> estas ideias em nosso FMR?"

## Interpretação registrada — e convite a corrigir

Interpretei `FMR` como `FPM` e o pedido como autorização para incorporar ao método o delta
operacional útil da conversa compartilhada, **sem** autorizar missão, execução científica,
aceite, freeze, publicação ou nova ação externa. Se a intenção era apenas pedir uma opinião,
Rodrigo pode corrigir e este writeback será superado, nunca apagado.

Fonte de método consultada:
`https://chatgpt.com/share/6a906bc6-a8f4-83e9-8e9e-889423113ad7`.
Ela orienta processo; não é evidência científica deste laboratório.

## Delta adotado

O `CLAUDE.md` §6.2 passa a explicitar:

1. `RESEARCH_ENGINEERING` pode ser altamente agentiva; `SCIENTIFIC_JUDGMENT` permanece sob
   autoridade humana.
2. Artefato, evidência material, evidência aceita, claim aceito e publicação são estados
   distintos; nenhuma promoção é automática.
3. Executor não controla irrestritamente implementação, teste e critério. Independência é
   declarada por eixo de linhagem, não por contagem de agentes.
4. Referência que sustenta claim nasce de retrieval verificável, com metadados e conteúdo
   conferidos.
5. Evidência nova leva manifesto compacto e verificável de proveniência de IA, sem
   chain-of-thought, segredo ou logging integral.

## Aprimoramentos locais sobre a proposta original

- O manifesto sugerido em YAML virou **JSON validável por máquina**.
- Diretórios históricos têm baseline explícito; não se fabrica proveniência retroativa.
- Diretório de evidência futuro sem manifesto falha no verificador e no hook de fim de turno.
- A independência registra eixos compartilhados e independentes; “outro agente” sozinho não
  conta como validação independente.
- Verificar DOI/metadados não basta: o trecho claim-bearing também precisa ser conferido.

## O que não foi importado

Não foram adotados múltiplos agentes por padrão, logging integral, peer review automático como
gate final, taxonomia extensa de autonomia, nem liberdade para o sistema escolher sozinho a
agenda científica. O FPM existente já oferece pré-registro, selagem, aceite humano e limites
de claim; duplicar essas camadas só aumentaria burocracia.

## Efeito no estado

Mudança de método, não missão. Nenhum claim científico muda. `MISSION-A005R` e as missões
autorizadas em `WRITEBACK-024/025` mantêm exatamente seus estados e gates.
