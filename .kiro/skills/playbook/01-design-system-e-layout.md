# 01 · Design system e layout

Resumo do "Painéis AFL v3" (base: Despensa 2.0 do Estúdio Abrasel). Detalhe completo: `design-system.md` do RF.

## Princípio central: tudo que é estático vai no fundo

O fundo de cada página é uma imagem (SVG convertido em PNG a 2×) com: abas com texto, logo, rótulos e caixas dos filtros, molduras dos cards com sombra, acento colorido dos KPIs, trilho dos botões, legendas fixas, ícones (i) e a nota de rodapé. No Power BI ficam só **botões, segmentadores e visuais**, todos com fundo e borda desligados. Isso garante o mesmo desenho em qualquer máquina e deixa os visuais leves.

- O texto do fundo é convertido em vetor (Open Sans, substituto aberto do Segoe UI) por `texto_path.py`.
- O fundo é registrado no `report.json` com **sufixo numérico aleatório no nome** (o Desktop guarda cache pelo nome; ao regravar o PNG, mantenha o nome já registrado).
- A página usa ajuste **"Ajustar à largura"** (`FitToWidth`).

## Canvas e grade

- Largura **1920 px**; altura da página conforme o conteúdo (RF: 1580; RAIS: 1652). A rolagem é permitida.
- Grade de **12 colunas de 138,67 px, margem 40, gutter 16**:
  - `cx(i) = 40 + i·(138,67 + 16)`
  - `cw(n) = n·138,67 + (n−1)·16`
- Fundo branco `#FFFFFF`.

## Faixas verticais

| Faixa | y | Altura | Conteúdo |
|---|---|---|---|
| Abas + logo | 24 | 56 | grupos de abas de 224 px (gap 32 entre grupos) e logo Abrasel verde à direita |
| Filtros | 136 | 48 | rótulo no fundo (linha de base y=124) e caixa; "Limpar filtros" de 220 px à direita |
| Manchete | 196 | 118 | texto de até 2 linhas + linha de contexto |
| KPIs | 324 | 192 | 3 cards de 4 colunas |
| Linha 2 | 540 | 456 | gráfico principal (8 col.) + card de 4 col. |
| Linha 3 | 1020 | 520 | ranking/detalhe (8 col.) + card de 4 col. |
| Nota | 1572 | 56 | aviso metodológico (texto #B54708 sobre #FEF0C7) |

## Navegação em matriz

Abas em grupos (ex.: **Tema** × **Recorte**). A combinação forma uma página por célula (RAIS: 4 temas × 2 recortes = 8 páginas; RF: 12). A aba ativa é só desenho no fundo (laranja, sublinhado); as demais recebem um **botão transparente** por cima com ação `PageNavigation` direta (não use marcadores). Estados: normal transparente (revela o rótulo do fundo), hover `#F58220` com texto branco, press `#B86218`. Mudar uma dimensão preserva as outras. Gerador: `navegacao_rais.py` / `navegacao_matricial.py`.

## Cards

- Fundo branco, borda 1 px `#DDDDDE`, raio 8, sombra md (desenhada no fundo).
- Respiro 24. Título-afirmação em x+24, y+16. Corpo do visual em x+16.
- **(i) no canto superior direito**: ícone de 24 px em (x+w−38, y+40 como centro), coberto por um gatilho transparente de 84×62 (ver 02).
- KPI: acento de 4 px no topo, na cor do papel; visual HTML em x+20, y+12, 172 px de altura (altura menor corta os chips).
- Em cards estreitos (4 colunas): título com altura 100 → legenda em y+120 → gráfico em y+146. Título HTML com mais de 2 linhas rola e fica feio: **encurte o texto**.

## Tipografia

| Uso | Fonte |
|---|---|
| manchete | Segoe UI Semibold, 34 px (HTML) |
| título de card | Segoe UI Semibold 24 px + subtítulo 20 px |
| valor de KPI | Segoe UI Semibold 53 px, `tabular-nums` |
| eixos, legendas, rótulos de dado, notas | **mínimo 16 pt**; não reduza |

Dentro do HTML Content os números usam `font-variant-numeric: tabular-nums` (o visual não enxerga a fonte DIN).

## Cores

| Papel | Hex |
|---|---|
| AFL / ação / seleção | `#F58220` (pressionado `#B86218`, fundo suave `#FDF7F1`) |
| positivo / ativas | `#17B26A` |
| negativo | `#ED1C24` |
| texto | `#1D1E21` e `#434446` |
| neutros | `#DDDDDE` (borda e categorias neutras), `#E8E8E9` (divisórias), `#98A2B3` (seleção atual) |
| aviso | texto `#B54708` sobre `#FEF0C7` |
| roxo (mulheres/pirâmide) | `#7F56D9` |

Regras: uma cor tem **um só significado** em todas as páginas; o laranja do AFL **nunca** aparece no mesmo gráfico que vermelho ou rosa; no máximo 3 cores de dado por gráfico; texto nunca leva a cor da série.

## Gráficos

- **Série no tempo = linha.** Barras só para comparar categorias. Séries com quebra de fonte são **interrompidas** (ver 03 e 04), nunca ligadas.
- Para "quanto cresceu por ano", prefira colunas de variação anual a índice com duas bases (índice base 100 em dois trechos confunde).
- Rankings: nomes oficiais, números completos, AFL em laranja contra neutro `#DDDDDE`, modo foco habilitado quando há muitas linhas.
- Eixo de anos em cards estreitos: eixo contínuo (rótulos espaçados), senão os anos giram e embolam.
