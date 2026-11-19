# RAIS Emprego Formal — Tabelas

Catálogo de tabelas do modelo. Cada uma com descrição, granularidade, colunas tipadas e source M resumido.

> **Voltar pra:** [00 · Overview](00-overview.md) · **Próxima:** [02 · Medidas](02-medidas.md)

---

## F_rais

> Fato principal: vínculos de emprego da RAIS já agregados, com contagem e somas de salário e idade.
> **Tipo:** Fato · **Origem:** DirectQuery · F_rais (Painel_RAIS)

### Descrição
Os números do painel saem daqui: `vinculos` (empregos em 31/12), `soma_salario_valido` / `qtd_salario_valido` (remuneração média) e `soma_idade` / `qtd_idade` (idade média). Lida em DirectQuery no modelo `Painel_RAIS`.

### Granularidade
1 linha = combinação de ano × município × CNAE × CBO × atributos do vínculo e do trabalhador (sexo, idade, escolaridade, cor/raça…).

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `uf` | string | Atributo | oculta |
| `ambito` | string | Atributo | — |
| `cnae_fiscal` | string | Chave estrangeira → D_Cnae | oculta |
| `cbo_2002` | string | Atributo | — |
| `categoria_vinculo` | string | Atributo | — |
| `natureza_empresa` | string | Atributo | — |
| `modalidade_contrato` | string | Atributo | — |
| `tipo_admissao` | string | Atributo | — |
| `trabalho_intermitente` | string | Atributo | — |
| `trabalho_parcial` | string | Atributo | — |
| `faixa_horas_contratuais` | string | Atributo | — |
| `sexo` | string | Chave estrangeira → D_Sexo | oculta |
| `faixa_idade` | string | Chave estrangeira → D_FaixaIdade | oculta |
| `escolaridade_agrupada` | string | Chave estrangeira → D_Escolaridade | oculta |
| `raca_cor` | string | Chave estrangeira → D_Raca | oculta |
| `indicador_portador_deficiencia` | string | Atributo | — |
| `tipo_deficiencia` | string | Atributo | — |
| `vinculos` | int64 | Métrica | oculta; formato `0` |
| `soma_salario_valido` | double | Métrica | oculta |
| `soma_sm_valido` | double | Métrica | oculta |
| `qtd_salario_valido` | int64 | Métrica | oculta; formato `0` |
| `soma_idade` | int64 | Métrica | oculta; formato `0` |
| `qtd_idade` | int64 | Métrica | oculta; formato `0` |
| `ano` | int64 | Chave estrangeira → D_Calendario | oculta; formato `0` |
| `id_municipio` | string | Chave estrangeira → D_regiao | oculta |

### Source M (resumo)
```m
// partição entity, modo directQuery
// entidade: F_rais
// fonte: 'DirectQuery para AS – Painel_RAIS' → AnalysisServices.Database("powerbi://api.powerbi.com/v1.0/myorg/Testes", "Painel_RAIS")
```

---

## D_AflAtividade

> As seis atividades do AFL, por código CNAE, com ordem.
> **Tipo:** Dimensão · **Origem:** Import · tabela digitada (#table)

### Descrição
Botões e rankings da página AFL.

### Granularidade
1 linha por CNAE do AFL.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `cnae_fiscal` | string | Chave primária | — |
| `nome` | string | Atributo | ordena por `ordem` |
| `ordem` | string | Atributo | — |

### Source M (resumo)
```m
let
    Fonte = #table(type table [cnae_fiscal = text, nome = text, ordem = text], {{ … linhas digitadas … }})
in
    Fonte
```

---

## D_Ano

> Lista de anos, ligada ao calendário.
> **Tipo:** Dimensão · **Origem:** Import · M (m)

### Descrição
Relação detectada automaticamente com `D_Calendario[Ano]`.

### Granularidade
1 linha por ano.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `ano` | int64 | Chave primária | formato `0` |

### Source M (resumo)
```m
let
    // Tabela local: a D_Ano não existe mais no Painel_RAIS. Anos da F_rais remota: 2009 a 2025 (incluir o ano novo aqui quando a base crescer).
    Anos = List.Numbers(2009, 2025 - 2009 + 1),
    Tabela = Table.FromList(Anos, Splitter.SplitByNothing(), {"ano"}),
    Tipado = Table.TransformColumnTypes(Tabela, {{"ano", Int64.Type}})
in
    Tipado
```

---

## D_Calendario

> Calendário diário de 2009 até o fim do ano corrente, com a fonte da RAIS e o trecho da série.
> **Tipo:** Dimensão · **Origem:** Import · M gerado (calendário)

### Descrição
Liga-se a `F_rais[ano]` por uma relação muitos-para-muitos. `Fonte RAIS` e `Trecho da Série` separam a RAIS antiga (até 2021) do eSocial (2022 em diante).

### Granularidade
1 linha por dia.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `Data` | dateTime | Atributo | formato `Long Date` |
| `Ano` | int64 | Chave estrangeira → D_Ano | formato `0` |
| `Mês Num` | int64 | Atributo | formato `0` |
| `Nome do Mês` | string | Atributo | ordena por `'Mês Num'` |
| `Dia` | int64 | Atributo | formato `0` |
| `Dia da Semana` | int64 | Atributo | formato `0` |
| `Nome do Dia` | string | Atributo | — |
| `Semestre` | string | Atributo | — |
| `Trimestre` | string | Atributo | — |
| `Mês/Ano` | string | Atributo | — |
| `Semana do Ano` | int64 | Atributo | formato `0` |
| `Semana do Mês` | int64 | Atributo | formato `0` |
| `Início da Semana` | dateTime | Atributo | formato `Long Date` |
| `Fim da Semana` | dateTime | Atributo | formato `Long Date` |
| `Mês Abrev` | string | Atributo | ordena por `'Mês Num'` |
| `Dias Uteis` | string | Atributo | — |
| `Dia da Semana Letra` | string | Atributo | — |
| `Semana do Mes Letra` | string | Atributo | — |
| `ano_mes_num` | string | Atributo | — |
| `Data ate Hoje` | string | Atributo | — |
| `Dia Atual` | string | Atributo | — |
| `Ano Trimestre` | string | Atributo | — |
| `Fonte RAIS` | string | Atributo | — |
| `Trecho da Série` | string | Atributo | — |

### Source M (resumo)
```m
let
    // Calendário padrão do time. A fato da RAIS é DirectQuery e só tem o ano, então o intervalo é fixo:
    // de 01/01/2009 (início da base) ao fim do ano corrente.
    DataInicial = #date(2009, 1, 1),
    DataFinal = Date.EndOfYear(Date.From(DateTime.LocalNow())),
    Duracao = Duration.Days(DataFinal - DataInicial) + 1,
    Fonte = List.Dates(DataInicial, Duracao, #duration(1, 0, 0, 0)),
    #"Convertido para Tabela" = Table.FromList(Fonte, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Convertido para Tabela",{{"Column1", type date}}),
    #"Colunas Renomeadas" = Table.RenameColumns(#"Tipo Alterado",{{"Column1", "Data"}}),
    #"Ano Inserido" = Table.AddColumn(#"Colunas Renomeadas", "Ano", each Date.Year([Data]), Int64.Type),
    #"Mês Inserido" = Table.AddColumn(#"Ano Inserido", "Mês", each Date.Month([Data]), Int64.Type),
    // … 30 linhas omitidas …
in
    #"Trecho Adicionado"
```

---

## D_Cnae

> Classificação CNAE das atividades, com a divisão e o grupo de setor (AFL, Comparável…).
> **Tipo:** Dimensão · **Origem:** DirectQuery · D_Cnae (Painel_RAIS)

### Descrição
Liga a fato aos setores. `grupo_setor` filtra D_GrupoSetor, `setor_comparavel_afl` filtra D_Comparavel e `cnae_fiscal` filtra D_AflAtividade.

### Granularidade
1 linha por subclasse CNAE (`cnae_fiscal`).

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `cnae_fiscal` | string | Chave estrangeira → D_AflAtividade | — |
| `nm_subclasse` | string | Atributo | — |
| `nm_classe` | string | Atributo | — |
| `divisao_afl` | string | Atributo | — |
| `setor_afl` | string | Atributo | — |
| `setor_comparavel_afl` | string | Chave estrangeira → D_Comparavel | — |
| `setor_principal` | string | Atributo | — |
| `grupo_setor` | string | Chave estrangeira → D_GrupoSetor | — |

### Source M (resumo)
```m
// partição entity, modo directQuery
// entidade: D_Cnae
// fonte: 'DirectQuery para AS – Painel_RAIS' → AnalysisServices.Database("powerbi://api.powerbi.com/v1.0/myorg/Testes", "Painel_RAIS")
```

---

## D_Comparavel

> Rótulo de exibição do setor comparável ao AFL.
> **Tipo:** Dimensão · **Origem:** Import · tabela digitada (#table)

### Descrição
Filtrada por `D_Cnae[setor_comparavel_afl]`.

### Granularidade
1 linha por setor comparável.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `comparavel_AFL` | string | Chave primária | — |
| `comparavel_AFL_rotulo` | string | Atributo | — |

### Source M (resumo)
```m
let
    Fonte = #table(type table [comparavel_AFL = text, comparavel_AFL_rotulo = text], {{"Sim", "Só os comparáveis ao AFL"}, {"Não", "Demais setores"}})
	in
	    Fonte
```

---

## D_Escolaridade

> Escolaridade agrupada em quatro níveis, com ordem.
> **Tipo:** Dimensão · **Origem:** DirectQuery · D_Escolaridade (Painel_RAIS)

### Descrição
Eixo dos gráficos de escolaridade e da razão salarial por escolaridade.

### Granularidade
1 linha por nível de escolaridade.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `escolaridade_agrupada` | string | Chave primária | ordena por `ordem` |
| `ordem` | int64 | Atributo | oculta |

### Source M (resumo)
```m
// partição entity, modo directQuery
// entidade: D_Escolaridade
// fonte: 'DirectQuery para AS – Painel_RAIS' → AnalysisServices.Database("powerbi://api.powerbi.com/v1.0/myorg/Testes", "Painel_RAIS")
```

---

## D_FaixaIdade

> Faixa de idade do trabalhador, com ordem.
> **Tipo:** Dimensão · **Origem:** DirectQuery · D_FaixaIdade (Painel_RAIS)

### Descrição
Eixo da pirâmide etária e base do indicador de jovens.

### Granularidade
1 linha por faixa de idade.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `faixa_idade` | string | Chave primária | ordena por `ordem` |
| `ordem` | int64 | Atributo | oculta |

### Source M (resumo)
```m
// partição entity, modo directQuery
// entidade: D_FaixaIdade
// fonte: 'DirectQuery para AS – Painel_RAIS' → AnalysisServices.Database("powerbi://api.powerbi.com/v1.0/myorg/Testes", "Painel_RAIS")
```

---

## D_GrupoSetor

> Grupo de setor usado em todo o painel (AFL × Comparável × demais).
> **Tipo:** Dimensão · **Origem:** DirectQuery · D_GrupoSetor (Painel_RAIS)

### Descrição
Base dos filtros AFL e Comparáveis em quase todas as medidas `_AFL` e `_Comparavel`.

### Granularidade
1 linha por grupo de setor.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `grupo_setor` | string | Chave primária | ordena por `ordem` |
| `ordem` | int64 | Atributo | oculta |

### Source M (resumo)
```m
// partição entity, modo directQuery
// entidade: D_GrupoSetor
// fonte: 'DirectQuery para AS – Painel_RAIS' → AnalysisServices.Database("powerbi://api.powerbi.com/v1.0/myorg/Testes", "Painel_RAIS")
```

---

## D_Raca

> Cor ou raça, agrupada em negros, brancos e outros, com a marca de declarada.
> **Tipo:** Dimensão · **Origem:** DirectQuery · D_Raca (Painel_RAIS)

### Descrição
Base dos percentuais por cor (só sobre quem declarou) e da razão salarial negros × brancos.

### Granularidade
1 linha por cor/raça.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `raca_cor` | string | Chave primária | ordena por `ordem` |
| `grupo_raca` | string | Atributo | — |
| `declarada` | string | Atributo | — |
| `ordem` | int64 | Atributo | oculta |

### Source M (resumo)
```m
// partição entity, modo directQuery
// entidade: D_Raca
// fonte: 'DirectQuery para AS – Painel_RAIS' → AnalysisServices.Database("powerbi://api.powerbi.com/v1.0/myorg/Testes", "Painel_RAIS")
```

---

## D_regiao

> Geografia: município, estado e sigla da UF.
> **Tipo:** Dimensão · **Origem:** DirectQuery · D_regiao (Painel_RAIS)

### Descrição
Mapas e rankings por UF, com drill para município.

### Granularidade
1 linha por município (`cod_municipio`).

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `cod_municipio` | string | Chave primária | — |
| `municipio` | string | Atributo | — |
| `estado` | string | Atributo | origem: `uf`; Nome completo do estado (na D_regiao remota a coluna chama uf). |
| `uf` | string | Atributo | origem: `sigla_uf`; Sigla da UF (na D_regiao remota a coluna chama sigla_uf). |

### Source M (resumo)
```m
// partição entity, modo directQuery
// entidade: D_regiao
// fonte: 'DirectQuery para AS – Painel_RAIS' → AnalysisServices.Database("powerbi://api.powerbi.com/v1.0/myorg/Testes", "Painel_RAIS")
```

---

## D_Sexo

> Sexo do trabalhador, com ordem de exibição.
> **Tipo:** Dimensão · **Origem:** DirectQuery · D_Sexo (Painel_RAIS)

### Descrição
Usada nos KPIs e gráficos de mulheres e na razão salarial por sexo.

### Granularidade
1 linha por sexo.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `sexo` | string | Chave primária | ordena por `ordem` |
| `ordem` | int64 | Atributo | oculta |

### Source M (resumo)
```m
// partição entity, modo directQuery
// entidade: D_Sexo
// fonte: 'DirectQuery para AS – Painel_RAIS' → AnalysisServices.Database("powerbi://api.powerbi.com/v1.0/myorg/Testes", "Painel_RAIS")
```

---

## D_Ct_MetEsc

> Botões de métrica do bloco de escolaridade (representatividade ou salário médio).
> **Tipo:** Auxiliar · **Origem:** Import · tabela digitada (#table)

### Descrição
Troca a métrica e o formato das medidas `Ct_Esc_*`.

### Granularidade
1 linha por métrica.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `metrica` | string | Atributo | ordena por `ordem` |
| `ordem` | string | Atributo | — |

### Source M (resumo)
```m
let
    Fonte = #table(type table [metrica = text, ordem = text], {{"Representatividade", "1"}, {"Salário médio", "2"}})
in
    Fonte
```

---

## D_Ct_MetMul

> Botões de métrica do bloco de mulheres (representatividade ou salário médio).
> **Tipo:** Auxiliar · **Origem:** Import · tabela digitada (#table)

### Descrição
Troca a métrica e o formato das medidas `Ct_Mul_*`.

### Granularidade
1 linha por métrica.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `metrica` | string | Atributo | ordena por `ordem` |
| `ordem` | string | Atributo | — |

### Source M (resumo)
```m
let
    Fonte = #table(type table [metrica = text, ordem = text], {{"Representatividade", "1"}, {"Salário médio", "2"}})
in
    Fonte
```

---

## D_Ct_MetNeg

> Botões de métrica do bloco de negros (representatividade ou salário médio).
> **Tipo:** Auxiliar · **Origem:** Import · tabela digitada (#table)

### Descrição
Troca a métrica e o formato das medidas `Ct_Neg_*`.

### Granularidade
1 linha por métrica.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `metrica` | string | Atributo | ordena por `ordem` |
| `ordem` | string | Atributo | — |

### Source M (resumo)
```m
let
    Fonte = #table(type table [metrica = text, ordem = text], {{"Representatividade", "1"}, {"Salário médio", "2"}})
in
    Fonte
```

---

## D_Ct_Modo

> Botões do ranking: 10 melhores ou 10 piores setores.
> **Tipo:** Auxiliar · **Origem:** Import · tabela digitada (#table)

### Descrição
Tabela de parâmetro da página de ranking.

### Granularidade
1 linha por opção.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `modo` | string | Atributo | ordena por `ordem` |
| `ordem` | string | Atributo | — |

### Source M (resumo)
```m
let
    Fonte = #table(type table [modo = text, ordem = text], {{"10 melhores setores", "1"}, {"10 piores setores", "2"}})
in
    Fonte
```

---

## D_Ct_Nivel

> Botões de nível de escolaridade da página de ranking.
> **Tipo:** Auxiliar · **Origem:** Import · tabela digitada (#table)

### Descrição
Tabela de parâmetro da página de ranking.

### Granularidade
1 linha por nível.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `nivel` | string | Atributo | ordena por `ordem` |
| `ordem` | string | Atributo | — |

### Source M (resumo)
```m
let
    Fonte = #table(type table [nivel = text, ordem = text], {{"Até fundamental", "1"}, {"Médio incompleto", "2"}, {"Médio completo", "3"}, {"Superior", "4"}})
in
    Fonte
```

---

## D_Ct_Setor

> Botões de setor da página de ranking.
> **Tipo:** Auxiliar · **Origem:** Import · tabela digitada (#table)

### Descrição
Tabela de parâmetro da página de ranking.

### Granularidade
1 linha por opção.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `setor` | string | Atributo | ordena por `ordem` |
| `ordem` | string | Atributo | — |

### Source M (resumo)
```m
let
    Fonte = #table(type table [setor = text, ordem = text], {{ … linhas digitadas … }})
in
    Fonte
```

---

## D_Indicador

> Os sete indicadores da página Quem contrata (botões).
> **Tipo:** Auxiliar · **Origem:** Import · tabela digitada (#table)

### Descrição
Tabela de parâmetro: a escolha troca o indicador de toda a página.

### Granularidade
1 linha por indicador.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `indicador` | string | Atributo | ordena por `ordem` |
| `ordem` | string | Atributo | — |
| `indicador_exibicao` | string | Atributo | ordena por `ordem` |

### Source M (resumo)
```m
let
    Fonte = #table(type table [indicador = text, indicador_exibicao = text, ordem = text], {{ … linhas digitadas … }})
in
    Fonte
```

---

## D_Info

> Textos dos ícones de informação (i) de cada visual.
> **Tipo:** Auxiliar · **Origem:** Import · tabela digitada (#table)

### Descrição
As medidas `Info_*` e as dicas leem esta tabela pela `Chave`.

### Granularidade
1 linha por chave `Página|Setor|Visual`.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `Chave` | string | Atributo | — |
| `Classe` | string | Atributo | — |
| `Titulo` | string | Atributo | — |
| `Extra` | string | Atributo | — |
| `Destaque` | string | Atributo | — |
| `CorBorda` | string | Atributo | — |
| `CorFundo` | string | Atributo | — |
| `P1` | string | Atributo | — |
| `P2` | string | Atributo | — |
| `P3` | string | Atributo | — |
| `P4` | string | Atributo | — |
| `P5` | string | Atributo | — |

### Source M (resumo)
```m
let
    Fonte = #table(type table [Chave = text, Classe = text, Titulo = text, Extra = text, Destaque = text, CorBorda = text, CorFundo = text, P1 = text, P2 = text, P3 = text, P4 = text, P5 = text], {{ … linhas digitadas … }})
in
    Fonte
```

---

## D_Rank_Divisao

> Lista de divisões CNAE usada no eixo dos rankings.
> **Tipo:** Auxiliar · **Origem:** Import · tabela digitada (#table)

### Descrição
Tabela local (import), sem relação: as medidas filtram a fato com ela.

### Granularidade
1 linha por divisão.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `nm_divisao` | string | Atributo | — |
| `setor_principal` | string | Atributo | — |

### Source M (resumo)
```m
let
    Fonte = #table(type table [nm_divisao = text, setor_principal = text], {{ … linhas digitadas … }})
in
    Fonte
```

---

## _medidas

> Tabela que só hospeda as medidas DAX do painel.
> **Tipo:** Medidas · **Origem:** Import · tabela digitada (#table)

### Descrição
Todas as medidas ficam aqui, organizadas por pastas (displayFolder).

### Granularidade
Sem linhas de dados.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `Coluna` | string | Atributo | oculta |

### Medidas hospedadas

- [Base\AFL](02-medidas.md#base-afl) — 3 medidas
- [Base\Ano](02-medidas.md#base-ano) — 3 medidas
- [Base\Apoio](02-medidas.md#base-apoio) — 1 medidas
- [Base\Comparavel](02-medidas.md#base-comparavel) — 3 medidas
- [Base\Empregos](02-medidas.md#base-empregos) — 5 medidas
- [Base\Remuneração](02-medidas.md#base-remuneração) — 3 medidas
- [Empregos\Apoio](02-medidas.md#empregos-apoio) — 5 medidas
- [Empregos\Atividades](02-medidas.md#empregos-atividades) — 1 medidas
- [Empregos\Ranking](02-medidas.md#empregos-ranking) — 5 medidas
- [Empregos\Séries](02-medidas.md#empregos-séries) — 4 medidas
- [Empregos\UF](02-medidas.md#empregos-uf) — 3 medidas
- [HTML\Dicas](02-medidas.md#html-dicas) — 6 medidas
- [HTML\Empregos](02-medidas.md#html-empregos) — 3 medidas
- [HTML\Empregos\KPIs](02-medidas.md#html-empregos-kpis) — 5 medidas
- [HTML\Empregos\Títulos](02-medidas.md#html-empregos-títulos) — 7 medidas
- [HTML\Notas compartilhadas](02-medidas.md#html-notas-compartilhadas) — 2 medidas
- [HTML\Quanto ganha](02-medidas.md#html-quanto-ganha) — 2 medidas
- [HTML\Quanto ganha\KPIs](02-medidas.md#html-quanto-ganha-kpis) — 6 medidas
- [HTML\Quanto ganha\Títulos](02-medidas.md#html-quanto-ganha-títulos) — 6 medidas
- [HTML\Quem contrata](02-medidas.md#html-quem-contrata) — 2 medidas
- [HTML\Quem contrata\KPIs](02-medidas.md#html-quem-contrata-kpis) — 6 medidas
- [HTML\Quem contrata\Títulos](02-medidas.md#html-quem-contrata-títulos) — 6 medidas
- [HTML\Quem trabalha](02-medidas.md#html-quem-trabalha) — 4 medidas
- [HTML\Quem trabalha\KPIs](02-medidas.md#html-quem-trabalha-kpis) — 6 medidas
- [HTML\Quem trabalha\Títulos](02-medidas.md#html-quem-trabalha-títulos) — 6 medidas
- [HTML\Tooltips de gráficos](02-medidas.md#html-tooltips-de-gráficos) — 25 medidas
- [Quanto ganha\Escolaridade](02-medidas.md#quanto-ganha-escolaridade) — 3 medidas
- [Quanto ganha\Razões](02-medidas.md#quanto-ganha-razões) — 12 medidas
- [Quanto ganha\Séries](02-medidas.md#quanto-ganha-séries) — 6 medidas
- [Quanto ganha\UF](02-medidas.md#quanto-ganha-uf) — 2 medidas
- [Quem contrata\Apoio](02-medidas.md#quem-contrata-apoio) — 4 medidas
- [Quem contrata\Atividades](02-medidas.md#quem-contrata-atividades) — 2 medidas
- [Quem contrata\Indicadores](02-medidas.md#quem-contrata-indicadores) — 4 medidas
- [Quem contrata\Perfil](02-medidas.md#quem-contrata-perfil) — 25 medidas
- [Quem contrata\Ranking](02-medidas.md#quem-contrata-ranking) — 15 medidas
- [Quem contrata\UF](02-medidas.md#quem-contrata-uf) — 1 medidas
- [Quem trabalha\AFL](02-medidas.md#quem-trabalha-afl) — 3 medidas
- [Quem trabalha\Comparável](02-medidas.md#quem-trabalha-comparável) — 3 medidas
- [Quem trabalha\Ocupações](02-medidas.md#quem-trabalha-ocupações) — 1 medidas
- [Quem trabalha\Perfil](02-medidas.md#quem-trabalha-perfil) — 8 medidas
- [Quem trabalha\Pirâmide](02-medidas.md#quem-trabalha-pirâmide) — 4 medidas

---

---

*XPERIUN · `/pbi-doc`*
