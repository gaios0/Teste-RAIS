# Playbook de painéis Power BI (Abrasel · Painéis AFL)

Conjunto de documentos para criar novos painéis Power BI com o mesmo padrão visual, de dados e de trabalho dos painéis **Receita Federal Empresas e Mercado** (RF) e **RAIS Emprego Formal**. Serve para pessoas e para quem usa uma IA (Claude Code, Copilot, ChatGPT) para ajudar a construir.

## Como usar com uma IA

1. Abra a IA na pasta do projeto (ou anexe os arquivos desta pasta).
2. Cole o prompt de `07-prompt-para-ia.md` e preencha o que for do painel novo.
3. Peça que ela **leia primeiro** `01`, `02`, `03` e `05`. Os documentos `04` e `06` entram quando a tarefa for de conteúdo ou de entrega.
4. Exija a validação do `06-checklist-novo-painel.md` antes de dar algo por pronto.

## Índice

| Arquivo | Para quê |
|---|---|
| `01-design-system-e-layout.md` | Grade, faixas, cards, tipografia, cores e o que vai no fundo |
| `02-padroes-power-bi-pbir.md` | Como os visuais, filtros, tooltips, navegação e drill são montados no PBIR, e o que não funciona |
| `03-padroes-dax-e-html.md` | Medidas HTML (KPI, manchete, título), séries com quebra, cuidados de DAX |
| `04-regras-de-conteudo-e-dados.md` | Como escrever e o que nunca fazer com os números (denominador, quebra de série, AFL × Comparáveis) |
| `05-fluxo-de-trabalho.md` | Geradores em Python, Git, trava contra sobrescrita, testes com o Desktop |
| `06-checklist-novo-painel.md` | Passo a passo e checklist de validação |
| `07-prompt-para-ia.md` | Prompt-modelo para colar na IA |
| `08-armadilhas-conhecidas.md` | Erros que já aconteceram e como evitar |

## Fontes de verdade

- Design system completo (tokens, componentes): `kiro-paineis-afl/.kiro/steering/design-system.md` e `design-system/project/` no repositório do RF.
- Estado funcional de cada painel: `docs/handoff-atual.md` de cada repositório.
- Planejamento do RAIS: `docs/planejamento-painel-rais.md`.

Em caso de conflito, vale o código e o handoff do painel; estes documentos resumem o padrão.
