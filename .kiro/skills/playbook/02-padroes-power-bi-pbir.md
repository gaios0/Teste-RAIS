# 02 · Padrões Power BI (PBIR)

Os painéis são projetos **PBIP** (relatório em PBIR + modelo em TMDL, texto puro). Muita coisa é gerada por scripts Python (ver 05). Este documento diz **como cada peça é montada** e o que já se descobriu que não funciona.

## Tipos de visual usados

| Peça | `visualType` | Observação |
|---|---|---|
| Manchete, KPI, título de card, tabelas HTML | `htmlContent443BE3AD55E043BF878BED274D3A6865` | visual personalizado (HTML Content); precisa estar em `publicCustomVisuals` no `report.json` |
| Série | `lineChart` | marcador + linha de 3 px; séries "Pré" e "Pós" quebra com a mesma cor |
| Variação anual | `clusteredColumnChart` | sem rótulos de dados; detalhe no tooltip |
| Ranking | `clusteredBarChart` | ordenado pela medida, rótulo completo fora da barra |
| Pirâmide etária | **`barChart`** | `barChart` = barra **empilhada**. `stackedBarChart` não existe e gera "visual personalizado não encontrado" |
| Filtros | `slicer` | `Dropdown` para a maioria; ver "Filtro de comparabilidade" |
| Botões de indicador/setor | `advancedSlicerVisual` | estilo Cards, tema cor 5 (laranja) no hover/press/selecionado |
| Limpar filtros | `image` | 3 estados (SVG registrados) + ação `ClearAllSlicers` |
| Abas | `actionButton` | `PageNavigation` direto |
| Gatilho do (i) | `clusteredColumnChart` | mini-coluna 100% transparente (ver abaixo) |

Todo visual: título, fundo, borda e cabeçalho desligados (`visualContainerObjects`), porque a moldura está no fundo. **Exceção:** visuais com modo foco/drill mantêm o cabeçalho (`visualHeader.show = true`; ele só aparece ao passar o mouse).

## Filtros (segmentadores)

- Sincronização por `syncGroup` (`filterChanges: true`, `fieldChanges: false`) com um nome por filtro (ano, UF, sexo, escolaridade, raça/cor, setores, divisão).
- **Ano**: `Dropdown`, `strictSingleSelect`, com filtro inicial no segmentador (o ano mais recente).
- **Limpar filtros**: botão-imagem com `ClearAllSlicers`.
- **Filtro de comparabilidade ("Setores")** — regra do RF, não mude: **não** use lista "Todos / Sim / Não". Use **caixa de marcar com um só item**, "Só os comparáveis ao AFL". Implementação: segmentador em modo `Basic` sobre a coluna rótulo (`comparavel_AFL_rotulo`), com **filtro no visual** pela coluna técnica (`comparavel_AFL = "Sim"`), que oculta a linha "Não" sem mudar a chave usada no DAX. Desmarcado = todos os setores.
- Páginas do recorte "AFL" levam **filtro de página** (`D_Cnae[setor_afl] = "Sim"`).

## Interações

- O gráfico de série **ignora o segmentador de Ano** (`NoFilter`) e **não filtra** os demais visuais.
- Botões de setor/indicador filtram só o que precisam (ranking) e usam `NoFilter` nos outros.
- Por padrão, clicar em barra filtra o resto (`drillFilterOtherVisuals: true`) — é o comportamento desejado nos gráficos de geografia.

## Geografia: UF → município (padrão RF)

Gráfico de barras com **hierarquia de dois níveis**: `Category` = [UF (ativo), município (**`"active": false`**)]. O usuário clica numa UF (filtra a página) e desce para municípios pelo cabeçalho do gráfico (modo drill). A medida precisa funcionar nos dois níveis: use `ISINSCOPE(F_rais[municipio])` para aplicar **base mínima** só no nível município (evita ranquear município minúsculo pelo percentual). Não corte em "top 10" no nível UF: mostre todas as UFs (rolagem + modo foco).

## Tooltips

**Limitação importante:** o **HTML Content não aceita tooltip de página**. Por isso:

1. **(i) informativos**: ícone desenhado no fundo + **gatilho transparente** (mini `clusteredColumnChart` nativo de 84×62 px, `fillTransparency 100`, rótulos e eixos desligados, `responsive=false`) com a medida constante `Info_Gatilho_Valor` e a categoria `D_Info[Chave]` **fixada por filtro de visual**. O tooltip é uma **página de tooltip** (`type: Tooltip`, `visibility: HiddenInViewMode`) com um HTML que lê a linha da `D_Info`.
2. **Texto compartilhado**: tabela `D_Info` (colunas Chave, Classe, Titulo, Extra, Destaque, CorBorda, CorFundo, P1..P5; importada por M "Enter data"), medida `Info_Texto_HTML` e **3 páginas por tamanho** (P 720×370, M 760×440, G 800×580). A classe vem do comprimento do texto. Para mudar um texto, edite a `D_Info`.
3. **KPI com exemplo numérico**: página de tooltip própria com uma medida HTML que usa os números da página ("para cada R$ 100 dos homens, as mulheres recebem R$ 88"), aberta pelo mesmo gatilho do (i).
4. **Gráficos nativos** (barras, colunas, linhas): `visualTooltip` = `{ section: <id da página>, type: 'Canvas', show: true }`. A página recebe o contexto do ponto sobrevoado; a medida HTML usa `SELECTEDVALUE` da categoria. Um tooltip por tipo de gráfico, compartilhado entre os recortes Todos/AFL (a medida detecta a página AFL por `SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"`).

Design do tooltip de gráfico: título do ponto (24 px), subtítulo de contexto (18 px cinza), linhas **AFL / Comparáveis / Seleção atual** com marcador de cor e valor, e uma **frase de leitura** num bloco de destaque laranja suave. A linha "Seleção atual" some na página AFL.

## Registro de recursos e tema

- Tema personalizado (`Pain_is_AFL___Est_dio_Abrasel_….json`) e SVG do botão limpar são copiados do RF.
- Imagens de fundo e SVGs ficam em `StaticResources/RegisteredResources` e são listados em `report.json` (`resourcePackages`).
- Quebras de linha e barras invertidas em strings de código gerado: ver `08-armadilhas-conhecidas.md`.

## Páginas de tooltip

JSON mínimo: `type: "Tooltip"`, `visibility: "HiddenInViewMode"`, `displayOption: "FitToPage"`, largura/altura do cartão; um visual HTML ocupando a página inteira. Entram no `pageOrder` depois das páginas de conteúdo.
