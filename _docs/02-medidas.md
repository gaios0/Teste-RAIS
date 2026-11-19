# RAIS Emprego Formal — Medidas

Catálogo de todas as medidas DAX do modelo, agrupadas pelos displayFolders.

> **Voltar pra:** [01 · Tabelas](01-tabelas.md) · **Próxima:** [03 · Relacionamentos](03-relacionamentos.md)

---

## Base\AFL

3 medidas.

### Empregos_Ref_AFL

`_medidas.Empregos_Ref_AFL` · formato `#,0`

**O que faz:**
Empregos_Ref só do grupo AFL, independente do filtro de setores da página.

**DAX:**
```dax
CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Rank_Divisao), REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`, `D_Rank_Divisao`.

**Usa:** `Empregos_Ref`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `Emp_Divisao`, `Emp_UF_Peso_AFL`, `Emp_UF_Peso_Geo`, `KPI_Peso_AFL_HTML`, `KPI_Peso_Total_HTML`, `Tip_Emp_Ano_HTML`, `Tip_Emp_Ano_Sem_Comparaveis_HTML`, `Tip_Emp_Atividade_HTML`, `Tip_Emp_UF_HTML`, `Tip_Ind_UF_HTML`, `Tip_Rem_Esc_HTML`, `Titulo_Emp_UF_Total_HTML`
**Aparece nas páginas:** Empregos · Todos os setores

---

### Empregos_Var_Pct_AFL

`_medidas.Empregos_Var_Pct_AFL` · formato `+0.0%;-0.0%;0.0%`

**O que faz:**
Empregos_Var_Pct só do grupo AFL, independente do filtro de setores da página.

**DAX:**
```dax
CALCULATE([Empregos_Var_Pct], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Empregos_Var_Pct`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `Empregos_Var_Pct_AFL_Pos`, `Empregos_Var_Pct_AFL_Pre`, `KPI_Emp_Total_HTML`, `Tip_Emp_Ano_HTML`, `Tip_Emp_Ano_Sem_Comparaveis_HTML`, `Titulo_Emp_Var_AFL_HTML`, `Titulo_Emp_Var_Total_HTML`

---

### Remuneracao_Media_Ref_AFL

`_medidas.Remuneracao_Media_Ref_AFL` · formato `#,0.00`

**O que faz:**
Remuneracao_Media_Ref só do grupo AFL, independente do filtro de setores da página.

**DAX:**
```dax
CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Remuneracao_Media_Ref`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `KPI_RemMedia_Total_HTML`, `Manchete_Salario_AFL_HTML`, `Manchete_Salario_Total_HTML`, `Rem_Esc_AFL`, `Rem_UF_Razao_Comp`, `Tip_Rem_Ano_HTML`, `Tip_Rem_Ano_Total_HTML`, `Tip_Rem_UF_HTML`, `Titulo_Rem_Esc_HTML`

---

## Base\Ano

3 medidas.

### Ano_Inicio_Trecho

`_medidas.Ano_Inicio_Trecho` · formato `0`

**O que faz:**
Primeiro ano do trecho comparável do ano de referência: 2009 (RAIS declaratória) ou 2022 (eSocial).

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), IF(A >= 2022, 2022, 2009))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`.

**Usa:** `Ano_Ref`
**É usada por:** `Emp_Sequencia_Altas_AFL`, `KPI_Jovens_AFL_HTML`, `KPI_Jovens_Total_HTML`, `Perf_Idade_Inicio`, `Titulo_Rem_Serie_HTML`

---

### Ano_Ref

`_medidas.Ano_Ref` · formato `0`

**O que faz:**
Ano de referência: o último ano com dados no contexto (com o segmentador de ano, o ano escolhido).

**DAX:**
```dax
CALCULATE(MAX(F_rais[ano]))
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular.

**Usa:** `F_rais[ano]`
**É usada por:** `Ano_Inicio_Trecho`, `Comparavel_Ano_Anterior`, `Contexto_Emp_AFL`, `Contexto_Emp_Total`, `Ct_Esc_Qtd`, `Ct_Esc_Rep`, `Ct_Esc_Sal`, `Ct_Esc_Tot`, `Ct_Mul_Qtd`, `Ct_Mul_Rep`, `Ct_Mul_Sal`, `Ct_Mul_Tot`, `Ct_Neg_Qtd`, `Ct_Neg_Rep`, `Ct_Neg_Sal`, `Ct_Neg_Tot`, `Emp_Contratos_HTML`, `Emp_Divisao`, `Emp_Sequencia_Altas_AFL`, `Empregos_Ano_Anterior`, `Empregos_Ref`, `Empregos_Ref_Todos`, `Empregos_Var_Pct_AFL_Pos`, `Empregos_Var_Pct_AFL_Pre`, `Empregos_Var_Pct_Sel_Pos`, `Empregos_Var_Pct_Sel_Pre`, `Ind_Ano`, `Ind_Valor_Ano`, `KPI_Ct_Esc_AFL_HTML`, `KPI_Ct_Esc_Total_HTML`, `KPI_Emp_AFL_HTML`, `KPI_Emp_Total_HTML`, `KPI_Escol_AFL_HTML`, `KPI_Escol_Total_HTML`, `KPI_Jovens_AFL_HTML`, `KPI_Jovens_Total_HTML`, `KPI_Mulheres_AFL_HTML`, `KPI_Mulheres_Total_HTML`, `KPI_Primeiro_Emprego_HTML`, `Manchete_Ct_AFL_HTML`, `Manchete_Ct_Total_HTML`, `Manchete_Emp_AFL_HTML`, `Manchete_Emp_Total_HTML`, `Manchete_Perfil_AFL_HTML`, `Manchete_Perfil_Total_HTML`, `Manchete_Salario_AFL_HTML`, `Manchete_Salario_Total_HTML`, `Perf_Ate24`, `Perf_Idade`, `Perf_Intermitente`, `Perf_MedioMais`, `Perf_Mulheres`, `Perf_Primeiro`, `Perf_Superior`, `Rem_Media_AFL_Pos`, `Rem_Media_AFL_Pre`, `Rem_Media_Comp_Pos`, `Rem_Media_Comp_Pre`, `Rem_Media_Sel_Pos`, `Rem_Media_Sel_Pre`, `Rem_Razao_Raca`, `Rem_Razao_Sexo`, `Remuneracao_Media_Ref`, `Remuneracao_Media_SM_Ref`, `Tip_CBO_HTML`, `Tip_Ct_Esc_HTML`, `Tip_Ct_Mul_HTML`, `Tip_Ct_Neg_HTML`, `Tip_Emp_Atividade_HTML`, `Tip_Emp_Divisao_HTML`, `Tip_Emp_UF_HTML`, `Tip_Pir_HTML`, `Tip_RazaoRaca_HTML`, `Tip_RazaoSexo_HTML`, `Titulo_CBO_HTML`, `Titulo_Emp_Atividades_HTML`, `Titulo_Emp_Contrato_HTML`, `Titulo_Emp_Ranking_HTML`, `Titulo_Emp_Var_AFL_HTML`, `Titulo_Emp_Var_Total_HTML`, `Titulo_Esc_HTML`, `Titulo_Pir_HTML`, `Titulo_Raca_HTML`, `Titulo_Rem_Serie_HTML`

---

### Comparavel_Ano_Anterior

`_medidas.Comparavel_Ano_Anterior` · formato `0`

**O que faz:**
1 quando o ano de referência pode ser comparado com o anterior (não é 2009 nem 2022, a quebra do eSocial).

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A) && A <> 2009 && A <> 2022, 1, 0)
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`.

**Usa:** `Ano_Ref`
**É usada por:** `Empregos_Ano_Anterior`

---

## Base\Apoio

1 medidas.

### Info_Gatilho_Valor

`_medidas.Info_Gatilho_Valor` · formato `0`

**O que faz:**
Valor constante usado pelos mini-gráficos transparentes que abrem tooltips (botões ⓘ).

**DAX:**
```dax
1
```

**Como funciona:**
Expressão direta, sem variáveis.

**Usa:** —
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL, Empregos · Todos os setores, Quanto ganha · AFL, Quanto ganha · Todos os setores, Quem trabalha · AFL, Quem trabalha · Todos os setores, Ranking · AFL, Ranking · Todos os setores

---

## Base\Comparavel

3 medidas.

### Empregos_Ref_Comparavel

`_medidas.Empregos_Ref_Comparavel` · formato `#,0`

**O que faz:**
Empregos_Ref só do grupo Comparável, independente do filtro de setores da página.

**DAX:**
```dax
CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Rank_Divisao), REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`, `D_Rank_Divisao`.

**Usa:** `Empregos_Ref`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `Emp_UF_Peso_AFL`, `KPI_Peso_AFL_HTML`, `KPI_Peso_Total_HTML`, `Tip_Emp_Ano_HTML`, `Tip_Emp_UF_HTML`

---

### Empregos_Var_Pct_Comparavel

`_medidas.Empregos_Var_Pct_Comparavel` · formato `+0.0%;-0.0%;0.0%`

**O que faz:**
Empregos_Var_Pct só do grupo Comparável, independente do filtro de setores da página.

**DAX:**
```dax
CALCULATE([Empregos_Var_Pct], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Empregos_Var_Pct`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `KPI_Emp_AFL_HTML`, `KPI_Emp_Total_HTML`, `Tip_Emp_Ano_HTML`, `Titulo_Emp_Var_AFL_HTML`

---

### Remuneracao_Media_Ref_Comparavel

`_medidas.Remuneracao_Media_Ref_Comparavel` · formato `#,0.00`

**O que faz:**
Remuneracao_Media_Ref só do grupo Comparável, independente do filtro de setores da página.

**DAX:**
```dax
CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Remuneracao_Media_Ref`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `KPI_RemMedia_AFL_HTML`, `Manchete_Salario_AFL_HTML`, `Rem_Esc_Comp`, `Rem_UF_Razao_Comp`, `Tip_Rem_Ano_HTML`, `Tip_Rem_UF_HTML`, `Titulo_Rem_Esc_HTML`

---

## Base\Empregos

5 medidas.

### Empregos

`_medidas.Empregos` · formato `#,0`

**O que faz:**
Vínculos ativos em 31/12 no contexto. Em visuais por ano é o estoque do ano; não some anos.

**DAX:**
```dax
VAR DivisoesSelecionadas = VALUES(D_Rank_Divisao[nm_divisao])
VAR HaFiltroDeRanking = ISFILTERED(D_Rank_Divisao[nm_divisao]) || ISFILTERED(D_Rank_Divisao[setor_principal])
VAR AFLSelecionado = SELECTEDVALUE(D_Rank_Divisao[nm_divisao]) = "AFL · conjunto de 6 CNAEs"
RETURN
	IF(
		NOT HaFiltroDeRanking,
		SUM(F_rais[vinculos]),
		IF(
			AFLSelecionado,
			CALCULATE(SUM(F_rais[vinculos]), REMOVEFILTERS(D_Cnae), D_Cnae[setor_afl] = "Sim"),
			CALCULATE(SUM(F_rais[vinculos]), KEEPFILTERS(TREATAS(DivisoesSelecionadas, D_Cnae[divisao_afl])))
		)
	)
```

**Como funciona:**
Guarda 3 variável(is) (`DivisoesSelecionadas`, `HaFiltroDeRanking`, `AFLSelecionado`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; aplica filtro virtual com `TREATAS`; lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`). Filtros limpos: `D_Cnae`.

**Usa:** `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_Rank_Divisao[nm_divisao]`, `D_Rank_Divisao[setor_principal]`, `F_rais[vinculos]`
**É usada por:** `Ct_Esc_Qtd`, `Ct_Esc_Rep`, `Ct_Esc_Tot`, `Ct_Mul_Qtd`, `Ct_Mul_Rep`, `Ct_Mul_Tot`, `Ct_Neg_Qtd`, `Ct_Neg_Rep`, `Ct_Neg_Tot`, `Emp_Contratos_HTML`, `Emp_Sequencia_Altas_AFL`, `Empregos_Ano_Anterior`, `Empregos_Ref`, `Empregos_Ref_Todos`, `Ind_Valor_Ano`, `Ind_Valor_Ctx`, `Ind_Valor_Div`, `KPI_Ct_Esc_AFL_HTML`, `KPI_Ct_Esc_Total_HTML`, `Titulo_Emp_Contrato_HTML`

---

### Empregos_Ano_Anterior

`_medidas.Empregos_Ano_Anterior` · formato `#,0`

**O que faz:**
Empregos em 31/12 do ano anterior; BLANK em 2009 e em 2022 (quebra do eSocial: 2022 não se compara com 2021).

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF([Comparavel_Ano_Anterior] = 1, CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A - 1))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Comparavel_Ano_Anterior`, `Empregos`, `D_Ano[ano]`
**É usada por:** `Empregos_Var`, `Empregos_Var_Pct`

---

### Empregos_Ref

`_medidas.Empregos_Ref` · formato `#,0`

**O que faz:**
Empregos formais em 31/12 do ano de referência (um único ano).

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`
**É usada por:** `Ct_Div_Emp`, `Emp_CBO_Top`, `Emp_Divisao`, `Emp_UF_Pct_AFL`, `Empregos_Ref_AFL`, `Empregos_Ref_Comparavel`, `Empregos_Var`, `Esc_Comparacao_Pagina_HTML`, `KPI_Emp_AFL_HTML`, `KPI_Emp_Total_HTML`, `Manchete_Emp_AFL_HTML`, `Manchete_Emp_Total_HTML`, `Manchete_Perfil_AFL_HTML`, `Manchete_Perfil_Total_HTML`, `Manchete_Salario_AFL_HTML`, `Manchete_Salario_Total_HTML`, `Perf_Ate24`, `Perf_Intermitente`, `Perf_MedioMais`, `Perf_Mulheres`, `Perf_Primeiro`, `Perf_Superior`, `Pir_Homens`, `Pir_Mulheres`, `Raca_Comparacao_Pagina_HTML`, `Rem_UF_Geo`, `Tip_CBO_HTML`, `Tip_Emp_Ano_HTML`, `Tip_Emp_Ano_Sem_Comparaveis_HTML`, `Tip_Emp_Atividade_HTML`, `Tip_Ind_Atividade_HTML`, `Tip_Ind_UF_HTML`, `Tip_Pir_HTML`, `Titulo_CBO_HTML`, `Titulo_Emp_Atividades_HTML`, `Titulo_Emp_UF_AFL_HTML`, `Titulo_Esc_HTML`, `Titulo_Esc_Pagina_HTML`, `Titulo_Raca_HTML`, `Titulo_Raca_Pagina_HTML`
**Aparece nas páginas:** Empregos · AFL

---

### Empregos_Var

`_medidas.Empregos_Var` · formato `+#,0;-#,0;0`

**O que faz:**
Variação absoluta dos empregos sobre o ano anterior (BLANK quando não há ano comparável).

**DAX:**
```dax
VAR Ant = [Empregos_Ano_Anterior]
RETURN IF(NOT ISBLANK(Ant), [Empregos_Ref] - Ant)
```

**Como funciona:**
Guarda 1 variável(is) (`Ant`) e devolve o resultado no `RETURN`.

**Usa:** `Empregos_Ano_Anterior`, `Empregos_Ref`
**É usada por:** `Empregos_Var_Pct`, `KPI_Emp_AFL_HTML`, `KPI_Emp_Total_HTML`, `Manchete_Emp_AFL_HTML`, `Manchete_Emp_Total_HTML`

---

### Empregos_Var_Pct

`_medidas.Empregos_Var_Pct` · formato `+0.0%;-0.0%;0.0%`

**O que faz:**
Variação % dos empregos sobre o ano anterior (BLANK quando não há ano comparável).

**DAX:**
```dax
DIVIDE([Empregos_Var], [Empregos_Ano_Anterior])
```

**Como funciona:**
Divide com `DIVIDE`, que devolve BLANK quando o divisor é zero.

**Usa:** `Empregos_Ano_Anterior`, `Empregos_Var`
**É usada por:** `Emp_Atividade_Var`, `Empregos_Var_Pct_AFL`, `Empregos_Var_Pct_Comparavel`, `Empregos_Var_Pct_Sel_Pos`, `Empregos_Var_Pct_Sel_Pre`, `KPI_Emp_AFL_HTML`, `KPI_Emp_Total_HTML`, `Manchete_Emp_AFL_HTML`, `Manchete_Emp_Total_HTML`, `Tip_Emp_Ano_HTML`, `Tip_Emp_Ano_Sem_Comparaveis_HTML`, `Titulo_Emp_Var_AFL_HTML`, `Titulo_Emp_Var_Total_HTML`

---

## Base\Remuneração

3 medidas.

### Remuneracao_Media

`_medidas.Remuneracao_Media` · formato `#,0.00`

**O que faz:**
Remuneração média de dezembro (R$ nominais) no contexto = soma ÷ quantidade de salários válidos (0,3 a 150 SM).

**DAX:**
```dax
DIVIDE(SUM(F_rais[soma_salario_valido]), SUM(F_rais[qtd_salario_valido]))
```

**Como funciona:**
Divide com `DIVIDE`, que devolve BLANK quando o divisor é zero.

**Usa:** `F_rais[qtd_salario_valido]`, `F_rais[soma_salario_valido]`
**É usada por:** `Ct_Esc_Sal`, `Ct_Mul_Sal`, `Ct_Neg_Sal`, `KPI_Ct_Esc_AFL_HTML`, `KPI_Ct_Esc_Total_HTML`, `Rem_Media_AFL_Pos`, `Rem_Media_AFL_Pre`, `Rem_Media_Comp_Pos`, `Rem_Media_Comp_Pre`, `Rem_Media_Sel_Pos`, `Rem_Media_Sel_Pre`, `Remuneracao_Media_Ref`

---

### Remuneracao_Media_Ref

`_medidas.Remuneracao_Media_Ref` · formato `#,0.00`

**O que faz:**
Remuneração média de dezembro do ano de referência (R$ nominais).

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Remuneracao_Media`, `D_Ano[ano]`
**É usada por:** `KPI_RemMedia_AFL_HTML`, `KPI_RemMedia_Total_HTML`, `Manchete_Salario_Total_HTML`, `Rem_Esc_Sel`, `Rem_Razao_Raca`, `Rem_Razao_Sexo`, `Rem_UF_Geo`, `Remuneracao_Media_Ref_AFL`, `Remuneracao_Media_Ref_Comparavel`, `Tip_CBO_HTML`, `Tip_Rem_Ano_HTML`, `Tip_Rem_Ano_Total_HTML`, `Tip_Rem_Gap_Raca_HTML`, `Tip_Rem_Gap_Sexo_HTML`, `Tip_Rem_UF_HTML`, `Titulo_Rem_UF_HTML`
**Aparece nas páginas:** Quem trabalha · AFL, Quem trabalha · Todos os setores

---

### Remuneracao_Media_SM_Ref

`_medidas.Remuneracao_Media_SM_Ref` · formato `0.00`

**O que faz:**
Remuneração média de dezembro do ano de referência em salários mínimos.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), CALCULATE(DIVIDE(SUM(F_rais[soma_sm_valido]), SUM(F_rais[qtd_salario_valido])), REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `D_Ano[ano]`, `F_rais[qtd_salario_valido]`, `F_rais[soma_sm_valido]`
**É usada por:** `KPI_RemMedia_AFL_HTML`, `KPI_RemMedia_Total_HTML`

---

## Empregos\Apoio

5 medidas.

### Contexto_Emp_AFL

`_medidas.Contexto_Emp_AFL` · formato `—`

**O que faz:**
Linha de contexto da página Empregos · AFL.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR TemUF = ISFILTERED(D_regiao[uf])
VAR NUF = COUNTROWS(VALUES(D_regiao[uf]))
VAR Local = IF(NOT TemUF || NUF = COUNTROWS(ALL(D_regiao[uf])), "Brasil", IF(NUF = 1, SELECTEDVALUE(D_regiao[estado]), NUF & " UFs"))
VAR Sexo = IF(ISFILTERED(D_Sexo[sexo]), CONCATENATEX(VALUES(D_Sexo[sexo]), D_Sexo[sexo], ", "), "")
VAR Esc = IF(ISFILTERED(D_Escolaridade[escolaridade_agrupada]), CONCATENATEX(VALUES(D_Escolaridade[escolaridade_agrupada]), D_Escolaridade[escolaridade_agrupada], ", "), "")
VAR Raca = IF(ISFILTERED(D_Raca[raca_cor]), CONCATENATEX(VALUES(D_Raca[raca_cor]), D_Raca[raca_cor], ", "), "")
VAR Setor = IF(ISFILTERED(D_AflAtividade[nome]) && COUNTROWS(VALUES(D_AflAtividade[nome])) < COUNTROWS(ALL(D_AflAtividade[nome])), CONCATENATEX(VALUES(D_AflAtividade[nome]), D_AflAtividade[nome], ", "), "alimentação fora do lar (AFL)")
VAR Partes = FILTER(UNION(ROW("@o", 1, "@t", "31/12/" & A), ROW("@o", 2, "@t", Local), ROW("@o", 3, "@t", Setor), ROW("@o", 4, "@t", Sexo),
    ROW("@o", 5, "@t", Esc), ROW("@o", 6, "@t", Raca), ROW("@o", 7, "@t", "RAIS (" & IF(A >= 2022, "eSocial", "declaratória") & ")")), NOT ISBLANK([@t]) && [@t] <> "")
VAR Texto = CONCATENATEX(Partes, [@t], " · ", [@o], ASC)
RETURN IF(ISBLANK(A), "", Texto)
```

**Como funciona:**
Guarda 10 variável(is) (`A`, `TemUF`, `NUF`, `Local`, `Sexo`, `Esc`, `Raca`, `Setor`…) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`); junta textos com `CONCATENATEX`.

**Usa:** `Ano_Ref`, `D_AflAtividade[nome]`, `D_Escolaridade[escolaridade_agrupada]`, `D_Raca[raca_cor]`, `D_Sexo[sexo]`, `D_regiao[estado]`, `D_regiao[uf]`
**É usada por:** `Manchete_Emp_AFL_HTML`, `Manchete_Perfil_AFL_HTML`, `Manchete_Salario_AFL_HTML`

---

### Contexto_Emp_Total

`_medidas.Contexto_Emp_Total` · formato `—`

**O que faz:**
Linha de contexto da página Empregos · Todos os setores.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR TemUF = ISFILTERED(D_regiao[uf])
VAR NUF = COUNTROWS(VALUES(D_regiao[uf]))
VAR Local = IF(NOT TemUF || NUF = COUNTROWS(ALL(D_regiao[uf])), "Brasil", IF(NUF = 1, SELECTEDVALUE(D_regiao[estado]), NUF & " UFs"))
VAR Sexo = IF(ISFILTERED(D_Sexo[sexo]), CONCATENATEX(VALUES(D_Sexo[sexo]), D_Sexo[sexo], ", "), "")
VAR Esc = IF(ISFILTERED(D_Escolaridade[escolaridade_agrupada]), CONCATENATEX(VALUES(D_Escolaridade[escolaridade_agrupada]), D_Escolaridade[escolaridade_agrupada], ", "), "")
VAR Raca = IF(ISFILTERED(D_Raca[raca_cor]), CONCATENATEX(VALUES(D_Raca[raca_cor]), D_Raca[raca_cor], ", "), "")
VAR Setor = [Setor_Emp_Total]
VAR Partes = FILTER(UNION(ROW("@o", 1, "@t", "31/12/" & A), ROW("@o", 2, "@t", Local), ROW("@o", 3, "@t", Setor), ROW("@o", 4, "@t", Sexo),
    ROW("@o", 5, "@t", Esc), ROW("@o", 6, "@t", Raca), ROW("@o", 7, "@t", "RAIS (" & IF(A >= 2022, "eSocial", "declaratória") & ")")), NOT ISBLANK([@t]) && [@t] <> "")
VAR Texto = CONCATENATEX(Partes, [@t], " · ", [@o], ASC)
RETURN IF(ISBLANK(A), "", Texto)
```

**Como funciona:**
Guarda 10 variável(is) (`A`, `TemUF`, `NUF`, `Local`, `Sexo`, `Esc`, `Raca`, `Setor`…) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`); junta textos com `CONCATENATEX`.

**Usa:** `Ano_Ref`, `Setor_Emp_Total`, `D_Escolaridade[escolaridade_agrupada]`, `D_Raca[raca_cor]`, `D_Sexo[sexo]`, `D_regiao[estado]`, `D_regiao[uf]`
**É usada por:** `Manchete_Emp_Total_HTML`, `Manchete_Perfil_Total_HTML`, `Manchete_Salario_Total_HTML`

---

### Emp_Sequencia_Altas_AFL

`_medidas.Emp_Sequencia_Altas_AFL` · formato `0`

**O que faz:**
Quantos anos seguidos o emprego do AFL subiu, terminando no ano de referência e sem atravessar a quebra de 2022.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR I = [Ano_Inicio_Trecho]
VAR T = ADDCOLUMNS(GENERATESERIES(I + 1, MAX(A, I + 1)), "@var", VAR y = [Value] RETURN
    CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = y) - CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = y - 1))
VAR UltimaNaoAlta = MAXX(FILTER(T, [@var] <= 0), [Value])
RETURN IF(A > I, A - COALESCE(UltimaNaoAlta, I), 0)
```

**Como funciona:**
Guarda 5 variável(is) (`A`, `I`, `T`, `y`, `UltimaNaoAlta`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; pega o maior valor de uma lista com `MAXX`; monta uma tabela virtual com `ADDCOLUMNS`. Filtros limpos: `D_Ano`, `D_Calendario`, `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Inicio_Trecho`, `Ano_Ref`, `Empregos`, `D_Ano[ano]`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `Manchete_Emp_AFL_HTML`, `Manchete_Emp_Total_HTML`

---

### Empregos_Ref_Todos

`_medidas.Empregos_Ref_Todos` · formato `#,0`

**O que faz:**
Empregos do ano de referência ignorando setor, comparabilidade e atividade (mantém UF, sexo, escolaridade e raça).

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), REMOVEFILTERS(D_Comparavel), REMOVEFILTERS(D_AflAtividade), REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_AflAtividade`, `D_Ano`, `D_Calendario`, `D_Cnae`, `D_Comparavel`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`
**É usada por:** `KPI_Peso_AFL_HTML`, `KPI_Peso_Total_HTML`, `Tip_Emp_Divisao_HTML`

---

### Setor_Emp_Total

`_medidas.Setor_Emp_Total` · formato `—`

**O que faz:**
Texto do recorte de setor da página Todos os setores: divisão(ões) escolhida(s), comparáveis, demais setores ou todos os setores.

**DAX:**
```dax
VAR NDiv = COUNTROWS(VALUES(D_Cnae[divisao_afl]))
RETURN IF(ISFILTERED(D_Cnae[divisao_afl]) && NDiv < COUNTROWS(ALL(D_Cnae[divisao_afl])), IF(NDiv = 1, SELECTEDVALUE(D_Cnae[divisao_afl]), NDiv & " divisões"),
    IF(ISFILTERED(D_Comparavel[comparavel_AFL_rotulo]) && COUNTROWS(VALUES(D_Comparavel[comparavel_AFL_rotulo])) = 1, SUBSTITUTE(LOWER(SELECTEDVALUE(D_Comparavel[comparavel_AFL_rotulo])), "afl", "AFL"), "todos os setores"))
```

**Como funciona:**
Guarda 1 variável(is) (`NDiv`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`).

**Usa:** `D_Cnae[divisao_afl]`, `D_Comparavel[comparavel_AFL_rotulo]`
**É usada por:** `Contexto_Emp_Total`, `Manchete_Emp_Total_HTML`, `Titulo_Emp_Var_AFL_HTML`, `Titulo_Emp_Var_Total_HTML`

---

## Empregos\Atividades

1 medidas.

### Emp_Atividade_Var

`_medidas.Emp_Atividade_Var` · formato `+0.0%;-0.0%;0.0%`

**O que faz:**
Variação % dos empregos da atividade do AFL sobre o ano anterior (BLANK quando não há ano comparável).

**DAX:**
```dax
[Empregos_Var_Pct]
```

**Como funciona:**
Expressão direta, sem variáveis.

**Usa:** `Empregos_Var_Pct`
**É usada por:** `Tip_Emp_Atividade_HTML`
**Aparece nas páginas:** Empregos · AFL

---

## Empregos\Ranking

5 medidas.

### Cor_Emp_Divisao

`_medidas.Cor_Emp_Divisao` · formato `—`

**O que faz:**
Cor do ranking: AFL em laranja, demais divisões em cinza neutro.

**DAX:**
```dax
IF(SELECTEDVALUE(D_Rank_Divisao[nm_divisao]) = "AFL · conjunto de 6 CNAEs", "#D97706", "#DDDDDE")
```

**Como funciona:**
Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `D_Rank_Divisao[nm_divisao]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · Todos os setores

---

### Emp_Divisao

`_medidas.Emp_Divisao` · formato `#,0`

**O que faz:**
Empregos em 31/12 da divisão de D_Rank_Divisao no ano de referência; o item AFL usa os seis CNAEs e as divisões não incluem os CNAEs do AFL.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
VAR A = [Ano_Ref]
RETURN IF(ISBLANK(Nome) || ISBLANK(A), BLANK(), IF(Nome = "AFL · conjunto de 6 CNAEs", [Empregos_Ref_AFL],
    CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 2 variável(is) (`Nome`, `A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `Empregos_Ref_AFL`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Emp_Divisao_Top`, `Emp_Posicao_AFL_Divisao`, `Emp_Total_Divisoes`, `Tip_Emp_Divisao_HTML`, `Tip_Ind_Divisao_HTML`

---

### Emp_Divisao_Top

`_medidas.Emp_Divisao_Top` · formato `#,0`

**O que faz:**
Valor do ranking: as 10 maiores divisões em empregos e sempre o AFL; as demais voltam BLANK.

**DAX:**
```dax
VAR EhAFL = SELECTEDVALUE(D_Rank_Divisao[nm_divisao]) = "AFL · conjunto de 6 CNAEs"
VAR Valor = [Emp_Divisao]
VAR Posicao = IF(NOT ISBLANK(Valor), RANKX(ALLSELECTED(D_Rank_Divisao[nm_divisao]), [Emp_Divisao], , DESC, DENSE))
RETURN IF(NOT ISBLANK(Valor) && (EhAFL || Posicao <= 10), Valor)
```

**Como funciona:**
Guarda 3 variável(is) (`EhAFL`, `Valor`, `Posicao`) e devolve o resultado no `RETURN`. Respeita só a seleção da página com `ALLSELECTED`; lê a escolha do usuário com `SELECTEDVALUE`; calcula posição com `RANKX`.

**Usa:** `Emp_Divisao`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · Todos os setores

---

### Emp_Posicao_AFL_Divisao

`_medidas.Emp_Posicao_AFL_Divisao` · formato `0`

**O que faz:**
Posição do AFL entre todas as divisões em empregos (ignora os botões de setor).

**DAX:**
```dax
VAR Divs = ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), "@v", [Emp_Divisao])
VAR Validas = FILTER(Divs, NOT ISBLANK([@v]))
VAR ValorAFL = MAXX(FILTER(Validas, [nm_divisao] = "AFL · conjunto de 6 CNAEs"), [@v])
RETURN IF(NOT ISBLANK(ValorAFL), COUNTROWS(FILTER(Validas, [@v] > ValorAFL)) + 1)
```

**Como funciona:**
Guarda 3 variável(is) (`Divs`, `Validas`, `ValorAFL`) e devolve o resultado no `RETURN`. Pega o maior valor de uma lista com `MAXX`; monta uma tabela virtual com `ADDCOLUMNS`.

**Usa:** `Emp_Divisao`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Manchete_Emp_Total_HTML`, `Titulo_Emp_Ranking_HTML`

---

### Emp_Total_Divisoes

`_medidas.Emp_Total_Divisoes` · formato `0`

**O que faz:**
Quantidade de divisões com empregos no contexto (ignora os botões de setor).

**DAX:**
```dax
COUNTROWS(FILTER(ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), "@v", [Emp_Divisao]), NOT ISBLANK([@v])))
```

**Como funciona:**
Monta uma tabela virtual com `ADDCOLUMNS`.

**Usa:** `Emp_Divisao`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Manchete_Emp_Total_HTML`, `Tip_Emp_Divisao_HTML`, `Titulo_Emp_Ranking_HTML`

---

## Empregos\Séries

4 medidas.

### Empregos_Var_Pct_AFL_Pos

`_medidas.Empregos_Var_Pct_AFL_Pos` · formato `+0%;-0%;0%`

**O que faz:**
Medida de apoio usada por outras medidas. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A) && A >= 2023, [Empregos_Var_Pct_AFL])
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`.

**Usa:** `Ano_Ref`, `Empregos_Var_Pct_AFL`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL

---

### Empregos_Var_Pct_AFL_Pre

`_medidas.Empregos_Var_Pct_AFL_Pre` · formato `+0%;-0%;0%`

**O que faz:**
Trechos da variação anual: 2022 inicia a nova fonte como base zero, sem ligação à série anterior.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A) && A < 2022, [Empregos_Var_Pct_AFL])
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`.

**Usa:** `Ano_Ref`, `Empregos_Var_Pct_AFL`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL

---

### Empregos_Var_Pct_Sel_Pos

`_medidas.Empregos_Var_Pct_Sel_Pos` · formato `+0%;-0%;0%`

**O que faz:**
Medida de apoio usada por outras medidas. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A) && A >= 2023, [Empregos_Var_Pct])
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`.

**Usa:** `Ano_Ref`, `Empregos_Var_Pct`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · Todos os setores

---

### Empregos_Var_Pct_Sel_Pre

`_medidas.Empregos_Var_Pct_Sel_Pre` · formato `+0%;-0%;0%`

**O que faz:**
Medida de apoio usada por outras medidas. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A) && A < 2022, [Empregos_Var_Pct])
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`.

**Usa:** `Ano_Ref`, `Empregos_Var_Pct`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · Todos os setores

---

## Empregos\UF

3 medidas.

### Emp_UF_Pct_AFL

`_medidas.Emp_UF_Pct_AFL` · formato `0.0%`

**O que faz:**
Participação do estado (ou do município, dentro do estado) no total de empregos do AFL em 31/12 do ano de referência. Total = todos os estados do filtro atual (ALLSELECTED); no nível município, o total do estado.

**DAX:**
```dax
VAR V = [Empregos_Ref]
VAR D = IF(ISINSCOPE(D_regiao[municipio]), CALCULATE([Empregos_Ref], REMOVEFILTERS(D_regiao[municipio])), CALCULATE([Empregos_Ref], ALLSELECTED(D_regiao)))
RETURN IF(NOT ISBLANK(V), DIVIDE(V, D))
```

**Como funciona:**
Guarda 2 variável(is) (`V`, `D`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; respeita só a seleção da página com `ALLSELECTED`; muda conforme o nível do visual (`ISINSCOPE`); divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_regiao[municipio]`.

**Usa:** `Empregos_Ref`, `D_regiao[municipio]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL

---

### Emp_UF_Peso_AFL

`_medidas.Emp_UF_Peso_AFL` · formato `0.0%`

**O que faz:**
Peso do AFL nos empregos comparáveis da UF: AFL ÷ (AFL + comparáveis).

**DAX:**
```dax
DIVIDE([Empregos_Ref_AFL], [Empregos_Ref_AFL] + [Empregos_Ref_Comparavel])
```

**Como funciona:**
Divide com `DIVIDE`, que devolve BLANK quando o divisor é zero.

**Usa:** `Empregos_Ref_AFL`, `Empregos_Ref_Comparavel`
**É usada por:** `Emp_UF_Peso_Geo`, `Tip_Emp_UF_HTML`, `Titulo_Emp_UF_AFL_HTML`, `Titulo_Emp_UF_Total_HTML`
**Aparece nas páginas:** Empregos · AFL

---

### Emp_UF_Peso_Geo

`_medidas.Emp_UF_Peso_Geo` · formato `0.0%`

**O que faz:**
Peso do AFL nos empregos comparáveis para o gráfico geográfico (UF e, ao descer, município; município só com 100 empregos do AFL ou mais).

**DAX:**
```dax
IF(ISINSCOPE(D_regiao[municipio]), IF([Empregos_Ref_AFL] >= 100, [Emp_UF_Peso_AFL]), [Emp_UF_Peso_AFL])
```

**Como funciona:**
Muda conforme o nível do visual (`ISINSCOPE`).

**Usa:** `Emp_UF_Peso_AFL`, `Empregos_Ref_AFL`, `D_regiao[municipio]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · Todos os setores

---

## HTML\Dicas

6 medidas.

### Tip_Contrata_Dif_HTML

`_medidas.Tip_Contrata_Dif_HTML` · formato `—`

**O que faz:**
Tooltip do KPI de diferença em pontos percentuais.

**DAX:**
```dax
VAR Afl = [Ind_Valor_AFL]
VAR Comp = [Ind_Valor_Comp]
VAR Dif = (Afl - Comp) * 100
VAR Rot = [Ind_Rotulo]
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:20px 24px;box-sizing:border-box;width:100%;height:100%;color:#1D1E21;'>"
 & "<div style='font-size:23px;line-height:28px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("O que é ponto percentual (p.p.)", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:10px;font-size:19px;line-height:27px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("É a diferença entre dois percentuais. Não é uma variação percentual: indo de 39,6% para 55,6%, a diferença é de 16,0 pontos percentuais, e não de 16%.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:16px;padding:12px 16px;background:#FDF7F1;border-left:4px solid #F58220;border-radius:6px;font-size:19px;line-height:28px;'><b>Exemplo</b><br>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Dif), "Sem dados para os filtros escolhidos.", "AFL " & FORMAT(Afl, "0.0%", "pt-BR") & " − Comparáveis " & FORMAT(Comp, "0.0%", "pt-BR") & " = " & IF(Dif > 0, "+", IF(Dif < 0, "−", "")) & FORMAT(ABS(Dif), "0.0", "pt-BR") & " p.p. (" & Rot & ")"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;"), "[[br]]", "<br>") & "</div>"
 & "<div style='margin-top:14px;font-size:16px;line-height:22px;color:#667085;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Comparáveis: setores usados como referência para o AFL.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 4 variável(is) (`Afl`, `Comp`, `Dif`, `Rot`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ind_Rotulo`, `Ind_Valor_AFL`, `Ind_Valor_Comp`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Dica · Contrata Dif

---

### Tip_Contrata_Max_AFL_HTML

`_medidas.Tip_Contrata_Max_AFL_HTML` · formato `—`

**O que faz:**
Tooltip do KPI de maior valor entre as atividades do AFL.

**DAX:**
```dax
VAR Lider = [Ind_Atividade_Lider]
VAR Valor = [Ind_Atividade_Lider_Valor]
VAR Frase = [Ind_Frase]
VAR Rot = [Ind_Rotulo]
VAR A = [Ind_Ano]
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:20px 24px;box-sizing:border-box;width:100%;height:100%;color:#1D1E21;'>"
 & "<div style='font-size:23px;line-height:28px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Maior valor entre as atividades", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:10px;font-size:19px;line-height:27px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("É a atividade (CNAE) do AFL com a maior participação de " & Rot & " entre os seus empregados.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:16px;padding:12px 16px;background:#FDF7F1;border-left:4px solid #F58220;border-radius:6px;font-size:19px;line-height:28px;'><b>Exemplo</b><br>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Valor), "Sem dados para os filtros escolhidos.", "Em " & A & ", " & Lider & ": " & FORMAT(Valor, "0.0%", "pt-BR") & " " & Frase & "."), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;"), "[[br]]", "<br>") & "</div>"
 & "<div style='margin-top:14px;font-size:16px;line-height:22px;color:#667085;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("O AFL reúne seis atividades: restaurantes, lanchonetes, bares com e sem entretenimento, padarias (revenda) e alimentos preparados para consumo domiciliar.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`Lider`, `Valor`, `Frase`, `Rot`, `A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ind_Ano`, `Ind_Atividade_Lider`, `Ind_Atividade_Lider_Valor`, `Ind_Frase`, `Ind_Rotulo`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Dica · Contrata Max AFL

---

### Tip_Contrata_Max_Total_HTML

`_medidas.Tip_Contrata_Max_Total_HTML` · formato `—`

**O que faz:**
Tooltip do KPI de maior valor entre as divisões.

**DAX:**
```dax
VAR Divisao = [Ind_Maior_Divisao]
VAR Valor = [Ind_Maior_Valor]
VAR Frase = [Ind_Frase]
VAR Rot = [Ind_Rotulo]
VAR A = [Ind_Ano]
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:20px 24px;box-sizing:border-box;width:100%;height:100%;color:#1D1E21;'>"
 & "<div style='font-size:23px;line-height:28px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Maior valor entre as divisões", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:10px;font-size:19px;line-height:27px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("É a divisão da CNAE com a maior participação de " & Rot & " entre os empregados, considerando só divisões com 50 mil empregos ou mais.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:16px;padding:12px 16px;background:#FDF7F1;border-left:4px solid #F58220;border-radius:6px;font-size:19px;line-height:28px;'><b>Exemplo</b><br>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Valor), "Sem dados para os filtros escolhidos.", "Em " & A & ", em " & Divisao & ", " & FORMAT(Valor, "0.0%", "pt-BR") & " " & Frase & "."), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;"), "[[br]]", "<br>") & "</div>"
 & "<div style='margin-top:14px;font-size:16px;line-height:22px;color:#667085;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Nome oficial da divisão CNAE.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`Divisao`, `Valor`, `Frase`, `Rot`, `A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ind_Ano`, `Ind_Frase`, `Ind_Maior_Divisao`, `Ind_Maior_Valor`, `Ind_Rotulo`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Dica · Contrata Max Total

---

### Tip_Contrata_Pos_HTML

`_medidas.Tip_Contrata_Pos_HTML` · formato `—`

**O que faz:**
Tooltip do KPI de posição do AFL no ranking de divisões.

**DAX:**
```dax
VAR Pos = [Ind_Posicao_AFL]
VAR N = [Ind_Total_Divisoes]
VAR Afl = [Ind_Valor_AFL]
VAR Frase = [Ind_Frase]
VAR Rot = [Ind_Rotulo]
VAR A = [Ind_Ano]
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:20px 24px;box-sizing:border-box;width:100%;height:100%;color:#1D1E21;'>"
 & "<div style='font-size:23px;line-height:28px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Posição do AFL no ranking", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:10px;font-size:19px;line-height:27px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("As divisões da CNAE com 50 mil empregos ou mais são ordenadas pela participação de " & Rot & " entre os empregados. A 1ª posição é a divisão em que essa participação é a maior. O AFL entra no ranking como um conjunto de 6 atividades.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:16px;padding:12px 16px;background:#FDF7F1;border-left:4px solid #F58220;border-radius:6px;font-size:19px;line-height:28px;'><b>Exemplo</b><br>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Pos), "Sem dados para os filtros escolhidos.", "Em " & A & ", " & FORMAT(Afl, "0.0%", "pt-BR") & " " & Frase & " no AFL. Ele é o " & Pos & "º entre " & N & " divisões" & IF(Pos > 1, ": " & (Pos - 1) & " divisões têm participação maior.", ": nenhuma divisão tem participação maior.")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;"), "[[br]]", "<br>") & "</div>"
 & "<div style='margin-top:14px;font-size:16px;line-height:22px;color:#667085;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("O indicador muda conforme o botão escolhido acima do ranking.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 6 variável(is) (`Pos`, `N`, `Afl`, `Frase`, `Rot`, `A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ind_Ano`, `Ind_Frase`, `Ind_Posicao_AFL`, `Ind_Rotulo`, `Ind_Total_Divisoes`, `Ind_Valor_AFL`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Dica · Contrata Pos

---

### Tip_RazaoRaca_HTML

`_medidas.Tip_RazaoRaca_HTML` · formato `—`

**O que faz:**
Tooltip do KPI de razão salarial (negros (pretos e pardos) ÷ brancos).

**DAX:**
```dax
VAR R = [Rem_Razao_Raca]
VAR RA = [Rem_Razao_Raca_AFL]
VAR RC = [Rem_Razao_Raca_Comp]
VAR A = [Ano_Ref]
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:20px 24px;box-sizing:border-box;width:100%;height:100%;color:#1D1E21;'>"
 & "<div style='font-size:23px;line-height:28px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Como ler: negros (pretos e pardos) ÷ brancos", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:10px;font-size:19px;line-height:27px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Divide a remuneração média de dezembro de negros (pretos e pardos) pela de brancos, com os mesmos filtros da página. 100% significa salários iguais; abaixo de 100%, os negros ganham menos.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:16px;padding:12px 16px;background:#FDF7F1;border-left:4px solid #F58220;border-radius:6px;font-size:19px;line-height:28px;'><b>Exemplo</b><br>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(R), "Sem dados para os filtros escolhidos.", "Para cada R$ 100 que os brancos recebem em média, os negros recebem R$ " & FORMAT(R * 100, "0", "pt-BR") & " (" & FORMAT(R, "0%", "pt-BR") & ")." & IF(ISBLANK(RA) || ISBLANK(RC), "", "[[br]]No AFL: R$ " & FORMAT(RA * 100, "0", "pt-BR") & " · nos Comparáveis: R$ " & FORMAT(RC * 100, "0", "pt-BR") & ".")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;"), "[[br]]", "<br>") & "</div>"
 & "<div style='margin-top:14px;font-size:16px;line-height:22px;color:#667085;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Remuneração de dezembro de " & A & ", em R$ nominais. Só entram empregados que declararam cor/raça.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 4 variável(is) (`R`, `RA`, `RC`, `A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Rem_Razao_Raca`, `Rem_Razao_Raca_AFL`, `Rem_Razao_Raca_Comp`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Dica · RazaoRaca

---

### Tip_RazaoSexo_HTML

`_medidas.Tip_RazaoSexo_HTML` · formato `—`

**O que faz:**
Tooltip do KPI de razão salarial (mulheres ÷ homens).

**DAX:**
```dax
VAR R = [Rem_Razao_Sexo]
VAR RA = [Rem_Razao_Sexo_AFL]
VAR RC = [Rem_Razao_Sexo_Comp]
VAR A = [Ano_Ref]
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:20px 24px;box-sizing:border-box;width:100%;height:100%;color:#1D1E21;'>"
 & "<div style='font-size:23px;line-height:28px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Como ler: mulheres ÷ homens", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:10px;font-size:19px;line-height:27px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Divide a remuneração média de dezembro de mulheres pela de homens, com os mesmos filtros da página. 100% significa salários iguais; abaixo de 100%, as mulheres ganham menos.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "<div style='margin-top:16px;padding:12px 16px;background:#FDF7F1;border-left:4px solid #F58220;border-radius:6px;font-size:19px;line-height:28px;'><b>Exemplo</b><br>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(R), "Sem dados para os filtros escolhidos.", "Para cada R$ 100 que os homens recebem em média, as mulheres recebem R$ " & FORMAT(R * 100, "0", "pt-BR") & " (" & FORMAT(R, "0%", "pt-BR") & ")." & IF(ISBLANK(RA) || ISBLANK(RC), "", "[[br]]No AFL: R$ " & FORMAT(RA * 100, "0", "pt-BR") & " · nos Comparáveis: R$ " & FORMAT(RC * 100, "0", "pt-BR") & ".")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;"), "[[br]]", "<br>") & "</div>"
 & "<div style='margin-top:14px;font-size:16px;line-height:22px;color:#667085;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Remuneração de dezembro de " & A & ", em R$ nominais. Todos os empregados, sem filtro de cor.", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
 & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 4 variável(is) (`R`, `RA`, `RC`, `A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Rem_Razao_Sexo`, `Rem_Razao_Sexo_AFL`, `Rem_Razao_Sexo_Comp`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Dica · RazaoSexo

---

## HTML\Empregos

3 medidas.

### Emp_Contratos_HTML

`_medidas.Emp_Contratos_HTML` · formato `—`

**O que faz:**
Tabela de contratos: AFL × Comparáveis, em % dos empregos de 31/12 do ano de referência (categorias exclusivas, na ordem intermitente, aprendiz, parcial, CLT, prazo determinado).

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR TotA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)
VAR cltA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] = "CLT Prazo Indeterminado"))
VAR detA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] IN {"CLT Prazo Determinado", "Contrato por Prazo Determinado", "Temporário", "Contrato Temporário"}))
VAR interA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] = "Sim"))
VAR parcA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] = "Sim"))
VAR aprA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] = "Aprendiz"))
VAR TotC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)
VAR cltC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] = "CLT Prazo Indeterminado"))
VAR detC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] IN {"CLT Prazo Determinado", "Contrato por Prazo Determinado", "Temporário", "Contrato Temporário"}))
VAR interC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] = "Sim"))
VAR parcC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] = "Sim"))
VAR aprC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] = "Aprendiz"))
RETURN IF(ISBLANK(A) || TotA = 0, "<div style='font-family:Segoe UI,Arial,sans-serif;font-size:21px;color:#434446;'>Sem dados para os filtros escolhidos.</div>",
    "<table style='width:100%;border-collapse:collapse;font-family:Segoe UI,Arial,sans-serif;font-size:21px;font-variant-numeric:tabular-nums;'><tr style='color:#434446;'><th style='text-align:left;font-weight:600;padding-bottom:6px;'>Contrato</th><th style='text-align:right;font-weight:600;color:#B86218;'>AFL</th><th style='text-align:right;font-weight:600;'>Comparáveis</th></tr>" & "<tr><td style='padding:9px 0;border-top:1px solid #E8E8E9;'>CLT por prazo indeterminado</td><td style='text-align:right;font-weight:600;border-top:1px solid #E8E8E9;'>" & IF(ISBLANK(TotA) || TotA = 0, "—", FORMAT(DIVIDE(cltA, TotA), "0.0%", "pt-BR")) & "</td><td style='text-align:right;color:#434446;border-top:1px solid #E8E8E9;'>" & IF(ISBLANK(TotC) || TotC = 0, "—", FORMAT(DIVIDE(cltC, TotC), "0.0%", "pt-BR")) & "</td></tr>" & "<tr><td style='padding:9px 0;border-top:1px solid #E8E8E9;'>Prazo determinado ou temporário</td><td style='text-align:right;font-weight:600;border-top:1px solid #E8E8E9;'>" & IF(ISBLANK(TotA) || TotA = 0, "—", FORMAT(DIVIDE(detA, TotA), "0.0%", "pt-BR")) & "</td><td style='text-align:right;color:#434446;border-top:1px solid #E8E8E9;'>" & IF(ISBLANK(TotC) || TotC = 0, "—", FORMAT(DIVIDE(detC, TotC), "0.0%", "pt-BR")) & "</td></tr>" & "<tr><td style='padding:9px 0;border-top:1px solid #E8E8E9;'>Intermitente</td><td style='text-align:right;font-weight:600;border-top:1px solid #E8E8E9;'>" & IF(ISBLANK(TotA) || TotA = 0, "—", FORMAT(DIVIDE(interA, TotA), "0.0%", "pt-BR")) & "</td><td style='text-align:right;color:#434446;border-top:1px solid #E8E8E9;'>" & IF(ISBLANK(TotC) || TotC = 0, "—", FORMAT(DIVIDE(interC, TotC), "0.0%", "pt-BR")) & "</td></tr>" & "<tr><td style='padding:9px 0;border-top:1px solid #E8E8E9;'>Parcial</td><td style='text-align:right;font-weight:600;border-top:1px solid #E8E8E9;'>" & IF(ISBLANK(TotA) || TotA = 0, "—", FORMAT(DIVIDE(parcA, TotA), "0.0%", "pt-BR")) & "</td><td style='text-align:right;color:#434446;border-top:1px solid #E8E8E9;'>" & IF(ISBLANK(TotC) || TotC = 0, "—", FORMAT(DIVIDE(parcC, TotC), "0.0%", "pt-BR")) & "</td></tr>" & "<tr><td style='padding:9px 0;border-top:1px solid #E8E8E9;'>Aprendiz</td><td style='text-align:right;font-weight:600;border-top:1px solid #E8E8E9;'>" & IF(ISBLANK(TotA) || TotA = 0, "—", FORMAT(DIVIDE(aprA, TotA), "0.0%", "pt-BR")) & "</td><td style='text-align:right;color:#434446;border-top:1px solid #E8E8E9;'>" & IF(ISBLANK(TotC) || TotC = 0, "—", FORMAT(DIVIDE(aprC, TotC), "0.0%", "pt-BR")) & "</td></tr>" & "</table>")
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 13 variável(is) (`A`, `TotA`, `cltA`, `detA`, `interA`, `parcA`, `aprA`, `TotC`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Ano`, `D_Calendario`, `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`, `D_GrupoSetor[grupo_setor]`, `F_rais[modalidade_contrato]`, `F_rais[trabalho_intermitente]`, `F_rais[trabalho_parcial]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL, Empregos · Todos os setores

---

### Manchete_Emp_AFL_HTML

`_medidas.Manchete_Emp_AFL_HTML` · formato `—`

**O que faz:**
Manchete da página Empregos · AFL.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR NUF = COUNTROWS(VALUES(D_regiao[uf]))
VAR Prep = IF(NOT ISFILTERED(D_regiao[uf]) || NUF = COUNTROWS(ALL(D_regiao[uf])), "No Brasil", IF(NUF = 1, "Em " & SELECTEDVALUE(D_regiao[estado]), "Nas " & NUF & " UFs escolhidas"))
VAR Valor = [Empregos_Ref]
VAR Variacao = [Empregos_Var]
VAR VarPct = [Empregos_Var_Pct]
VAR Seq = [Emp_Sequencia_Altas_AFL]
VAR Contexto = [Contexto_Emp_AFL]
VAR Fecho = SWITCH(TRUE(), ISBLANK(Variacao), IF(A = 2022, "primeiro ano da fonte eSocial", "primeiro ano da série"),
    Variacao > 0, IF(Seq >= 2, Seq & "ª alta seguida", "alta de " & IF(ISBLANK(VarPct), "—", FORMAT(VarPct, "0.0%", "pt-BR"))), Variacao < 0, "queda de " & IF(ISBLANK(ABS(VarPct)), "—", FORMAT(ABS(VarPct), "0.0%", "pt-BR")) & " sobre " & (A - 1), "estável")
VAR Texto = Prep & ", o AFL fechou " & A & " com " & FORMAT(Valor, "#,0", "pt-BR") & " empregos formais: " & Fecho
VAR Valido = NOT ISBLANK(A) && NOT ISBLANK(Valor)
RETURN
    IF(NOT Valido,
        "<div role='text' style='width:100%;height:118px;font-family:Segoe UI,Arial,sans-serif;font-size:24px;color:#434446;'>Não há dados para os filtros selecionados.</div>",
        "<div role='group' aria-label='Resumo do emprego formal' style='width:100%;height:118px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
            & "<div style='max-height:84px;overflow:hidden;'><span style='display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;min-width:0;font-size:34px;line-height:40px;font-weight:600;font-variant-numeric:tabular-nums;overflow:hidden;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Texto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span></div>"
            & "<div style='height:30px;margin:4px 0 0;font-size:24px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Contexto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
        & "</div>")
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 11 variável(is) (`A`, `NUF`, `Prep`, `Valor`, `Variacao`, `VarPct`, `Seq`, `Contexto`…) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`); escolhe o resultado com `SWITCH`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Contexto_Emp_AFL`, `Emp_Sequencia_Altas_AFL`, `Empregos_Ref`, `Empregos_Var`, `Empregos_Var_Pct`, `D_regiao[estado]`, `D_regiao[uf]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL

---

### Manchete_Emp_Total_HTML

`_medidas.Manchete_Emp_Total_HTML` · formato `—`

**O que faz:**
Manchete da página Empregos · Todos os setores.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR NUF = COUNTROWS(VALUES(D_regiao[uf]))
VAR Prep = IF(NOT ISFILTERED(D_regiao[uf]) || NUF = COUNTROWS(ALL(D_regiao[uf])), "No Brasil", IF(NUF = 1, "Em " & SELECTEDVALUE(D_regiao[estado]), "Nas " & NUF & " UFs escolhidas"))
VAR Valor = [Empregos_Ref]
VAR Variacao = [Empregos_Var]
VAR VarPct = [Empregos_Var_Pct]
VAR Seq = [Emp_Sequencia_Altas_AFL]
VAR Contexto = [Contexto_Emp_Total]
VAR Pos = [Emp_Posicao_AFL_Divisao]
VAR Divs = [Emp_Total_Divisoes]
VAR SetorTxt = [Setor_Emp_Total]
VAR Texto = Prep & ", " & IF(SetorTxt = "todos os setores", "o emprego formal", "o emprego em " & SetorTxt) & " fechou " & A & " com " & FORMAT(Valor, "#,0", "pt-BR") & " vínculos" & IF(ISBLANK(Pos) || SetorTxt <> "todos os setores", "", "; o AFL é a " & Pos & "ª maior divisão entre " & Divs)
VAR Valido = NOT ISBLANK(A) && NOT ISBLANK(Valor)
RETURN
    IF(NOT Valido,
        "<div role='text' style='width:100%;height:118px;font-family:Segoe UI,Arial,sans-serif;font-size:24px;color:#434446;'>Não há dados para os filtros selecionados.</div>",
        "<div role='group' aria-label='Resumo do emprego formal' style='width:100%;height:118px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
            & "<div style='max-height:84px;overflow:hidden;'><span style='display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;min-width:0;font-size:34px;line-height:40px;font-weight:600;font-variant-numeric:tabular-nums;overflow:hidden;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Texto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span></div>"
            & "<div style='height:30px;margin:4px 0 0;font-size:24px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Contexto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
        & "</div>")
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 13 variável(is) (`A`, `NUF`, `Prep`, `Valor`, `Variacao`, `VarPct`, `Seq`, `Contexto`…) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`); formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Contexto_Emp_Total`, `Emp_Posicao_AFL_Divisao`, `Emp_Sequencia_Altas_AFL`, `Emp_Total_Divisoes`, `Empregos_Ref`, `Empregos_Var`, `Empregos_Var_Pct`, `Setor_Emp_Total`, `D_regiao[estado]`, `D_regiao[uf]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · Todos os setores

---

## HTML\Empregos\KPIs

5 medidas.

### KPI_Emp_AFL_HTML

`_medidas.KPI_Emp_AFL_HTML` · formato `—`

**O que faz:**
KPI de empregos (página AFL): estoque em 31/12 com variação e referência dos comparáveis.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Valor = [Empregos_Ref]
VAR Variacao = [Empregos_Var]
VAR VarPct = [Empregos_Var_Pct]
VAR Icone = SWITCH(TRUE(), Variacao > 0, "▲", Variacao < 0, "▼", "●")
VAR Cor = SWITCH(TRUE(), Variacao > 0, "#137547", Variacao < 0, "#B42318", "#434446")
VAR Linha = IF(NOT ISBLANK(Variacao), Icone & " " & IF(Variacao > 0, "+", IF(Variacao < 0, "−", "")) & FORMAT(ABS(Variacao), "#,0", "pt-BR") & " (" & IF(ISBLANK(VarPct), "—", IF(VarPct > 0, "+", IF(VarPct < 0, "−", "")) & FORMAT(ABS(VarPct), "0.0%", "pt-BR")) & ") sobre " & (A - 1),
    IF(A = 2022, "2022 não se compara com 2021 (nova fonte: eSocial)", "Primeiro ano da série"))
VAR CorLinha = IF(ISBLANK(Variacao), "#434446", Cor)
VAR VarComp = [Empregos_Var_Pct_Comparavel]
RETURN
    "<div role='group' aria-label='KPI de empregos formais' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Empregos em 31/12/" & A & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & FORMAT(Valor, "#,0", "pt-BR") & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & CorLinha & ";overflow:hidden;'>" & Linha & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>Comparáveis " & IF(ISBLANK(VarComp), "—", IF(VarComp > 0, "+", IF(VarComp < 0, "−", "")) & FORMAT(ABS(VarComp), "0.0%", "pt-BR")) & " <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 9 variável(is) (`A`, `Valor`, `Variacao`, `VarPct`, `Icone`, `Cor`, `Linha`, `CorLinha`…) e devolve o resultado no `RETURN`. Escolhe o resultado com `SWITCH`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `Empregos_Var`, `Empregos_Var_Pct`, `Empregos_Var_Pct_Comparavel`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL

---

### KPI_Emp_Total_HTML

`_medidas.KPI_Emp_Total_HTML` · formato `—`

**O que faz:**
KPI de empregos (página Todos os setores): estoque em 31/12 com variação, chip AFL e referência dos comparáveis.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Valor = [Empregos_Ref]
VAR Variacao = [Empregos_Var]
VAR VarPct = [Empregos_Var_Pct]
VAR Icone = SWITCH(TRUE(), Variacao > 0, "▲", Variacao < 0, "▼", "●")
VAR Cor = SWITCH(TRUE(), Variacao > 0, "#137547", Variacao < 0, "#B42318", "#434446")
VAR Linha = IF(NOT ISBLANK(Variacao), Icone & " " & IF(Variacao > 0, "+", IF(Variacao < 0, "−", "")) & FORMAT(ABS(Variacao), "#,0", "pt-BR") & " (" & IF(ISBLANK(VarPct), "—", IF(VarPct > 0, "+", IF(VarPct < 0, "−", "")) & FORMAT(ABS(VarPct), "0.0%", "pt-BR")) & ") sobre " & (A - 1),
    IF(A = 2022, "2022 não se compara com 2021 (nova fonte: eSocial)", "Primeiro ano da série"))
VAR CorLinha = IF(ISBLANK(Variacao), "#434446", Cor)
VAR VarAFL = [Empregos_Var_Pct_AFL]
VAR VarComp = [Empregos_Var_Pct_Comparavel]
RETURN
    "<div role='group' aria-label='KPI de empregos formais' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Empregos em 31/12/" & A & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & FORMAT(Valor, "#,0", "pt-BR") & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & CorLinha & ";overflow:hidden;'>" & Linha & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #D97706;border-radius:6px;background:#FDF7F1;color:#B86218;font-size:20px;line-height:26px;font-weight:600;'>AFL " & IF(ISBLANK(VarAFL), "—", IF(VarAFL > 0, "+", IF(VarAFL < 0, "−", "")) & FORMAT(ABS(VarAFL), "0.0%", "pt-BR")) & "</span>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>Comparáveis " & IF(ISBLANK(VarComp), "—", IF(VarComp > 0, "+", IF(VarComp < 0, "−", "")) & FORMAT(ABS(VarComp), "0.0%", "pt-BR")) & " <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 10 variável(is) (`A`, `Valor`, `Variacao`, `VarPct`, `Icone`, `Cor`, `Linha`, `CorLinha`…) e devolve o resultado no `RETURN`. Escolhe o resultado com `SWITCH`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `Empregos_Var`, `Empregos_Var_Pct`, `Empregos_Var_Pct_AFL`, `Empregos_Var_Pct_Comparavel`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · Todos os setores

---

### KPI_Peso_AFL_HTML

`_medidas.KPI_Peso_AFL_HTML` · formato `—`

**O que faz:**
KPI de peso (página AFL): AFL ÷ (AFL + comparáveis) e participação em todo o emprego formal.

**DAX:**
```dax
VAR Afl = [Empregos_Ref_AFL]
VAR Comp = [Empregos_Ref_Comparavel]
VAR Todos = [Empregos_Ref_Todos]
VAR Peso = DIVIDE(Afl, Afl + Comp)
VAR PesoTodos = DIVIDE(Afl, Todos)
RETURN
    "<div role='group' aria-label='KPI de peso do AFL' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:20px;line-height:24px;font-weight:600;color:#434446;max-height:48px;overflow:hidden;'>" & "Representatividade de empregos do setor AFL em setores comparáveis" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK(Peso), "—", FORMAT(Peso, "0.0%", "pt-BR")) & "</div>"
        & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='font-size:21px;color:#434446;'>" & IF(ISBLANK(PesoTodos), "—", FORMAT(PesoTodos, "0.0%", "pt-BR")) & " de todo o emprego formal</span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`Afl`, `Comp`, `Todos`, `Peso`, `PesoTodos`) e devolve o resultado no `RETURN`. Divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Empregos_Ref_AFL`, `Empregos_Ref_Comparavel`, `Empregos_Ref_Todos`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL

---

### KPI_Peso_Total_HTML

`_medidas.KPI_Peso_Total_HTML` · formato `—`

**O que faz:**
KPI de peso (página Todos os setores): AFL ÷ todo o emprego formal e AFL ÷ (AFL + comparáveis).

**DAX:**
```dax
VAR Afl = [Empregos_Ref_AFL]
VAR Comp = [Empregos_Ref_Comparavel]
VAR Todos = [Empregos_Ref_Todos]
VAR Peso = DIVIDE(Afl, Todos)
VAR PesoComp = DIVIDE(Afl, Afl + Comp)
RETURN
    "<div role='group' aria-label='KPI de peso do AFL' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Presença do AFL nos empregos" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK(Peso), "—", FORMAT(Peso, "0.0%", "pt-BR")) & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & "#434446" & ";overflow:hidden;'>" & "de todo o emprego formal" & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>" & IF(ISBLANK(PesoComp), "—", FORMAT(PesoComp, "0.0%", "pt-BR")) & " do AFL + comparáveis <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`Afl`, `Comp`, `Todos`, `Peso`, `PesoComp`) e devolve o resultado no `RETURN`. Divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Empregos_Ref_AFL`, `Empregos_Ref_Comparavel`, `Empregos_Ref_Todos`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · Todos os setores

---

### KPI_Primeiro_Emprego_HTML

`_medidas.KPI_Primeiro_Emprego_HTML` · formato `—`

**O que faz:**
Card de KPI em HTML. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR P = [Perf_Primeiro]
RETURN "<div style='width:100%;height:172px;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;overflow:hidden;'><div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;'>Primeiro emprego</div><div style='margin-top:8px;font-size:53px;line-height:58px;font-weight:600;'>" & IF(ISBLANK(P), "—", FORMAT(P,"0.0%","pt-BR")) & "</div><div style='margin-top:4px;font-size:21px;line-height:26px;color:#434446;'>" & IF(A > 2021, "Sem dados em " & A & " · disponível até 2021", "dos empregos no ano selecionado") & "</div></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 2 variável(is) (`A`, `P`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Perf_Primeiro`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL, Empregos · Todos os setores

---

## HTML\Empregos\Títulos

7 medidas.

### Titulo_Emp_Atividades_HTML

`_medidas.Titulo_Emp_Atividades_HTML` · formato `—`

**O que faz:**
Título das atividades do AFL: atividade líder e peso nos empregos do AFL.

**DAX:**
```dax
VAR T = FILTER(ADDCOLUMNS(VALUES(D_AflAtividade[nome]), "@v", [Empregos_Ref]), NOT ISBLANK([@v]))
VAR Tot = SUMX(T, [@v])
VAR Lider = TOPN(1, T, [@v], DESC, D_AflAtividade[nome], ASC)
VAR Nome = CONCATENATEX(Lider, D_AflAtividade[nome], "")
VAR Peso = DIVIDE(MAXX(Lider, [@v]), Tot)
VAR L1 = IF(Tot = 0, "Sem dados para os filtros escolhidos", IF(COUNTROWS(T) = 1, Nome & " reúne todos os empregos do filtro", Nome & " concentra " & IF(ISBLANK(Peso), "—", FORMAT(Peso, "0.0%", "pt-BR")) & " dos empregos do AFL"))
VAR L2 = IF(Tot = 0, "", "Empregos em 31/12/" & [Ano_Ref] & " nas 6 atividades (CNAEs) do AFL")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#1D1E21" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 7 variável(is) (`T`, `Tot`, `Lider`, `Nome`, `Peso`, `L1`, `L2`) e devolve o resultado no `RETURN`. Divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; pega os primeiros com `TOPN`; soma linha a linha com `SUMX`; pega o maior valor de uma lista com `MAXX`; monta uma tabela virtual com `ADDCOLUMNS`; junta textos com `CONCATENATEX`.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `D_AflAtividade[nome]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL

---

### Titulo_Emp_Contrato_HTML

`_medidas.Titulo_Emp_Contrato_HTML` · formato `—`

**O que faz:**
Título do card de contratos: % de CLT por prazo indeterminado no AFL e o contraste com os comparáveis.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR TotA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)
VAR cltA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] = "CLT Prazo Indeterminado"))
VAR detA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] IN {"CLT Prazo Determinado", "Contrato por Prazo Determinado", "Temporário", "Contrato Temporário"}))
VAR interA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] = "Sim"))
VAR parcA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] = "Sim"))
VAR aprA = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] = "Aprendiz"))
VAR TotC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)
VAR cltC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] = "CLT Prazo Indeterminado"))
VAR detC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] IN {"CLT Prazo Determinado", "Contrato por Prazo Determinado", "Temporário", "Contrato Temporário"}))
VAR interC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] = "Sim"))
VAR parcC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] <> "Aprendiz"), KEEPFILTERS(F_rais[trabalho_parcial] = "Sim"))
VAR aprC = CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] <> "Sim"), KEEPFILTERS(F_rais[modalidade_contrato] = "Aprendiz"))
VAR PA = DIVIDE(cltA, TotA)
VAR PC = DIVIDE(cltC, TotC)
VAR DA = DIVIDE(detA, TotA)
VAR DC = DIVIDE(detC, TotC)
VAR L1 = IF(ISBLANK(A) || TotA = 0, "Sem dados para os filtros escolhidos", IF(ISBLANK(PA), "—", FORMAT(PA, "0.0%", "pt-BR")) & " dos empregos do AFL são CLT por prazo indeterminado")
VAR L2 = IF(L1 = "Sem dados para os filtros escolhidos", "", "Prazo determinado ou temporário: " & IF(ISBLANK(DA), "—", FORMAT(DA, "0.0%", "pt-BR")) & " no AFL e " & IF(ISBLANK(DC), "—", FORMAT(DC, "0.0%", "pt-BR")) & " nos comparáveis")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#1D1E21" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 19 variável(is) (`A`, `TotA`, `cltA`, `detA`, `interA`, `parcA`, `aprA`, `TotC`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Ano`, `D_Calendario`, `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`, `D_GrupoSetor[grupo_setor]`, `F_rais[modalidade_contrato]`, `F_rais[trabalho_intermitente]`, `F_rais[trabalho_parcial]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL, Empregos · Todos os setores

---

### Titulo_Emp_Ranking_HTML

`_medidas.Titulo_Emp_Ranking_HTML` · formato `—`

**O que faz:**
Título do ranking de divisões: posição do AFL em empregos e em crescimento.

**DAX:**
```dax
VAR Pos = [Emp_Posicao_AFL_Divisao]
VAR N = [Emp_Total_Divisoes]
VAR L1 = IF(ISBLANK(Pos), "O AFL não tem empregos para os filtros escolhidos", IF(Pos = 1, "O AFL é a maior divisão do emprego formal entre as " & N, "O AFL é a " & Pos & "ª maior divisão do emprego formal entre as " & N))
VAR L2 = IF(ISBLANK(Pos), "", "O gráfico mostra as 10 maiores divisões e o AFL, em empregos de 31/12/" & [Ano_Ref] & ". Compare por participação, nunca o AFL contra o total.")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#F58220" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 4 variável(is) (`Pos`, `N`, `L1`, `L2`) e devolve o resultado no `RETURN`.

**Usa:** `Ano_Ref`, `Emp_Posicao_AFL_Divisao`, `Emp_Total_Divisoes`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · Todos os setores

---

### Titulo_Emp_UF_AFL_HTML

`_medidas.Titulo_Emp_UF_AFL_HTML` · formato `—`

**O que faz:**
Título das UFs (página AFL): UF líder e participação nos empregos do AFL, com a UF onde o AFL mais pesa.

**DAX:**
```dax
VAR T = FILTER(ADDCOLUMNS(VALUES(D_regiao[uf]), "@v", [Empregos_Ref], "@p", [Emp_UF_Peso_AFL]), NOT ISBLANK([@v]))
VAR Tot = SUMX(T, [@v])
VAR Lider = TOPN(1, T, [@v], DESC, D_regiao[uf], ASC)
VAR UF = CONCATENATEX(Lider, D_regiao[uf], "")
VAR UFN = COALESCE(LOOKUPVALUE(D_regiao[estado], D_regiao[uf], UF), UF)
VAR Mais = TOPN(1, T, [@p], DESC, D_regiao[uf], ASC)
VAR UFMais = CONCATENATEX(Mais, D_regiao[uf], "")
VAR UFMaisN = COALESCE(LOOKUPVALUE(D_regiao[estado], D_regiao[uf], UFMais), UFMais)
VAR PMais = MAXX(Mais, [@p])
VAR L1 = IF(Tot = 0, "Sem dados para os filtros escolhidos", IF(COUNTROWS(T) = 1, UFN & " reúne os empregos do filtro", UFN & " tem " & IF(ISBLANK(DIVIDE(MAXX(Lider, [@v]), Tot)), "—", FORMAT(DIVIDE(MAXX(Lider, [@v]), Tot), "0.0%", "pt-BR")) & " dos empregos do AFL"))
VAR L2 = IF(Tot = 0 || COUNTROWS(T) = 1, "", "Onde o AFL pesa mais: " & UFMaisN & " (" & IF(ISBLANK(PMais), "—", FORMAT(PMais, "0.0%", "pt-BR")) & " dos empregos comparáveis)")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#1D1E21" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 11 variável(is) (`T`, `Tot`, `Lider`, `UF`, `UFN`, `Mais`, `UFMais`, `UFMaisN`…) e devolve o resultado no `RETURN`. Divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; pega os primeiros com `TOPN`; soma linha a linha com `SUMX`; pega o maior valor de uma lista com `MAXX`; monta uma tabela virtual com `ADDCOLUMNS`; busca um valor em outra tabela com `LOOKUPVALUE`.

**Usa:** `Emp_UF_Peso_AFL`, `Empregos_Ref`, `D_regiao[estado]`, `D_regiao[uf]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL

---

### Titulo_Emp_UF_Total_HTML

`_medidas.Titulo_Emp_UF_Total_HTML` · formato `—`

**O que faz:**
Título das UFs (página Todos os setores): UF onde o AFL mais pesa no emprego comparável.

**DAX:**
```dax
VAR T = FILTER(ADDCOLUMNS(VALUES(D_regiao[uf]), "@a", [Empregos_Ref_AFL], "@p", [Emp_UF_Peso_AFL]), NOT ISBLANK([@a]))
VAR Mais = TOPN(1, T, [@p], DESC, D_regiao[uf], ASC)
VAR UFMais = CONCATENATEX(Mais, D_regiao[uf], "")
VAR UFMaisN = COALESCE(LOOKUPVALUE(D_regiao[estado], D_regiao[uf], UFMais), UFMais)
VAR PMais = MAXX(Mais, [@p])
VAR L1 = IF(COUNTROWS(T) = 0, "Sem dados para os filtros escolhidos", IF(COUNTROWS(T) = 1, "Peso do AFL nos empregos comparáveis", "Em " & UFMaisN & ", o AFL é " & IF(ISBLANK(PMais), "—", FORMAT(PMais, "0.0%", "pt-BR")) & " do emprego comparável"))
VAR L2 = IF(COUNTROWS(T) = 0, "", "Peso do AFL nos empregos comparáveis, nas 10 UFs com mais empregos do AFL")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#1D1E21" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 7 variável(is) (`T`, `Mais`, `UFMais`, `UFMaisN`, `PMais`, `L1`, `L2`) e devolve o resultado no `RETURN`. Pega os primeiros com `TOPN`; pega o maior valor de uma lista com `MAXX`; monta uma tabela virtual com `ADDCOLUMNS`; busca um valor em outra tabela com `LOOKUPVALUE`; junta textos com `CONCATENATEX`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Emp_UF_Peso_AFL`, `Empregos_Ref_AFL`, `D_regiao[estado]`, `D_regiao[uf]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · Todos os setores

---

### Titulo_Emp_Var_AFL_HTML

`_medidas.Titulo_Emp_Var_AFL_HTML` · formato `—`

**O que faz:**
Título da variação anual do emprego (página AFL).

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR VA = [Empregos_Var_Pct_AFL]
VAR VC = [Empregos_Var_Pct_Comparavel]
VAR VS = [Empregos_Var_Pct]
VAR Nome = IF([Setor_Emp_Total] = "todos os setores", "o mercado formal", [Setor_Emp_Total])
VAR L1 = IF(ISBLANK(A), "Sem dados para os filtros escolhidos", IF(ISBLANK(VA), IF(A = 2022, "2022 não pode ser comparado com 2021 (nova fonte: eSocial)", "2009 é o primeiro ano da série: não há ano anterior"), "Em " & A & ", a quantidade de empregos " & IF(VA >= 0, "subiu ", "caiu ") & IF(ISBLANK(ABS(VA)), "—", FORMAT(ABS(VA), "0.0%", "pt-BR")) & IF(ISBLANK(VC), "", " (Comparáveis: " & IF(ISBLANK(VC), "—", IF(VC > 0, "+", IF(VC < 0, "−", "")) & FORMAT(ABS(VC), "0.0%", "pt-BR")) & ")")))
VAR L2 = IF(ISBLANK(A), "", "Variação do emprego em 31/12 sobre 31/12 do ano anterior. Escolha o ano no filtro Ano; 2022 não tem comparação (nova fonte: eSocial)")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#F58220" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 7 variável(is) (`A`, `VA`, `VC`, `VS`, `Nome`, `L1`, `L2`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Empregos_Var_Pct`, `Empregos_Var_Pct_AFL`, `Empregos_Var_Pct_Comparavel`, `Setor_Emp_Total`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · AFL

---

### Titulo_Emp_Var_Total_HTML

`_medidas.Titulo_Emp_Var_Total_HTML` · formato `—`

**O que faz:**
Título da variação anual do emprego (página Todos os setores).

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR VA = [Empregos_Var_Pct_AFL]
VAR VS = [Empregos_Var_Pct]
VAR Nome = IF([Setor_Emp_Total] = "todos os setores", "o mercado formal", [Setor_Emp_Total])
VAR L1 = IF(ISBLANK(A), "Sem dados para os filtros escolhidos", IF(ISBLANK(VA), IF(A = 2022, "2022 não pode ser comparado com 2021 (nova fonte: eSocial)", "2009 é o primeiro ano da série: não há ano anterior"), "Em " & A & ": AFL " & IF(ISBLANK(VA), "—", IF(VA > 0, "+", IF(VA < 0, "−", "")) & FORMAT(ABS(VA), "0.0%", "pt-BR")) & ", " & Nome & " " & IF(ISBLANK(VS), "—", IF(VS > 0, "+", IF(VS < 0, "−", "")) & FORMAT(ABS(VS), "0.0%", "pt-BR"))))
VAR L2 = IF(ISBLANK(A), "", "Variação do emprego em 31/12 sobre 31/12 do ano anterior. Escolha o ano no filtro Ano; 2022 não tem comparação (nova fonte: eSocial)")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#F58220" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 6 variável(is) (`A`, `VA`, `VS`, `Nome`, `L1`, `L2`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Empregos_Var_Pct`, `Empregos_Var_Pct_AFL`, `Setor_Emp_Total`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Empregos · Todos os setores

---

## HTML\Notas compartilhadas

2 medidas.

### Guia_Leitura_RAIS_HTML

`_medidas.Guia_Leitura_RAIS_HTML` · formato `—`

**O que faz:**
Guia de leitura e glossário compartilhado por todas as páginas do painel RAIS.

**DAX:**
```dax
VAR _A = 0
RETURN
    "<div role='note' aria-label='Guia de leitura e glossário do painel RAIS' style='width:1040px;height:900px;box-sizing:border-box;padding:22px 26px;background:#FFFFFF;border:1px solid #D9DDE5;border-top:6px solid #F58220;border-radius:8px;color:#434446;font-family:Segoe UI,Arial,sans-serif;font-size:17px;line-height:23px;overflow:hidden;'>"
    & "<div style='font-size:25px;line-height:31px;font-weight:700;color:#1D1E21;'>INFORMAÇÕES PARA LEITURA</div>"
    & "<div style='font-size:18px;line-height:25px;color:#667085;margin-top:3px;margin-bottom:16px;'>Um guia rápido para explorar o painel de emprego formal e interpretar os indicadores da RAIS.</div>"
    & "<div style='display:flex;gap:14px;margin-bottom:19px;'><div style='flex:1;min-width:0;padding:13px 16px;background:#FDF7F1;border-radius:6px;'><strong style='display:block;color:#B86218;margin-bottom:5px;'>Passe o mouse para descobrir mais</strong>Gráficos, números, manchetes e ícones ⓘ têm explicações adicionais. Mantenha o cursor sobre a informação; não é preciso clicar.</div><div style='flex:1;min-width:0;padding:13px 16px;background:#FDF7F1;border-radius:6px;'><strong style='display:block;color:#B86218;margin-bottom:5px;'>Explore os recortes</strong>Use os filtros, clique nas barras e consulte as abas para alternar tema e universo. Limpar filtros volta à leitura inicial da página.</div></div>"
    & "<div style='font-size:15px;line-height:21px;font-weight:700;letter-spacing:1px;color:#B86218;margin-bottom:12px;'>GLOSSÁRIO · MEDIDAS E CONCEITOS</div>"
    & "<div style='display:flex;gap:28px;'><div style='flex:1;min-width:0;'><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>RAIS / estoque de empregos</strong> — Retrato dos vínculos formais ativos em 31 de dezembro. Conta vínculos, não pessoas: quem tem dois empregos aparece duas vezes.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Ano de referência e defasagem</strong> — A RAIS é anual e divulgada com defasagem. O filtro Ano define o retrato de 31/12 usado nos indicadores.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Quebra da série em 2022</strong> — Desde 2022, a fonte é o eSocial, que ampliou a cobertura. Por isso, 2022 em diante não deve ser comparado diretamente com anos anteriores; as séries são interrompidas.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>AFL</strong> — Alimentação Fora do Lar: conjunto de seis CNAEs definidos no painel. Nos rankings, aparece como grupo próprio.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Comparáveis ao AFL</strong> — Atividades usadas como referência para comparar o AFL. A comparação-padrão é AFL × Comparáveis.</div></div>"
    & "<div style='flex:1;min-width:0;'><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Todos os setores / AFL</strong> — A primeira visão mostra o contexto de mercado e a seleção dos filtros; a aba AFL restringe o painel às seis atividades de alimentação fora do lar.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Remuneração</strong> — Salário de dezembro, em R$ nominais (sem correção pela inflação). A média considera salários válidos de 0,3 a 150 salários mínimos.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Percentuais e p.p.</strong> — Todo percentual informa uma parcela do universo mostrado. Pontos percentuais (p.p.) são diferença entre percentuais: de 30% para 35% = 5 p.p.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Cor ou raça</strong> — Os percentuais consideram somente quem declarou a informação. Pretos e pardos formam o grupo de negros.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>CNAE / divisão</strong> — CNAE é a classificação da atividade econômica; divisão é um agrupamento de CNAEs. Os nomes dos rankings seguem essa classificação.</div></div></div>"
    & "<div style='margin-top:4px;padding-top:11px;border-top:1px solid #E6E8ED;font-size:16px;line-height:22px;color:#667085;'><strong>Antes de comparar:</strong> confira ano, localidade, filtros e a nota metodológica da página. Ela indica quando há quebra de série, universo restrito ou dado indisponível.</div></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 1 variável(is) (`_A`) e devolve o resultado no `RETURN`.

**Usa:** —
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Informações para leitura

---

### Info_Texto_HTML

`_medidas.Info_Texto_HTML` · formato `—`

**O que faz:**
Cartão do (i): lê a linha da D_Info escolhida pela categoria do gatilho.

**DAX:**
```dax
VAR Chave = SELECTEDVALUE(D_Info[Chave])
VAR Titulo = SELECTEDVALUE(D_Info[Titulo], "")
VAR Extra = SELECTEDVALUE(D_Info[Extra], "")
VAR Destaque = SELECTEDVALUE(D_Info[Destaque], "")
VAR Borda = SELECTEDVALUE(D_Info[CorBorda], "#1D1E21")
VAR Fundo = SELECTEDVALUE(D_Info[CorFundo], "#F7F7F7")
VAR P1 = SELECTEDVALUE(D_Info[P1], "")
VAR P2 = SELECTEDVALUE(D_Info[P2], "")
VAR P3 = SELECTEDVALUE(D_Info[P3], "")
VAR P4 = SELECTEDVALUE(D_Info[P4], "")
VAR P5 = SELECTEDVALUE(D_Info[P5], "")
VAR Corpo = IF(P1 = "", "", "<div>" & P1 & "</div>") & IF(P2 = "", "", "<div style='margin-top:8px;'>" & P2 & "</div>") & IF(P3 = "", "", "<div style='margin-top:8px;'>" & P3 & "</div>") & IF(P4 = "", "", "<div style='margin-top:8px;'>" & P4 & "</div>") & IF(P5 = "", "", "<div style='margin-top:8px;'>" & P5 & "</div>")
RETURN IF(ISBLANK(Chave) || Titulo = "", "<div role='note' style='font-family:Segoe UI,Arial,sans-serif;font-size:21px;color:#434446;padding:12px;'>Texto indisponível.</div>",
    "<div role='note' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:12px 14px;background:#FFFFFF;color:#1D1E21;font-family:Segoe UI,Arial,sans-serif;overflow:hidden;'>"
    & "<div style='font-size:24px;line-height:30px;font-weight:600;margin-bottom:8px;'>" & Titulo & "</div>" & Extra
    & IF(Destaque = "", "", "<div style='padding:7px 9px;border-left:4px solid " & Borda & ";border-radius:0 6px 6px 0;background:" & Fundo & ";font-size:21px;line-height:27px;margin-bottom:8px;'>" & Destaque & "</div>")
    & "<div style='font-size:21px;line-height:28px;color:#434446;'>" & Corpo & "</div></div>")
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 12 variável(is) (`Chave`, `Titulo`, `Extra`, `Destaque`, `Borda`, `Fundo`, `P1`, `P2`…) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `D_Info[Chave]`, `D_Info[CorBorda]`, `D_Info[CorFundo]`, `D_Info[Destaque]`, `D_Info[Extra]`, `D_Info[P1]`, `D_Info[P2]`, `D_Info[P3]`, `D_Info[P4]`, `D_Info[P5]`, `D_Info[Titulo]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip (i) compartilhado · G, Tooltip (i) compartilhado · M, Tooltip (i) compartilhado · P

---

## HTML\Quanto ganha

2 medidas.

### Manchete_Salario_AFL_HTML

`_medidas.Manchete_Salario_AFL_HTML` · formato `—`

**O que faz:**
Manchete da página Quanto ganha · AFL.

**DAX:**
```dax
VAR NUF = COUNTROWS(VALUES(D_regiao[uf]))
VAR Prep = IF(NOT ISFILTERED(D_regiao[uf]) || NUF = COUNTROWS(ALL(D_regiao[uf])), "No Brasil", IF(NUF = 1, "Em " & SELECTEDVALUE(D_regiao[estado]), "Nas " & NUF & " UFs escolhidas"))
VAR A = [Ano_Ref]
VAR MediaAFL = [Remuneracao_Media_Ref_AFL]
VAR MediaComp = [Remuneracao_Media_Ref_Comparavel]
VAR Texto = IF(ISBLANK(MediaAFL), Prep & ", sem dados de remuneração do AFL para os filtros escolhidos", Prep & ", os trabalhadores do AFL ganhavam, em média, R$ " & FORMAT(MediaAFL, "#,0", "pt-BR") & " em dez/" & A & IF(ISBLANK(MediaComp), "", ": " & FORMAT(DIVIDE(MediaAFL, MediaComp), "0%", "pt-BR") & " da média dos Comparáveis"))
VAR Contexto = [Contexto_Emp_AFL] & " · valores nominais"
VAR Valido = NOT ISBLANK([Ano_Ref]) && NOT ISBLANK([Empregos_Ref])
RETURN
    IF(NOT Valido,
        "<div role='text' style='width:100%;height:118px;font-family:Segoe UI,Arial,sans-serif;font-size:24px;color:#434446;'>Não há dados para os filtros selecionados.</div>",
        "<div role='group' aria-label='Remuneração dos empregados' style='width:100%;height:118px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
            & "<div style='max-height:84px;overflow:hidden;'><span style='display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;min-width:0;font-size:34px;line-height:40px;font-weight:600;font-variant-numeric:tabular-nums;overflow:hidden;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Texto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span></div>"
            & "<div style='height:30px;margin:4px 0 0;font-size:24px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Contexto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
        & "</div>")
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 8 variável(is) (`NUF`, `Prep`, `A`, `MediaAFL`, `MediaComp`, `Texto`, `Contexto`, `Valido`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`); divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Contexto_Emp_AFL`, `Empregos_Ref`, `Remuneracao_Media_Ref_AFL`, `Remuneracao_Media_Ref_Comparavel`, `D_regiao[estado]`, `D_regiao[uf]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL

---

### Manchete_Salario_Total_HTML

`_medidas.Manchete_Salario_Total_HTML` · formato `—`

**O que faz:**
Manchete da página Quanto ganha · Total.

**DAX:**
```dax
VAR NUF = COUNTROWS(VALUES(D_regiao[uf]))
VAR Prep = IF(NOT ISFILTERED(D_regiao[uf]) || NUF = COUNTROWS(ALL(D_regiao[uf])), "No Brasil", IF(NUF = 1, "Em " & SELECTEDVALUE(D_regiao[estado]), "Nas " & NUF & " UFs escolhidas"))
VAR Media = [Remuneracao_Media_Ref]
VAR MediaAFL = [Remuneracao_Media_Ref_AFL]
VAR A = [Ano_Ref]
VAR Texto = Prep & ", a remuneração média de dezembro de " & A & " foi R$ " & FORMAT(Media, "#,0", "pt-BR") & IF(ISBLANK(MediaAFL), "", "; no AFL, R$ " & FORMAT(MediaAFL, "#,0", "pt-BR"))
VAR Contexto = [Contexto_Emp_Total] & " · valores nominais"
VAR Valido = NOT ISBLANK([Ano_Ref]) && NOT ISBLANK([Empregos_Ref])
RETURN
    IF(NOT Valido,
        "<div role='text' style='width:100%;height:118px;font-family:Segoe UI,Arial,sans-serif;font-size:24px;color:#434446;'>Não há dados para os filtros selecionados.</div>",
        "<div role='group' aria-label='Remuneração dos empregados' style='width:100%;height:118px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
            & "<div style='max-height:84px;overflow:hidden;'><span style='display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;min-width:0;font-size:34px;line-height:40px;font-weight:600;font-variant-numeric:tabular-nums;overflow:hidden;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Texto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span></div>"
            & "<div style='height:30px;margin:4px 0 0;font-size:24px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Contexto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
        & "</div>")
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 8 variável(is) (`NUF`, `Prep`, `Media`, `MediaAFL`, `A`, `Texto`, `Contexto`, `Valido`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`); formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Contexto_Emp_Total`, `Empregos_Ref`, `Remuneracao_Media_Ref`, `Remuneracao_Media_Ref_AFL`, `D_regiao[estado]`, `D_regiao[uf]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · Todos os setores

---

## HTML\Quanto ganha\KPIs

6 medidas.

### KPI_RazaoRaca_AFL_HTML

`_medidas.KPI_RazaoRaca_AFL_HTML` · formato `—`

**O que faz:**
KPI da razão de remuneração (Negros dos brancos).

**DAX:**
```dax
VAR _A = 0
RETURN
    "<div role='group' aria-label='KPI de razão salarial (Negros)' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Negros ganham, em média," & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK([Rem_Razao_Raca]), "—", FORMAT(ABS(1 - [Rem_Razao_Raca]), "0%", "pt-BR") & "<span style='font-size:24px;font-weight:600;'> " & IF([Rem_Razao_Raca] <= 1, "a menos", "a mais") & "</span><span style='font-size:24px;font-weight:400;'> que os brancos</span>") & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & "#434446" & ";overflow:hidden;'>" & "da remuneração média de dezembro" & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>Comparáveis " & IF(ISBLANK([Rem_Razao_Raca_Comp]), "—", FORMAT(ABS(1 - [Rem_Razao_Raca_Comp]), "0%", "pt-BR") & IF([Rem_Razao_Raca_Comp] <= 1, " a menos", " a mais")) & " <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 1 variável(is) (`_A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Rem_Razao_Raca`, `Rem_Razao_Raca_Comp`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL

---

### KPI_RazaoRaca_Total_HTML

`_medidas.KPI_RazaoRaca_Total_HTML` · formato `—`

**O que faz:**
KPI da razão de remuneração (Negros dos brancos).

**DAX:**
```dax
VAR _A = 0
RETURN
    "<div role='group' aria-label='KPI de razão salarial (Negros)' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Negros ganham, em média," & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK([Rem_Razao_Raca]), "—", FORMAT(ABS(1 - [Rem_Razao_Raca]), "0%", "pt-BR") & "<span style='font-size:24px;font-weight:600;'> " & IF([Rem_Razao_Raca] <= 1, "a menos", "a mais") & "</span><span style='font-size:24px;font-weight:400;'> que os brancos</span>") & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & "#434446" & ";overflow:hidden;'>" & "da remuneração média de dezembro" & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #D97706;border-radius:6px;background:#FDF7F1;color:#B86218;font-size:20px;line-height:26px;font-weight:600;'>AFL " & IF(ISBLANK([Rem_Razao_Raca_AFL]), "—", FORMAT(ABS(1 - [Rem_Razao_Raca_AFL]), "0%", "pt-BR") & IF([Rem_Razao_Raca_AFL] <= 1, " a menos", " a mais")) & "</span></div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 1 variável(is) (`_A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Rem_Razao_Raca`, `Rem_Razao_Raca_AFL`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · Todos os setores

---

### KPI_RazaoSexo_AFL_HTML

`_medidas.KPI_RazaoSexo_AFL_HTML` · formato `—`

**O que faz:**
KPI da razão de remuneração (Mulheres dos homens).

**DAX:**
```dax
VAR _A = 0
RETURN
    "<div role='group' aria-label='KPI de razão salarial (Mulheres)' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Mulheres ganham, em média," & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK([Rem_Razao_Sexo]), "—", FORMAT(ABS(1 - [Rem_Razao_Sexo]), "0%", "pt-BR") & "<span style='font-size:24px;font-weight:600;'> " & IF([Rem_Razao_Sexo] <= 1, "a menos", "a mais") & "</span><span style='font-size:24px;font-weight:400;'> que os homens</span>") & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & "#434446" & ";overflow:hidden;'>" & "da remuneração média de dezembro" & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>Comparáveis " & IF(ISBLANK([Rem_Razao_Sexo_Comp]), "—", FORMAT(ABS(1 - [Rem_Razao_Sexo_Comp]), "0%", "pt-BR") & IF([Rem_Razao_Sexo_Comp] <= 1, " a menos", " a mais")) & " <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 1 variável(is) (`_A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Rem_Razao_Sexo`, `Rem_Razao_Sexo_Comp`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL

---

### KPI_RazaoSexo_Total_HTML

`_medidas.KPI_RazaoSexo_Total_HTML` · formato `—`

**O que faz:**
KPI da razão de remuneração (Mulheres dos homens).

**DAX:**
```dax
VAR _A = 0
RETURN
    "<div role='group' aria-label='KPI de razão salarial (Mulheres)' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Mulheres ganham, em média," & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK([Rem_Razao_Sexo]), "—", FORMAT(ABS(1 - [Rem_Razao_Sexo]), "0%", "pt-BR") & "<span style='font-size:24px;font-weight:600;'> " & IF([Rem_Razao_Sexo] <= 1, "a menos", "a mais") & "</span><span style='font-size:24px;font-weight:400;'> que os homens</span>") & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & "#434446" & ";overflow:hidden;'>" & "da remuneração média de dezembro" & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #D97706;border-radius:6px;background:#FDF7F1;color:#B86218;font-size:20px;line-height:26px;font-weight:600;'>AFL " & IF(ISBLANK([Rem_Razao_Sexo_AFL]), "—", FORMAT(ABS(1 - [Rem_Razao_Sexo_AFL]), "0%", "pt-BR") & IF([Rem_Razao_Sexo_AFL] <= 1, " a menos", " a mais")) & "</span></div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 1 variável(is) (`_A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Rem_Razao_Sexo`, `Rem_Razao_Sexo_AFL`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · Todos os setores

---

### KPI_RemMedia_AFL_HTML

`_medidas.KPI_RemMedia_AFL_HTML` · formato `—`

**O que faz:**
KPI de remuneração média de dezembro (página AFL), com salários mínimos e chip dos Comparáveis.

**DAX:**
```dax
VAR Media = [Remuneracao_Media_Ref]
VAR SM = [Remuneracao_Media_SM_Ref]
VAR MediaComp = [Remuneracao_Media_Ref_Comparavel]
RETURN
    "<div role='group' aria-label='KPI de remuneração média' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Remuneração média de dezembro" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK(Media), "—", "R$ " & FORMAT(Media, "#,0", "pt-BR")) & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:#434446;overflow:hidden;'>" & IF(ISBLANK(SM), "sem dado para os filtros", FORMAT(SM, "0.00", "pt-BR") & " salário mínimo") & "</div>"
        & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>Comparáveis " & IF(ISBLANK(MediaComp), "—", "R$ " & FORMAT(MediaComp, "#,0", "pt-BR")) & " <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 3 variável(is) (`Media`, `SM`, `MediaComp`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Remuneracao_Media_Ref`, `Remuneracao_Media_Ref_Comparavel`, `Remuneracao_Media_SM_Ref`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL

---

### KPI_RemMedia_Total_HTML

`_medidas.KPI_RemMedia_Total_HTML` · formato `—`

**O que faz:**
KPI de remuneração média de dezembro, com salários mínimos e chip do AFL.

**DAX:**
```dax
VAR Media = [Remuneracao_Media_Ref]
VAR SM = [Remuneracao_Media_SM_Ref]
VAR MediaAFL = [Remuneracao_Media_Ref_AFL]
RETURN
    "<div role='group' aria-label='KPI de remuneração média' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Remuneração média de dezembro" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK(Media), "—", "R$ " & FORMAT(Media, "#,0", "pt-BR")) & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:#434446;overflow:hidden;'>" & IF(ISBLANK(SM), "sem dado para os filtros", FORMAT(SM, "0.00", "pt-BR") & " salário mínimo") & "</div>"
        & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #D97706;border-radius:6px;background:#FDF7F1;color:#B86218;font-size:20px;line-height:26px;font-weight:600;'>AFL " & IF(ISBLANK(MediaAFL), "—", "R$ " & FORMAT(MediaAFL, "#,0", "pt-BR")) & "</span></div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 3 variável(is) (`Media`, `SM`, `MediaAFL`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Remuneracao_Media_Ref`, `Remuneracao_Media_Ref_AFL`, `Remuneracao_Media_SM_Ref`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · Todos os setores

---

## HTML\Quanto ganha\Títulos

6 medidas.

### Rotulo_Gap_Raca_HTML

`_medidas.Rotulo_Gap_Raca_HTML` · formato `—`

**O que faz:**
Rótulo do gráfico de razão (Salário dos negros como % do dos brancos).

**DAX:**
```dax
"<div style='font-family:Segoe UI,Arial,sans-serif;font-size:19px;line-height:23px;font-weight:600;color:#1D1E21;white-space:normal;'>Diferença salarial dos negros em relação aos brancos, por escolaridade</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips).

**Usa:** —
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

### Rotulo_Gap_Sexo_HTML

`_medidas.Rotulo_Gap_Sexo_HTML` · formato `—`

**O que faz:**
Rótulo do gráfico de razão (Salário das mulheres como % do dos homens).

**DAX:**
```dax
"<div style='font-family:Segoe UI,Arial,sans-serif;font-size:19px;line-height:23px;font-weight:600;color:#1D1E21;white-space:normal;'>Diferença salarial das mulheres em relação aos homens, por escolaridade</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips).

**Usa:** —
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

### Titulo_Rem_Esc_HTML

`_medidas.Titulo_Rem_Esc_HTML` · formato `—`

**O que faz:**
Título da remuneração por escolaridade: quanto o AFL paga em relação aos Comparáveis com superior completo.

**DAX:**
```dax
VAR Sup = CALCULATE(DIVIDE([Remuneracao_Media_Ref_AFL], [Remuneracao_Media_Ref_Comparavel]), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Superior Completo"))
VAR Med = CALCULATE(DIVIDE([Remuneracao_Media_Ref_AFL], [Remuneracao_Media_Ref_Comparavel]), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Médio Completo"))
VAR L1 = IF(ISBLANK(Sup), "Sem dados para os filtros escolhidos", "Com superior completo, o AFL paga " & FORMAT(Sup, "0%", "pt-BR") & " da média dos Comparáveis")
VAR L2 = IF(ISBLANK(Sup), "", "Com médio completo: " & FORMAT(Med, "0%", "pt-BR") & " · média de dezembro, R$ nominais")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#1D1E21" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 4 variável(is) (`Sup`, `Med`, `L1`, `L2`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Remuneracao_Media_Ref_AFL`, `Remuneracao_Media_Ref_Comparavel`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

### Titulo_Rem_Gap_HTML

`_medidas.Titulo_Rem_Gap_HTML` · formato `—`

**O que faz:**
Título das diferenças salariais por sexo e cor, em linguagem direta.

**DAX:**
```dax
VAR S = [Rem_Razao_Sexo_AFL]
VAR SC = [Rem_Razao_Sexo_Comp]
VAR R = [Rem_Razao_Raca_AFL]
VAR RC = [Rem_Razao_Raca_Comp]
VAR L1 = IF(ISBLANK(S), "Sem dados para os filtros escolhidos", IF(S < 1, "Mulheres ganham " & FORMAT(1 - S, "0%", "pt-BR") & " a menos que os homens no AFL", IF(S > 1, "Mulheres ganham " & FORMAT(S - 1, "0%", "pt-BR") & " a mais que os homens no AFL", "Mulheres e homens ganham o mesmo no AFL")))
VAR L2 = IF(ISBLANK(R), "", IF(R < 1, "Negros ganham " & FORMAT(1 - R, "0%", "pt-BR") & " a menos que os brancos no AFL", IF(R > 1, "Negros ganham " & FORMAT(R - 1, "0%", "pt-BR") & " a mais que os brancos no AFL", "Negros e brancos ganham o mesmo no AFL")) & " · média de dezembro, sem filtro de escolaridade")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#1D1E21" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 6 variável(is) (`S`, `SC`, `R`, `RC`, `L1`, `L2`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Rem_Razao_Raca_AFL`, `Rem_Razao_Raca_Comp`, `Rem_Razao_Sexo_AFL`, `Rem_Razao_Sexo_Comp`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

### Titulo_Rem_Serie_HTML

`_medidas.Titulo_Rem_Serie_HTML` · formato `—`

**O que faz:**
Título da série de remuneração média do AFL entre o início do trecho e o ano de referência.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR I = [Ano_Inicio_Trecho]
VAR L1 = IF(ISBLANK(A), "Sem dados para os filtros escolhidos", IF(A <= I, I & " é o primeiro ano do trecho", "Evolução da remuneração media do AFL entre " & I & " e " & A))
VAR L2 = IF(ISBLANK(A), "", "Remuneração media de dezembro em R$ nominais. 2021 e 2022 não se comparam (eSocial)")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#F58220" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 4 variável(is) (`A`, `I`, `L1`, `L2`) e devolve o resultado no `RETURN`.

**Usa:** `Ano_Inicio_Trecho`, `Ano_Ref`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

### Titulo_Rem_UF_HTML

`_medidas.Titulo_Rem_UF_HTML` · formato `—`

**O que faz:**
Título das UFs: maior média e maior distância para os Comparáveis.

**DAX:**
```dax
VAR T = FILTER(ADDCOLUMNS(VALUES(D_regiao[uf]), "@v", [Remuneracao_Media_Ref], "@r", [Rem_UF_Razao_Comp]), NOT ISBLANK([@v]))
VAR Lider1 = TOPN(1, T, [@v], DESC, D_regiao[uf], ASC)
VAR UF = CONCATENATEX(Lider1, D_regiao[uf], "")
VAR UFN = COALESCE(LOOKUPVALUE(D_regiao[estado], D_regiao[uf], UF), UF)
VAR V = MAXX(Lider1, [@v])
VAR Pior = TOPN(1, FILTER(T, NOT ISBLANK([@r])), [@r], ASC, D_regiao[uf], ASC)
VAR UFP = CONCATENATEX(Pior, D_regiao[uf], "")
VAR UFPN = COALESCE(LOOKUPVALUE(D_regiao[estado], D_regiao[uf], UFP), UFP)
VAR RP = MAXX(Pior, [@r])
VAR L1 = IF(COUNTROWS(T) = 0, "Sem dados para os filtros escolhidos", IF(COUNTROWS(T) = 1, UFN & ": R$ " & FORMAT(V, "#,0", "pt-BR"), UFN & " paga a maior média: R$ " & FORMAT(V, "#,0", "pt-BR")))
VAR L2 = IF(COUNTROWS(T) < 2 || ISBLANK(RP), "", "Maior distância para os Comparáveis: " & UFPN & " (AFL " & FORMAT(RP, "0%", "pt-BR") & " da média comparável)")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#1D1E21" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 11 variável(is) (`T`, `Lider1`, `UF`, `UFN`, `V`, `Pior`, `UFP`, `UFPN`…) e devolve o resultado no `RETURN`. Pega os primeiros com `TOPN`; pega o maior valor de uma lista com `MAXX`; monta uma tabela virtual com `ADDCOLUMNS`; busca um valor em outra tabela com `LOOKUPVALUE`; junta textos com `CONCATENATEX`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Rem_UF_Razao_Comp`, `Remuneracao_Media_Ref`, `D_regiao[estado]`, `D_regiao[uf]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

## HTML\Quem contrata

2 medidas.

### Manchete_Ct_AFL_HTML

`_medidas.Manchete_Ct_AFL_HTML` · formato `—`

**O que faz:**
Título e subtítulo da página Quem contrata (AFL); falam em salário médio quando os três gráficos estão nesse valor.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR SalMul = COALESCE(SELECTEDVALUE(D_Ct_MetMul[metrica]), "Representatividade") = "Salário médio"
VAR SalNeg = COALESCE(SELECTEDVALUE(D_Ct_MetNeg[metrica]), "Representatividade") = "Salário médio"
VAR SalEsc = COALESCE(SELECTEDVALUE(D_Ct_MetEsc[metrica]), "Representatividade") = "Salário médio"
VAR NSal = IF(SalMul, 1, 0) + IF(SalNeg, 1, 0) + IF(SalEsc, 1, 0)
VAR Titulo = IF(NSal = 3, "Ranking do AFL: salário médio por perfil dos empregados", "Ranking do AFL: quem mais contrata por perfil dos empregados")
VAR Resumo = IF(NSal = 3, "valores em salário médio de dezembro (R$ nominais)", IF(NSal = 0, "valores em representatividade (% dos empregos)", "valores conforme o botão de cada gráfico"))
VAR Sub = IF(ISBLANK(A), "Não há dados para os filtros selecionados", "Empregos em 31/12/" & A & " · " & Resumo & " · os seis CNAEs do AFL respeitam os filtros aplicados")
RETURN "<div role='group' aria-label='Quem mais contrata, por perfil dos empregados' style='width:100%;height:92px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
    & "<div style='font-size:34px;line-height:42px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" & Titulo & "</div>"
    & "<div style='margin-top:4px;font-size:22px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" & Sub & "</div></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 8 variável(is) (`A`, `SalMul`, `SalNeg`, `SalEsc`, `NSal`, `Titulo`, `Resumo`, `Sub`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Ano_Ref`, `D_Ct_MetEsc[metrica]`, `D_Ct_MetMul[metrica]`, `D_Ct_MetNeg[metrica]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · AFL

---

### Manchete_Ct_Total_HTML

`_medidas.Manchete_Ct_Total_HTML` · formato `—`

**O que faz:**
Título e subtítulo da página Quem contrata (Total); falam em salário médio quando os três gráficos estão nesse valor.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR SalMul = COALESCE(SELECTEDVALUE(D_Ct_MetMul[metrica]), "Representatividade") = "Salário médio"
VAR SalNeg = COALESCE(SELECTEDVALUE(D_Ct_MetNeg[metrica]), "Representatividade") = "Salário médio"
VAR SalEsc = COALESCE(SELECTEDVALUE(D_Ct_MetEsc[metrica]), "Representatividade") = "Salário médio"
VAR NSal = IF(SalMul, 1, 0) + IF(SalNeg, 1, 0) + IF(SalEsc, 1, 0)
VAR Titulo = IF(NSal = 3, "Ranking dos setores: salário médio por perfil dos empregados", "Ranking dos setores: quem mais contrata por perfil dos empregados")
VAR Resumo = IF(NSal = 3, "valores em salário médio de dezembro (R$ nominais)", IF(NSal = 0, "valores em representatividade (% dos empregos)", "valores conforme o botão de cada gráfico"))
VAR Sub = IF(ISBLANK(A), "Não há dados para os filtros selecionados", "Empregos em 31/12/" & A & " · " & Resumo & " · setores e divisões respeitam os filtros aplicados · AFL em destaque")
RETURN "<div role='group' aria-label='Quem mais contrata, por perfil dos empregados' style='width:100%;height:92px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
    & "<div style='font-size:34px;line-height:42px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" & Titulo & "</div>"
    & "<div style='margin-top:4px;font-size:22px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" & Sub & "</div></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 8 variável(is) (`A`, `SalMul`, `SalNeg`, `SalEsc`, `NSal`, `Titulo`, `Resumo`, `Sub`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Ano_Ref`, `D_Ct_MetEsc[metrica]`, `D_Ct_MetMul[metrica]`, `D_Ct_MetNeg[metrica]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · Todos os setores

---

## HTML\Quem contrata\KPIs

6 medidas.

### KPI_Ct_Esc_AFL_HTML

`_medidas.KPI_Ct_Esc_AFL_HTML` · formato `—`

**O que faz:**
KPI de escolaridade (AFL): participação (%) e salário médio (R$) de quatro níveis, em fontes maiores.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR T = CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)
VAR RMC = DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Médio Completo")), T)
VAR SMC = CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Médio Completo"))
VAR RSC = DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Superior Completo")), T)
VAR SSC = CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Superior Completo"))
VAR RFC = DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Fundamental Completo")), T)
VAR SFC = CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Fundamental Completo"))
VAR RMI = DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Médio Incompleto")), T)
VAR SMI = CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Médio Incompleto"))
RETURN IF(ISBLANK(A), "",
    "<div role='group' aria-label='Escolaridade: participação e salário médio' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
    & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>Escolaridade</div>"
    & "<div style='font-size:18px;line-height:22px;color:#434446;white-space:nowrap;'>participação (%) · salário médio (R$)</div>"
    & "<div style='display:grid;grid-template-columns:1fr 1fr;gap:4px 14px;margin-top:6px;font-variant-numeric:tabular-nums;'>"
    & "<div style='min-width:0;'><div style='font-size:20px;line-height:24px;color:#434446;white-space:nowrap;'>Médio completo</div><div style='font-size:26px;line-height:30px;font-weight:600;white-space:nowrap;'>" & IF(ISBLANK(RMC), "—", FORMAT(RMC, "0.0%", "pt-BR")) & " · " & IF(ISBLANK(SMC), "—", "R$ " & FORMAT(SMC, "#,0", "pt-BR")) & "</div></div>"
    & "<div style='min-width:0;'><div style='font-size:20px;line-height:24px;color:#434446;white-space:nowrap;'>Superior completo</div><div style='font-size:26px;line-height:30px;font-weight:600;white-space:nowrap;'>" & IF(ISBLANK(RSC), "—", FORMAT(RSC, "0.0%", "pt-BR")) & " · " & IF(ISBLANK(SSC), "—", "R$ " & FORMAT(SSC, "#,0", "pt-BR")) & "</div></div>"
    & "<div style='min-width:0;'><div style='font-size:20px;line-height:24px;color:#434446;white-space:nowrap;'>Fundamental completo</div><div style='font-size:26px;line-height:30px;font-weight:600;white-space:nowrap;'>" & IF(ISBLANK(RFC), "—", FORMAT(RFC, "0.0%", "pt-BR")) & " · " & IF(ISBLANK(SFC), "—", "R$ " & FORMAT(SFC, "#,0", "pt-BR")) & "</div></div>"
    & "<div style='min-width:0;'><div style='font-size:20px;line-height:24px;color:#434446;white-space:nowrap;'>Médio incompleto</div><div style='font-size:26px;line-height:30px;font-weight:600;white-space:nowrap;'>" & IF(ISBLANK(RMI), "—", FORMAT(RMI, "0.0%", "pt-BR")) & " · " & IF(ISBLANK(SMI), "—", "R$ " & FORMAT(SMI, "#,0", "pt-BR")) & "</div></div>"
    & "</div></div>")
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 10 variável(is) (`A`, `T`, `RMC`, `SMC`, `RSC`, `SSC`, `RFC`, `SFC`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `Remuneracao_Media`, `D_Ano[ano]`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · AFL

---

### KPI_Ct_Esc_Total_HTML

`_medidas.KPI_Ct_Esc_Total_HTML` · formato `—`

**O que faz:**
KPI de escolaridade (Total): participação (%) e salário médio (R$) de quatro níveis, em fontes maiores.

**DAX:**
```dax
VAR SetFiltro = TREATAS(VALUES(D_Ct_Setor[setor]), D_Cnae[setor_principal])
VAR NSet = COUNTROWS(VALUES(D_Ct_Setor[setor]))
VAR Onde = IF(NSet = 1, "no setor selecionado", IF(NSet = COUNTROWS(ALL(D_Ct_Setor[setor])), "em todos os setores", "nos setores selecionados"))
VAR A = [Ano_Ref]
VAR T = CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(SetFiltro))
VAR RMC = DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(SetFiltro), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Médio Completo")), T)
VAR SMC = CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(SetFiltro), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Médio Completo"))
VAR RSC = DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(SetFiltro), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Superior Completo")), T)
VAR SSC = CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(SetFiltro), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Superior Completo"))
VAR RFC = DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(SetFiltro), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Fundamental Completo")), T)
VAR SFC = CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(SetFiltro), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Fundamental Completo"))
VAR RMI = DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(SetFiltro), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Médio Incompleto")), T)
VAR SMI = CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(SetFiltro), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "Médio Incompleto"))
RETURN IF(ISBLANK(A), "",
    "<div role='group' aria-label='Escolaridade: participação e salário médio' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
    & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>Escolaridade</div>"
    & "<div style='font-size:18px;line-height:22px;color:#434446;white-space:nowrap;'>participação (%) · salário médio (R$)</div>"
    & "<div style='display:grid;grid-template-columns:1fr 1fr;gap:4px 14px;margin-top:6px;font-variant-numeric:tabular-nums;'>"
    & "<div style='min-width:0;'><div style='font-size:20px;line-height:24px;color:#434446;white-space:nowrap;'>Médio completo</div><div style='font-size:26px;line-height:30px;font-weight:600;white-space:nowrap;'>" & IF(ISBLANK(RMC), "—", FORMAT(RMC, "0.0%", "pt-BR")) & " · " & IF(ISBLANK(SMC), "—", "R$ " & FORMAT(SMC, "#,0", "pt-BR")) & "</div></div>"
    & "<div style='min-width:0;'><div style='font-size:20px;line-height:24px;color:#434446;white-space:nowrap;'>Superior completo</div><div style='font-size:26px;line-height:30px;font-weight:600;white-space:nowrap;'>" & IF(ISBLANK(RSC), "—", FORMAT(RSC, "0.0%", "pt-BR")) & " · " & IF(ISBLANK(SSC), "—", "R$ " & FORMAT(SSC, "#,0", "pt-BR")) & "</div></div>"
    & "<div style='min-width:0;'><div style='font-size:20px;line-height:24px;color:#434446;white-space:nowrap;'>Fundamental completo</div><div style='font-size:26px;line-height:30px;font-weight:600;white-space:nowrap;'>" & IF(ISBLANK(RFC), "—", FORMAT(RFC, "0.0%", "pt-BR")) & " · " & IF(ISBLANK(SFC), "—", "R$ " & FORMAT(SFC, "#,0", "pt-BR")) & "</div></div>"
    & "<div style='min-width:0;'><div style='font-size:20px;line-height:24px;color:#434446;white-space:nowrap;'>Médio incompleto</div><div style='font-size:26px;line-height:30px;font-weight:600;white-space:nowrap;'>" & IF(ISBLANK(RMI), "—", FORMAT(RMI, "0.0%", "pt-BR")) & " · " & IF(ISBLANK(SMI), "—", "R$ " & FORMAT(SMI, "#,0", "pt-BR")) & "</div></div>"
    & "</div></div>")
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 13 variável(is) (`SetFiltro`, `NSet`, `Onde`, `A`, `T`, `RMC`, `SMC`, `RSC`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; aplica filtro virtual com `TREATAS`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `Remuneracao_Media`, `D_Ano[ano]`, `D_Cnae[setor_principal]`, `D_Ct_Setor[setor]`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · Todos os setores

---

### KPI_Ct_Mul_AFL_HTML

`_medidas.KPI_Ct_Mul_AFL_HTML` · formato `—`

**O que faz:**
KPI de mulheres (AFL): salário médio (valor grande) e representatividade (linha de baixo), cada um rotulado.

**DAX:**
```dax
VAR Rep = CALCULATE([Ct_Mul_Rep])
VAR Sal = CALCULATE([Ct_Mul_Sal])
RETURN
    "<div role='group' aria-label='KPI de mulheres' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Mulheres empregadas" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK(Sal), "—", "R$ " & FORMAT(Sal, "#,0", "pt-BR")) & "<span style='font-size:22px;font-weight:400;color:#434446;'> salário médio</span>" & "</div>"
        & "<div style='margin-top:3px;font-size:20px;line-height:24px;max-height:48px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;color:" & "#434446" & ";overflow:hidden;'>" & IF(ISBLANK(Rep), "sem dados para os filtros escolhidos", "Representatividade: <b style='color:#1D1E21;'>" & FORMAT(Rep, "0.0%", "pt-BR") & " dos empregos</b> " & "no AFL") & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 2 variável(is) (`Rep`, `Sal`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ct_Mul_Rep`, `Ct_Mul_Sal`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · AFL

---

### KPI_Ct_Mul_Total_HTML

`_medidas.KPI_Ct_Mul_Total_HTML` · formato `—`

**O que faz:**
KPI de mulheres (Total): salário médio (valor grande) e representatividade (linha de baixo), cada um rotulado.

**DAX:**
```dax
VAR SetFiltro = TREATAS(VALUES(D_Ct_Setor[setor]), D_Cnae[setor_principal])
VAR NSet = COUNTROWS(VALUES(D_Ct_Setor[setor]))
VAR Onde = IF(NSet = 1, "no setor selecionado", IF(NSet = COUNTROWS(ALL(D_Ct_Setor[setor])), "em todos os setores", "nos setores selecionados"))
VAR Rep = CALCULATE([Ct_Mul_Rep], KEEPFILTERS(SetFiltro))
VAR Sal = CALCULATE([Ct_Mul_Sal], KEEPFILTERS(SetFiltro))
RETURN
    "<div role='group' aria-label='KPI de mulheres' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Mulheres empregadas" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK(Sal), "—", "R$ " & FORMAT(Sal, "#,0", "pt-BR")) & "<span style='font-size:22px;font-weight:400;color:#434446;'> salário médio</span>" & "</div>"
        & "<div style='margin-top:3px;font-size:20px;line-height:24px;max-height:48px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;color:" & "#434446" & ";overflow:hidden;'>" & IF(ISBLANK(Rep), "sem dados para os filtros escolhidos", "Representatividade: <b style='color:#1D1E21;'>" & FORMAT(Rep, "0.0%", "pt-BR") & " dos empregos</b> " & Onde) & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`SetFiltro`, `NSet`, `Onde`, `Rep`, `Sal`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; aplica filtro virtual com `TREATAS`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ct_Mul_Rep`, `Ct_Mul_Sal`, `D_Cnae[setor_principal]`, `D_Ct_Setor[setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · Todos os setores

---

### KPI_Ct_Neg_AFL_HTML

`_medidas.KPI_Ct_Neg_AFL_HTML` · formato `—`

**O que faz:**
KPI de negros (pretos + pardos) (AFL): salário médio (valor grande) e representatividade (linha de baixo), cada um rotulado.

**DAX:**
```dax
VAR Rep = CALCULATE([Ct_Neg_Rep])
VAR Sal = CALCULATE([Ct_Neg_Sal])
RETURN
    "<div role='group' aria-label='KPI de negros' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Negros (pretos + pardos)" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK(Sal), "—", "R$ " & FORMAT(Sal, "#,0", "pt-BR")) & "<span style='font-size:22px;font-weight:400;color:#434446;'> salário médio</span>" & "</div>"
        & "<div style='margin-top:3px;font-size:20px;line-height:24px;max-height:48px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;color:" & "#434446" & ";overflow:hidden;'>" & IF(ISBLANK(Rep), "sem dados para os filtros escolhidos", "Representatividade: <b style='color:#1D1E21;'>" & FORMAT(Rep, "0.0%", "pt-BR") & " dos que declararam cor</b> " & "no AFL") & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 2 variável(is) (`Rep`, `Sal`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ct_Neg_Rep`, `Ct_Neg_Sal`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · AFL

---

### KPI_Ct_Neg_Total_HTML

`_medidas.KPI_Ct_Neg_Total_HTML` · formato `—`

**O que faz:**
KPI de negros (pretos + pardos) (Total): salário médio (valor grande) e representatividade (linha de baixo), cada um rotulado.

**DAX:**
```dax
VAR SetFiltro = TREATAS(VALUES(D_Ct_Setor[setor]), D_Cnae[setor_principal])
VAR NSet = COUNTROWS(VALUES(D_Ct_Setor[setor]))
VAR Onde = IF(NSet = 1, "no setor selecionado", IF(NSet = COUNTROWS(ALL(D_Ct_Setor[setor])), "em todos os setores", "nos setores selecionados"))
VAR Rep = CALCULATE([Ct_Neg_Rep], KEEPFILTERS(SetFiltro))
VAR Sal = CALCULATE([Ct_Neg_Sal], KEEPFILTERS(SetFiltro))
RETURN
    "<div role='group' aria-label='KPI de negros' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Negros (pretos + pardos)" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK(Sal), "—", "R$ " & FORMAT(Sal, "#,0", "pt-BR")) & "<span style='font-size:22px;font-weight:400;color:#434446;'> salário médio</span>" & "</div>"
        & "<div style='margin-top:3px;font-size:20px;line-height:24px;max-height:48px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;color:" & "#434446" & ";overflow:hidden;'>" & IF(ISBLANK(Rep), "sem dados para os filtros escolhidos", "Representatividade: <b style='color:#1D1E21;'>" & FORMAT(Rep, "0.0%", "pt-BR") & " dos que declararam cor</b> " & Onde) & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`SetFiltro`, `NSet`, `Onde`, `Rep`, `Sal`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; aplica filtro virtual com `TREATAS`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ct_Neg_Rep`, `Ct_Neg_Sal`, `D_Cnae[setor_principal]`, `D_Ct_Setor[setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · Todos os setores

---

## HTML\Quem contrata\Títulos

6 medidas.

### Titulo_Ct_Esc_AFL_HTML

`_medidas.Titulo_Ct_Esc_AFL_HTML` · formato `—`

**O que faz:**
Título do ranking por escolaridade (AFL); muda com os botões de nível e de valor.

**DAX:**
```dax
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetEsc[metrica]), "Representatividade") = "Salário médio"
VAR Niv = COALESCE(SELECTEDVALUE(D_Ct_Nivel[nivel]), "Médio completo")
VAR NomeNivel = SWITCH(Niv, "Até fundamental", "até o fundamental completo", "Médio incompleto", "médio incompleto", "Superior", "superior (completo ou não)", "médio completo")
VAR L1 = IF(Sal, "Salário médio por CNAE do AFL — escolaridade", "Representatividade por CNAE do AFL — escolaridade")
VAR L2 = "Nível: " & NomeNivel & " · " & IF(Sal, "salário médio de dezembro dos empregados do nível em cada CNAE do AFL (R$ nominais)", "participação do nível no total de empregos de cada CNAE do AFL") & ". Valores absolutos no tooltip."
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#F58220" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`Sal`, `Niv`, `NomeNivel`, `L1`, `L2`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; escolhe o resultado com `SWITCH`.

**Usa:** `D_Ct_MetEsc[metrica]`, `D_Ct_Nivel[nivel]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · AFL

---

### Titulo_Ct_Esc_Total_HTML

`_medidas.Titulo_Ct_Esc_Total_HTML` · formato `—`

**O que faz:**
Título do ranking por escolaridade (Total); muda com os botões de nível e de valor.

**DAX:**
```dax
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetEsc[metrica]), "Representatividade") = "Salário médio"
VAR Niv = COALESCE(SELECTEDVALUE(D_Ct_Nivel[nivel]), "Médio completo")
VAR NomeNivel = SWITCH(Niv, "Até fundamental", "até o fundamental completo", "Médio incompleto", "médio incompleto", "Superior", "superior (completo ou não)", "médio completo")
VAR L1 = IF(Sal, "Salário médio por divisão — escolaridade", "Representatividade por divisão — escolaridade")
VAR L2 = "Nível: " & NomeNivel & " · " & IF(Sal, "salário médio de dezembro dos empregados do nível em cada divisão (R$ nominais)", "participação do nível no total de empregos de cada divisão") & ". Valores absolutos no tooltip."
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#F58220" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`Sal`, `Niv`, `NomeNivel`, `L1`, `L2`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; escolhe o resultado com `SWITCH`.

**Usa:** `D_Ct_MetEsc[metrica]`, `D_Ct_Nivel[nivel]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · Todos os setores

---

### Titulo_Ct_Mul_AFL_HTML

`_medidas.Titulo_Ct_Mul_AFL_HTML` · formato `—`

**O que faz:**
Título do ranking (mulheres, AFL); muda com o botão Representatividade / Salário médio.

**DAX:**
```dax
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetMul[metrica]), "Representatividade") = "Salário médio"
VAR L1 = IF(Sal, "CNAEs com maior salário médio entre as mulheres", "CNAEs com maior representatividade de mulheres")
VAR L2 = IF(Sal, "Salário médio: remuneração média de dezembro das mulheres em cada CNAE, em R$ nominais. Detalhes no tooltip.", "Representatividade: participação de mulheres no total de empregos em cada CNAE. Valores absolutos no tooltip.")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#7F56D9" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 3 variável(is) (`Sal`, `L1`, `L2`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `D_Ct_MetMul[metrica]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · AFL

---

### Titulo_Ct_Mul_Total_HTML

`_medidas.Titulo_Ct_Mul_Total_HTML` · formato `—`

**O que faz:**
Título do ranking (mulheres, Total); muda com o botão Representatividade / Salário médio.

**DAX:**
```dax
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetMul[metrica]), "Representatividade") = "Salário médio"
VAR Piores = COALESCE(SELECTEDVALUE(D_Ct_Modo[modo]), "10 melhores setores") = "10 piores setores"
VAR L1 = IF(Sal, IF(Piores, "Divisões com menor salário médio entre as mulheres", "Divisões com maior salário médio entre as mulheres"), IF(Piores, "Divisões com menor representatividade de mulheres", "Divisões com maior representatividade de mulheres"))
VAR L2 = IF(Sal, "Salário médio: remuneração média de dezembro das mulheres na divisão, em R$ nominais. Detalhes no tooltip.", "Representatividade: participação de mulheres no total de empregos na divisão. Valores absolutos no tooltip.")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#7F56D9" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 4 variável(is) (`Sal`, `Piores`, `L1`, `L2`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `D_Ct_MetMul[metrica]`, `D_Ct_Modo[modo]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · Todos os setores

---

### Titulo_Ct_Neg_AFL_HTML

`_medidas.Titulo_Ct_Neg_AFL_HTML` · formato `—`

**O que faz:**
Título do ranking (negros (pretos + pardos), AFL); muda com o botão Representatividade / Salário médio.

**DAX:**
```dax
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetNeg[metrica]), "Representatividade") = "Salário médio"
VAR L1 = IF(Sal, "CNAEs com maior salário médio entre os negros", "CNAEs com maior representatividade de negros")
VAR L2 = IF(Sal, "Salário médio: remuneração média de dezembro dos negros em cada CNAE, em R$ nominais. Detalhes no tooltip.", "Representatividade: participação de negros (pretos + pardos) entre quem declarou cor em cada CNAE. Valores absolutos no tooltip.")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#434446" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 3 variável(is) (`Sal`, `L1`, `L2`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `D_Ct_MetNeg[metrica]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · AFL

---

### Titulo_Ct_Neg_Total_HTML

`_medidas.Titulo_Ct_Neg_Total_HTML` · formato `—`

**O que faz:**
Título do ranking (negros (pretos + pardos), Total); muda com o botão Representatividade / Salário médio.

**DAX:**
```dax
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetNeg[metrica]), "Representatividade") = "Salário médio"
VAR Piores = COALESCE(SELECTEDVALUE(D_Ct_Modo[modo]), "10 melhores setores") = "10 piores setores"
VAR L1 = IF(Sal, IF(Piores, "Divisões com menor salário médio entre os negros", "Divisões com maior salário médio entre os negros"), IF(Piores, "Divisões com menor representatividade de negros", "Divisões com maior representatividade de negros"))
VAR L2 = IF(Sal, "Salário médio: remuneração média de dezembro dos negros na divisão, em R$ nominais. Detalhes no tooltip.", "Representatividade: participação de negros (pretos + pardos) entre quem declarou cor na divisão. Valores absolutos no tooltip.")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#434446" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 4 variável(is) (`Sal`, `Piores`, `L1`, `L2`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `D_Ct_MetNeg[metrica]`, `D_Ct_Modo[modo]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · Todos os setores

---

## HTML\Quem trabalha

4 medidas.

### Esc_Comparacao_Pagina_HTML

`_medidas.Esc_Comparacao_Pagina_HTML` · formato `—`

**O que faz:**
Composição de escolaridade: a barra superior resume a página e as linhas comparam página e AFL.

**DAX:**
```dax
VAR TP = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Escolaridade))
VAR TA = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade))
VAR PaginaAFL = SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"
VAR TC = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Escolaridade))
VAR P0 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"}), TP)
VAR P1 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] = "Médio Incompleto"), TP)
VAR P2 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] = "Médio Completo"), TP)
VAR P3 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"}), TP)
VAR A0 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"}), TA)
VAR A1 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] = "Médio Incompleto"), TA)
VAR A2 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] = "Médio Completo"), TA)
VAR A3 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"}), TA)
VAR C0 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"}), TC)
VAR C1 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] = "Médio Incompleto"), TC)
VAR C2 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] = "Médio Completo"), TC)
VAR C3 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"}), TC)
VAR V0 = IF(PaginaAFL, C0, P0)
VAR V1 = IF(PaginaAFL, C1, P1)
VAR V2 = IF(PaginaAFL, C2, P2)
VAR V3 = IF(PaginaAFL, C3, P3)
VAR Rotulo = IF(PaginaAFL, "Comparáveis", "Página")
VAR Base = IF(PaginaAFL, TC, TP)
VAR Dica0 = "Até fundamental · " & Rotulo & ": " & FORMAT(V0, "0.0%", "pt-BR") & " (" & FORMAT(V0 * Base, "#,0", "pt-BR") & " empregos)"
VAR Dica1 = "Médio incompleto · " & Rotulo & ": " & FORMAT(V1, "0.0%", "pt-BR") & " (" & FORMAT(V1 * Base, "#,0", "pt-BR") & " empregos)"
VAR Dica2 = "Médio completo · " & Rotulo & ": " & FORMAT(V2, "0.0%", "pt-BR") & " (" & FORMAT(V2 * Base, "#,0", "pt-BR") & " empregos)"
VAR Dica3 = "Superior · " & Rotulo & ": " & FORMAT(V3, "0.0%", "pt-BR") & " (" & FORMAT(V3 * Base, "#,0", "pt-BR") & " empregos)"
VAR DicaA0 = "Até fundamental · AFL: " & FORMAT(A0, "0.0%", "pt-BR") & " (" & FORMAT(A0 * TA, "#,0", "pt-BR") & " empregos)"
VAR DicaA1 = "Médio incompleto · AFL: " & FORMAT(A1, "0.0%", "pt-BR") & " (" & FORMAT(A1 * TA, "#,0", "pt-BR") & " empregos)"
VAR DicaA2 = "Médio completo · AFL: " & FORMAT(A2, "0.0%", "pt-BR") & " (" & FORMAT(A2 * TA, "#,0", "pt-BR") & " empregos)"
VAR DicaA3 = "Superior · AFL: " & FORMAT(A3, "0.0%", "pt-BR") & " (" & FORMAT(A3 * TA, "#,0", "pt-BR") & " empregos)"
VAR Stack = "<div style='height:14px;display:flex;overflow:hidden;border-radius:3px;background:#EEF0F4;margin:2px 0 4px;'><i title='" & IF(PaginaAFL, DicaA0, Dica0) & "' style='display:block;min-width:2px;width:" & FORMAT(IF(PaginaAFL, A0, V0) * 100, "0.00", "en-US") & "%;background:#DFE6FF;'></i><i title='" & IF(PaginaAFL, DicaA1, Dica1) & "' style='display:block;min-width:2px;width:" & FORMAT(IF(PaginaAFL, A1, V1) * 100, "0.00", "en-US") & "%;background:#A9B8FF;'></i><i title='" & IF(PaginaAFL, DicaA2, Dica2) & "' style='display:block;min-width:2px;width:" & FORMAT(IF(PaginaAFL, A2, V2) * 100, "0.00", "en-US") & "%;background:#6267EC;'></i><i title='" & IF(PaginaAFL, DicaA3, Dica3) & "' style='display:block;min-width:2px;width:" & FORMAT(IF(PaginaAFL, A3, V3) * 100, "0.00", "en-US") & "%;background:#312E81;'></i></div>"
VAR Cab = "<div style='display:grid;grid-template-columns:1fr 68px 80px;gap:8px;color:#667085;font-size:12px;padding:4px 0;'><span>Escolaridade</span><span style='text-align:right;'>" & Rotulo & "</span><span style='text-align:right;'>AFL</span></div>"
VAR Linha0 = "<div style='display:grid;grid-template-columns:1fr 68px 80px;gap:8px;align-items:center;min-height:37px;border-top:1px solid #EDF0F2;font-size:15px;'><span><i style='display:inline-block;width:10px;height:10px;background:#DFE6FF;border-radius:2px;margin-right:7px;'></i>Até fundamental</span><b style='text-align:right;font-weight:600;'>" & FORMAT(V0, "0.0%", "pt-BR") & "</b><span style='text-align:right;color:#B86218;border:1px solid #F5A05C;border-radius:4px;padding:3px 6px;font-weight:600;'>" & FORMAT(A0, "0.0%", "pt-BR") & "</span></div>"
VAR Linha1 = "<div style='display:grid;grid-template-columns:1fr 68px 80px;gap:8px;align-items:center;min-height:37px;border-top:1px solid #EDF0F2;font-size:15px;'><span><i style='display:inline-block;width:10px;height:10px;background:#A9B8FF;border-radius:2px;margin-right:7px;'></i>Médio incompleto</span><b style='text-align:right;font-weight:600;'>" & FORMAT(V1, "0.0%", "pt-BR") & "</b><span style='text-align:right;color:#B86218;border:1px solid #F5A05C;border-radius:4px;padding:3px 6px;font-weight:600;'>" & FORMAT(A1, "0.0%", "pt-BR") & "</span></div>"
VAR Linha2 = "<div style='display:grid;grid-template-columns:1fr 68px 80px;gap:8px;align-items:center;min-height:37px;border-top:1px solid #EDF0F2;font-size:15px;'><span><i style='display:inline-block;width:10px;height:10px;background:#6267EC;border-radius:2px;margin-right:7px;'></i>Médio completo</span><b style='text-align:right;font-weight:600;'>" & FORMAT(V2, "0.0%", "pt-BR") & "</b><span style='text-align:right;color:#B86218;border:1px solid #F5A05C;border-radius:4px;padding:3px 6px;font-weight:600;'>" & FORMAT(A2, "0.0%", "pt-BR") & "</span></div>"
VAR Linha3 = "<div style='display:grid;grid-template-columns:1fr 68px 80px;gap:8px;align-items:center;min-height:37px;border-top:1px solid #EDF0F2;font-size:15px;'><span><i style='display:inline-block;width:10px;height:10px;background:#312E81;border-radius:2px;margin-right:7px;'></i>Superior</span><b style='text-align:right;font-weight:600;'>" & FORMAT(V3, "0.0%", "pt-BR") & "</b><span style='text-align:right;color:#B86218;border:1px solid #F5A05C;border-radius:4px;padding:3px 6px;font-weight:600;'>" & FORMAT(A3, "0.0%", "pt-BR") & "</span></div>"
RETURN "<style>div[style*='font-size:11px']{font-size:13px!important}div[style*='font-size:12px']{font-size:14px!important}div[style*='font-size:15px']{font-size:17px!important}</style><div style='font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;padding:0 10px 0 0;box-sizing:border-box;'>" & Stack & "<div style='display:flex;justify-content:space-between;color:#667085;font-size:11px;margin-bottom:8px;'><span>Composição dos " & IF(PaginaAFL, "AFL", LOWER(Rotulo)) & "</span><span>100%</span></div>" & Cab & SUBSTITUTE(SUBSTITUTE(Linha0, "<b style=", "<b title='" & Dica0 & "' style="), "<span style='text-align:right;color:#B86218", "<span title='" & DicaA0 & "' style='text-align:right;color:#B86218") & SUBSTITUTE(SUBSTITUTE(Linha1, "<b style=", "<b title='" & Dica1 & "' style="), "<span style='text-align:right;color:#B86218", "<span title='" & DicaA1 & "' style='text-align:right;color:#B86218") & SUBSTITUTE(SUBSTITUTE(Linha2, "<b style=", "<b title='" & Dica2 & "' style="), "<span style='text-align:right;color:#B86218", "<span title='" & DicaA2 & "' style='text-align:right;color:#B86218") & SUBSTITUTE(SUBSTITUTE(Linha3, "<b style=", "<b title='" & Dica3 & "' style="), "<span style='text-align:right;color:#B86218", "<span title='" & DicaA3 & "' style='text-align:right;color:#B86218") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 36 variável(is) (`TP`, `TA`, `PaginaAFL`, `TC`, `P0`, `P1`, `P2`, `P3`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_Escolaridade`, `D_GrupoSetor`.

**Usa:** `Empregos_Ref`, `D_Cnae[setor_afl]`, `D_Escolaridade[escolaridade_agrupada]`, `D_GrupoSetor[grupo_setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL, Quem trabalha · Todos os setores

---

### Manchete_Perfil_AFL_HTML

`_medidas.Manchete_Perfil_AFL_HTML` · formato `—`

**O que faz:**
Manchete da página Quem trabalha · AFL.

**DAX:**
```dax
VAR NUF = COUNTROWS(VALUES(D_regiao[uf]))
VAR Prep = IF(NOT ISFILTERED(D_regiao[uf]) || NUF = COUNTROWS(ALL(D_regiao[uf])), "No Brasil", IF(NUF = 1, "Em " & SELECTEDVALUE(D_regiao[estado]), "Nas " & NUF & " UFs escolhidas"))
VAR Texto = Prep & ", o empregado do AFL tem em média " & FORMAT([Perf_Idade], "0.0", "pt-BR") & " anos e " & IF(ISBLANK([Perf_Mulheres]), "—", FORMAT([Perf_Mulheres], "0.0%", "pt-BR")) & " são mulheres (Comparáveis: " & FORMAT(CALCULATE([Perf_Idade], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável"), "0.0", "pt-BR") & " anos e " & IF(ISBLANK([Perf_Mulheres_Comp]), "—", FORMAT([Perf_Mulheres_Comp], "0.0%", "pt-BR")) & ")"
VAR Contexto = [Contexto_Emp_AFL]
VAR Valido = NOT ISBLANK([Ano_Ref]) && NOT ISBLANK([Empregos_Ref])
RETURN
    IF(NOT Valido,
        "<div role='text' style='width:100%;height:118px;font-family:Segoe UI,Arial,sans-serif;font-size:24px;color:#434446;'>Não há dados para os filtros selecionados.</div>",
        "<div role='group' aria-label='Perfil dos empregados' style='width:100%;height:118px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
            & "<div style='max-height:84px;overflow:hidden;'><span style='display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;min-width:0;font-size:34px;line-height:40px;font-weight:600;font-variant-numeric:tabular-nums;overflow:hidden;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Texto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span></div>"
            & "<div style='height:30px;margin:4px 0 0;font-size:24px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Contexto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
        & "</div>")
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`NUF`, `Prep`, `Texto`, `Contexto`, `Valido`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`); formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Contexto_Emp_AFL`, `Empregos_Ref`, `Perf_Idade`, `Perf_Mulheres`, `Perf_Mulheres_Comp`, `D_GrupoSetor[grupo_setor]`, `D_regiao[estado]`, `D_regiao[uf]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL

---

### Manchete_Perfil_Total_HTML

`_medidas.Manchete_Perfil_Total_HTML` · formato `—`

**O que faz:**
Manchete da página Quem trabalha · Total.

**DAX:**
```dax
VAR NUF = COUNTROWS(VALUES(D_regiao[uf]))
VAR Prep = IF(NOT ISFILTERED(D_regiao[uf]) || NUF = COUNTROWS(ALL(D_regiao[uf])), "No Brasil", IF(NUF = 1, "Em " & SELECTEDVALUE(D_regiao[estado]), "Nas " & NUF & " UFs escolhidas"))
VAR Texto = Prep & ", o empregado tem em média " & FORMAT([Perf_Idade], "0.0", "pt-BR") & " anos e " & IF(ISBLANK([Perf_Mulheres]), "—", FORMAT([Perf_Mulheres], "0.0%", "pt-BR")) & " são mulheres; no AFL, " & FORMAT(CALCULATE([Perf_Idade], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"), "0.0", "pt-BR") & " anos e " & IF(ISBLANK([Perf_Mulheres_AFL]), "—", FORMAT([Perf_Mulheres_AFL], "0.0%", "pt-BR"))
VAR Contexto = [Contexto_Emp_Total]
VAR Valido = NOT ISBLANK([Ano_Ref]) && NOT ISBLANK([Empregos_Ref])
RETURN
    IF(NOT Valido,
        "<div role='text' style='width:100%;height:118px;font-family:Segoe UI,Arial,sans-serif;font-size:24px;color:#434446;'>Não há dados para os filtros selecionados.</div>",
        "<div role='group' aria-label='Perfil dos empregados' style='width:100%;height:118px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
            & "<div style='max-height:84px;overflow:hidden;'><span style='display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;min-width:0;font-size:34px;line-height:40px;font-weight:600;font-variant-numeric:tabular-nums;overflow:hidden;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Texto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span></div>"
            & "<div style='height:30px;margin:4px 0 0;font-size:24px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Contexto, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>"
        & "</div>")
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`NUF`, `Prep`, `Texto`, `Contexto`, `Valido`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`); formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Contexto_Emp_Total`, `Empregos_Ref`, `Perf_Idade`, `Perf_Mulheres`, `Perf_Mulheres_AFL`, `D_GrupoSetor[grupo_setor]`, `D_regiao[estado]`, `D_regiao[uf]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · Todos os setores

---

### Raca_Comparacao_Pagina_HTML

`_medidas.Raca_Comparacao_Pagina_HTML` · formato `—`

**O que faz:**
Composição de cor ou raça: a barra superior resume a página e as linhas comparam página e AFL.

**DAX:**
```dax
VAR TP = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Raca), D_Raca[declarada] = "Sim")
VAR TA = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[declarada] = "Sim")
VAR PaginaAFL = SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"
VAR TC = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[declarada] = "Sim")
VAR P0 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Branca", D_Raca[declarada] = "Sim"), TP)
VAR P1 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Negra", D_Raca[declarada] = "Sim"), TP)
VAR P2 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Amarela", D_Raca[declarada] = "Sim"), TP)
VAR P3 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Indígena", D_Raca[declarada] = "Sim"), TP)
VAR A0 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Branca", D_Raca[declarada] = "Sim"), TA)
VAR A1 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Negra", D_Raca[declarada] = "Sim"), TA)
VAR A2 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Amarela", D_Raca[declarada] = "Sim"), TA)
VAR A3 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Indígena", D_Raca[declarada] = "Sim"), TA)
VAR C0 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Branca", D_Raca[declarada] = "Sim"), TC)
VAR C1 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Negra", D_Raca[declarada] = "Sim"), TC)
VAR C2 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Amarela", D_Raca[declarada] = "Sim"), TC)
VAR C3 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Indígena", D_Raca[declarada] = "Sim"), TC)
VAR V0 = IF(PaginaAFL, C0, P0)
VAR V1 = IF(PaginaAFL, C1, P1)
VAR V2 = IF(PaginaAFL, C2, P2)
VAR V3 = IF(PaginaAFL, C3, P3)
VAR Rotulo = IF(PaginaAFL, "Comparáveis", "Página")
VAR Base = IF(PaginaAFL, TC, TP)
VAR Dica0 = "Branca · " & Rotulo & ": " & FORMAT(V0, "0.0%", "pt-BR") & " (" & FORMAT(V0 * Base, "#,0", "pt-BR") & " empregos)"
VAR Dica1 = "Negra (preta + parda) · " & Rotulo & ": " & FORMAT(V1, "0.0%", "pt-BR") & " (" & FORMAT(V1 * Base, "#,0", "pt-BR") & " empregos)"
VAR Dica2 = "Amarela · " & Rotulo & ": " & FORMAT(V2, "0.0%", "pt-BR") & " (" & FORMAT(V2 * Base, "#,0", "pt-BR") & " empregos)"
VAR Dica3 = "Indígena · " & Rotulo & ": " & FORMAT(V3, "0.0%", "pt-BR") & " (" & FORMAT(V3 * Base, "#,0", "pt-BR") & " empregos)"
VAR DicaA0 = "Branca · AFL: " & FORMAT(A0, "0.0%", "pt-BR") & " (" & FORMAT(A0 * TA, "#,0", "pt-BR") & " empregos)"
VAR DicaA1 = "Negra (preta + parda) · AFL: " & FORMAT(A1, "0.0%", "pt-BR") & " (" & FORMAT(A1 * TA, "#,0", "pt-BR") & " empregos)"
VAR DicaA2 = "Amarela · AFL: " & FORMAT(A2, "0.0%", "pt-BR") & " (" & FORMAT(A2 * TA, "#,0", "pt-BR") & " empregos)"
VAR DicaA3 = "Indígena · AFL: " & FORMAT(A3, "0.0%", "pt-BR") & " (" & FORMAT(A3 * TA, "#,0", "pt-BR") & " empregos)"
VAR Stack = "<div style='height:14px;display:flex;overflow:hidden;border-radius:3px;background:#EEF0F4;margin:2px 0 4px;'><i title='" & IF(PaginaAFL, DicaA0, Dica0) & "' style='display:block;min-width:2px;width:" & FORMAT(IF(PaginaAFL, A0, V0) * 100, "0.00", "en-US") & "%;background:#CBD2DD;'></i><i title='" & IF(PaginaAFL, DicaA1, Dica1) & "' style='display:block;min-width:2px;width:" & FORMAT(IF(PaginaAFL, A1, V1) * 100, "0.00", "en-US") & "%;background:#536176;'></i><i title='" & IF(PaginaAFL, DicaA2, Dica2) & "' style='display:block;min-width:2px;width:" & FORMAT(IF(PaginaAFL, A2, V2) * 100, "0.00", "en-US") & "%;background:#9CA7B7;'></i><i title='" & IF(PaginaAFL, DicaA3, Dica3) & "' style='display:block;min-width:2px;width:" & FORMAT(IF(PaginaAFL, A3, V3) * 100, "0.00", "en-US") & "%;background:#282A2E;'></i></div>"
VAR Cab = "<div style='display:grid;grid-template-columns:1fr 68px 80px;gap:8px;color:#667085;font-size:12px;padding:4px 0;'><span>Cor ou raça</span><span style='text-align:right;'>" & Rotulo & "</span><span style='text-align:right;'>AFL</span></div>"
VAR Linha0 = "<div style='display:grid;grid-template-columns:1fr 68px 80px;gap:8px;align-items:center;min-height:37px;border-top:1px solid #EDF0F2;font-size:15px;'><span><i style='display:inline-block;width:10px;height:10px;background:#CBD2DD;border-radius:2px;margin-right:7px;'></i>Branca</span><b style='text-align:right;font-weight:600;'>" & FORMAT(V0, "0.0%", "pt-BR") & "</b><span style='text-align:right;color:#B86218;border:1px solid #F5A05C;border-radius:4px;padding:3px 6px;font-weight:600;'>" & FORMAT(A0, "0.0%", "pt-BR") & "</span></div>"
VAR Linha1 = "<div style='display:grid;grid-template-columns:1fr 68px 80px;gap:8px;align-items:center;min-height:37px;border-top:1px solid #EDF0F2;font-size:15px;'><span><i style='display:inline-block;width:10px;height:10px;background:#536176;border-radius:2px;margin-right:7px;'></i>Negra (preta + parda)</span><b style='text-align:right;font-weight:600;'>" & FORMAT(V1, "0.0%", "pt-BR") & "</b><span style='text-align:right;color:#B86218;border:1px solid #F5A05C;border-radius:4px;padding:3px 6px;font-weight:600;'>" & FORMAT(A1, "0.0%", "pt-BR") & "</span></div>"
VAR Linha2 = "<div style='display:grid;grid-template-columns:1fr 68px 80px;gap:8px;align-items:center;min-height:37px;border-top:1px solid #EDF0F2;font-size:15px;'><span><i style='display:inline-block;width:10px;height:10px;background:#9CA7B7;border-radius:2px;margin-right:7px;'></i>Amarela</span><b style='text-align:right;font-weight:600;'>" & FORMAT(V2, "0.0%", "pt-BR") & "</b><span style='text-align:right;color:#B86218;border:1px solid #F5A05C;border-radius:4px;padding:3px 6px;font-weight:600;'>" & FORMAT(A2, "0.0%", "pt-BR") & "</span></div>"
VAR Linha3 = "<div style='display:grid;grid-template-columns:1fr 68px 80px;gap:8px;align-items:center;min-height:37px;border-top:1px solid #EDF0F2;font-size:15px;'><span><i style='display:inline-block;width:10px;height:10px;background:#282A2E;border-radius:2px;margin-right:7px;'></i>Indígena</span><b style='text-align:right;font-weight:600;'>" & FORMAT(V3, "0.0%", "pt-BR") & "</b><span style='text-align:right;color:#B86218;border:1px solid #F5A05C;border-radius:4px;padding:3px 6px;font-weight:600;'>" & FORMAT(A3, "0.0%", "pt-BR") & "</span></div>"
RETURN "<style>div[style*='font-size:11px']{font-size:13px!important}div[style*='font-size:12px']{font-size:14px!important}div[style*='font-size:15px']{font-size:17px!important}</style><div style='font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;padding:0 10px 0 0;box-sizing:border-box;'>" & Stack & "<div style='display:flex;justify-content:space-between;color:#667085;font-size:11px;margin-bottom:8px;'><span>Composição dos " & IF(PaginaAFL, "AFL", LOWER(Rotulo)) & "</span><span>100%</span></div>" & Cab & SUBSTITUTE(SUBSTITUTE(Linha0, "<b style=", "<b title='" & Dica0 & "' style="), "<span style='text-align:right;color:#B86218", "<span title='" & DicaA0 & "' style='text-align:right;color:#B86218") & SUBSTITUTE(SUBSTITUTE(Linha1, "<b style=", "<b title='" & Dica1 & "' style="), "<span style='text-align:right;color:#B86218", "<span title='" & DicaA1 & "' style='text-align:right;color:#B86218") & SUBSTITUTE(SUBSTITUTE(Linha2, "<b style=", "<b title='" & Dica2 & "' style="), "<span style='text-align:right;color:#B86218", "<span title='" & DicaA2 & "' style='text-align:right;color:#B86218") & SUBSTITUTE(SUBSTITUTE(Linha3, "<b style=", "<b title='" & Dica3 & "' style="), "<span style='text-align:right;color:#B86218", "<span title='" & DicaA3 & "' style='text-align:right;color:#B86218") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 36 variável(is) (`TP`, `TA`, `PaginaAFL`, `TC`, `P0`, `P1`, `P2`, `P3`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`, `D_Raca`.

**Usa:** `Empregos_Ref`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Raca[declarada]`, `D_Raca[grupo_raca]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL, Quem trabalha · Todos os setores

---

## HTML\Quem trabalha\KPIs

6 medidas.

### KPI_Escol_AFL_HTML

`_medidas.KPI_Escol_AFL_HTML` · formato `—`

**O que faz:**
KPI de ensino médio completo ou mais, com superior.

**DAX:**
```dax
VAR _A = [Ano_Ref]
RETURN
    "<div role='group' aria-label='KPI de escolaridade' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Ensino médio completo ou mais" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK([Perf_MedioMais]), "—", FORMAT([Perf_MedioMais], "0.0%", "pt-BR")) & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & "#434446" & ";overflow:hidden;'>" & "superior (completo ou não): " & IF(ISBLANK([Perf_Superior]), "—", FORMAT([Perf_Superior], "0.0%", "pt-BR")) & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>Comparáveis " & IF(ISBLANK([Perf_MedioMais_Comp]), "—", FORMAT([Perf_MedioMais_Comp], "0.0%", "pt-BR")) & " <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 1 variável(is) (`_A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Perf_MedioMais`, `Perf_MedioMais_Comp`, `Perf_Superior`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL

---

### KPI_Escol_Total_HTML

`_medidas.KPI_Escol_Total_HTML` · formato `—`

**O que faz:**
KPI de ensino médio completo ou mais, com superior.

**DAX:**
```dax
VAR _A = [Ano_Ref]
RETURN
    "<div role='group' aria-label='KPI de escolaridade' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Ensino médio completo ou mais" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK([Perf_MedioMais]), "—", FORMAT([Perf_MedioMais], "0.0%", "pt-BR")) & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & "#434446" & ";overflow:hidden;'>" & "superior (completo ou não): " & IF(ISBLANK([Perf_Superior]), "—", FORMAT([Perf_Superior], "0.0%", "pt-BR")) & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #D97706;border-radius:6px;background:#FDF7F1;color:#B86218;font-size:20px;line-height:26px;font-weight:600;'>AFL " & IF(ISBLANK([Perf_MedioMais_AFL]), "—", FORMAT([Perf_MedioMais_AFL], "0.0%", "pt-BR")) & "</span>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>Comparáveis " & IF(ISBLANK([Perf_MedioMais_Comp]), "—", FORMAT([Perf_MedioMais_Comp], "0.0%", "pt-BR")) & " <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 1 variável(is) (`_A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Perf_MedioMais`, `Perf_MedioMais_AFL`, `Perf_MedioMais_Comp`, `Perf_Superior`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · Todos os setores

---

### KPI_Jovens_AFL_HTML

`_medidas.KPI_Jovens_AFL_HTML` · formato `—`

**O que faz:**
KPI de empregados até 24 anos, com idade média.

**DAX:**
```dax
VAR Idade = [Perf_Idade]
VAR IdadeI = [Perf_Idade_Inicio]
VAR I = [Ano_Inicio_Trecho]
RETURN
    "<div role='group' aria-label='KPI de jovens' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Até 24 anos" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK([Perf_Ate24]), "—", FORMAT([Perf_Ate24], "0.0%", "pt-BR")) & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & "#434446" & ";overflow:hidden;'>" & "idade média " & FORMAT(Idade, "0.0", "pt-BR") & " anos" & IF([Ano_Ref] > I, " (" & FORMAT(IdadeI, "0.0", "pt-BR") & " em " & I & ")", "") & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>Comparáveis " & IF(ISBLANK([Perf_Ate24_Comp]), "—", FORMAT([Perf_Ate24_Comp], "0.0%", "pt-BR")) & " <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 3 variável(is) (`Idade`, `IdadeI`, `I`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Inicio_Trecho`, `Ano_Ref`, `Perf_Ate24`, `Perf_Ate24_Comp`, `Perf_Idade`, `Perf_Idade_Inicio`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL

---

### KPI_Jovens_Total_HTML

`_medidas.KPI_Jovens_Total_HTML` · formato `—`

**O que faz:**
KPI de empregados até 24 anos, com idade média.

**DAX:**
```dax
VAR Idade = [Perf_Idade]
VAR IdadeI = [Perf_Idade_Inicio]
VAR I = [Ano_Inicio_Trecho]
RETURN
    "<div role='group' aria-label='KPI de jovens' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Até 24 anos" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK([Perf_Ate24]), "—", FORMAT([Perf_Ate24], "0.0%", "pt-BR")) & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & "#434446" & ";overflow:hidden;'>" & "idade média " & FORMAT(Idade, "0.0", "pt-BR") & " anos" & IF([Ano_Ref] > I, " (" & FORMAT(IdadeI, "0.0", "pt-BR") & " em " & I & ")", "") & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #D97706;border-radius:6px;background:#FDF7F1;color:#B86218;font-size:20px;line-height:26px;font-weight:600;'>AFL " & IF(ISBLANK([Perf_Ate24_AFL]), "—", FORMAT([Perf_Ate24_AFL], "0.0%", "pt-BR")) & "</span>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>Comparáveis " & IF(ISBLANK([Perf_Ate24_Comp]), "—", FORMAT([Perf_Ate24_Comp], "0.0%", "pt-BR")) & " <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 3 variável(is) (`Idade`, `IdadeI`, `I`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Inicio_Trecho`, `Ano_Ref`, `Perf_Ate24`, `Perf_Ate24_AFL`, `Perf_Ate24_Comp`, `Perf_Idade`, `Perf_Idade_Inicio`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · Todos os setores

---

### KPI_Mulheres_AFL_HTML

`_medidas.KPI_Mulheres_AFL_HTML` · formato `—`

**O que faz:**
KPI de mulheres (% dos empregos), com chips.

**DAX:**
```dax
VAR _A = [Ano_Ref]
RETURN
    "<div role='group' aria-label='KPI de participação de mulheres' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Mulheres" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK([Perf_Mulheres]), "—", FORMAT([Perf_Mulheres], "0.0%", "pt-BR")) & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & "#434446" & ";overflow:hidden;'>" & "dos empregos em 31/12/" & [Ano_Ref] & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>Comparáveis " & IF(ISBLANK([Perf_Mulheres_Comp]), "—", FORMAT([Perf_Mulheres_Comp], "0.0%", "pt-BR")) & " <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 1 variável(is) (`_A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Perf_Mulheres`, `Perf_Mulheres_Comp`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL

---

### KPI_Mulheres_Total_HTML

`_medidas.KPI_Mulheres_Total_HTML` · formato `—`

**O que faz:**
KPI de mulheres (% dos empregos), com chips.

**DAX:**
```dax
VAR _A = [Ano_Ref]
RETURN
    "<div role='group' aria-label='KPI de participação de mulheres' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>"
        & "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>" & "Mulheres" & "</div>"
        & "<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>" & IF(ISBLANK([Perf_Mulheres]), "—", FORMAT([Perf_Mulheres], "0.0%", "pt-BR")) & "</div>"
        & "<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:" & "#434446" & ";overflow:hidden;'>" & "dos empregos em 31/12/" & [Ano_Ref] & "</div>" & "<div style='display:flex;gap:8px;margin-top:3px;white-space:nowrap;'>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #D97706;border-radius:6px;background:#FDF7F1;color:#B86218;font-size:20px;line-height:26px;font-weight:600;'>AFL " & IF(ISBLANK([Perf_Mulheres_AFL]), "—", FORMAT([Perf_Mulheres_AFL], "0.0%", "pt-BR")) & "</span>" & "<span style='display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;'>Comparáveis " & IF(ISBLANK([Perf_Mulheres_Comp]), "—", FORMAT([Perf_Mulheres_Comp], "0.0%", "pt-BR")) & " <span style='font-weight:400;font-size:17px;color:#434446;'>· ref.</span></span>" & "</div>"
        & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 1 variável(is) (`_A`) e devolve o resultado no `RETURN`. Formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Perf_Mulheres`, `Perf_Mulheres_AFL`, `Perf_Mulheres_Comp`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · Todos os setores

---

## HTML\Quem trabalha\Títulos

6 medidas.

### Titulo_CBO_HTML

`_medidas.Titulo_CBO_HTML` · formato `—`

**O que faz:**
Título das ocupações: a mais comum, seus empregos e % de mulheres.

**DAX:**
```dax
VAR T = FILTER(ADDCOLUMNS(VALUES(F_rais[cbo_2002]), "@v", [Empregos_Ref]), NOT ISBLANK([@v]))
VAR Lider1 = TOPN(1, T, [@v], DESC, F_rais[cbo_2002], ASC)
VAR Nome = CONCATENATEX(Lider1, F_rais[cbo_2002], "")
VAR V = MAXX(Lider1, [@v])
VAR Mul = CALCULATE([Perf_Mulheres], KEEPFILTERS(TREATAS({Nome}, F_rais[cbo_2002])))
VAR L1 = IF(COUNTROWS(T) = 0, "Sem dados para os filtros escolhidos", Nome & " é a ocupação mais comum: " & FORMAT(V, "#,0", "pt-BR") & " empregos")
VAR L2 = IF(COUNTROWS(T) = 0, "", "Mulheres: " & IF(ISBLANK(Mul), "—", FORMAT(Mul, "0.0%", "pt-BR")) & " · ocupações (CBO) com mais empregos em 31/12/" & [Ano_Ref])
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#1D1E21" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 7 variável(is) (`T`, `Lider1`, `Nome`, `V`, `Mul`, `L1`, `L2`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; aplica filtro virtual com `TREATAS`; pega os primeiros com `TOPN`; pega o maior valor de uma lista com `MAXX`; monta uma tabela virtual com `ADDCOLUMNS`; junta textos com `CONCATENATEX`.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `Perf_Mulheres`, `F_rais[cbo_2002]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL, Quem trabalha · Todos os setores

---

### Titulo_Esc_HTML

`_medidas.Titulo_Esc_HTML` · formato `—`

**O que faz:**
Título da escolaridade: ensino médio completo e superior, AFL × Comparáveis.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR TotA = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade))
VAR E0A = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"}), TotA)
VAR E1A = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"Médio Incompleto"}), TotA)
VAR E2A = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"Médio Completo"}), TotA)
VAR E3A = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"}), TotA)
VAR TotC = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Escolaridade))
VAR E0C = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"}), TotC)
VAR E1C = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"Médio Incompleto"}), TotC)
VAR E2C = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"Médio Completo"}), TotC)
VAR E3C = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"}), TotC)
VAR L1 = IF(ISBLANK(A) || TotA = 0, "Sem dados para os filtros escolhidos", IF(ISBLANK(E2A), "—", FORMAT(E2A, "0.0%", "pt-BR")) & " dos empregados do AFL têm o ensino médio completo")
VAR L2 = IF(ISBLANK(A) || TotA = 0, "", "Superior (completo ou não): " & IF(ISBLANK(E3A), "—", FORMAT(E3A, "0.0%", "pt-BR")) & " no AFL e " & IF(ISBLANK(E3C), "—", FORMAT(E3C, "0.0%", "pt-BR")) & " nos Comparáveis")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#312E81" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 13 variável(is) (`A`, `TotA`, `E0A`, `E1A`, `E2A`, `E3A`, `TotC`, `E0C`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_Escolaridade`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `D_Escolaridade[escolaridade_agrupada]`, `D_GrupoSetor[grupo_setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL

---

### Titulo_Esc_Pagina_HTML

`_medidas.Titulo_Esc_Pagina_HTML` · formato `—`

**O que faz:**
Manchete de escolaridade da visão geral: identifica a categoria predominante na página e a contrasta com o AFL.

**DAX:**
```dax
VAR TP = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Escolaridade))
VAR TA = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade))
VAR P0 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"}), TP)
VAR P1 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] = "Médio Incompleto"), TP)
VAR P2 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] = "Médio Completo"), TP)
VAR P3 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"}), TP)
VAR A0 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"}), TA)
VAR A1 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] = "Médio Incompleto"), TA)
VAR A2 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] = "Médio Completo"), TA)
VAR A3 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"}), TA)
VAR Maior = MAX(P0, MAX(P1, MAX(P2, P3)))
VAR Cat = SWITCH(TRUE(), Maior = P0, "até fundamental", Maior = P1, "médio incompleto", Maior = P2, "médio completo", "superior")
VAR AFL = SWITCH(TRUE(), Maior = P0, A0, Maior = P1, A1, Maior = P2, A2, A3)
VAR T1 = "O ensino com maior presença de empregados é o " & Cat & " com " & FORMAT(Maior, "0.0%", "pt-BR") & " dos empregados"
VAR T2 = "No AFL, " & Cat & " representa " & FORMAT(AFL, "0.0%", "pt-BR")
RETURN "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;padding:4px 56px 4px 0;display:flex;gap:10px;font-family:Segoe UI,Arial,sans-serif;overflow:hidden;'><span style='width:4px;align-self:stretch;background:#312E81;border-radius:2px;'></span><span><span style='display:block;font-size:24px;line-height:28px;font-weight:600;'>" & T1 & "</span><span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & T2 & "</span></span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 15 variável(is) (`TP`, `TA`, `P0`, `P1`, `P2`, `P3`, `A0`, `A1`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; escolhe o resultado com `SWITCH`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_Escolaridade`, `D_GrupoSetor`.

**Usa:** `Empregos_Ref`, `D_Escolaridade[escolaridade_agrupada]`, `D_GrupoSetor[grupo_setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · Todos os setores

---

### Titulo_Pir_HTML

`_medidas.Titulo_Pir_HTML` · formato `—`

**O que faz:**
Título da pirâmide: em quantas faixas de idade as mulheres são maioria.

**DAX:**
```dax
VAR T = ADDCOLUMNS(FILTER(VALUES(D_FaixaIdade[faixa_idade]), D_FaixaIdade[faixa_idade] <> "Não categorizado"), "@m", -[Pir_Mulheres], "@h", [Pir_Homens])
VAR N = COUNTROWS(FILTER(T, NOT ISBLANK([@m]) && NOT ISBLANK([@h])))
VAR NM = COUNTROWS(FILTER(T, [@m] > [@h]))
VAR L1 = IF(N = 0, "Sem dados para os filtros escolhidos", IF(NM = N, "As mulheres são maioria em todas as " & N & " faixas de idade", IF(NM = 0, "Os homens são maioria em todas as " & N & " faixas de idade", "As mulheres são maioria em " & NM & " das " & N & " faixas de idade")))
VAR L2 = IF(N = 0, "", "% do total de empregos em 31/12/" & [Ano_Ref] & ", por faixa de idade e sexo. O tooltip mostra os Comparáveis (referência)")
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#7F56D9" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`T`, `N`, `NM`, `L1`, `L2`) e devolve o resultado no `RETURN`. Monta uma tabela virtual com `ADDCOLUMNS`.

**Usa:** `Ano_Ref`, `Pir_Homens`, `Pir_Mulheres`, `D_FaixaIdade[faixa_idade]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL, Quem trabalha · Todos os setores

---

### Titulo_Raca_HTML

`_medidas.Titulo_Raca_HTML` · formato `—`

**O que faz:**
Título de cor/raça: % de negros entre quem declarou, AFL × Comparáveis.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR DeclA = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[declarada] = "Sim")
VAR TotRA = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca))
VAR R0A = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Branca", D_Raca[declarada] = "Sim"), DeclA)
VAR R1A = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Negra", D_Raca[declarada] = "Sim"), DeclA)
VAR R2A = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Amarela", D_Raca[declarada] = "Sim"), DeclA)
VAR R3A = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Indígena", D_Raca[declarada] = "Sim"), DeclA)
VAR PriA = CALCULATE([Perf_Primeiro], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca))
VAR IntA = CALCULATE([Perf_Intermitente], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca))
VAR IntNA = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), F_rais[trabalho_intermitente] = "Sim")
VAR DeclC = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[declarada] = "Sim")
VAR TotRC = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca))
VAR R0C = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Branca", D_Raca[declarada] = "Sim"), DeclC)
VAR R1C = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Negra", D_Raca[declarada] = "Sim"), DeclC)
VAR R2C = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Amarela", D_Raca[declarada] = "Sim"), DeclC)
VAR R3C = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Indígena", D_Raca[declarada] = "Sim"), DeclC)
VAR PriC = CALCULATE([Perf_Primeiro], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca))
VAR IntC = CALCULATE([Perf_Intermitente], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca))
VAR IntNC = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), F_rais[trabalho_intermitente] = "Sim")
VAR L1 = IF(ISBLANK(A) || DeclA = 0, "Sem dados para os filtros escolhidos", IF(ISBLANK(R1A), "—", FORMAT(R1A, "0.0%", "pt-BR")) & " dos empregados do AFL que declararam cor são negros")
VAR L2 = IF(ISBLANK(A) || DeclA = 0, "", "Comparáveis: " & IF(ISBLANK(R1C), "—", FORMAT(R1C, "0.0%", "pt-BR")) & " · declararam cor: " & IF(ISBLANK(DIVIDE(DeclA, TotRA)), "—", FORMAT(DIVIDE(DeclA, TotRA), "0.0%", "pt-BR")))
RETURN
    "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>"
        & "<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:" & "#475467" & ";'></span>"
        & "<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>"
        & "<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L1, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>"
        & IF(L2 = "", "", "<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(L2, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span>") & "</span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 21 variável(is) (`A`, `DeclA`, `TotRA`, `R0A`, `R1A`, `R2A`, `R3A`, `PriA`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`, `D_Raca`.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `Perf_Intermitente`, `Perf_Primeiro`, `D_GrupoSetor[grupo_setor]`, `D_Raca[declarada]`, `D_Raca[grupo_raca]`, `F_rais[trabalho_intermitente]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL

---

### Titulo_Raca_Pagina_HTML

`_medidas.Titulo_Raca_Pagina_HTML` · formato `—`

**O que faz:**
Manchete de cor ou raça da visão geral: identifica a categoria predominante na página e a contrasta com o AFL.

**DAX:**
```dax
VAR TP = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Raca), D_Raca[declarada] = "Sim")
VAR TA = CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[declarada] = "Sim")
VAR P0 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Branca", D_Raca[declarada] = "Sim"), TP)
VAR P1 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Negra", D_Raca[declarada] = "Sim"), TP)
VAR P2 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Amarela", D_Raca[declarada] = "Sim"), TP)
VAR P3 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Indígena", D_Raca[declarada] = "Sim"), TP)
VAR A0 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Branca", D_Raca[declarada] = "Sim"), TA)
VAR A1 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Negra", D_Raca[declarada] = "Sim"), TA)
VAR A2 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Amarela", D_Raca[declarada] = "Sim"), TA)
VAR A3 = DIVIDE(CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Indígena", D_Raca[declarada] = "Sim"), TA)
VAR Maior = MAX(P0, MAX(P1, MAX(P2, P3)))
VAR Cat = SWITCH(TRUE(), Maior = P0, "branca", Maior = P1, "negra (preta + parda)", Maior = P2, "amarela", "indígena")
VAR AFL = SWITCH(TRUE(), Maior = P0, A0, Maior = P1, A1, Maior = P2, A2, A3)
VAR T1 = "A raça com maior presença de empregados é a " & Cat & " com " & FORMAT(Maior, "0.0%", "pt-BR") & " dos empregados"
VAR T2 = "No AFL, a raça " & Cat & " representa " & FORMAT(AFL, "0.0%", "pt-BR")
RETURN "<div role='heading' aria-level='3' style='width:100%;height:100%;box-sizing:border-box;padding:4px 56px 4px 0;display:flex;gap:10px;font-family:Segoe UI,Arial,sans-serif;overflow:hidden;'><span style='width:4px;align-self:stretch;background:#475467;border-radius:2px;'></span><span><span style='display:block;font-size:24px;line-height:28px;font-weight:600;'>" & T1 & "</span><span style='display:block;font-size:20px;line-height:26px;color:#434446;'>" & T2 & "</span></span></div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 15 variável(is) (`TP`, `TA`, `P0`, `P1`, `P2`, `P3`, `A0`, `A1`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; escolhe o resultado com `SWITCH`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`, `D_Raca`.

**Usa:** `Empregos_Ref`, `D_GrupoSetor[grupo_setor]`, `D_Raca[declarada]`, `D_Raca[grupo_raca]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · Todos os setores

---

## HTML\Tooltips de gráficos

25 medidas.

### Tip_CBO_HTML

`_medidas.Tip_CBO_HTML` · formato `—`

**O que faz:**
Tooltip da ocupação (CBO): empregos, peso no recorte, mulheres e remuneração média.

**DAX:**
```dax
VAR O = SELECTEDVALUE(F_rais[cbo_2002])
VAR E = [Empregos_Ref]
VAR Peso = DIVIDE(E, CALCULATE([Empregos_Ref], REMOVEFILTERS(F_rais[cbo_2002])))
VAR Mul = [Perf_Mulheres]
VAR R = [Remuneracao_Media_Ref]
VAR RGeral = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(F_rais[cbo_2002]))
VAR Razao = DIVIDE(R, RGeral)
VAR Leitura = IF(ISBLANK(Razao), "", IF(Razao >= 1, "Paga acima da média do recorte.", "Paga abaixo da média do recorte."))
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(O, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos em 31/12/" & [Ano_Ref], "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(E, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK("Peso no recorte: " & IF(ISBLANK(Peso), "—", FORMAT(Peso, "0.0%", "pt-BR"))), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Peso no recorte: " & IF(ISBLANK(Peso), "—", FORMAT(Peso, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#7F56D9;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Mulheres", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Mul), "—", FORMAT(Mul, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#17B26A;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Remuneração média de dezembro", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(R), "—", "R$ " & FORMAT(R, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK(IF(ISBLANK(Razao), BLANK(), FORMAT(Razao, "0%", "pt-BR") & " da média do recorte")), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Razao), BLANK(), FORMAT(Razao, "0%", "pt-BR") & " da média do recorte"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 8 variável(is) (`O`, `E`, `Peso`, `Mul`, `R`, `RGeral`, `Razao`, `Leitura`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `F_rais[cbo_2002]`.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `Perf_Mulheres`, `Remuneracao_Media_Ref`, `F_rais[cbo_2002]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · CBO

---

### Tip_Ct_Esc_HTML

`_medidas.Tip_Ct_Esc_HTML` · formato `—`

**O que faz:**
Tooltip do ranking por perfil (empregados do nível de escolaridade escolhido): participação, salário médio, quantidades e referência do AFL.

**DAX:**
```dax
VAR Niv = COALESCE(SELECTEDVALUE(D_Ct_Nivel[nivel]), "Médio completo")
VAR EhAfl = ISFILTERED(D_AflAtividade[nome])
VAR Nome = IF(EhAfl, SELECTEDVALUE(D_AflAtividade[nome]), SELECTEDVALUE(D_Rank_Divisao[nm_divisao]))
VAR Rep = IF(EhAfl, [Ct_Esc_Rep], [Ct_Esc_Div_Rep])
VAR Sal = IF(EhAfl, [Ct_Esc_Sal], [Ct_Esc_Div_Sal])
VAR Qtd = IF(EhAfl, [Ct_Esc_Qtd], [Ct_Esc_Div_Qtd])
VAR Tot = IF(EhAfl, [Ct_Esc_Tot], [Ct_Esc_Div_Tot])
VAR RepAfl = IF(EhAfl || Nome = "AFL · conjunto de 6 CNAEs", BLANK(), CALCULATE([Ct_Esc_Rep], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"))
VAR SalAfl = IF(EhAfl || Nome = "AFL · conjunto de 6 CNAEs", BLANK(), CALCULATE([Ct_Esc_Sal], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"))
VAR Leitura = IF(ISBLANK(RepAfl) || ISBLANK(Rep), "", "Participação em relação ao AFL: " & IF(ISBLANK(Rep) || ISBLANK(RepAfl), "", IF(Rep >= RepAfl, "+", "−") & FORMAT(ABS(Rep - RepAfl) * 100, "0.0", "pt-BR") & " p.p.") & ".")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Nome, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos em 31/12/" & [Ano_Ref] & " · nível: " & SWITCH(Niv, "Até fundamental", "até o fundamental completo", "Médio incompleto", "médio incompleto", "Superior", "superior (completo ou não)", "médio completo"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Nível no total de empregos", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Rep), "—", FORMAT(Rep, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK(FORMAT(Qtd, "#,0", "pt-BR") & " de " & FORMAT(Tot, "#,0", "pt-BR") & " empregos"), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(Qtd, "#,0", "pt-BR") & " de " & FORMAT(Tot, "#,0", "pt-BR") & " empregos", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Salário médio (dezembro, R$ nominais)", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Sal), "—", "R$ " & FORMAT(Sal, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(NOT ISBLANK(RepAfl), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL (referência)", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(RepAfl), "—", FORMAT(RepAfl, "0.0%", "pt-BR")) & " · " & IF(ISBLANK(SalAfl), "—", "R$ " & FORMAT(SalAfl, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 10 variável(is) (`Niv`, `EhAfl`, `Nome`, `Rep`, `Sal`, `Qtd`, `Tot`, `RepAfl`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`); escolhe o resultado com `SWITCH`; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Ct_Esc_Div_Qtd`, `Ct_Esc_Div_Rep`, `Ct_Esc_Div_Sal`, `Ct_Esc_Div_Tot`, `Ct_Esc_Qtd`, `Ct_Esc_Rep`, `Ct_Esc_Sal`, `Ct_Esc_Tot`, `D_AflAtividade[nome]`, `D_Ct_Nivel[nivel]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Ranking · escolaridade

---

### Tip_Ct_Mul_HTML

`_medidas.Tip_Ct_Mul_HTML` · formato `—`

**O que faz:**
Tooltip do ranking por perfil (mulheres): participação, salário médio, quantidades e referência do AFL.

**DAX:**
```dax
VAR EhAfl = ISFILTERED(D_AflAtividade[nome])
VAR Nome = IF(EhAfl, SELECTEDVALUE(D_AflAtividade[nome]), SELECTEDVALUE(D_Rank_Divisao[nm_divisao]))
VAR Rep = IF(EhAfl, [Ct_Mul_Rep], [Ct_Mul_Div_Rep])
VAR Sal = IF(EhAfl, [Ct_Mul_Sal], [Ct_Mul_Div_Sal])
VAR Qtd = IF(EhAfl, [Ct_Mul_Qtd], [Ct_Mul_Div_Qtd])
VAR Tot = IF(EhAfl, [Ct_Mul_Tot], [Ct_Mul_Div_Tot])
VAR RepAfl = IF(EhAfl || Nome = "AFL · conjunto de 6 CNAEs", BLANK(), CALCULATE([Ct_Mul_Rep], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"))
VAR SalAfl = IF(EhAfl || Nome = "AFL · conjunto de 6 CNAEs", BLANK(), CALCULATE([Ct_Mul_Sal], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"))
VAR Leitura = IF(ISBLANK(RepAfl) || ISBLANK(Rep), "", "Participação em relação ao AFL: " & IF(ISBLANK(Rep) || ISBLANK(RepAfl), "", IF(Rep >= RepAfl, "+", "−") & FORMAT(ABS(Rep - RepAfl) * 100, "0.0", "pt-BR") & " p.p.") & ".")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Nome, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos em 31/12/" & [Ano_Ref], "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#7F56D9;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Mulheres no total de empregos", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Rep), "—", FORMAT(Rep, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK(FORMAT(Qtd, "#,0", "pt-BR") & " de " & FORMAT(Tot, "#,0", "pt-BR") & " empregos"), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(Qtd, "#,0", "pt-BR") & " de " & FORMAT(Tot, "#,0", "pt-BR") & " empregos", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Salário médio (dezembro, R$ nominais)", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Sal), "—", "R$ " & FORMAT(Sal, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(NOT ISBLANK(RepAfl), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL (referência)", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(RepAfl), "—", FORMAT(RepAfl, "0.0%", "pt-BR")) & " · " & IF(ISBLANK(SalAfl), "—", "R$ " & FORMAT(SalAfl, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 9 variável(is) (`EhAfl`, `Nome`, `Rep`, `Sal`, `Qtd`, `Tot`, `RepAfl`, `SalAfl`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`); formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Ct_Mul_Div_Qtd`, `Ct_Mul_Div_Rep`, `Ct_Mul_Div_Sal`, `Ct_Mul_Div_Tot`, `Ct_Mul_Qtd`, `Ct_Mul_Rep`, `Ct_Mul_Sal`, `Ct_Mul_Tot`, `D_AflAtividade[nome]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Ranking · mulheres

---

### Tip_Ct_Neg_HTML

`_medidas.Tip_Ct_Neg_HTML` · formato `—`

**O que faz:**
Tooltip do ranking por perfil (negros (pretos + pardos)): participação, salário médio, quantidades e referência do AFL.

**DAX:**
```dax
VAR EhAfl = ISFILTERED(D_AflAtividade[nome])
VAR Nome = IF(EhAfl, SELECTEDVALUE(D_AflAtividade[nome]), SELECTEDVALUE(D_Rank_Divisao[nm_divisao]))
VAR Rep = IF(EhAfl, [Ct_Neg_Rep], [Ct_Neg_Div_Rep])
VAR Sal = IF(EhAfl, [Ct_Neg_Sal], [Ct_Neg_Div_Sal])
VAR Qtd = IF(EhAfl, [Ct_Neg_Qtd], [Ct_Neg_Div_Qtd])
VAR Tot = IF(EhAfl, [Ct_Neg_Tot], [Ct_Neg_Div_Tot])
VAR RepAfl = IF(EhAfl || Nome = "AFL · conjunto de 6 CNAEs", BLANK(), CALCULATE([Ct_Neg_Rep], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"))
VAR SalAfl = IF(EhAfl || Nome = "AFL · conjunto de 6 CNAEs", BLANK(), CALCULATE([Ct_Neg_Sal], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"))
VAR Leitura = IF(ISBLANK(RepAfl) || ISBLANK(Rep), "", "Participação em relação ao AFL: " & IF(ISBLANK(Rep) || ISBLANK(RepAfl), "", IF(Rep >= RepAfl, "+", "−") & FORMAT(ABS(Rep - RepAfl) * 100, "0.0", "pt-BR") & " p.p.") & ".")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Nome, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos em 31/12/" & [Ano_Ref], "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Negros entre quem declarou cor", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Rep), "—", FORMAT(Rep, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK(FORMAT(Qtd, "#,0", "pt-BR") & " de " & FORMAT(Tot, "#,0", "pt-BR") & " empregos"), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(Qtd, "#,0", "pt-BR") & " de " & FORMAT(Tot, "#,0", "pt-BR") & " empregos", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Salário médio (dezembro, R$ nominais)", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Sal), "—", "R$ " & FORMAT(Sal, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(NOT ISBLANK(RepAfl), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL (referência)", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(RepAfl), "—", FORMAT(RepAfl, "0.0%", "pt-BR")) & " · " & IF(ISBLANK(SalAfl), "—", "R$ " & FORMAT(SalAfl, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 9 variável(is) (`EhAfl`, `Nome`, `Rep`, `Sal`, `Qtd`, `Tot`, `RepAfl`, `SalAfl`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; muda de comportamento conforme o que está filtrado (`ISFILTERED`); formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Ct_Neg_Div_Qtd`, `Ct_Neg_Div_Rep`, `Ct_Neg_Div_Sal`, `Ct_Neg_Div_Tot`, `Ct_Neg_Qtd`, `Ct_Neg_Rep`, `Ct_Neg_Sal`, `Ct_Neg_Tot`, `D_AflAtividade[nome]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Ranking · negros

---

### Tip_Emp_Ano_HTML

`_medidas.Tip_Emp_Ano_HTML` · formato `—`

**O que faz:**
Tooltip do ano na variação anual do emprego: empregos e variação do AFL, Comparáveis e seleção atual.

**DAX:**
```dax
VAR A = SELECTEDVALUE(D_Calendario[Ano])
VAR EA = [Empregos_Ref_AFL]
VAR VA = [Empregos_Var_Pct_AFL]
VAR EC = [Empregos_Ref_Comparavel]
VAR VC = [Empregos_Var_Pct_Comparavel]
VAR ES = [Empregos_Ref]
VAR VS = [Empregos_Var_Pct]
VAR PaginaAFL = SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"
VAR Leitura = IF(ISBLANK(VA) || ISBLANK(VC), "", "Em " & A & ", o emprego do AFL " & IF(VA >= VC, "cresceu mais", "cresceu menos") & " que o dos Comparáveis (" & IF(ISBLANK(VA) || ISBLANK(VC), "", IF(VA >= VC, "+", "−") & FORMAT(ABS(VA - VC) * 100, "0.0", "pt-BR") & " p.p.") & ").")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("31/12/" & A, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(VA), IF(A = 2022, "Sem comparação com 2021: nova fonte (eSocial)", "Primeiro ano da série"), "Variação sobre 31/12/" & (A - 1)), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(EA, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK(IF(ISBLANK(VA), BLANK(), IF(ISBLANK(VA), "—", IF(VA > 0, "+", IF(VA < 0, "−", "")) & FORMAT(ABS(VA), "0.0%", "pt-BR")))), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(VA), BLANK(), IF(ISBLANK(VA), "—", IF(VA > 0, "+", IF(VA < 0, "−", "")) & FORMAT(ABS(VA), "0.0%", "pt-BR"))), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Comparáveis", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(EC, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK(IF(ISBLANK(VC), BLANK(), IF(ISBLANK(VC), "—", IF(VC > 0, "+", IF(VC < 0, "−", "")) & FORMAT(ABS(VC), "0.0%", "pt-BR")))), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(VC), BLANK(), IF(ISBLANK(VC), "—", IF(VC > 0, "+", IF(VC < 0, "−", "")) & FORMAT(ABS(VC), "0.0%", "pt-BR"))), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(NOT PaginaAFL, "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#98A2B3;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Seleção atual", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(ES, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK(IF(ISBLANK(VS), BLANK(), IF(ISBLANK(VS), "—", IF(VS > 0, "+", IF(VS < 0, "−", "")) & FORMAT(ABS(VS), "0.0%", "pt-BR")))), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(VS), BLANK(), IF(ISBLANK(VS), "—", IF(VS > 0, "+", IF(VS < 0, "−", "")) & FORMAT(ABS(VS), "0.0%", "pt-BR"))), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 9 variável(is) (`A`, `EA`, `VA`, `EC`, `VC`, `ES`, `VS`, `PaginaAFL`…) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Empregos_Ref`, `Empregos_Ref_AFL`, `Empregos_Ref_Comparavel`, `Empregos_Var_Pct`, `Empregos_Var_Pct_AFL`, `Empregos_Var_Pct_Comparavel`, `D_Calendario[Ano]`, `D_Cnae[setor_afl]`
**É usada por:** `Tip_Emp_Ano_PorPagina_HTML`

---

### Tip_Emp_Ano_PorPagina_HTML

`_medidas.Tip_Emp_Ano_PorPagina_HTML` · formato `—`

**O que faz:**
Tooltip anual ajustado à página: seleção atual em Todos e referência no AFL.

**DAX:**
```dax
IF(SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim", [Tip_Emp_Ano_HTML], [Tip_Emp_Ano_Sem_Comparaveis_HTML])
```

**Como funciona:**
Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Tip_Emp_Ano_HTML`, `Tip_Emp_Ano_Sem_Comparaveis_HTML`, `D_Cnae[setor_afl]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Emp Ano

---

### Tip_Emp_Ano_Sem_Comparaveis_HTML

`_medidas.Tip_Emp_Ano_Sem_Comparaveis_HTML` · formato `—`

**O que faz:**
Tooltip anual de empregos sem a referência de Comparáveis.

**DAX:**
```dax
VAR A = SELECTEDVALUE(D_Calendario[Ano])
VAR EA = [Empregos_Ref_AFL]
VAR VA = [Empregos_Var_Pct_AFL]
VAR ES = [Empregos_Ref]
VAR VS = [Empregos_Var_Pct]
VAR PaginaAFL = SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"
VAR Sub = IF(ISBLANK(VA), IF(A = 2022, "Sem comparação com 2021: nova fonte (eSocial)", "Primeiro ano da série"), "Variação sobre 31/12/" & (A - 1))
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>"
    & "<div style='font-size:24px;line-height:30px;font-weight:600;'>31/12/" & A & "</div>"
    & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & Sub & "</div>"
    & "<div style='margin-top:12px;font-size:20px;'><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>AFL <b style='float:right;font-size:22px;'>" & FORMAT(EA, "#,0", "pt-BR") & "</b><div style='font-size:17px;color:#667085;margin-left:20px;'>" & IF(ISBLANK(VA), "", FORMAT(VA, "+0.0%;-0.0%;0.0%", "pt-BR")) & "</div></div>"
    & IF(NOT PaginaAFL, "<div style='margin-top:12px;font-size:20px;'><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#98A2B3;margin-right:8px;'></span>Seleção atual <b style='float:right;font-size:22px;'>" & FORMAT(ES, "#,0", "pt-BR") & "</b><div style='font-size:17px;color:#667085;margin-left:20px;'>" & IF(ISBLANK(VS), "", FORMAT(VS, "+0.0%;-0.0%;0.0%", "pt-BR")) & "</div></div>", "")
    & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 7 variável(is) (`A`, `EA`, `VA`, `ES`, `VS`, `PaginaAFL`, `Sub`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Empregos_Ref`, `Empregos_Ref_AFL`, `Empregos_Var_Pct`, `Empregos_Var_Pct_AFL`, `D_Calendario[Ano]`, `D_Cnae[setor_afl]`
**É usada por:** `Tip_Emp_Ano_PorPagina_HTML`

---

### Tip_Emp_Atividade_HTML

`_medidas.Tip_Emp_Atividade_HTML` · formato `—`

**O que faz:**
Tooltip da atividade do AFL: empregos, peso no AFL, variação e posição.

**DAX:**
```dax
VAR N = SELECTEDVALUE(D_AflAtividade[nome])
VAR E = [Empregos_Ref]
VAR Tot = CALCULATE([Empregos_Ref_AFL], REMOVEFILTERS(D_AflAtividade))
VAR Peso = DIVIDE(E, Tot)
VAR VarAno = [Emp_Atividade_Var]
VAR Pos = IF(NOT ISBLANK(E), RANKX(ALL(D_AflAtividade[nome]), [Empregos_Ref], , DESC, DENSE))
VAR Leitura = ""
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(N, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos em 31/12/" & [Ano_Ref], "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(E, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK(IF(ISBLANK(VarAno), BLANK(), IF(ISBLANK(VarAno), "—", IF(VarAno > 0, "+", IF(VarAno < 0, "−", "")) & FORMAT(ABS(VarAno), "0.0%", "pt-BR")) & " sobre o ano anterior")), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(VarAno), BLANK(), IF(ISBLANK(VarAno), "—", IF(VarAno > 0, "+", IF(VarAno < 0, "−", "")) & FORMAT(ABS(VarAno), "0.0%", "pt-BR")) & " sobre o ano anterior"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Peso nos empregos do AFL", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Peso), "—", FORMAT(Peso, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Posição entre as atividades", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Pos), "—", Pos & "ª de 6"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 7 variável(is) (`N`, `E`, `Tot`, `Peso`, `VarAno`, `Pos`, `Leitura`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; calcula posição com `RANKX`; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_AflAtividade`.

**Usa:** `Ano_Ref`, `Emp_Atividade_Var`, `Empregos_Ref`, `Empregos_Ref_AFL`, `D_AflAtividade[nome]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Emp Atividade

---

### Tip_Emp_Divisao_HTML

`_medidas.Tip_Emp_Divisao_HTML` · formato `—`

**O que faz:**
Tooltip da divisão no ranking de empregos: empregos, peso no emprego formal e posição.

**DAX:**
```dax
VAR N = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
VAR E = [Emp_Divisao]
VAR Tot = [Empregos_Ref_Todos]
VAR Pos = IF(NOT ISBLANK(E), RANKX(ALL(D_Rank_Divisao[nm_divisao]), [Emp_Divisao], , DESC, DENSE))
VAR NDiv = [Emp_Total_Divisoes]
VAR Peso = DIVIDE(E, Tot)
VAR Leitura = IF(ISBLANK(Pos), "", IF(N = "AFL · conjunto de 6 CNAEs", "O AFL reúne seis atividades de alimentação fora do lar; as demais barras são divisões da CNAE.", "Divisão da CNAE (dois dígitos)."))
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(N, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos em 31/12/" & [Ano_Ref], "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(E, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Peso no emprego formal", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Peso), "—", FORMAT(Peso, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Posição no ranking", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Pos), "—", Pos & "º de " & NDiv), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 7 variável(is) (`N`, `E`, `Tot`, `Pos`, `NDiv`, `Peso`, `Leitura`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; calcula posição com `RANKX`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Ano_Ref`, `Emp_Divisao`, `Emp_Total_Divisoes`, `Empregos_Ref_Todos`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Emp Divisao

---

### Tip_Emp_UF_HTML

`_medidas.Tip_Emp_UF_HTML` · formato `—`

**O que faz:**
Tooltip da UF: empregos do AFL e dos Comparáveis, peso do AFL e parte do AFL do país.

**DAX:**
```dax
VAR UFNome = SELECTEDVALUE(D_regiao[estado], SELECTEDVALUE(D_regiao[uf]))
VAR Mun = SELECTEDVALUE(D_regiao[municipio])
VAR UF = IF(ISBLANK(Mun), UFNome, Mun & " · " & SELECTEDVALUE(D_regiao[uf]))
VAR EA = [Empregos_Ref_AFL]
VAR EC = [Empregos_Ref_Comparavel]
VAR Peso = [Emp_UF_Peso_AFL]
VAR ParteBR = DIVIDE(EA, CALCULATE([Empregos_Ref_AFL], REMOVEFILTERS(D_regiao)))
VAR Leitura = IF(ISBLANK(Peso), "", "A cada 100 empregos de AFL + Comparáveis em " & UF & ", " & FORMAT(Peso * 100, "0", "pt-BR") & " são do AFL.")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UF, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos em 31/12/" & [Ano_Ref], "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(EA, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK("Parte do AFL do país: " & IF(ISBLANK(ParteBR), "—", FORMAT(ParteBR, "0.0%", "pt-BR"))), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Parte do AFL do país: " & IF(ISBLANK(ParteBR), "—", FORMAT(ParteBR, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Comparáveis", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(EC, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Peso do AFL nos Comparáveis", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Peso), "—", FORMAT(Peso, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 8 variável(is) (`UFNome`, `Mun`, `UF`, `EA`, `EC`, `Peso`, `ParteBR`, `Leitura`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_regiao`.

**Usa:** `Ano_Ref`, `Emp_UF_Peso_AFL`, `Empregos_Ref_AFL`, `Empregos_Ref_Comparavel`, `D_regiao[estado]`, `D_regiao[municipio]`, `D_regiao[uf]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Emp UF

---

### Tip_Ind_Ano_HTML

`_medidas.Tip_Ind_Ano_HTML` · formato `—`

**O que faz:**
Tooltip do ano na série do indicador de contratação.

**DAX:**
```dax
VAR A = SELECTEDVALUE(D_Calendario[Ano])
VAR VA = CALCULATE([Ind_Valor_Ano], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
VAR VC = CALCULATE([Ind_Valor_Ano], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
VAR VS = [Ind_Valor_Ano]
VAR Rot = [Ind_Rotulo]
VAR PaginaAFL = SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"
VAR Leitura = IF(ISBLANK(VA) || ISBLANK(VC), "Sem dados para este indicador neste ano.", "O AFL está " & IF(ISBLANK(VA) || ISBLANK(VC), "", IF(VA >= VC, "+", "−") & FORMAT(ABS(VA - VC) * 100, "0.0", "pt-BR") & " p.p.") & " em relação aos Comparáveis.")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("31/12/" & A, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Participação de " & Rot, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(VA), "—", FORMAT(VA, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Comparáveis", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(VC), "—", FORMAT(VC, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(NOT PaginaAFL, "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#98A2B3;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Seleção atual", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(VS), "—", FORMAT(VS, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 7 variável(is) (`A`, `VA`, `VC`, `VS`, `Rot`, `PaginaAFL`, `Leitura`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ind_Rotulo`, `Ind_Valor_Ano`, `D_Calendario[Ano]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Ind Ano

---

### Tip_Ind_Atividade_HTML

`_medidas.Tip_Ind_Atividade_HTML` · formato `—`

**O que faz:**
Tooltip da atividade do AFL: valor do indicador e comparação com o AFL inteiro.

**DAX:**
```dax
VAR N = SELECTEDVALUE(D_AflAtividade[nome])
VAR V = [Ind_Valor_Ctx]
VAR Afl = [Ind_Valor_AFL]
VAR E = [Empregos_Ref]
VAR Rot = [Ind_Rotulo]
VAR Leitura = IF(ISBLANK(V) || ISBLANK(Afl), "", "A atividade está " & IF(ISBLANK(V) || ISBLANK(Afl), "", IF(V >= Afl, "+", "−") & FORMAT(ABS(V - Afl) * 100, "0.0", "pt-BR") & " p.p.") & " em relação à média do AFL.")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(N, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Participação de " & Rot & " em " & [Ind_Ano], "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Na atividade", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(V), "—", FORMAT(V, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("No AFL inteiro", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Afl), "—", FORMAT(Afl, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos da atividade", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(E, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 6 variável(is) (`N`, `V`, `Afl`, `E`, `Rot`, `Leitura`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Empregos_Ref`, `Ind_Ano`, `Ind_Rotulo`, `Ind_Valor_AFL`, `Ind_Valor_Ctx`, `D_AflAtividade[nome]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Ind Atividade

---

### Tip_Ind_Divisao_HTML

`_medidas.Tip_Ind_Divisao_HTML` · formato `—`

**O que faz:**
Tooltip da divisão no ranking de contratação: valor do indicador, posição e diferença para o AFL.

**DAX:**
```dax
VAR N = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
VAR V = [Ind_Valor_Div]
VAR Afl = [Ind_Valor_AFL]
VAR E = [Emp_Divisao]
VAR Rot = [Ind_Rotulo]
VAR Pos = IF(NOT ISBLANK(V), RANKX(ALL(D_Rank_Divisao[nm_divisao]), [Ind_Valor_Div], , DESC, DENSE))
VAR NDiv = [Ind_Total_Divisoes]
VAR Leitura = IF(ISBLANK(V) || ISBLANK(Afl), "", IF(N = "AFL · conjunto de 6 CNAEs", "É o conjunto de seis atividades do AFL.", "O AFL está " & IF(ISBLANK(Afl) || ISBLANK(V), "", IF(Afl >= V, "+", "−") & FORMAT(ABS(Afl - V) * 100, "0.0", "pt-BR") & " p.p.") & " em relação a esta divisão."))
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(N, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Participação de " & Rot & " em " & [Ind_Ano], "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Na divisão", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(V), "—", FORMAT(V, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK("Posição: " & IF(ISBLANK(Pos), "—", Pos & "º de " & NDiv)), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Posição: " & IF(ISBLANK(Pos), "—", Pos & "º de " & NDiv), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("No AFL", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Afl), "—", FORMAT(Afl, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos da divisão", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(E, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 8 variável(is) (`N`, `V`, `Afl`, `E`, `Rot`, `Pos`, `NDiv`, `Leitura`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; calcula posição com `RANKX`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Emp_Divisao`, `Ind_Ano`, `Ind_Rotulo`, `Ind_Total_Divisoes`, `Ind_Valor_AFL`, `Ind_Valor_Div`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Ind Divisao

---

### Tip_Ind_UF_HTML

`_medidas.Tip_Ind_UF_HTML` · formato `—`

**O que faz:**
Tooltip da UF na contratação: valor do indicador no recorte e no AFL da UF.

**DAX:**
```dax
VAR UFNome = SELECTEDVALUE(D_regiao[estado], SELECTEDVALUE(D_regiao[uf]))
VAR Mun = SELECTEDVALUE(D_regiao[municipio])
VAR UF = IF(ISBLANK(Mun), UFNome, Mun & " · " & SELECTEDVALUE(D_regiao[uf]))
VAR V = [Ind_Valor_Ctx]
VAR VA = [Ind_UF_AFL_Dica]
VAR E = [Empregos_Ref]
VAR EA = [Empregos_Ref_AFL]
VAR Rot = [Ind_Rotulo]
VAR PaginaAFL = SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"
VAR Leitura = IF(ISBLANK(V) || ISBLANK(VA) || PaginaAFL, "", "O AFL está " & IF(ISBLANK(VA) || ISBLANK(V), "", IF(VA >= V, "+", "−") & FORMAT(ABS(VA - V) * 100, "0.0", "pt-BR") & " p.p.") & " em relação ao recorte nesta UF.")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UF, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Participação de " & Rot & " em " & [Ind_Ano], "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(NOT PaginaAFL, "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#98A2B3;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Recorte da página", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(V), "—", FORMAT(V, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK("Empregos: " & FORMAT(E, "#,0", "pt-BR")), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos: " & FORMAT(E, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(VA), "—", FORMAT(VA, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK("Empregos do AFL: " & FORMAT(EA, "#,0", "pt-BR")), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos do AFL: " & FORMAT(EA, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 10 variável(is) (`UFNome`, `Mun`, `UF`, `V`, `VA`, `E`, `EA`, `Rot`…) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Empregos_Ref`, `Empregos_Ref_AFL`, `Ind_Ano`, `Ind_Rotulo`, `Ind_UF_AFL_Dica`, `Ind_Valor_Ctx`, `D_Cnae[setor_afl]`, `D_regiao[estado]`, `D_regiao[municipio]`, `D_regiao[uf]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Ind UF

---

### Tip_Pir_HTML

`_medidas.Tip_Pir_HTML` · formato `—`

**O que faz:**
Tooltip da pirâmide: empregos da faixa, peso da faixa e participação de mulheres (recorte, AFL e Comparáveis).

**DAX:**
```dax
VAR F = SELECTEDVALUE(D_FaixaIdade[faixa_idade])
VAR E = [Empregos_Ref]
VAR Mul = DIVIDE(CALCULATE([Empregos_Ref], KEEPFILTERS(D_Sexo[sexo] = "Mulher")), E)
VAR MulC = CALCULATE(DIVIDE(CALCULATE([Empregos_Ref], KEEPFILTERS(D_Sexo[sexo] = "Mulher")), [Empregos_Ref]), REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
VAR MulA = CALCULATE(DIVIDE(CALCULATE([Empregos_Ref], KEEPFILTERS(D_Sexo[sexo] = "Mulher")), [Empregos_Ref]), REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
VAR TotFaixa = DIVIDE(E, CALCULATE([Empregos_Ref], REMOVEFILTERS(D_FaixaIdade)))
VAR Leitura = IF(ISBLANK(Mul), "", IF(Mul > 0.5, "As mulheres são maioria nesta faixa.", "Os homens são maioria nesta faixa."))
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Faixa de " & F & " anos", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos em 31/12/" & [Ano_Ref], "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos da faixa", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(FORMAT(E, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK("Peso da faixa no recorte: " & IF(ISBLANK(TotFaixa), "—", FORMAT(TotFaixa, "0.0%", "pt-BR"))), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Peso da faixa no recorte: " & IF(ISBLANK(TotFaixa), "—", FORMAT(TotFaixa, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#7F56D9;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Mulheres na faixa (recorte)", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(Mul), "—", FORMAT(Mul, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(NOT(SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Mulheres na faixa · AFL", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(MulA), "—", FORMAT(MulA, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Mulheres na faixa · Comparáveis", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(MulC), "—", FORMAT(MulC, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 7 variável(is) (`F`, `E`, `Mul`, `MulC`, `MulA`, `TotFaixa`, `Leitura`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_FaixaIdade`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `D_Cnae[setor_afl]`, `D_FaixaIdade[faixa_idade]`, `D_GrupoSetor[grupo_setor]`, `D_Sexo[sexo]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Pir

---

### Tip_Rem_Ano_HTML

`_medidas.Tip_Rem_Ano_HTML` · formato `—`

**O que faz:**
Tooltip do ano na série de remuneração: média do AFL e dos Comparáveis.

**DAX:**
```dax
VAR A = SELECTEDVALUE(D_Calendario[Ano])
VAR MA = [Remuneracao_Media_Ref_AFL]
VAR MC = [Remuneracao_Media_Ref_Comparavel]
VAR MS = [Remuneracao_Media_Ref]
VAR Razao = DIVIDE(MA, MC)
VAR PaginaAFL = SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"
VAR Leitura = IF(ISBLANK(Razao), "", "O AFL pagou, em média, " & FORMAT(Razao, "0%", "pt-BR") & " do que pagaram os Comparáveis. Valores nominais: não descontam a inflação.")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Dezembro de " & A, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Remuneração de dezembro, R$ nominais", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL · média", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(MA), "—", "R$ " & FORMAT(MA, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Comparáveis · média", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(MC), "—", "R$ " & FORMAT(MC, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(NOT PaginaAFL, "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#98A2B3;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Seleção atual · média", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(MS), "—", "R$ " & FORMAT(MS, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 7 variável(is) (`A`, `MA`, `MC`, `MS`, `Razao`, `PaginaAFL`, `Leitura`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Remuneracao_Media_Ref`, `Remuneracao_Media_Ref_AFL`, `Remuneracao_Media_Ref_Comparavel`, `D_Calendario[Ano]`, `D_Cnae[setor_afl]`
**É usada por:** `Tip_Rem_Ano_Total_HTML`

---

### Tip_Rem_Ano_Total_HTML

`_medidas.Tip_Rem_Ano_Total_HTML` · formato `—`

**O que faz:**
Tooltip anual de remuneração da página Todos: exibe a média das séries.

**DAX:**
```dax
VAR A = SELECTEDVALUE(D_Calendario[Ano])
VAR MA = [Remuneracao_Media_Ref_AFL]
VAR MS = [Remuneracao_Media_Ref]
VAR LinhaA = "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>AFL · média</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & IF(ISBLANK(MA), "—", "R$ " & FORMAT(MA, "#,0", "pt-BR")) & "</b></div></div>"
VAR LinhaS = "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#98A2B3;margin-right:8px;'></span>Seleção atual · média</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & IF(ISBLANK(MS), "—", "R$ " & FORMAT(MS, "#,0", "pt-BR")) & "</b></div></div>"
RETURN
	IF(SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim", [Tip_Rem_Ano_HTML],
	"<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>"
	& "<div style='font-size:24px;line-height:30px;font-weight:600;'>Dezembro de " & A & "</div>"
	& "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>Remuneração de dezembro, R$ nominais</div>"
	& LinhaA & LinhaS
	& "</div>")
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 5 variável(is) (`A`, `MA`, `MS`, `LinhaA`, `LinhaS`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Remuneracao_Media_Ref`, `Remuneracao_Media_Ref_AFL`, `Tip_Rem_Ano_HTML`, `D_Calendario[Ano]`, `D_Cnae[setor_afl]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Rem Ano

---

### Tip_Rem_Esc_HTML

`_medidas.Tip_Rem_Esc_HTML` · formato `—`

**O que faz:**
Tooltip da escolaridade: média do AFL, dos Comparáveis e da seleção, e empregos do AFL.

**DAX:**
```dax
VAR E = SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada])
VAR MA = [Rem_Esc_AFL]
VAR MC = [Rem_Esc_Comp]
VAR MS = [Rem_Esc_Sel]
VAR Razao = DIVIDE(MA, MC)
VAR NA = [Empregos_Ref_AFL]
VAR PaginaAFL = SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"
VAR Leitura = IF(ISBLANK(Razao), "", "Nesta escolaridade o AFL paga " & FORMAT(Razao, "0%", "pt-BR") & " da média dos Comparáveis.")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(E, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Remuneração média de dezembro, R$ nominais", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(MA), "—", "R$ " & FORMAT(MA, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK("Empregos do AFL: " & FORMAT(NA, "#,0", "pt-BR")), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Empregos do AFL: " & FORMAT(NA, "#,0", "pt-BR"), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Comparáveis", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(MC), "—", "R$ " & FORMAT(MC, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(NOT PaginaAFL, "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#98A2B3;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Seleção atual", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(MS), "—", "R$ " & FORMAT(MS, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 8 variável(is) (`E`, `MA`, `MC`, `MS`, `Razao`, `NA`, `PaginaAFL`, `Leitura`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Empregos_Ref_AFL`, `Rem_Esc_AFL`, `Rem_Esc_Comp`, `Rem_Esc_Sel`, `D_Cnae[setor_afl]`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** `Tip_Rem_Esc_Total_HTML`

---

### Tip_Rem_Esc_Total_HTML

`_medidas.Tip_Rem_Esc_Total_HTML` · formato `—`

**O que faz:**
Tooltip em HTML. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
IF(SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim", [Tip_Rem_Esc_HTML], SUBSTITUTE([Tip_Rem_Esc_HTML], "Comparáveis", "Referência"))
```

**Como funciona:**
Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Tip_Rem_Esc_HTML`, `D_Cnae[setor_afl]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Rem Esc

---

### Tip_Rem_Gap_Raca_HTML

`_medidas.Tip_Rem_Gap_Raca_HTML` · formato `—`

**O que faz:**
Tooltip da razão negros ÷ brancos por escolaridade: razão e salários médios de cada grupo no AFL e nos Comparáveis.

**DAX:**
```dax
VAR E = SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada])
VAR RA = [Rem_Razao_Raca_AFL]
VAR RC = [Rem_Razao_Raca_Comp]
VAR RS = [Rem_Razao_Raca]
VAR AA = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Negra")
VAR AB = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Branca")
VAR CA = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Negra")
VAR CB = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Branca")
VAR PaginaAFL = SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"
VAR Leitura = IF(ISBLANK(RA) || ISBLANK(RC), "", "A diferença no AFL é " & IF(RA >= RC, "menor", "maior") & " que nos Comparáveis (" & IF(ISBLANK(RA) || ISBLANK(RC), "", IF(RA >= RC, "+", "−") & FORMAT(ABS(RA - RC) * 100, "0.0", "pt-BR") & " p.p.") & "). 100% = salários iguais.")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(E, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Salário dos negros como % do dos brancos", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(RA), "—", FORMAT(RA, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK("Negros " & IF(ISBLANK(AA), "—", "R$ " & FORMAT(AA, "#,0", "pt-BR")) & " · brancos " & IF(ISBLANK(AB), "—", "R$ " & FORMAT(AB, "#,0", "pt-BR"))), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Negros " & IF(ISBLANK(AA), "—", "R$ " & FORMAT(AA, "#,0", "pt-BR")) & " · brancos " & IF(ISBLANK(AB), "—", "R$ " & FORMAT(AB, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Comparáveis", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(RC), "—", FORMAT(RC, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK("Negros " & IF(ISBLANK(CA), "—", "R$ " & FORMAT(CA, "#,0", "pt-BR")) & " · brancos " & IF(ISBLANK(CB), "—", "R$ " & FORMAT(CB, "#,0", "pt-BR"))), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Negros " & IF(ISBLANK(CA), "—", "R$ " & FORMAT(CA, "#,0", "pt-BR")) & " · brancos " & IF(ISBLANK(CB), "—", "R$ " & FORMAT(CB, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(NOT PaginaAFL, "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#98A2B3;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Seleção atual", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(RS), "—", FORMAT(RS, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 10 variável(is) (`E`, `RA`, `RC`, `RS`, `AA`, `AB`, `CA`, `CB`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`, `D_Raca`.

**Usa:** `Rem_Razao_Raca`, `Rem_Razao_Raca_AFL`, `Rem_Razao_Raca_Comp`, `Remuneracao_Media_Ref`, `D_Cnae[setor_afl]`, `D_Escolaridade[escolaridade_agrupada]`, `D_GrupoSetor[grupo_setor]`, `D_Raca[grupo_raca]`
**É usada por:** `Tip_Rem_Gap_Raca_Total_HTML`

---

### Tip_Rem_Gap_Raca_Total_HTML

`_medidas.Tip_Rem_Gap_Raca_Total_HTML` · formato `—`

**O que faz:**
Tooltip em HTML. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
IF(SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim", [Tip_Rem_Gap_Raca_HTML], SUBSTITUTE([Tip_Rem_Gap_Raca_HTML], "Comparáveis", "Referência"))
```

**Como funciona:**
Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Tip_Rem_Gap_Raca_HTML`, `D_Cnae[setor_afl]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Rem Gap Raca

---

### Tip_Rem_Gap_Sexo_HTML

`_medidas.Tip_Rem_Gap_Sexo_HTML` · formato `—`

**O que faz:**
Tooltip da razão mulheres ÷ homens por escolaridade: razão e salários médios de cada grupo no AFL e nos Comparáveis.

**DAX:**
```dax
VAR E = SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada])
VAR RA = [Rem_Razao_Sexo_AFL]
VAR RC = [Rem_Razao_Sexo_Comp]
VAR RS = [Rem_Razao_Sexo]
VAR AA = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Sexo), D_Sexo[sexo] = "Mulher")
VAR AB = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Sexo), D_Sexo[sexo] = "Homem")
VAR CA = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Sexo), D_Sexo[sexo] = "Mulher")
VAR CB = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Sexo), D_Sexo[sexo] = "Homem")
VAR PaginaAFL = SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"
VAR Leitura = IF(ISBLANK(RA) || ISBLANK(RC), "", "A diferença no AFL é " & IF(RA >= RC, "menor", "maior") & " que nos Comparáveis (" & IF(ISBLANK(RA) || ISBLANK(RC), "", IF(RA >= RC, "+", "−") & FORMAT(ABS(RA - RC) * 100, "0.0", "pt-BR") & " p.p.") & "). 100% = salários iguais.")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(E, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Salário dos mulheres como % do dos homens", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(RA), "—", FORMAT(RA, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK("Mulheres " & IF(ISBLANK(AA), "—", "R$ " & FORMAT(AA, "#,0", "pt-BR")) & " · homens " & IF(ISBLANK(AB), "—", "R$ " & FORMAT(AB, "#,0", "pt-BR"))), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Mulheres " & IF(ISBLANK(AA), "—", "R$ " & FORMAT(AA, "#,0", "pt-BR")) & " · homens " & IF(ISBLANK(AB), "—", "R$ " & FORMAT(AB, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Comparáveis", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(RC), "—", FORMAT(RC, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & IF(ISBLANK("Mulheres " & IF(ISBLANK(CA), "—", "R$ " & FORMAT(CA, "#,0", "pt-BR")) & " · homens " & IF(ISBLANK(CB), "—", "R$ " & FORMAT(CB, "#,0", "pt-BR"))), "", "<div style='font-size:17px;color:#667085;margin-left:20px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Mulheres " & IF(ISBLANK(CA), "—", "R$ " & FORMAT(CA, "#,0", "pt-BR")) & " · homens " & IF(ISBLANK(CB), "—", "R$ " & FORMAT(CB, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>", "") & IF(NOT PaginaAFL, "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#98A2B3;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Seleção atual", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(RS), "—", FORMAT(RS, "0.0%", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 10 variável(is) (`E`, `RA`, `RC`, `RS`, `AA`, `AB`, `CA`, `CB`…) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; formata números como texto em pt-BR com `FORMAT`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`, `D_Sexo`.

**Usa:** `Rem_Razao_Sexo`, `Rem_Razao_Sexo_AFL`, `Rem_Razao_Sexo_Comp`, `Remuneracao_Media_Ref`, `D_Cnae[setor_afl]`, `D_Escolaridade[escolaridade_agrupada]`, `D_GrupoSetor[grupo_setor]`, `D_Sexo[sexo]`
**É usada por:** `Tip_Rem_Gap_Sexo_Total_HTML`

---

### Tip_Rem_Gap_Sexo_Total_HTML

`_medidas.Tip_Rem_Gap_Sexo_Total_HTML` · formato `—`

**O que faz:**
Tooltip em HTML. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
IF(SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim", [Tip_Rem_Gap_Sexo_HTML], SUBSTITUTE([Tip_Rem_Gap_Sexo_HTML], "Comparáveis", "Referência"))
```

**Como funciona:**
Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Tip_Rem_Gap_Sexo_HTML`, `D_Cnae[setor_afl]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Rem Gap Sexo

---

### Tip_Rem_UF_HTML

`_medidas.Tip_Rem_UF_HTML` · formato `—`

**O que faz:**
Tooltip da UF na remuneração: média do recorte, do AFL e dos Comparáveis.

**DAX:**
```dax
VAR UFNome = SELECTEDVALUE(D_regiao[estado], SELECTEDVALUE(D_regiao[uf]))
VAR Mun = SELECTEDVALUE(D_regiao[municipio])
VAR UF = IF(ISBLANK(Mun), UFNome, Mun & " · " & SELECTEDVALUE(D_regiao[uf]))
VAR M = [Remuneracao_Media_Ref]
VAR MA = [Remuneracao_Media_Ref_AFL]
VAR MC = [Remuneracao_Media_Ref_Comparavel]
VAR Razao = [Rem_UF_Razao_Comp]
VAR PaginaAFL = SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"
VAR Leitura = IF(ISBLANK(Razao), "", "Em " & UF & " o AFL paga " & FORMAT(Razao, "0%", "pt-BR") & " da média dos Comparáveis.")
RETURN
    "<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>" & "<div style='font-size:24px;line-height:30px;font-weight:600;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UF, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & "<div style='font-size:18px;line-height:24px;color:#667085;margin-top:2px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Remuneração média de dezembro, R$ nominais", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>" & IF(NOT PaginaAFL, "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#98A2B3;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Recorte da página", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(M), "—", "R$ " & FORMAT(M, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#D97706;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("AFL", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(MA), "—", "R$ " & FORMAT(MA, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(TRUE(), "<div style='margin-top:12px;'><div style='display:flex;justify-content:space-between;align-items:baseline;font-size:20px;'><span><span style='display:inline-block;width:12px;height:12px;border-radius:3px;background:#434446;margin-right:8px;'></span>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE("Comparáveis", "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</span><b style='font-size:22px;font-variant-numeric:tabular-nums;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(IF(ISBLANK(MC), "—", "R$ " & FORMAT(MC, "#,0", "pt-BR")), "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</b></div>" & "</div>", "") & IF(Leitura = "", "", "<div style='margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;'>" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Leitura, "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;") & "</div>") & "</div>"
```

**Como funciona:**
Monta um texto HTML para um visual de HTML (cards, títulos, tooltips). Guarda 9 variável(is) (`UFNome`, `Mun`, `UF`, `M`, `MA`, `MC`, `Razao`, `PaginaAFL`…) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; formata números como texto em pt-BR com `FORMAT`.

**Usa:** `Rem_UF_Razao_Comp`, `Remuneracao_Media_Ref`, `Remuneracao_Media_Ref_AFL`, `Remuneracao_Media_Ref_Comparavel`, `D_Cnae[setor_afl]`, `D_regiao[estado]`, `D_regiao[municipio]`, `D_regiao[uf]`
**É usada por:** `Tip_Rem_UF_Total_HTML`

---

### Tip_Rem_UF_Total_HTML

`_medidas.Tip_Rem_UF_Total_HTML` · formato `—`

**O que faz:**
Tooltip em HTML. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
IF(SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim", [Tip_Rem_UF_HTML], SUBSTITUTE([Tip_Rem_UF_HTML], "Comparáveis", "Referência"))
```

**Como funciona:**
Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Tip_Rem_UF_HTML`, `D_Cnae[setor_afl]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Tooltip · Rem UF

---

## Quanto ganha\Escolaridade

3 medidas.

### Rem_Esc_AFL

`_medidas.Rem_Esc_AFL` · formato `#,0`

**O que faz:**
Remuneração média de dezembro por escolaridade, AFL (categorias sem informação ficam BLANK).

**DAX:**
```dax
IF(SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada]) IN {"< 1 ano de estudo", "Ignorado/Faltante"}, BLANK(), [Remuneracao_Media_Ref_AFL])
```

**Como funciona:**
Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Remuneracao_Media_Ref_AFL`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** `Tip_Rem_Esc_HTML`
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

### Rem_Esc_Comp

`_medidas.Rem_Esc_Comp` · formato `#,0`

**O que faz:**
Remuneração média de dezembro por escolaridade, Comparáveis.

**DAX:**
```dax
IF(SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada]) IN {"< 1 ano de estudo", "Ignorado/Faltante"}, BLANK(), [Remuneracao_Media_Ref_Comparavel])
```

**Como funciona:**
Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Remuneracao_Media_Ref_Comparavel`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** `Tip_Rem_Esc_HTML`
**Aparece nas páginas:** Quanto ganha · AFL

---

### Rem_Esc_Sel

`_medidas.Rem_Esc_Sel` · formato `#,0`

**O que faz:**
Remuneração média de dezembro por escolaridade na seleção atual (setores/divisão filtrados).

**DAX:**
```dax
IF(SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada]) IN {"< 1 ano de estudo", "Ignorado/Faltante"}, BLANK(), [Remuneracao_Media_Ref])
```

**Como funciona:**
Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Remuneracao_Media_Ref`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** `Tip_Rem_Esc_HTML`
**Aparece nas páginas:** Quanto ganha · Todos os setores

---

## Quanto ganha\Razões

12 medidas.

### Dif_Salarial_Raca

`_medidas.Dif_Salarial_Raca` · formato `0%`

**O que faz:**
Diferença entre grupos. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
IF(NOT ISBLANK([Rem_Razao_Raca]), 1 - [Rem_Razao_Raca])
```

**Como funciona:**
Expressão direta, sem variáveis.

**Usa:** `Rem_Razao_Raca`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · Todos os setores

---

### Dif_Salarial_Raca_AFL

`_medidas.Dif_Salarial_Raca_AFL` · formato `0%`

**O que faz:**
Diferença entre grupos. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
IF(NOT ISBLANK([Rem_Razao_Raca_AFL]), 1 - [Rem_Razao_Raca_AFL])
```

**Como funciona:**
Expressão direta, sem variáveis.

**Usa:** `Rem_Razao_Raca_AFL`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

### Dif_Salarial_Raca_Comp

`_medidas.Dif_Salarial_Raca_Comp` · formato `0%`

**O que faz:**
Diferença entre grupos. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
IF(NOT ISBLANK([Rem_Razao_Raca_Comp]), 1 - [Rem_Razao_Raca_Comp])
```

**Como funciona:**
Expressão direta, sem variáveis.

**Usa:** `Rem_Razao_Raca_Comp`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL

---

### Dif_Salarial_Sexo

`_medidas.Dif_Salarial_Sexo` · formato `0%`

**O que faz:**
Diferença até a igualdade salarial (100%) por sexo e raça/cor.

**DAX:**
```dax
IF(NOT ISBLANK([Rem_Razao_Sexo]), 1 - [Rem_Razao_Sexo])
```

**Como funciona:**
Expressão direta, sem variáveis.

**Usa:** `Rem_Razao_Sexo`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · Todos os setores

---

### Dif_Salarial_Sexo_AFL

`_medidas.Dif_Salarial_Sexo_AFL` · formato `0%`

**O que faz:**
Diferença entre grupos. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
IF(NOT ISBLANK([Rem_Razao_Sexo_AFL]), 1 - [Rem_Razao_Sexo_AFL])
```

**Como funciona:**
Expressão direta, sem variáveis.

**Usa:** `Rem_Razao_Sexo_AFL`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

### Dif_Salarial_Sexo_Comp

`_medidas.Dif_Salarial_Sexo_Comp` · formato `0%`

**O que faz:**
Diferença entre grupos. *(inferido do nome; não há descrição no TMDL)*

**DAX:**
```dax
IF(NOT ISBLANK([Rem_Razao_Sexo_Comp]), 1 - [Rem_Razao_Sexo_Comp])
```

**Como funciona:**
Expressão direta, sem variáveis.

**Usa:** `Rem_Razao_Sexo_Comp`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL

---

### Rem_Razao_Raca

`_medidas.Rem_Razao_Raca` · formato `0%`

**O que faz:**
Razão da remuneração média (negros ÷ brancos) no contexto.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Fora = ISBLANK(A) || (SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada]) IN {"< 1 ano de estudo", "Ignorado/Faltante"})
VAR Num = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Negra")
VAR Den = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Branca")
RETURN IF(Fora, BLANK(), DIVIDE(Num, Den))
```

**Como funciona:**
Guarda 4 variável(is) (`A`, `Fora`, `Num`, `Den`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_Raca`.

**Usa:** `Ano_Ref`, `Remuneracao_Media_Ref`, `D_Escolaridade[escolaridade_agrupada]`, `D_Raca[grupo_raca]`
**É usada por:** `Dif_Salarial_Raca`, `KPI_RazaoRaca_AFL_HTML`, `KPI_RazaoRaca_Total_HTML`, `Rem_Razao_Raca_AFL`, `Rem_Razao_Raca_Comp`, `Tip_RazaoRaca_HTML`, `Tip_Rem_Gap_Raca_HTML`

---

### Rem_Razao_Raca_AFL

`_medidas.Rem_Razao_Raca_AFL` · formato `0%`

**O que faz:**
Razão da remuneração média (negros ÷ brancos) no contexto do AFL.

**DAX:**
```dax
CALCULATE([Rem_Razao_Raca], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Rem_Razao_Raca`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `Dif_Salarial_Raca_AFL`, `KPI_RazaoRaca_Total_HTML`, `Tip_RazaoRaca_HTML`, `Tip_Rem_Gap_Raca_HTML`, `Titulo_Rem_Gap_HTML`

---

### Rem_Razao_Raca_Comp

`_medidas.Rem_Razao_Raca_Comp` · formato `0%`

**O que faz:**
Razão da remuneração média (negros ÷ brancos) no contexto do Comp.

**DAX:**
```dax
CALCULATE([Rem_Razao_Raca], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Rem_Razao_Raca`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `Dif_Salarial_Raca_Comp`, `KPI_RazaoRaca_AFL_HTML`, `Tip_RazaoRaca_HTML`, `Tip_Rem_Gap_Raca_HTML`, `Titulo_Rem_Gap_HTML`

---

### Rem_Razao_Sexo

`_medidas.Rem_Razao_Sexo` · formato `0%`

**O que faz:**
Razão da remuneração média (mulheres ÷ homens) no contexto.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Fora = ISBLANK(A) || (SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada]) IN {"< 1 ano de estudo", "Ignorado/Faltante"})
VAR Num = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_Sexo), D_Sexo[sexo] = "Mulher")
VAR Den = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(D_Sexo), D_Sexo[sexo] = "Homem")
RETURN IF(Fora, BLANK(), DIVIDE(Num, Den))
```

**Como funciona:**
Guarda 4 variável(is) (`A`, `Fora`, `Num`, `Den`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_Sexo`.

**Usa:** `Ano_Ref`, `Remuneracao_Media_Ref`, `D_Escolaridade[escolaridade_agrupada]`, `D_Sexo[sexo]`
**É usada por:** `Dif_Salarial_Sexo`, `KPI_RazaoSexo_AFL_HTML`, `KPI_RazaoSexo_Total_HTML`, `Rem_Razao_Sexo_AFL`, `Rem_Razao_Sexo_Comp`, `Tip_RazaoSexo_HTML`, `Tip_Rem_Gap_Sexo_HTML`

---

### Rem_Razao_Sexo_AFL

`_medidas.Rem_Razao_Sexo_AFL` · formato `0%`

**O que faz:**
Razão da remuneração média (mulheres ÷ homens) no contexto do AFL.

**DAX:**
```dax
CALCULATE([Rem_Razao_Sexo], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Rem_Razao_Sexo`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `Dif_Salarial_Sexo_AFL`, `KPI_RazaoSexo_Total_HTML`, `Tip_RazaoSexo_HTML`, `Tip_Rem_Gap_Sexo_HTML`, `Titulo_Rem_Gap_HTML`

---

### Rem_Razao_Sexo_Comp

`_medidas.Rem_Razao_Sexo_Comp` · formato `0%`

**O que faz:**
Razão da remuneração média (mulheres ÷ homens) no contexto do Comp.

**DAX:**
```dax
CALCULATE([Rem_Razao_Sexo], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Rem_Razao_Sexo`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `Dif_Salarial_Sexo_Comp`, `KPI_RazaoSexo_AFL_HTML`, `Tip_RazaoSexo_HTML`, `Tip_Rem_Gap_Sexo_HTML`, `Titulo_Rem_Gap_HTML`

---

## Quanto ganha\Séries

6 medidas.

### Rem_Media_AFL_Pos

`_medidas.Rem_Media_AFL_Pos` · formato `#,0`

**O que faz:**
Remuneração média de dezembro do AFL, trecho Pos; BLANK fora do trecho.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A) && A >= 2022, CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`, `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Remuneracao_Media`, `D_Ano[ano]`, `D_GrupoSetor[grupo_setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

### Rem_Media_AFL_Pre

`_medidas.Rem_Media_AFL_Pre` · formato `#,0`

**O que faz:**
Remuneração média de dezembro do AFL, trecho Pre; BLANK fora do trecho.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A) && A < 2022, CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`, `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Remuneracao_Media`, `D_Ano[ano]`, `D_GrupoSetor[grupo_setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

### Rem_Media_Comp_Pos

`_medidas.Rem_Media_Comp_Pos` · formato `#,0`

**O que faz:**
Remuneração média de dezembro do Comparáveis, trecho Pos; BLANK fora do trecho.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A) && A >= 2022, CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`, `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Remuneracao_Media`, `D_Ano[ano]`, `D_GrupoSetor[grupo_setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL

---

### Rem_Media_Comp_Pre

`_medidas.Rem_Media_Comp_Pre` · formato `#,0`

**O que faz:**
Remuneração média de dezembro do Comparáveis, trecho Pre; BLANK fora do trecho.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A) && A < 2022, CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`, `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ano_Ref`, `Remuneracao_Media`, `D_Ano[ano]`, `D_GrupoSetor[grupo_setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL

---

### Rem_Media_Sel_Pos

`_medidas.Rem_Media_Sel_Pos` · formato `#,0`

**O que faz:**
Remuneração média de dezembro da seleção atual (setores/divisão filtrados), trecho Pos.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A) && A >= 2022, CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Remuneracao_Media`, `D_Ano[ano]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · Todos os setores

---

### Rem_Media_Sel_Pre

`_medidas.Rem_Media_Sel_Pre` · formato `#,0`

**O que faz:**
Remuneração média de dezembro da seleção atual (setores/divisão filtrados), trecho Pre.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A) && A < 2022, CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Remuneracao_Media`, `D_Ano[ano]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · Todos os setores

---

## Quanto ganha\UF

2 medidas.

### Rem_UF_Geo

`_medidas.Rem_UF_Geo` · formato `#,0`

**O que faz:**
Remuneração média de dezembro para o gráfico geográfico (UF e, ao descer, município; município só com 300 empregos ou mais).

**DAX:**
```dax
IF(ISINSCOPE(D_regiao[municipio]), IF([Empregos_Ref] >= 300, [Remuneracao_Media_Ref]), [Remuneracao_Media_Ref])
```

**Como funciona:**
Muda conforme o nível do visual (`ISINSCOPE`).

**Usa:** `Empregos_Ref`, `Remuneracao_Media_Ref`, `D_regiao[municipio]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

### Rem_UF_Razao_Comp

`_medidas.Rem_UF_Razao_Comp` · formato `0%`

**O que faz:**
Remuneração média do AFL na UF ÷ média dos Comparáveis na UF.

**DAX:**
```dax
DIVIDE([Remuneracao_Media_Ref_AFL], [Remuneracao_Media_Ref_Comparavel])
```

**Como funciona:**
Divide com `DIVIDE`, que devolve BLANK quando o divisor é zero.

**Usa:** `Remuneracao_Media_Ref_AFL`, `Remuneracao_Media_Ref_Comparavel`
**É usada por:** `Tip_Rem_UF_HTML`, `Titulo_Rem_UF_HTML`
**Aparece nas páginas:** Quanto ganha · AFL, Quanto ganha · Todos os setores

---

## Quem contrata\Apoio

4 medidas.

### Ind_Ano

`_medidas.Ind_Ano` · formato `0`

**O que faz:**
Ano de cálculo do indicador no ranking: primeiro emprego só existe até 2021 (usa o menor entre o ano e 2021); intermitente, desde 2018.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Ind = [Ind_Atual]
RETURN IF(ISBLANK(A), BLANK(), IF(Ind = "Primeiro emprego", MIN(A, 2021), IF(Ind = "Intermitente" && A < 2018, BLANK(), A)))
```

**Como funciona:**
Guarda 2 variável(is) (`A`, `Ind`) e devolve o resultado no `RETURN`.

**Usa:** `Ano_Ref`, `Ind_Atual`
**É usada por:** `Ind_Valor_Ctx`, `Ind_Valor_Div`, `Tip_Contrata_Max_AFL_HTML`, `Tip_Contrata_Max_Total_HTML`, `Tip_Contrata_Pos_HTML`, `Tip_Ind_Atividade_HTML`, `Tip_Ind_Divisao_HTML`, `Tip_Ind_UF_HTML`

---

### Ind_Atual

`_medidas.Ind_Atual` · formato `—`

**O que faz:**
Indicador escolhido nos botões (padrão: Mulheres).

**DAX:**
```dax
COALESCE(SELECTEDVALUE(D_Indicador[indicador]), "Mulheres")
```

**Como funciona:**
Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `D_Indicador[indicador]`
**É usada por:** `Ind_Ano`, `Ind_Frase`, `Ind_Rotulo`, `Ind_Valor_Ano`, `Ind_Valor_Ctx`

---

### Ind_Frase

`_medidas.Ind_Frase` · formato `—`

**O que faz:**
Frase do indicador para as manchetes.

**DAX:**
```dax
SWITCH([Ind_Atual], "Primeiro emprego", "dos empregados estavam no primeiro emprego", "Mulheres", "dos empregados são mulheres", "Até 24 anos", "dos empregados têm até 24 anos", "55 anos ou mais", "dos empregados têm 55 anos ou mais", "Superior", "dos empregados têm superior (completo ou não)", "Negros", "dos empregados que declararam cor são negros", "Intermitente", "dos empregados têm contrato intermitente", "")
```

**Como funciona:**
Escolhe o resultado com `SWITCH`.

**Usa:** `Ind_Atual`
**É usada por:** `Tip_Contrata_Max_AFL_HTML`, `Tip_Contrata_Max_Total_HTML`, `Tip_Contrata_Pos_HTML`

---

### Ind_Rotulo

`_medidas.Ind_Rotulo` · formato `—`

**O que faz:**
Nome do indicador por extenso.

**DAX:**
```dax
SWITCH([Ind_Atual], "Primeiro emprego", "primeiro emprego", "Mulheres", "mulheres", "Até 24 anos", "jovens até 24 anos", "55 anos ou mais", "empregados com 55 anos ou mais", "Superior", "superior (completo ou não)", "Negros", "negros (entre quem declarou cor)", "Intermitente", "contrato intermitente", "")
```

**Como funciona:**
Escolhe o resultado com `SWITCH`.

**Usa:** `Ind_Atual`
**É usada por:** `Tip_Contrata_Dif_HTML`, `Tip_Contrata_Max_AFL_HTML`, `Tip_Contrata_Max_Total_HTML`, `Tip_Contrata_Pos_HTML`, `Tip_Ind_Ano_HTML`, `Tip_Ind_Atividade_HTML`, `Tip_Ind_Divisao_HTML`, `Tip_Ind_UF_HTML`

---

## Quem contrata\Atividades

2 medidas.

### Ind_Atividade_Lider

`_medidas.Ind_Atividade_Lider` · formato `—`

**O que faz:**
Atividade do AFL com o maior valor do indicador.

**DAX:**
```dax
VAR T = FILTER(ADDCOLUMNS(VALUES(D_AflAtividade[nome]), "@v", [Ind_Valor_Ctx]), NOT ISBLANK([@v]))
RETURN CONCATENATEX(TOPN(1, T, [@v], DESC, D_AflAtividade[nome], ASC), D_AflAtividade[nome], "")
```

**Como funciona:**
Guarda 1 variável(is) (`T`) e devolve o resultado no `RETURN`. Pega os primeiros com `TOPN`; monta uma tabela virtual com `ADDCOLUMNS`; junta textos com `CONCATENATEX`.

**Usa:** `Ind_Valor_Ctx`, `D_AflAtividade[nome]`
**É usada por:** `Tip_Contrata_Max_AFL_HTML`

---

### Ind_Atividade_Lider_Valor

`_medidas.Ind_Atividade_Lider_Valor` · formato `0.0%`

**O que faz:**
Maior valor do indicador entre as atividades do AFL.

**DAX:**
```dax
VAR T = FILTER(ADDCOLUMNS(VALUES(D_AflAtividade[nome]), "@v", [Ind_Valor_Ctx]), NOT ISBLANK([@v]))
RETURN MAXX(T, [@v])
```

**Como funciona:**
Guarda 1 variável(is) (`T`) e devolve o resultado no `RETURN`. Pega o maior valor de uma lista com `MAXX`; monta uma tabela virtual com `ADDCOLUMNS`.

**Usa:** `Ind_Valor_Ctx`, `D_AflAtividade[nome]`
**É usada por:** `Tip_Contrata_Max_AFL_HTML`

---

## Quem contrata\Indicadores

4 medidas.

### Ind_Valor_AFL

`_medidas.Ind_Valor_AFL` · formato `0.0%`

**O que faz:**
Indicador escolhido, só do AFL.

**DAX:**
```dax
CALCULATE([Ind_Valor_Ctx], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ind_Valor_Ctx`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `Tip_Contrata_Dif_HTML`, `Tip_Contrata_Pos_HTML`, `Tip_Ind_Atividade_HTML`, `Tip_Ind_Divisao_HTML`

---

### Ind_Valor_Ano

`_medidas.Ind_Valor_Ano` · formato `0.0%`

**O que faz:**
Participação do indicador escolhido no ano do contexto (para séries; primeiro emprego só até 2021 e intermitente desde 2018).

**DAX:**
```dax
VAR Ind = [Ind_Atual]
VAR A = IF(([Ind_Atual] = "Primeiro emprego" && [Ano_Ref] > 2021) || ([Ind_Atual] = "Intermitente" && [Ano_Ref] < 2018), BLANK(), [Ano_Ref])
RETURN IF(ISBLANK(A), BLANK(), SWITCH(Ind,
    "Primeiro emprego", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[tipo_admissao] = "Primeiro Emprego")), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    "Mulheres", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Sexo[sexo] = "Mulher")), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    "Até 24 anos", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_FaixaIdade[faixa_idade] IN {"14-17", "18-24"})), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    "55 anos ou mais", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_FaixaIdade[faixa_idade] IN {"55-64", "65+"})), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    "Superior", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"})), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    "Negros", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Raca[grupo_raca] = "Negra")), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Raca[declarada] = "Sim"))),
    "Intermitente", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] = "Sim")), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    BLANK()))
```

**Como funciona:**
Guarda 2 variável(is) (`Ind`, `A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; escolhe o resultado com `SWITCH`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `Ind_Atual`, `D_Ano[ano]`, `D_Escolaridade[escolaridade_agrupada]`, `D_FaixaIdade[faixa_idade]`, `D_Raca[declarada]`, `D_Raca[grupo_raca]`, `D_Sexo[sexo]`, `F_rais[tipo_admissao]`, `F_rais[trabalho_intermitente]`
**É usada por:** `Tip_Ind_Ano_HTML`

---

### Ind_Valor_Comp

`_medidas.Ind_Valor_Comp` · formato `0.0%`

**O que faz:**
Indicador escolhido, só dos Comparáveis.

**DAX:**
```dax
CALCULATE([Ind_Valor_Ctx], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ind_Valor_Ctx`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `Tip_Contrata_Dif_HTML`

---

### Ind_Valor_Ctx

`_medidas.Ind_Valor_Ctx` · formato `0.0%`

**O que faz:**
Participação do indicador escolhido no contexto (categoria do visual, filtros e grupo), no ano do ranking.

**DAX:**
```dax
VAR Ind = [Ind_Atual]
VAR A = [Ind_Ano]
RETURN IF(ISBLANK(A), BLANK(), SWITCH(Ind,
    "Primeiro emprego", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[tipo_admissao] = "Primeiro Emprego")), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    "Mulheres", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Sexo[sexo] = "Mulher")), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    "Até 24 anos", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_FaixaIdade[faixa_idade] IN {"14-17", "18-24"})), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    "55 anos ou mais", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_FaixaIdade[faixa_idade] IN {"55-64", "65+"})), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    "Superior", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"})), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    "Negros", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Raca[grupo_raca] = "Negra")), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Raca[declarada] = "Sim"))),
    "Intermitente", DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(F_rais[trabalho_intermitente] = "Sim")), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)),
    BLANK()))
```

**Como funciona:**
Guarda 2 variável(is) (`Ind`, `A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; escolhe o resultado com `SWITCH`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Empregos`, `Ind_Ano`, `Ind_Atual`, `D_Ano[ano]`, `D_Escolaridade[escolaridade_agrupada]`, `D_FaixaIdade[faixa_idade]`, `D_Raca[declarada]`, `D_Raca[grupo_raca]`, `D_Sexo[sexo]`, `F_rais[tipo_admissao]`, `F_rais[trabalho_intermitente]`
**É usada por:** `Ind_Atividade_Lider`, `Ind_Atividade_Lider_Valor`, `Ind_UF_AFL_Dica`, `Ind_Valor_AFL`, `Ind_Valor_Comp`, `Ind_Valor_Div`, `Tip_Ind_Atividade_HTML`, `Tip_Ind_UF_HTML`

---

## Quem contrata\Perfil

25 medidas.

### Ct_Div_Emp

`_medidas.Ct_Div_Emp` · formato `#,0`

**O que faz:**
Empregos em 31/12 da divisão da categoria (ou do conjunto AFL), para o piso do ranking.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Empregos_Ref`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Ct_Esc_Valor`, `Ct_Mul_Valor`, `Ct_Neg_Valor`

---

### Ct_Esc_Div_Qtd

`_medidas.Ct_Esc_Div_Qtd` · formato `#,0`

**O que faz:**
Quantidade de empregos (empregados do nível de escolaridade escolhido) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Esc_Qtd], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Esc_Qtd], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Esc_Qtd`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Tip_Ct_Esc_HTML`

---

### Ct_Esc_Div_Rep

`_medidas.Ct_Esc_Div_Rep` · formato `0.0%`

**O que faz:**
Representatividade (empregados do nível de escolaridade escolhido) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Esc_Rep], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Esc_Rep], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Esc_Rep`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Ct_Esc_Valor`, `Tip_Ct_Esc_HTML`

---

### Ct_Esc_Div_Sal

`_medidas.Ct_Esc_Div_Sal` · formato `#,0.00`

**O que faz:**
Salário médio (empregados do nível de escolaridade escolhido) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Esc_Sal], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Esc_Sal], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Esc_Sal`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Ct_Esc_Valor`, `Tip_Ct_Esc_HTML`

---

### Ct_Esc_Div_Tot

`_medidas.Ct_Esc_Div_Tot` · formato `#,0`

**O que faz:**
Denominador (empregados do nível de escolaridade escolhido) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Esc_Tot], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Esc_Tot], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Esc_Tot`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Tip_Ct_Esc_HTML`

---

### Ct_Esc_Qtd

`_medidas.Ct_Esc_Qtd` · formato `#,0`

**O que faz:**
Empregos em 31/12 do ano de referência: empregados do nível de escolaridade escolhido, no contexto.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Niv = COALESCE(SELECTEDVALUE(D_Ct_Nivel[nivel]), "Médio completo")
RETURN IF(NOT ISBLANK(A), SWITCH(Niv, "Até fundamental", CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"})), "Médio incompleto", CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Médio Incompleto"})), "Superior", CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"})), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Médio Completo"}))))
```

**Como funciona:**
Guarda 2 variável(is) (`A`, `Niv`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; escolhe o resultado com `SWITCH`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`, `D_Ct_Nivel[nivel]`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** `Ct_Esc_Div_Qtd`, `Tip_Ct_Esc_HTML`

---

### Ct_Esc_Rep

`_medidas.Ct_Esc_Rep` · formato `0.0%`

**O que faz:**
Representatividade: participação de empregados do nível de escolaridade escolhido no total de empregos do contexto, em 31/12 do ano de referência.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Niv = COALESCE(SELECTEDVALUE(D_Ct_Nivel[nivel]), "Médio completo")
RETURN IF(NOT ISBLANK(A), DIVIDE(SWITCH(Niv, "Até fundamental", CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"})), "Médio incompleto", CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Médio Incompleto"})), "Superior", CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"})), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Médio Completo"}))), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)))
```

**Como funciona:**
Guarda 2 variável(is) (`A`, `Niv`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; escolhe o resultado com `SWITCH`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`, `D_Ct_Nivel[nivel]`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** `Ct_Esc_Div_Rep`, `Ct_Esc_Valor_AFL`, `Tip_Ct_Esc_HTML`

---

### Ct_Esc_Sal

`_medidas.Ct_Esc_Sal` · formato `#,0.00`

**O que faz:**
Salário médio de dezembro (R$ nominais) de empregados do nível de escolaridade escolhido no contexto, no ano de referência.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Niv = COALESCE(SELECTEDVALUE(D_Ct_Nivel[nivel]), "Médio completo")
RETURN IF(NOT ISBLANK(A), SWITCH(Niv, "Até fundamental", CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"})), "Médio incompleto", CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Médio Incompleto"})), "Superior", CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"})), CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Médio Completo"}))))
```

**Como funciona:**
Guarda 2 variável(is) (`A`, `Niv`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; escolhe o resultado com `SWITCH`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Remuneracao_Media`, `D_Ano[ano]`, `D_Ct_Nivel[nivel]`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** `Ct_Esc_Div_Sal`, `Ct_Esc_Valor_AFL`, `Tip_Ct_Esc_HTML`

---

### Ct_Esc_Tot

`_medidas.Ct_Esc_Tot` · formato `#,0`

**O que faz:**
Empregos em 31/12 do ano de referência que servem de denominador da participação de empregados do nível de escolaridade escolhido.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`
**É usada por:** `Ct_Esc_Div_Tot`, `Tip_Ct_Esc_HTML`

---

### Ct_Mul_Div_Qtd

`_medidas.Ct_Mul_Div_Qtd` · formato `#,0`

**O que faz:**
Quantidade de empregos (mulheres) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Mul_Qtd], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Mul_Qtd], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Mul_Qtd`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Tip_Ct_Mul_HTML`

---

### Ct_Mul_Div_Rep

`_medidas.Ct_Mul_Div_Rep` · formato `0.0%`

**O que faz:**
Representatividade (mulheres) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Mul_Rep], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Mul_Rep], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Mul_Rep`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Ct_Mul_Valor`, `Tip_Ct_Mul_HTML`

---

### Ct_Mul_Div_Sal

`_medidas.Ct_Mul_Div_Sal` · formato `#,0.00`

**O que faz:**
Salário médio (mulheres) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Mul_Sal], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Mul_Sal], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Mul_Sal`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Ct_Mul_Valor`, `Tip_Ct_Mul_HTML`

---

### Ct_Mul_Div_Tot

`_medidas.Ct_Mul_Div_Tot` · formato `#,0`

**O que faz:**
Denominador (mulheres) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Mul_Tot], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Mul_Tot], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Mul_Tot`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Tip_Ct_Mul_HTML`

---

### Ct_Mul_Qtd

`_medidas.Ct_Mul_Qtd` · formato `#,0`

**O que faz:**
Empregos em 31/12 do ano de referência: mulheres, no contexto.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Sexo[sexo] = "Mulher")))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`, `D_Sexo[sexo]`
**É usada por:** `Ct_Mul_Div_Qtd`, `Tip_Ct_Mul_HTML`

---

### Ct_Mul_Rep

`_medidas.Ct_Mul_Rep` · formato `0.0%`

**O que faz:**
Representatividade: participação de mulheres no total de empregos do contexto, em 31/12 do ano de referência.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Sexo[sexo] = "Mulher")), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`, `D_Sexo[sexo]`
**É usada por:** `Ct_Mul_Div_Rep`, `Ct_Mul_Valor_AFL`, `KPI_Ct_Mul_AFL_HTML`, `KPI_Ct_Mul_Total_HTML`, `Tip_Ct_Mul_HTML`

---

### Ct_Mul_Sal

`_medidas.Ct_Mul_Sal` · formato `#,0.00`

**O que faz:**
Salário médio de dezembro (R$ nominais) de mulheres no contexto, no ano de referência.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Sexo[sexo] = "Mulher")))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Remuneracao_Media`, `D_Ano[ano]`, `D_Sexo[sexo]`
**É usada por:** `Ct_Mul_Div_Sal`, `Ct_Mul_Valor_AFL`, `KPI_Ct_Mul_AFL_HTML`, `KPI_Ct_Mul_Total_HTML`, `Tip_Ct_Mul_HTML`

---

### Ct_Mul_Tot

`_medidas.Ct_Mul_Tot` · formato `#,0`

**O que faz:**
Empregos em 31/12 do ano de referência que servem de denominador da participação de mulheres.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`
**É usada por:** `Ct_Mul_Div_Tot`, `Tip_Ct_Mul_HTML`

---

### Ct_Neg_Div_Qtd

`_medidas.Ct_Neg_Div_Qtd` · formato `#,0`

**O que faz:**
Quantidade de empregos (negros (pretos + pardos)) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Neg_Qtd], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Neg_Qtd], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Neg_Qtd`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Tip_Ct_Neg_HTML`

---

### Ct_Neg_Div_Rep

`_medidas.Ct_Neg_Div_Rep` · formato `0.0%`

**O que faz:**
Representatividade (negros (pretos + pardos)) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Neg_Rep], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Neg_Rep], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Neg_Rep`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Ct_Neg_Valor`, `Tip_Ct_Neg_HTML`

---

### Ct_Neg_Div_Sal

`_medidas.Ct_Neg_Div_Sal` · formato `#,0.00`

**O que faz:**
Salário médio (negros (pretos + pardos)) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Neg_Sal], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Neg_Sal], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Neg_Sal`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Ct_Neg_Valor`, `Tip_Ct_Neg_HTML`

---

### Ct_Neg_Div_Tot

`_medidas.Ct_Neg_Div_Tot` · formato `#,0`

**O que faz:**
Denominador (negros (pretos + pardos)) da divisão da categoria; o item AFL usa os seis CNAEs.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
RETURN IF(ISBLANK(Nome), BLANK(),
    IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ct_Neg_Tot], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
        CALCULATE([Ct_Neg_Tot], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"))))
```

**Como funciona:**
Guarda 1 variável(is) (`Nome`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ct_Neg_Tot`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Tip_Ct_Neg_HTML`

---

### Ct_Neg_Qtd

`_medidas.Ct_Neg_Qtd` · formato `#,0`

**O que faz:**
Empregos em 31/12 do ano de referência: negros (pretos + pardos), no contexto.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Raca[grupo_raca] = "Negra")))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`, `D_Raca[grupo_raca]`
**É usada por:** `Ct_Neg_Div_Qtd`, `Tip_Ct_Neg_HTML`

---

### Ct_Neg_Rep

`_medidas.Ct_Neg_Rep` · formato `0.0%`

**O que faz:**
Representatividade: participação de negros (pretos + pardos) no total de empregos do contexto, em 31/12 do ano de referência.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), DIVIDE(CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Raca[grupo_raca] = "Negra")), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Raca[declarada] = "Sim"))))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`, `D_Raca[declarada]`, `D_Raca[grupo_raca]`
**É usada por:** `Ct_Neg_Div_Rep`, `Ct_Neg_Valor_AFL`, `KPI_Ct_Neg_AFL_HTML`, `KPI_Ct_Neg_Total_HTML`, `Tip_Ct_Neg_HTML`

---

### Ct_Neg_Sal

`_medidas.Ct_Neg_Sal` · formato `#,0.00`

**O que faz:**
Salário médio de dezembro (R$ nominais) de negros (pretos + pardos) no contexto, no ano de referência.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), CALCULATE([Remuneracao_Media], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Raca[grupo_raca] = "Negra")))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Remuneracao_Media`, `D_Ano[ano]`, `D_Raca[grupo_raca]`
**É usada por:** `Ct_Neg_Div_Sal`, `Ct_Neg_Valor_AFL`, `KPI_Ct_Neg_AFL_HTML`, `KPI_Ct_Neg_Total_HTML`, `Tip_Ct_Neg_HTML`

---

### Ct_Neg_Tot

`_medidas.Ct_Neg_Tot` · formato `#,0`

**O que faz:**
Empregos em 31/12 do ano de referência que servem de denominador da participação de negros (pretos + pardos) (só quem declarou cor).

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A, KEEPFILTERS(D_Raca[declarada] = "Sim")))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `Empregos`, `D_Ano[ano]`, `D_Raca[declarada]`
**É usada por:** `Ct_Neg_Div_Tot`, `Tip_Ct_Neg_HTML`

---

## Quem contrata\Ranking

15 medidas.

### Cor_Ind_Divisao

`_medidas.Cor_Ind_Divisao` · formato `—`

**O que faz:**
Cor do ranking: AFL em laranja, demais em cinza.

**DAX:**
```dax
IF(SELECTEDVALUE(D_Rank_Divisao[nm_divisao]) = "AFL · conjunto de 6 CNAEs", "#D97706", "#DDDDDE")
```

**Como funciona:**
Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `D_Rank_Divisao[nm_divisao]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · Todos os setores

---

### Ct_Esc_Ord

`_medidas.Ct_Esc_Ord` · formato `0.0000`

**O que faz:**
Chave de ordenação do ranking por divisão: o valor (ou o oposto nas 10 piores). O AFL fica na posição do seu valor, junto das demais divisões.

**DAX:**
```dax
VAR V = [Ct_Esc_Valor]
VAR Piores = COALESCE(SELECTEDVALUE(D_Ct_Modo[modo]), "10 melhores setores") = "10 piores setores"
RETURN IF(ISBLANK(V), BLANK(), IF(Piores, -V, V))
```

**Como funciona:**
Guarda 2 variável(is) (`V`, `Piores`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Ct_Esc_Valor`, `D_Ct_Modo[modo]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · Todos os setores

---

### Ct_Esc_Valor

`_medidas.Ct_Esc_Valor` · formato `dinâmico`

**O que faz:**
Valor do ranking por divisão (empregados do nível de escolaridade escolhido): representatividade OU salário médio, conforme o botão do gráfico. Mostra as 10 melhores (ou 10 piores) divisões do setor escolhido, com piso de 50.000 empregos, e sempre o AFL (fora do cálculo).

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
VAR EhAFL = Nome = "AFL · conjunto de 6 CNAEs"
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetEsc[metrica]), "Representatividade") = "Salário médio"
VAR Piores = COALESCE(SELECTEDVALUE(D_Ct_Modo[modo]), "10 melhores setores") = "10 piores setores"
VAR Setores = VALUES(D_Ct_Setor[setor])
VAR NoSetor = CONTAINS(Setores, D_Ct_Setor[setor], SELECTEDVALUE(D_Rank_Divisao[setor_principal]))
VAR Meu = IF(NOT ISBLANK(Nome) && (EhAFL || NoSetor), IF(Sal, [Ct_Esc_Div_Sal], [Ct_Esc_Div_Rep]))
VAR Tab = FILTER(FILTER(ALL(D_Rank_Divisao[nm_divisao], D_Rank_Divisao[setor_principal]), D_Rank_Divisao[nm_divisao] <> "AFL · conjunto de 6 CNAEs" && D_Rank_Divisao[setor_principal] IN Setores), [Ct_Div_Emp] >= 50000)
VAR Pos = IF(NOT(EhAFL) && NoSetor && NOT ISBLANK(Meu) && [Ct_Div_Emp] >= 50000,
    IF(Piores, RANKX(Tab, IF(Sal, [Ct_Esc_Div_Sal], [Ct_Esc_Div_Rep]), , ASC, DENSE),
        RANKX(Tab, IF(Sal, [Ct_Esc_Div_Sal], [Ct_Esc_Div_Rep]), , DESC, DENSE)))
RETURN IF(EhAFL, Meu, IF(NOT ISBLANK(Pos) && Pos <= 10, Meu))
```

**Como funciona:**
Guarda 9 variável(is) (`Nome`, `EhAFL`, `Sal`, `Piores`, `Setores`, `NoSetor`, `Meu`, `Tab`…) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; calcula posição com `RANKX`.

**Usa:** `Ct_Div_Emp`, `Ct_Esc_Div_Rep`, `Ct_Esc_Div_Sal`, `D_Ct_MetEsc[metrica]`, `D_Ct_Modo[modo]`, `D_Ct_Setor[setor]`, `D_Rank_Divisao[nm_divisao]`, `D_Rank_Divisao[setor_principal]`
**É usada por:** `Ct_Esc_Ord`
**Aparece nas páginas:** Ranking · Todos os setores

---

### Ct_Esc_Valor_AFL

`_medidas.Ct_Esc_Valor_AFL` · formato `dinâmico`

**O que faz:**
Valor do ranking por CNAE do AFL (empregados do nível de escolaridade escolhido): representatividade OU salário médio, conforme o botão do gráfico.

**DAX:**
```dax
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetEsc[metrica]), "Representatividade") = "Salário médio"
RETURN IF(Sal, [Ct_Esc_Sal], [Ct_Esc_Rep])
```

**Como funciona:**
Guarda 1 variável(is) (`Sal`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Ct_Esc_Rep`, `Ct_Esc_Sal`, `D_Ct_MetEsc[metrica]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · AFL

---

### Ct_Mul_Ord

`_medidas.Ct_Mul_Ord` · formato `0.0000`

**O que faz:**
Chave de ordenação do ranking por divisão: o valor (ou o oposto nas 10 piores). O AFL fica na posição do seu valor, junto das demais divisões.

**DAX:**
```dax
VAR V = [Ct_Mul_Valor]
VAR Piores = COALESCE(SELECTEDVALUE(D_Ct_Modo[modo]), "10 melhores setores") = "10 piores setores"
RETURN IF(ISBLANK(V), BLANK(), IF(Piores, -V, V))
```

**Como funciona:**
Guarda 2 variável(is) (`V`, `Piores`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Ct_Mul_Valor`, `D_Ct_Modo[modo]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · Todos os setores

---

### Ct_Mul_Valor

`_medidas.Ct_Mul_Valor` · formato `dinâmico`

**O que faz:**
Valor do ranking por divisão (mulheres): representatividade OU salário médio, conforme o botão do gráfico. Mostra as 10 melhores (ou 10 piores) divisões do setor escolhido, com piso de 50.000 empregos, e sempre o AFL (fora do cálculo).

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
VAR EhAFL = Nome = "AFL · conjunto de 6 CNAEs"
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetMul[metrica]), "Representatividade") = "Salário médio"
VAR Piores = COALESCE(SELECTEDVALUE(D_Ct_Modo[modo]), "10 melhores setores") = "10 piores setores"
VAR Setores = VALUES(D_Ct_Setor[setor])
VAR NoSetor = CONTAINS(Setores, D_Ct_Setor[setor], SELECTEDVALUE(D_Rank_Divisao[setor_principal]))
VAR Meu = IF(NOT ISBLANK(Nome) && (EhAFL || NoSetor), IF(Sal, [Ct_Mul_Div_Sal], [Ct_Mul_Div_Rep]))
VAR Tab = FILTER(FILTER(ALL(D_Rank_Divisao[nm_divisao], D_Rank_Divisao[setor_principal]), D_Rank_Divisao[nm_divisao] <> "AFL · conjunto de 6 CNAEs" && D_Rank_Divisao[setor_principal] IN Setores), [Ct_Div_Emp] >= 50000)
VAR Pos = IF(NOT(EhAFL) && NoSetor && NOT ISBLANK(Meu) && [Ct_Div_Emp] >= 50000,
    IF(Piores, RANKX(Tab, IF(Sal, [Ct_Mul_Div_Sal], [Ct_Mul_Div_Rep]), , ASC, DENSE),
        RANKX(Tab, IF(Sal, [Ct_Mul_Div_Sal], [Ct_Mul_Div_Rep]), , DESC, DENSE)))
RETURN IF(EhAFL, Meu, IF(NOT ISBLANK(Pos) && Pos <= 10, Meu))
```

**Como funciona:**
Guarda 9 variável(is) (`Nome`, `EhAFL`, `Sal`, `Piores`, `Setores`, `NoSetor`, `Meu`, `Tab`…) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; calcula posição com `RANKX`.

**Usa:** `Ct_Div_Emp`, `Ct_Mul_Div_Rep`, `Ct_Mul_Div_Sal`, `D_Ct_MetMul[metrica]`, `D_Ct_Modo[modo]`, `D_Ct_Setor[setor]`, `D_Rank_Divisao[nm_divisao]`, `D_Rank_Divisao[setor_principal]`
**É usada por:** `Ct_Mul_Ord`
**Aparece nas páginas:** Ranking · Todos os setores

---

### Ct_Mul_Valor_AFL

`_medidas.Ct_Mul_Valor_AFL` · formato `dinâmico`

**O que faz:**
Valor do ranking por CNAE do AFL (mulheres): representatividade OU salário médio, conforme o botão do gráfico.

**DAX:**
```dax
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetMul[metrica]), "Representatividade") = "Salário médio"
RETURN IF(Sal, [Ct_Mul_Sal], [Ct_Mul_Rep])
```

**Como funciona:**
Guarda 1 variável(is) (`Sal`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Ct_Mul_Rep`, `Ct_Mul_Sal`, `D_Ct_MetMul[metrica]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · AFL

---

### Ct_Neg_Ord

`_medidas.Ct_Neg_Ord` · formato `0.0000`

**O que faz:**
Chave de ordenação do ranking por divisão: o valor (ou o oposto nas 10 piores). O AFL fica na posição do seu valor, junto das demais divisões.

**DAX:**
```dax
VAR V = [Ct_Neg_Valor]
VAR Piores = COALESCE(SELECTEDVALUE(D_Ct_Modo[modo]), "10 melhores setores") = "10 piores setores"
RETURN IF(ISBLANK(V), BLANK(), IF(Piores, -V, V))
```

**Como funciona:**
Guarda 2 variável(is) (`V`, `Piores`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Ct_Neg_Valor`, `D_Ct_Modo[modo]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · Todos os setores

---

### Ct_Neg_Valor

`_medidas.Ct_Neg_Valor` · formato `dinâmico`

**O que faz:**
Valor do ranking por divisão (negros (pretos + pardos)): representatividade OU salário médio, conforme o botão do gráfico. Mostra as 10 melhores (ou 10 piores) divisões do setor escolhido, com piso de 50.000 empregos, e sempre o AFL (fora do cálculo).

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
VAR EhAFL = Nome = "AFL · conjunto de 6 CNAEs"
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetNeg[metrica]), "Representatividade") = "Salário médio"
VAR Piores = COALESCE(SELECTEDVALUE(D_Ct_Modo[modo]), "10 melhores setores") = "10 piores setores"
VAR Setores = VALUES(D_Ct_Setor[setor])
VAR NoSetor = CONTAINS(Setores, D_Ct_Setor[setor], SELECTEDVALUE(D_Rank_Divisao[setor_principal]))
VAR Meu = IF(NOT ISBLANK(Nome) && (EhAFL || NoSetor), IF(Sal, [Ct_Neg_Div_Sal], [Ct_Neg_Div_Rep]))
VAR Tab = FILTER(FILTER(ALL(D_Rank_Divisao[nm_divisao], D_Rank_Divisao[setor_principal]), D_Rank_Divisao[nm_divisao] <> "AFL · conjunto de 6 CNAEs" && D_Rank_Divisao[setor_principal] IN Setores), [Ct_Div_Emp] >= 50000)
VAR Pos = IF(NOT(EhAFL) && NoSetor && NOT ISBLANK(Meu) && [Ct_Div_Emp] >= 50000,
    IF(Piores, RANKX(Tab, IF(Sal, [Ct_Neg_Div_Sal], [Ct_Neg_Div_Rep]), , ASC, DENSE),
        RANKX(Tab, IF(Sal, [Ct_Neg_Div_Sal], [Ct_Neg_Div_Rep]), , DESC, DENSE)))
RETURN IF(EhAFL, Meu, IF(NOT ISBLANK(Pos) && Pos <= 10, Meu))
```

**Como funciona:**
Guarda 9 variável(is) (`Nome`, `EhAFL`, `Sal`, `Piores`, `Setores`, `NoSetor`, `Meu`, `Tab`…) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`; calcula posição com `RANKX`.

**Usa:** `Ct_Div_Emp`, `Ct_Neg_Div_Rep`, `Ct_Neg_Div_Sal`, `D_Ct_MetNeg[metrica]`, `D_Ct_Modo[modo]`, `D_Ct_Setor[setor]`, `D_Rank_Divisao[nm_divisao]`, `D_Rank_Divisao[setor_principal]`
**É usada por:** `Ct_Neg_Ord`
**Aparece nas páginas:** Ranking · Todos os setores

---

### Ct_Neg_Valor_AFL

`_medidas.Ct_Neg_Valor_AFL` · formato `dinâmico`

**O que faz:**
Valor do ranking por CNAE do AFL (negros (pretos + pardos)): representatividade OU salário médio, conforme o botão do gráfico.

**DAX:**
```dax
VAR Sal = COALESCE(SELECTEDVALUE(D_Ct_MetNeg[metrica]), "Representatividade") = "Salário médio"
RETURN IF(Sal, [Ct_Neg_Sal], [Ct_Neg_Rep])
```

**Como funciona:**
Guarda 1 variável(is) (`Sal`) e devolve o resultado no `RETURN`. Lê a escolha do usuário com `SELECTEDVALUE`.

**Usa:** `Ct_Neg_Rep`, `Ct_Neg_Sal`, `D_Ct_MetNeg[metrica]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Ranking · AFL

---

### Ind_Maior_Divisao

`_medidas.Ind_Maior_Divisao` · formato `—`

**O que faz:**
Nome da divisão com o maior valor do indicador.

**DAX:**
```dax
VAR T = FILTER(ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), "@v", [Ind_Valor_Div]), NOT ISBLANK([@v]) && [nm_divisao] <> "AFL · conjunto de 6 CNAEs")
RETURN CONCATENATEX(TOPN(1, T, [@v], DESC, [nm_divisao], ASC), [nm_divisao], "")
```

**Como funciona:**
Guarda 1 variável(is) (`T`) e devolve o resultado no `RETURN`. Pega os primeiros com `TOPN`; monta uma tabela virtual com `ADDCOLUMNS`; junta textos com `CONCATENATEX`.

**Usa:** `Ind_Valor_Div`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Tip_Contrata_Max_Total_HTML`

---

### Ind_Maior_Valor

`_medidas.Ind_Maior_Valor` · formato `0.0%`

**O que faz:**
Maior valor do indicador entre as divisões.

**DAX:**
```dax
VAR T = FILTER(ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), "@v", [Ind_Valor_Div]), NOT ISBLANK([@v]) && [nm_divisao] <> "AFL · conjunto de 6 CNAEs")
RETURN MAXX(T, [@v])
```

**Como funciona:**
Guarda 1 variável(is) (`T`) e devolve o resultado no `RETURN`. Pega o maior valor de uma lista com `MAXX`; monta uma tabela virtual com `ADDCOLUMNS`.

**Usa:** `Ind_Valor_Div`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Tip_Contrata_Max_Total_HTML`

---

### Ind_Posicao_AFL

`_medidas.Ind_Posicao_AFL` · formato `0`

**O que faz:**
Posição do AFL entre todas as divisões no indicador escolhido.

**DAX:**
```dax
VAR T = FILTER(ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), "@v", [Ind_Valor_Div]), NOT ISBLANK([@v]))
VAR VA = MAXX(FILTER(T, [nm_divisao] = "AFL · conjunto de 6 CNAEs"), [@v])
RETURN IF(NOT ISBLANK(VA), COUNTROWS(FILTER(T, [@v] > VA)) + 1)
```

**Como funciona:**
Guarda 2 variável(is) (`T`, `VA`) e devolve o resultado no `RETURN`. Pega o maior valor de uma lista com `MAXX`; monta uma tabela virtual com `ADDCOLUMNS`.

**Usa:** `Ind_Valor_Div`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Tip_Contrata_Pos_HTML`

---

### Ind_Total_Divisoes

`_medidas.Ind_Total_Divisoes` · formato `0`

**O que faz:**
Quantidade de divisões com o indicador calculável.

**DAX:**
```dax
COUNTROWS(FILTER(ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), "@v", [Ind_Valor_Div]), NOT ISBLANK([@v])))
```

**Como funciona:**
Monta uma tabela virtual com `ADDCOLUMNS`.

**Usa:** `Ind_Valor_Div`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Tip_Contrata_Pos_HTML`, `Tip_Ind_Divisao_HTML`

---

### Ind_Valor_Div

`_medidas.Ind_Valor_Div` · formato `0.0%`

**O que faz:**
Indicador escolhido por divisão (item AFL = seis CNAEs); só divisões com 50.000 empregos ou mais.

**DAX:**
```dax
VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])
VAR A = [Ind_Ano]
VAR Den = IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL", REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A),
    CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não"), REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A))
VAR Val = IF(Nome = "AFL · conjunto de 6 CNAEs", CALCULATE([Ind_Valor_Ctx], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"),
    CALCULATE([Ind_Valor_Ctx], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = "Não")))
RETURN IF(ISBLANK(Nome) || ISBLANK(A) || Den < 50000, BLANK(), Val)
```

**Como funciona:**
Guarda 4 variável(is) (`Nome`, `A`, `Den`, `Val`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`. Filtros limpos: `D_Ano`, `D_Calendario`, `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Empregos`, `Ind_Ano`, `Ind_Valor_Ctx`, `D_Ano[ano]`, `D_Cnae[divisao_afl]`, `D_Cnae[setor_afl]`, `D_GrupoSetor[grupo_setor]`, `D_Rank_Divisao[nm_divisao]`
**É usada por:** `Ind_Maior_Divisao`, `Ind_Maior_Valor`, `Ind_Posicao_AFL`, `Ind_Total_Divisoes`, `Tip_Ind_Divisao_HTML`

---

## Quem contrata\UF

1 medidas.

### Ind_UF_AFL_Dica

`_medidas.Ind_UF_AFL_Dica` · formato `0.0%`

**O que faz:**
Indicador escolhido no AFL da UF (para o tooltip do ranking de UFs do mercado).

**DAX:**
```dax
CALCULATE([Ind_Valor_Ctx], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Ind_Valor_Ctx`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `Tip_Ind_UF_HTML`

---

## Quem trabalha\AFL

3 medidas.

### Perf_Ate24_AFL

`_medidas.Perf_Ate24_AFL` · formato `0.0%`

**O que faz:**
Perf_Ate24 só do AFL.

**DAX:**
```dax
CALCULATE([Perf_Ate24], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Perf_Ate24`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `KPI_Jovens_Total_HTML`

---

### Perf_MedioMais_AFL

`_medidas.Perf_MedioMais_AFL` · formato `0.0%`

**O que faz:**
Perf_MedioMais só do AFL.

**DAX:**
```dax
CALCULATE([Perf_MedioMais], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Perf_MedioMais`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `KPI_Escol_Total_HTML`

---

### Perf_Mulheres_AFL

`_medidas.Perf_Mulheres_AFL` · formato `0.0%`

**O que faz:**
Perf_Mulheres só do AFL.

**DAX:**
```dax
CALCULATE([Perf_Mulheres], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Perf_Mulheres`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `KPI_Mulheres_Total_HTML`, `Manchete_Perfil_Total_HTML`

---

## Quem trabalha\Comparável

3 medidas.

### Perf_Ate24_Comp

`_medidas.Perf_Ate24_Comp` · formato `0.0%`

**O que faz:**
Perf_Ate24 só dos Comparáveis.

**DAX:**
```dax
CALCULATE([Perf_Ate24], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Perf_Ate24`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `KPI_Jovens_AFL_HTML`, `KPI_Jovens_Total_HTML`

---

### Perf_MedioMais_Comp

`_medidas.Perf_MedioMais_Comp` · formato `0.0%`

**O que faz:**
Perf_MedioMais só dos Comparáveis.

**DAX:**
```dax
CALCULATE([Perf_MedioMais], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Perf_MedioMais`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `KPI_Escol_AFL_HTML`, `KPI_Escol_Total_HTML`

---

### Perf_Mulheres_Comp

`_medidas.Perf_Mulheres_Comp` · formato `0.0%`

**O que faz:**
Perf_Mulheres só dos Comparáveis.

**DAX:**
```dax
CALCULATE([Perf_Mulheres], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Perf_Mulheres`, `D_GrupoSetor[grupo_setor]`
**É usada por:** `KPI_Mulheres_AFL_HTML`, `KPI_Mulheres_Total_HTML`, `Manchete_Perfil_AFL_HTML`

---

## Quem trabalha\Ocupações

1 medidas.

### Emp_CBO_Top

`_medidas.Emp_CBO_Top` · formato `#,0`

**O que faz:**
Empregos por ocupação (CBO); as 300 maiores (o gráfico mostra as primeiras e rola; o modo foco amplia).

**DAX:**
```dax
VAR V = [Empregos_Ref]
VAR R = IF(NOT ISBLANK(V), RANKX(ALLSELECTED(F_rais[cbo_2002]), [Empregos_Ref], , DESC, DENSE))
RETURN IF(NOT ISBLANK(V) && R <= 300, V)
```

**Como funciona:**
Guarda 2 variável(is) (`V`, `R`) e devolve o resultado no `RETURN`. Respeita só a seleção da página com `ALLSELECTED`; calcula posição com `RANKX`.

**Usa:** `Empregos_Ref`, `F_rais[cbo_2002]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL, Quem trabalha · Todos os setores

---

## Quem trabalha\Perfil

8 medidas.

### Perf_Ate24

`_medidas.Perf_Ate24` · formato `0.0%`

**O que faz:**
Participação (Ate24) nos empregos de 31/12 do ano de referência, no contexto da página.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Num = CALCULATE([Empregos_Ref], KEEPFILTERS(D_FaixaIdade[faixa_idade] IN {"14-17", "18-24"}))
VAR Den = [Empregos_Ref]
RETURN IF(ISBLANK(A) || NOT(TRUE()), BLANK(), DIVIDE(Num, Den))
```

**Como funciona:**
Guarda 3 variável(is) (`A`, `Num`, `Den`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `D_FaixaIdade[faixa_idade]`
**É usada por:** `KPI_Jovens_AFL_HTML`, `KPI_Jovens_Total_HTML`, `Perf_Ate24_AFL`, `Perf_Ate24_Comp`

---

### Perf_Idade

`_medidas.Perf_Idade` · formato `0.0`

**O que faz:**
Idade média dos empregados em 31/12 do ano de referência.

**DAX:**
```dax
VAR A = [Ano_Ref]
RETURN IF(NOT ISBLANK(A), DIVIDE(CALCULATE(SUM(F_rais[soma_idade]), REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A), CALCULATE(SUM(F_rais[qtd_idade]), REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A)))
```

**Como funciona:**
Guarda 1 variável(is) (`A`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Ref`, `D_Ano[ano]`, `F_rais[qtd_idade]`, `F_rais[soma_idade]`
**É usada por:** `KPI_Jovens_AFL_HTML`, `KPI_Jovens_Total_HTML`, `Manchete_Perfil_AFL_HTML`, `Manchete_Perfil_Total_HTML`

---

### Perf_Idade_Inicio

`_medidas.Perf_Idade_Inicio` · formato `0.0`

**O que faz:**
Idade média no primeiro ano do trecho comparável.

**DAX:**
```dax
VAR I = [Ano_Inicio_Trecho]
RETURN IF(NOT ISBLANK(I), DIVIDE(CALCULATE(SUM(F_rais[soma_idade]), REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = I), CALCULATE(SUM(F_rais[qtd_idade]), REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = I)))
```

**Como funciona:**
Guarda 1 variável(is) (`I`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_Ano`, `D_Calendario`.

**Usa:** `Ano_Inicio_Trecho`, `D_Ano[ano]`, `F_rais[qtd_idade]`, `F_rais[soma_idade]`
**É usada por:** `KPI_Jovens_AFL_HTML`, `KPI_Jovens_Total_HTML`

---

### Perf_Intermitente

`_medidas.Perf_Intermitente` · formato `0.0%`

**O que faz:**
Participação (Intermitente) nos empregos de 31/12 do ano de referência, no contexto da página.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Num = CALCULATE([Empregos_Ref], KEEPFILTERS(F_rais[trabalho_intermitente] = "Sim"))
VAR Den = [Empregos_Ref]
RETURN IF(ISBLANK(A) || NOT(A >= 2018), BLANK(), DIVIDE(Num, Den))
```

**Como funciona:**
Guarda 3 variável(is) (`A`, `Num`, `Den`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `F_rais[trabalho_intermitente]`
**É usada por:** `Titulo_Raca_HTML`

---

### Perf_MedioMais

`_medidas.Perf_MedioMais` · formato `0.0%`

**O que faz:**
Participação (MedioMais) nos empregos de 31/12 do ano de referência, no contexto da página.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Num = CALCULATE([Empregos_Ref], KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Médio Completo", "Superior Incompleto", "Superior Completo"}))
VAR Den = [Empregos_Ref]
RETURN IF(ISBLANK(A) || NOT(TRUE()), BLANK(), DIVIDE(Num, Den))
```

**Como funciona:**
Guarda 3 variável(is) (`A`, `Num`, `Den`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** `KPI_Escol_AFL_HTML`, `KPI_Escol_Total_HTML`, `Perf_MedioMais_AFL`, `Perf_MedioMais_Comp`

---

### Perf_Mulheres

`_medidas.Perf_Mulheres` · formato `0.0%`

**O que faz:**
Participação (Mulheres) nos empregos de 31/12 do ano de referência, no contexto da página.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Num = CALCULATE([Empregos_Ref], KEEPFILTERS(D_Sexo[sexo] = "Mulher"))
VAR Den = [Empregos_Ref]
RETURN IF(ISBLANK(A) || NOT(TRUE()), BLANK(), DIVIDE(Num, Den))
```

**Como funciona:**
Guarda 3 variável(is) (`A`, `Num`, `Den`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `D_Sexo[sexo]`
**É usada por:** `KPI_Mulheres_AFL_HTML`, `KPI_Mulheres_Total_HTML`, `Manchete_Perfil_AFL_HTML`, `Manchete_Perfil_Total_HTML`, `Perf_Mulheres_AFL`, `Perf_Mulheres_Comp`, `Tip_CBO_HTML`, `Titulo_CBO_HTML`
**Aparece nas páginas:** Quem trabalha · AFL, Quem trabalha · Todos os setores

---

### Perf_Primeiro

`_medidas.Perf_Primeiro` · formato `0.0%`

**O que faz:**
Participação (Primeiro) nos empregos de 31/12 do ano de referência, no contexto da página.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Num = CALCULATE([Empregos_Ref], KEEPFILTERS(F_rais[tipo_admissao] = "Primeiro Emprego"))
VAR Den = [Empregos_Ref]
RETURN IF(ISBLANK(A) || NOT(A <= 2021), BLANK(), DIVIDE(Num, Den))
```

**Como funciona:**
Guarda 3 variável(is) (`A`, `Num`, `Den`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `F_rais[tipo_admissao]`
**É usada por:** `KPI_Primeiro_Emprego_HTML`, `Titulo_Raca_HTML`

---

### Perf_Superior

`_medidas.Perf_Superior` · formato `0.0%`

**O que faz:**
Participação (Superior) nos empregos de 31/12 do ano de referência, no contexto da página.

**DAX:**
```dax
VAR A = [Ano_Ref]
VAR Num = CALCULATE([Empregos_Ref], KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"}))
VAR Den = [Empregos_Ref]
RETURN IF(ISBLANK(A) || NOT(TRUE()), BLANK(), DIVIDE(Num, Den))
```

**Como funciona:**
Guarda 3 variável(is) (`A`, `Num`, `Den`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero.

**Usa:** `Ano_Ref`, `Empregos_Ref`, `D_Escolaridade[escolaridade_agrupada]`
**É usada por:** `KPI_Escol_AFL_HTML`, `KPI_Escol_Total_HTML`

---

## Quem trabalha\Pirâmide

4 medidas.

### Pir_Homens

`_medidas.Pir_Homens` · formato `0.0%;0.0%;0.0%`

**O que faz:**
Pirâmide etária: % de homens em cada faixa sobre o total de empregos do contexto (mulheres com sinal negativo).

**DAX:**
```dax
VAR F = SELECTEDVALUE(D_FaixaIdade[faixa_idade])
RETURN IF(ISBLANK(F) || F = "Não categorizado", BLANK(), DIVIDE(CALCULATE([Empregos_Ref], KEEPFILTERS(D_Sexo[sexo] = "Homem")), CALCULATE([Empregos_Ref], REMOVEFILTERS(D_FaixaIdade))))
```

**Como funciona:**
Guarda 1 variável(is) (`F`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_FaixaIdade`.

**Usa:** `Empregos_Ref`, `D_FaixaIdade[faixa_idade]`, `D_Sexo[sexo]`
**É usada por:** `Pir_Homens_Comp`, `Titulo_Pir_HTML`
**Aparece nas páginas:** Quem trabalha · AFL, Quem trabalha · Todos os setores

---

### Pir_Homens_Comp

`_medidas.Pir_Homens_Comp` · formato `0.0%;0.0%;0.0%`

**O que faz:**
Pir_Homens dos Comparáveis (referência no tooltip).

**DAX:**
```dax
CALCULATE([Pir_Homens], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Pir_Homens`, `D_GrupoSetor[grupo_setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL, Quem trabalha · Todos os setores

---

### Pir_Mulheres

`_medidas.Pir_Mulheres` · formato `0.0%;0.0%;0.0%`

**O que faz:**
Pirâmide etária: % de mulheres em cada faixa sobre o total de empregos do contexto (mulheres com sinal negativo).

**DAX:**
```dax
VAR F = SELECTEDVALUE(D_FaixaIdade[faixa_idade])
RETURN IF(ISBLANK(F) || F = "Não categorizado", BLANK(), -DIVIDE(CALCULATE([Empregos_Ref], KEEPFILTERS(D_Sexo[sexo] = "Mulher")), CALCULATE([Empregos_Ref], REMOVEFILTERS(D_FaixaIdade))))
```

**Como funciona:**
Guarda 1 variável(is) (`F`) e devolve o resultado no `RETURN`. Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`; lê a escolha do usuário com `SELECTEDVALUE`; divide com `DIVIDE`, que devolve BLANK quando o divisor é zero. Filtros limpos: `D_FaixaIdade`.

**Usa:** `Empregos_Ref`, `D_FaixaIdade[faixa_idade]`, `D_Sexo[sexo]`
**É usada por:** `Pir_Mulheres_Comp`, `Titulo_Pir_HTML`
**Aparece nas páginas:** Quem trabalha · AFL, Quem trabalha · Todos os setores

---

### Pir_Mulheres_Comp

`_medidas.Pir_Mulheres_Comp` · formato `0.0%;0.0%;0.0%`

**O que faz:**
Pir_Mulheres dos Comparáveis (referência no tooltip).

**DAX:**
```dax
CALCULATE([Pir_Mulheres], REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável")
```

**Como funciona:**
Usa `CALCULATE` para trocar o filtro antes de calcular; limpa filtros com `REMOVEFILTERS`. Filtros limpos: `D_Cnae`, `D_GrupoSetor`.

**Usa:** `Pir_Mulheres`, `D_GrupoSetor[grupo_setor]`
**É usada por:** nenhuma medida (medida-raiz)
**Aparece nas páginas:** Quem trabalha · AFL, Quem trabalha · Todos os setores

---


---

*XPERIUN · `/pbi-doc`*
