# Painel RAIS · Emprego Formal — handoff (02/11/2026)

## Estado
- **Etapa 1 feita e vista no Desktop:** tema **Empregos** (Todos os setores e AFL). Faltam: Quem trabalha, Quanto ganha e Quem contrata (6 páginas), tooltips nativos/(i) compartilhados e a navegação entre as 8 páginas (padrão do RF: `PageNavigation` sobre as abas).
- Modelo: `scripts/modelo_base.py` gera `D_Calendario`, tabelas locais (`D_Comparavel`, `D_AflAtividade`, `D_Rank_Divisao`), relações e `_medidas` (medidas-base + `dax_rais.py`). Testes: `scripts/testar_paginas.py emp` (usa `DEFINE MEASURE`, não precisa reabrir o Desktop).
- Páginas: `scripts/pagina_rais.py` (recusa sobrescrever; `--refazer` recria) + `pbir_rais.py` (construtores de visuais) + `fundo_rais.py` / `config_paginas.py` (fundo SVG/PNG por página). Fundos em `docs/fundos/`, prévias em `docs/previa/`.
- Página em branco original (`533042cd0022947b421a`, "Página 1") mantida no fim da ordem: apagar com confirmação.

## Regras (decisões do Sabino)
- Remuneração: salário de dezembro, R$ nominais, sem deflação; média = soma ÷ qtd de salários válidos; mediana da `F_Mediana`; rodapé "Valores nominais, remuneração de dezembro".
- Comparação de referência sempre **AFL × Comparável** (sem Demais nem total do setor privado); a página Todos os setores tem a caixa "Só os comparáveis ao AFL".
- Quebra de 2022 (eSocial): variação de 2022 sobre 2021 = BLANK; linhas não atravessam a quebra (séries Pré 2009–2021 e Pós 2022 em diante); crescimento médio parte do início do trecho; primeiro emprego só até 2021.
- Gráficos de série em **linha** (índice base 100 no início do trecho); barras só para comparar categorias. Cores: AFL #F58220 só contra cinza; sexo roxo/verde-azulado (novo).
- "Ajustar à largura" (displayOption FitToWidth), canvas 1920 × 1652.

## Operação
- Tabelas locais importadas (calendário etc.) precisam de **Atualizar agora** na primeira abertura (o PBIP não guarda cache). Ano padrão do segmentador: 2025 (fixo no visual; atualizar quando entrar 2026).
- Ao regenerar páginas com o Desktop aberto: feche sem salvar e reabra.

## Ajuste visual — 06/11/2026
- Os campos de filtro dos oito fundos ficaram sem contorno cinza (traço branco), mantendo o Power BI sem fundo e sem borda sobre o desenho estático.
- Foi incluída, no topo de todas as páginas de conteúdo, a faixa **INFORMAÇÕES PARA LEITURA**. O mouse sobre a faixa abre o tooltip compartilhado `a3d1f2c4e6b8097a1c60`, com glossário RAIS: estoque de vínculos em 31/12, defasagem, quebra RAIS/eSocial em 2022, AFL × Comparáveis, remuneração nominal, p.p., cor/raça e CNAE.
- Validação feita: JSONs do relatório desserializados e fundos PNG renderizados/inspecionados. **Ainda não testado no Power BI Desktop:** abertura do tooltip, renderização do HTML/DAX e comportamento do painel após recarregar o PBIP.

## Ajuste de filtros — 09/11/2026
- Nas quatro páginas **Todos os setores**, o filtro superior de Divisão foi removido; o fundo foi atualizado para não manter o elemento estático correspondente.
- Os slicers dropdown ficaram sem contorno visível; o seletor de setores principais agora não tem preenchimento no estado normal e mantém preenchimento somente em hover/seleção.
- O filtro passou a exibir exclusivamente a opção **Somente comparáveis ao AFL**. Desmarcado, considera os setores comparáveis e os demais, sempre com AFL excluído nas páginas Todos os setores.
- Os gráficos de UF usam barras verdes (`#17B26A`). A faixa de informações recebeu a mesma margem vertical zero do padrão ajustado na página Empregos · Todos os setores.
- Validação estrutural: JSONs das páginas e visuais desserializados; a abertura no Power BI Desktop continua necessária para conferir a renderização e atualizar a tabela local `D_Comparavel`.

## Correção de acabamento — 09/11/2026
- As caixas dos filtros voltaram a ter exclusivamente a moldura `#DDDDDE` desenhada no fundo; os segmentadores permanecem sem borda própria.
- O fundo das páginas Todos os setores foi recomposto sem **Divisão** e com Localização, Sexo, Escolaridade e Raça/cor deslocados para a esquerda; os visuais sobrepostos seguem a mesma geometria.
- O segmentador Setores recebeu também o `filterConfig` técnico do padrão da Receita Federal (`D_Comparavel[comparavel_AFL] = "Sim"`), garantindo uma única caixa de marcar.
- As oito medidas de manchete passaram de 34 px para 36 px (linha de 42 px), para evitar a barra de rolagem lateral.

## Ajuste de Setores — 09/11/2026
- O item único do filtro passou a se chamar **Só os comparáveis ao AFL**.
- A largura de Setores nas páginas Todos os setores é 360 px; Localização, Sexo, Escolaridade e Raça/cor foram deslocados e redimensionados no PBIR e no fundo para manter os gaps, sem sobreposição.
- Os quatro PNGs de fundo foram renderizados novamente com as molduras estáticas claras dos campos.

## Reaplicação por cache — 09/11/2026
- A leitura dos arquivos confirmou manchetes em 36 px / linha de 42 px e molduras estáticas nos SVGs, mas o Desktop ainda podia servir o PNG antigo pelo nome.
- Os quatro fundos Todos os setores foram registrados novamente com novos nomes (`…202611091` a `…202611094`) e as páginas foram apontadas para esses recursos, forçando a atualização do cache ao reabrir o PBIP.

## Correção definitiva de bordas — 09/11/2026
- Foi removida dos oito SVGs uma regra CSS residual que sobrescrevia a borda das caixas de filtro para branco. Os PNGs agora exibem o traço `#DDDDDE` do background.
- As manchetes foram ampliadas novamente, para **38 px** com linha de 44 px.
- Todos os oito fundos receberam novos recursos registrados (`…202611095` a `…202611102`) para impedir que o Desktop reutilize imagem em cache.

## Títulos internos de Empregos — 09/11/2026
- A barra mostrada no card não era da manchete geral da página: era dos visuais HTML de título internos. As quatro caixas de título de **Empregos · Todos os setores** receberam 2 px adicionais de altura (série 92, contrato 114, ranking 86 e UF 114).
- Para o título do ranking, o seletor de setores e o gráfico foram deslocados 2 px, preservando o espaçamento e o limite inferior do card.
- A manchete geral voltou ao padrão do design system (34 px / linha 40 px); aumentar sua tipografia não eliminava a barra dos títulos internos.

## Série de variação de empregos — 09/11/2026
- Em **Empregos · Todos os setores**, o gráfico anual de variação foi convertido de colunas agrupadas para linhas, com marcadores e rótulos de valor.
- A série **Comparáveis (referência)** foi removida desse gráfico e da legenda; permanecem AFL (laranja) e Seleção atual (cinza-azulado).
- O fundo da página foi renderizado e registrado novamente como `empregos-todos-bg202611103.png` para atualizar a legenda sem cache.

## Tooltip e título da variação — 09/11/2026
- O tooltip anual de empregos passou a usar uma medida dedicada, com somente AFL e Seleção atual; a página de tooltip `c71` aponta para essa medida.
- O título do gráfico anual em Empregos · Todos os setores também deixou de citar a variação dos Comparáveis.

## Perfil · HTML compacto — 10/11/2026
- Escolaridade passou a usar a medida `Esc_Barras_RF_HTML` nas abas Todos os setores e AFL, com barras empilhadas compactas e legenda no padrão de composição do RF.
- Cor/raça passou a usar `Raca_RF_HTML` nas mesmas abas, preservando as quatro categorias e compactando a apresentação.
- A pirâmide etária da aba AFL recebeu a mesma geometria ajustada manualmente na aba Todos os setores.
## Escolaridade — legenda e rótulos (10/11/2026)

- A legenda do gráfico de escolaridade passou a ter quatro itens estruturados: cada quadrado de cor fica junto ao seu texto e cada categoria ocupa uma linha.
- Rótulos internos das barras aparecem somente em segmentos de pelo menos 10%, preservando uma casa decimal e alinhamento vertical centralizado.

## Quanto ganha — escolaridade (10/11/2026)

- O gráfico de salário médio por escolaridade de **Todos os setores** recebeu a mesma geometria e espaçamento ajustados manualmente na aba **AFL**.
- Para acomodar o gráfico ampliado sem alterar a altura da página, o card de escolaridade foi ampliado e o card inferior direito (UF) foi deslocado e reduzido para caber acima da nota metodológica.
- Os fundos foram renderizados e registrados novamente como `ganha-afl-bg202611112.png` e `ganha-todos-bg202611113.png`, evitando o cache do Desktop.

## Quem contrata v2 — protótipo "Ranking de quem mais contrata por perfil dos empregados" (16/11/2026)

- As duas páginas da aba (`a3d1f2c4e6b8097a1c41` Todos os setores e `...c42` AFL) foram refeitas no desenho do protótipo: manchete, três KPIs (mulheres, negros, escolaridade), dois rankings por perfil e um ranking por escolaridade. Abas, faixa de leitura, Limpar filtros e segmentadores de filtro foram mantidos (só reposicionados, com Contrato incluído e sem sobreposição).
- **Todos os setores:** botões "10 melhores / 10 piores setores" e "Setor selecionado" (padrão: Serviços); o AFL fica fora do ranking e aparece sempre como último item em laranja. **AFL:** sem esses dois filtros; os gráficos mostram os seis CNAEs do AFL.
- **Único desvio do protótipo (pedido):** cada gráfico mostra um valor por vez, escolhido por botão no próprio card: Representatividade (participação) ou Salário médio. O rótulo muda de % para R$ pelo formato condicional `[<=1]0.0%;"R$ "#,0` aplicado no visual.
- Texto: "empregados/empregos" no lugar de "contratadas/contratações", porque a RAIS é estoque de vínculos em 31/12 (não fluxo de admissões). Negros = pretos + pardos sobre quem declarou cor. Piso de 50 mil empregos por divisão (igual ao da versão anterior).
- Gerador novo e isolado: `scripts/contrata_v2.py` (+ `dax_contrata2.py`, `verificar_contrata_v2.py`). **Não rode `pagina_rais.py --refazer` nem `modelo_base.py`**: eles estão defasados em relação às páginas e ao modelo salvos (Contrato, D_Indicador, medidas RF) e apagariam ajustes manuais. `contrata_v2.py` só acrescenta as medidas `Ct_*`, `KPI_Ct_*`, `Titulo_Ct_*`, `Manchete_Ct_*`, `Tip_Ct_*` ao `_medidas.tmdl`, cria as tabelas locais `D_Ct_*` (botões), refaz as duas páginas e cria três páginas de tooltip (`c81` mulheres, `c82` negros, `c83` escolaridade).
- As medidas e páginas antigas de Quem contrata (indicador, série, UF, tabela e tooltips `c54`–`c57`) continuam no projeto, sem uso.
- Validação feita: JSONs desserializados e todas as medidas/colunas/tabelas dos visuais conferidas contra o TMDL (`scripts/verificar_contrata_v2.py`); fundos renderizados e inspecionados.
- **Não testado no Power BI Desktop:** o DAX (ranking com RANKX, formato condicional, ordenação por medida no campo Tooltips), os botões, o tooltip e a renderização. Ao abrir o PBIP é preciso **Atualizar agora** para carregar as seis tabelas `D_Ct_*`. Nada foi commitado nem enviado ao GitHub.

### Quem contrata v2 — correções (16/11/2026)
- Rótulos dos rankings: o formato condicional `[<=1]…` não funciona no Power BI (aparecia literal). As medidas `Ct_*_Valor` e `Ct_*_Valor_AFL` agora usam **formato dinâmico** (`formatStringDefinition`): `0.0%` em Representatividade e `\R$ #,0` em Salário médio. Nos gráficos não há mais formato fixo.
- No TMDL, `formatStringDefinition` é objeto filho e tem de vir **depois** de `displayFolder`/`lineageTag`; antes disso o Desktop recusou o projeto ("Invalid indentation", `_medidas`, linha 3200).
- `scripts/validar_tmdl.ps1` carrega o modelo com o parser oficial (biblioteca baixada do NuGet para a pasta temporária) e pega erro de TMDL sem abrir o Desktop. Rode depois de qualquer alteração em `.tmdl`. Ele **não** valida DAX.
- Fluxo depois de ajustes manuais no Desktop: `python contrata_v2.py` (só medidas, réplica das posições no AFL e fundos); `--so-medidas` regrava apenas as medidas; `--recriar` refaz tudo e descarta os ajustes.

- (17/11/2026) O Desktop recusou o projeto com "TMDL objects cannot be merged… FormatStringDefinition": sobraram seis linhas `formatStringDefinition` soltas no meio do `_medidas.tmdl` (restos da regravação das medidas), todas atribuídas à mesma medida. O arquivo foi restaurado da versão do Git e as medidas novas regravadas; `contrata_v2.py` agora remove os blocos antigos por linha e **aborta** se houver mais de um `formatStringDefinition` por medida ou fora das medidas `Ct_*`. `scripts/reparar_medidas.py` compara o arquivo atual com o Git (ignorando as medidas `Ct_*`) e, com `--reparar`, restaura a base do Git.

### Quem contrata v2 — textos adaptáveis e KPIs (17/11/2026)
- Manchete da página: fala em "salário médio" quando os três gráficos estão nesse valor; o subtítulo resume o que está na tela (salário médio, representatividade ou "conforme o botão de cada gráfico").
- Títulos dos cards de ranking: o 1º texto também muda com o botão (ex.: "Divisões com maior representatividade de mulheres" / "…maior salário médio entre as mulheres"; "menor" nas 10 piores). Card de escolaridade: "Salário médio por divisão — escolaridade" / "Representatividade por divisão — escolaridade".
- KPIs de mulheres e negros: o valor grande vem com o rótulo "salário médio" ao lado e a linha de baixo começa com "Representatividade:". KPI de escolaridade: fontes maiores (níveis 20 px, valores 26 px) e legenda "participação (%) · salário médio (R$)". O gráfico do card de escolaridade passou a 18 px nos eixos e rótulos.
- Causa dos `formatStringDefinition` soltos (erro do Desktop): o Desktop grava o objeto filho depois de uma linha em branco; o removedor antigo parava na linha em branco e deixava o filho para trás. O removedor agora trata essa linha em branco como parte do bloco, e a regravação é idempotente.

### Aba "Ranking" (17/11/2026)
- A aba "Quem contrata" passou a se chamar **Ranking** nas 8 páginas: a faixa de abas (96 px do topo) dos fundos de Empregos, Quem trabalha e Quanto ganha foi redesenhada e colada nos PNGs já ajustados à mão (fundos novos registrados: *-bg202611171414.png); texto dos botões de navegação (hover/press) e alt text também. Script: scripts/nav_ranking.py (--testar compara a faixa desenhada com a dos PNGs atuais). Os displayName das páginas c41/c42 e dos tooltips viraram "Ranking · …".
- Botões de navegação: o estado pressionado deixou de ser #B86218 (marrom escuro) e passou a #F58220, igual ao hover; o estado padrão ganhou texto explicitamente desligado.
- Manchetes: "Ranking dos setores: quem mais contrata por perfil dos empregados" e "Ranking do AFL: …"; com os três gráficos em salário médio, "…: salário médio por perfil dos empregados".
