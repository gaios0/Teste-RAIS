# 07 · Prompt-modelo para a IA

Cole o bloco abaixo no início da conversa, preenchendo os campos entre `<>`. Ele foi escrito para ferramentas de código (Claude Code) com acesso ao repositório; em ferramentas sem acesso, anexe os arquivos `01` a `05` e `08` deste playbook.

---

```text
Você vai me ajudar a construir/alterar um painel Power BI (projeto PBIP) no padrão "Painéis AFL" da Abrasel.

CONTEXTO DO PAINEL
- Nome e objetivo: <ex.: RAIS Emprego Formal — perguntas do Painel 2 do Congresso>
- Fonte de dados e defasagem: <...>
- Páginas (matriz): <ex.: 4 temas × 2 recortes (Todos os setores | AFL)>
- Pergunta de negócio desta tarefa: <...>

ANTES DE AGIR, LEIA (nesta ordem)
1. docs/playbook/README.md e os arquivos 01, 02, 03, 05, 08
2. docs/handoff-atual.md (estado funcional) e `git status --short --branch`
3. Para conteúdo/números: docs/playbook/04 e o planejamento do painel

REGRAS INEGOCIÁVEIS
- Converse em português do Brasil. Se algo for ambíguo, pergunte antes de fazer.
- Peça confirmação antes de excluir qualquer coisa ou de qualquer ação difícil de reverter.
- NÃO rode geradores que regravam páginas/modelo (pagina_rais.py --refazer, modelo_base.py) se houver alterações não commitadas: podem ser edições manuais minhas no Desktop. Mostre o git status e me pergunte.
- Git: stage só por caminho específico; nunca git add -A/., reset --hard, clean -fd ou force push.
- Mantenha o design system: tudo que é estático vai no fundo; visuais com fundo/borda desligados; texto mínimo 16 pt; uma cor, um significado; laranja #F58220 = AFL.
- Dados: nunca somar estoques de períodos diferentes; interromper séries na quebra de fonte; todo percentual com denominador claro; diferença entre percentuais em p.p.; valores nominais declarados.
- A página "Todos os setores" deve ser revisada gráfico a gráfico: nenhum gráfico pode apenas repetir o AFL.
- O HTML Content não aceita tooltip de página: use o padrão (i) com gatilho transparente.
- Diferencie "JSON válido" de "testado no Power BI Desktop". Se o Desktop estiver fechado, diga que o DAX não foi testado.

COMO TRABALHAR
- Faça mudanças pequenas e coesas; commit por entrega.
- Para cada medida nova: descrição, pasta, formato, escape do texto dinâmico, VAR antes de RETURN.
- Ao terminar: liste o que foi feito, o que NÃO foi validado no Desktop e o que preciso fazer (reabrir o PBIP, Atualizar agora, etc.).

TAREFA
<descreva aqui o que quer>
```

---

## Variações úteis

- **Só texto/conteúdo:** troque "COMO TRABALHAR" por "Proponha manchetes e títulos no padrão do `04`; não altere arquivos".
- **Só revisão:** peça que a IA percorra o `06-checklist-novo-painel.md` página por página e liste o que falha, sem alterar nada.
- **Painel novo:** peça primeiro a prévia em HTML/PNG e o planejamento (`docs/planejamento-*.md`); só depois o modelo e as páginas.
