# 03 · Padrões de DAX e HTML

## Medidas HTML (KPI, manchete, título)

Todo texto de apresentação vem de **medidas DAX que devolvem HTML**, exibidas no HTML Content. Isso permite manchetes que mudam com os filtros.

### Regras de código

1. **Escape de tudo que é dinâmico.** Todo texto que entra no HTML passa por `esc()`: troca `&`, `<`, `>`, aspas e apóstrofo por entidades. Só o HTML fixo do próprio padrão não é escapado. (Se precisar de `<br>` dentro de um texto escapado, use um marcador como `[[br]]` e faça `SUBSTITUTE` depois do escape.)
2. **Medida sem `VAR` própria não pode começar com `RETURN`.** Comece sempre com pelo menos uma `VAR` (ex.: `VAR _A = [Ano_Ref]`).
3. **Não use `Var` nem `Top` como nome de variável** (palavras reservadas que já quebraram).
4. **Medida dentro de filtro booleano do `CALCULATE` não funciona** (`D_Ano[ano] = [Medida]`): guarde o valor em uma `VAR` e use a variável.
5. **Nome de medida sempre entre colchetes** quando você a referencia; nome de variável, sem. Cuidado ao gerar código por Python: um helper que formata "nome de variável" não pode receber nome de medida.
6. Um só cálculo-base por conceito (ex.: `Ind_Valor_Ctx`) e variantes por `CALCULATE` com filtros de grupo (AFL, Comparável).

### Peças reutilizáveis (módulo `dax_rais.py`)

| Peça | Papel |
|---|---|
| `esc(x)` | escape do texto dinâmico |
| `pct(v, sinal)` / `num(v)` | formatação pt-BR com "—" quando em branco |
| `chip_afl(txt)` / `chip_ref(txt)` | chips "AFL …" (laranja) e "Comparáveis … · ref." (cinza) |
| `kpi_html(aria, rotulo, valor, linha3, cor3, chips, duas)` | KPI de 172 px; `duas=True` deixa a linha 3 quebrar em 2 linhas |
| `titulo_html(L1, L2, cor_barra)` | título de card com barra à esquerda, L1 24 px e L2 20 px |
| `manchete_corpo(texto, contexto, aria)` | manchete de até 2 linhas + contexto |

KPIs levam sempre: rótulo, valor grande, linha de comparação e **chips AFL × Comparáveis** (na página AFL só o chip de referência).

## Contexto e anos

- **Ano de referência** (`Ano_Ref`): vem do segmentador de Ano. Estoques são calculados para **um único ano** (`REMOVEFILTERS(D_Calendario)` + ano fixo). **Nunca some estoques de anos diferentes.**
- Série com **quebra de fonte**: duas medidas por série ("Pré" até o ano anterior à quebra e "Pós" a partir dela), mesma cor, BLANK fora do trecho. A linha não atravessa a quebra.
- Medidas "do grupo" independentes dos filtros de setor: `CALCULATE([medida], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")` (e `"Comparável"`).
- **Seleção atual** = a mesma medida sem os filtros de grupo (respeita setor, divisão, UF etc.). Só aparece na página "Todos os setores".

## Níveis de detalhe

- `ISINSCOPE(coluna)` para saber se o visual está no nível de município (drill) e aplicar base mínima.
- `RANKX(ALLSELECTED(coluna), medida, , DESC, DENSE)` para posição; guarde o ranking numa `VAR`.
- Item sintético "AFL · conjunto de 6 CNAEs" no ranking de divisões: é uma categoria à parte, sem dupla contagem com a divisão que contém o AFL.

## Tooltips (medidas)

Modelo em `dax_tooltips.py`: `cab()` (título/subtítulo), `linha()` (marcador de cor + rótulo + valor + detalhe, com condição para sumir), `nota()` (frase de leitura), `montar()` (junta tudo). Tooltips de KPI com exemplo numérico em `dax_dicas.py`. A frase de leitura sempre compara AFL com Comparáveis em **pontos percentuais** (`pp()`).

## Convenções

- Pasta de exibição (`displayFolder`) por tema: `HTML\<Tema>\KPIs`, `\Títulos`, `Tooltips de gráficos`, `Séries`, `Ranking`…
- Medidas auxiliares ocultas (`isHidden`), sobretudo as de apoio e as de cor.
- Cor por medida (`Cor_Emp_Divisao`…) para destacar o AFL no ranking.
- Cada medida tem descrição (`///`) dizendo o que calcula e o que devolve em branco.
