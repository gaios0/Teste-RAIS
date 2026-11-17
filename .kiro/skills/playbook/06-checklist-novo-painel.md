# 06 · Checklist para um painel novo

## 1. Antes de desenhar

- [ ] Perguntas de negócio escritas (quem pergunta, que decisão ajuda). Cada página responde a perguntas, não exibe tabelas.
- [ ] Fonte de dados, periodicidade, **defasagem** e quebras de série conhecidas e registradas.
- [ ] Definição do universo (AFL, Comparáveis) vinda da dimensão oficial, não recriada.
- [ ] Matriz de páginas definida (ex.: Tema × Recorte) e nomes das abas.
- [ ] Decisões de produto registradas no planejamento: nominal ou real, piso estatístico, denominador de cada percentual.
- [ ] Prévia em HTML/PNG das páginas aprovada antes de construir no Power BI (barato de mudar).

## 2. Modelo

- [ ] Dimensões conformadas (calendário, UF, CNAE, grupo de setor) com relações explícitas.
- [ ] Tabelas locais de apoio por M "Enter data" (rótulos, ranking, indicadores, `D_Info`).
- [ ] Medidas por tema em módulos Python; uma medida-base por conceito e variantes por grupo.
- [ ] Toda medida com descrição, pasta e formato; auxiliares ocultas.

## 3. Página (cada célula da matriz)

- [ ] Fundo gerado (abas, filtros, cards, (i), nota) e registrado com nome estável.
- [ ] Manchete + 3 KPIs + 4 cards; títulos-afirmação que cabem em 2 linhas.
- [ ] KPIs com chips AFL × Comparáveis e 172 px de altura.
- [ ] Filtros: Ano (único, inicial = último), UF, sexo, escolaridade, raça/cor; "Setores" como caixa de marcar de um item e "Divisão" na página Todos; CNAE AFL na página AFL; Limpar filtros.
- [ ] Gráfico de série com quebra de fonte interrompida; ignora o filtro de Ano.
- [ ] **Página "Todos os setores" revisada gráfico a gráfico** (nenhum gráfico apenas repete o AFL; existe "Seleção atual").
- [ ] Gráficos de UF com drill UF → município e base mínima nos municípios.
- [ ] Rankings com modo foco e AFL em laranja.
- [ ] (i) em todos os cartões; tooltip de página em todos os gráficos nativos.
- [ ] Navegação matricial entre as páginas; aba ativa só desenhada.
- [ ] Nota de rodapé com a ressalva metodológica da página.

## 4. Validação (no Power BI Desktop, não só por JSON)

- [ ] Reabrir o PBIP, atualizar tabelas locais, rodar `testar_paginas.py`.
- [ ] Todas as medidas HTML devolvem texto sem erro nos recortes Todos e AFL e com filtros de UF, setor e divisão.
- [ ] Números conferidos contra uma consulta independente (ex.: soma por UF = total).
- [ ] Texto não é cortado (manchete, KPI, títulos, rótulos); legendas não encostam nos títulos.
- [ ] Hover/press das abas, clique nas UFs, drill, modo foco, (i), tooltips, Limpar filtros.
- [ ] Série não atravessa a quebra; 2022 e o primeiro ano aparecem como "sem comparação".
- [ ] Texto ≥ 16 pt; nenhuma cor com dois significados.
- [ ] Acessibilidade: textos alternativos nos botões (`altText`), contraste do texto.

## 5. Entrega

- [ ] Handoff atualizado (o que foi feito, o que **não** foi validado no Desktop, IDs de páginas e visuais).
- [ ] Commit por caminho específico; mudanças incidentais do Power BI fora do commit.
- [ ] Documentos deste playbook atualizados se algum padrão mudou.
