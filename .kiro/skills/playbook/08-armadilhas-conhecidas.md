# 08 · Armadilhas conhecidas

Erros reais do projeto e o que fazer. Atualize esta lista a cada descoberta.

## Power BI / PBIR

| Sintoma | Causa | Solução |
|---|---|---|
| "Para ver este visual personalizado, adicione-o ao relatório: stackedBarChart" | tipo de visual inexistente | barra empilhada é `barChart` |
| Tooltip de página não abre sobre KPI/manchete | HTML Content não suporta | gatilho transparente nativo + (i) |
| Texto de manchete cortado com "…" | `white-space:nowrap` + reticências | permitir 2 linhas (`-webkit-line-clamp:2`) e subir a altura do contêiner |
| Chips do KPI cortados | visual com 156 px | usar 172 px e posicionar em y+12 |
| Título HTML com barra de rolagem | texto de 3+ linhas no card estreito | encurtar; reservar 100 px; legenda e gráfico mais abaixo |
| Anos do eixo girados e embolados | eixo categórico em card estreito | eixo `Continuous` |
| Fundo antigo aparece depois de regerar | cache por nome do arquivo | manter o nome já registrado ao regravar o PNG |
| Dropdown "Todos" no filtro de setores | desvio do padrão | caixa de marcar de um item com filtro de visual `comparavel_AFL = Sim` |
| Gráfico de UF só repete o AFL na página Todos | medida com `G_AFL` fixo | versão por contexto (ex.: `Ind_UF_Todos_Geo`) + tooltip com o AFL |
| Descer para município some barras | medida com ranking `ALLSELECTED(D_UF[uf])` | medida de geografia sem top-N e com `ISINSCOPE` para a base mínima |
| Município minúsculo lidera o ranking | percentual de base pequena | base mínima no nível município |

## DAX

| Sintoma | Causa | Solução |
|---|---|---|
| "The syntax for 'RETURN' is incorrect" | medida começa com `RETURN` sem `VAR` | `VAR _A = …` antes |
| "Falha ao resolver o nome 'X'" | nome de medida sem colchetes (ou variável inexistente) | `[Medida]`; declarar a `VAR` |
| `PLACEHOLDER … True/False expression` | medida em filtro booleano do `CALCULATE` | guardar em `VAR` |
| Erro com variável chamada `Var` ou `Top` | palavras reservadas | outro nome |
| KPI "—" na página AFL | mediana só existe para setor/UF/sexo/escolaridade | cair para a mediana do grupo AFL quando não há filtro de atividade |
| HTML aparece como texto (`&lt;br&gt;`) | `esc()` escapou o HTML do próprio padrão | passar só o dado pelo `esc()`; marcador `[[br]]` + `SUBSTITUTE` |
| Medida duplicada | mesmo nome em dois módulos | `Counter` sobre `medidas()` antes de gravar |

## Ferramentas e scripts

| Sintoma | Causa | Solução |
|---|---|---|
| Barras invertidas e `\n` corrompidos em código Python gerado por *heredoc* do shell | o shell processa as sequências | gravar o script com a ferramenta de escrita de arquivo, ou usar `chr(92)` |
| Editor de texto rejeita `\n` literal | idem | âncoras curtas sem barras |
| `git fetch/push` trava | rede/credencial | `timeout` |
| Testes de DAX falham com erro de PowerShell "expressão de valor nulo" | Power BI Desktop fechado (sem `msmdsrv`) | reabrir o PBIP |
| `Não pode ser criada uma tabela 'D_Indicador'` | tentou simular tabela que já existe no modelo | rodar sem a simulação |

## Processo

- **Edições manuais sobrescritas** por `pagina_rais.py --refazer` / `modelo_base.py`: aconteceu uma vez. Use a trava (`seguranca.py`), commite antes e peça "Salvar como" para recuperar do Desktop (ver `05`).
- **Afirmar teste sem teste**: JSON válido não prova que hover, drill ou tooltip funcionam. Escreva "não testado no Desktop" no handoff.
- **Mudar de padrão sem avisar**: o filtro de comparabilidade, por exemplo, já foi definido no RF (caixa de marcar, um item); não recrie à vontade.
