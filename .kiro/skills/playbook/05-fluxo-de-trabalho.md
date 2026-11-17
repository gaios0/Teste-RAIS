# 05 · Fluxo de trabalho (geradores, Git, testes)

## Estrutura de um projeto

```
<painel>.pbip
<painel>.Report/definition/…        # PBIR: páginas, visuais, report.json
<painel>.SemanticModel/definition/… # TMDL: tabelas, medidas, relações
scripts/                            # geradores Python
docs/                               # planejamento, handoff, fundos, playbook
assets/                             # fontes, ícones (lucide), logo
```

## Geradores (RAIS)

| Script | Faz |
|---|---|
| `modelo_base.py` | calendário, tabelas locais (D_Comparavel, D_AflAtividade, D_Rank_Divisao, D_Indicador, D_Info), relações e **todas as medidas** em `_medidas.tmdl` |
| `dax_rais*.py`, `dax_dicas.py`, `dax_tooltips.py` | definição das medidas por tema (HTML, séries, rankings, tooltips) |
| `info_rais.py` | textos dos (i) → tabela `D_Info` |
| `fundo_rais.py` | fundo SVG → PNG (via Edge headless) |
| `config_paginas.py` | acentos, legendas, trilhos e notas de cada página |
| `pbir_rais.py` | construtores de visuais PBIR |
| `pagina_rais.py` | monta páginas, visuais, tooltips, navegação e `pages.json` |
| `navegacao_rais.py` | botões das abas |
| `testar_paginas.py` | avalia as medidas no modelo aberto (ver abaixo) |
| `seguranca.py` | trava contra sobrescrever edições manuais |

**Regerar:** `python modelo_base.py` e `python pagina_rais.py --refazer` (a geração dos fundos leva alguns minutos; rode em segundo plano). Os scripts são idempotentes.

## Regra de ouro: edições manuais

Quem ajusta algo à mão no Desktop e salva cria mudanças no working tree que **os geradores apagam**. Por isso:

1. `seguranca.py` interrompe os geradores se houver alterações não commitadas em páginas, recursos ou modelo. Use `--forcar` só depois de commitar ou copiar o estado.
2. Se alguém editou à mão, **primeiro commite o estado**, depois leve a mudança para o gerador, só então regenere.
3. Pedir ao usuário "Salvar como" em outra pasta é a forma segura de recuperar o que está só na memória do Desktop.

## Git

- Uma branch por entrega coesa (`feature/…`, `fix/…`, `chore/…`).
- Stage **sempre por caminho específico**; nunca `git add -A` / `git add .` em árvore com mudanças incidentais do Power BI.
- Nunca `reset --hard`, `clean -fd`, force push ou remoções em massa sem pedido explícito.
- Peça confirmação antes de excluir qualquer coisa.
- Mantenha fora de commits de feature: `editorSettings.json`, caminhos pessoais em `expressions.tmdl`, metadados e `diagramLayout.json`, `__pycache__`.
- Commits terminam com a linha de coautoria definida pelo time/ferramenta.

## Testar medidas

- Com o Desktop aberto e o modelo carregado, `testar_paginas.py <alvo>` monta um `DEFINE MEASURE` de **todas** as medidas e avalia consultas por tema (`emp`, `perfil`, `salario`, `contrata`, `ajustes`). Qualquer erro de sintaxe em uma medida derruba todas as consultas, então ele serve como compilação.
- Tabelas locais novas só existem depois de reabrir o PBIP e clicar em **Atualizar agora**. Antes disso, é possível simular a tabela com `DEFINE TABLE`.
- **Sem o Desktop aberto não há como testar DAX.** Gere, commite, e peça que a pessoa reabra o PBIP.

## Validação mínima antes de declarar pronto

- JSONs alterados abrem sem erro (`json.load` / `ConvertFrom-Json`).
- `git diff --check` só nos arquivos da tarefa.
- Nomes de medidas, campos e IDs de página conferidos por busca.
- Nada fora do escopo está em stage.
- Reabrir o PBIP e olhar: TMDL/DAX, renderização, hover, drill, tooltips, navegação.
- **Diferencie validação estrutural (JSON válido) de teste real no Desktop.** Nunca afirme que uma interação funciona só porque o JSON é válido.

## Ambiente (Windows)

- Python com `PYTHONIOENCODING=utf-8`.
- Edge headless (`msedge.exe --headless --screenshot`) renderiza SVG/HTML → PNG.
- Consultas ao modelo aberto por ADOMD no `msmdsrv` local; capturas de tela do Desktop por script PowerShell.
- `git fetch/push` às vezes travam: use `timeout`.
