# RAIS Emprego Formal — Dependências

Grafo de dependências entre medidas. Útil pra entender o impacto de mudanças e priorizar refator.

> **Voltar pra:** [03 · Relacionamentos](03-relacionamentos.md)

---

## Árvores por medida-raiz

Medidas-raiz são as que não são usadas por nenhuma outra. Mostram a árvore descendente até chegar nas colunas-folha.

### Manchete_Emp_Total_HTML
```
Manchete_Emp_Total_HTML
├─ Ano_Ref
│  └─ F_rais[ano]
├─ Contexto_Emp_Total
│  ├─ Ano_Ref (já mapeada acima)
│  ├─ Setor_Emp_Total
│  │  ├─ D_Cnae[divisao_afl]
│  │  └─ D_Comparavel[comparavel_AFL_rotulo]
│  ├─ D_Escolaridade[escolaridade_agrupada]
│  ├─ D_Raca[raca_cor]
│  ├─ D_Sexo[sexo]
│  ├─ D_regiao[estado]
│  └─ D_regiao[uf]
├─ Emp_Posicao_AFL_Divisao
│  ├─ Emp_Divisao
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Empregos_Ref (…)
│  │  ├─ Empregos_Ref_AFL (…)
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Emp_Sequencia_Altas_AFL
│  ├─ Ano_Inicio_Trecho
│  │  └─ Ano_Ref (já mapeada acima)
│  ├─ Ano_Ref (já mapeada acima)
│  ├─ Empregos
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_Rank_Divisao[nm_divisao]
│  │  ├─ D_Rank_Divisao[setor_principal]
│  │  └─ F_rais[vinculos]
│  ├─ D_Ano[ano]
│  └─ D_GrupoSetor[grupo_setor]
├─ Emp_Total_Divisoes
│  ├─ Emp_Divisao (já mapeada acima)
│  └─ D_Rank_Divisao[nm_divisao]
├─ Empregos_Ref
│  ├─ Ano_Ref (já mapeada acima)
│  ├─ Empregos (já mapeada acima)
│  └─ D_Ano[ano]
├─ Empregos_Var
│  ├─ Empregos_Ano_Anterior
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Comparavel_Ano_Anterior (…)
│  │  ├─ Empregos (já mapeada acima)
│  │  └─ D_Ano[ano]
│  └─ Empregos_Ref (já mapeada acima)
├─ Empregos_Var_Pct
│  ├─ Empregos_Ano_Anterior (já mapeada acima)
│  └─ Empregos_Var (já mapeada acima)
├─ Setor_Emp_Total (já mapeada acima)
├─ D_regiao[estado]
└─ D_regiao[uf]
```

### Tip_Emp_Ano_PorPagina_HTML
```
Tip_Emp_Ano_PorPagina_HTML
├─ Tip_Emp_Ano_HTML
│  ├─ Empregos_Ref
│  │  ├─ Ano_Ref
│  │  │  └─ F_rais[ano]
│  │  ├─ Empregos
│  │  │  ├─ D_Cnae[divisao_afl]
│  │  │  ├─ D_Cnae[setor_afl]
│  │  │  ├─ D_Rank_Divisao[nm_divisao]
│  │  │  ├─ D_Rank_Divisao[setor_principal]
│  │  │  └─ F_rais[vinculos]
│  │  └─ D_Ano[ano]
│  ├─ Empregos_Ref_AFL
│  │  ├─ Empregos_Ref (já mapeada acima)
│  │  └─ D_GrupoSetor[grupo_setor]
│  ├─ Empregos_Ref_Comparavel
│  │  ├─ Empregos_Ref (já mapeada acima)
│  │  └─ D_GrupoSetor[grupo_setor]
│  ├─ Empregos_Var_Pct
│  │  ├─ Empregos_Ano_Anterior (…)
│  │  └─ Empregos_Var (…)
│  ├─ Empregos_Var_Pct_AFL
│  │  ├─ Empregos_Var_Pct (já mapeada acima)
│  │  └─ D_GrupoSetor[grupo_setor]
│  ├─ Empregos_Var_Pct_Comparavel
│  │  ├─ Empregos_Var_Pct (já mapeada acima)
│  │  └─ D_GrupoSetor[grupo_setor]
│  ├─ D_Calendario[Ano]
│  └─ D_Cnae[setor_afl]
├─ Tip_Emp_Ano_Sem_Comparaveis_HTML
│  ├─ Empregos_Ref (já mapeada acima)
│  ├─ Empregos_Ref_AFL (já mapeada acima)
│  ├─ Empregos_Var_Pct (já mapeada acima)
│  ├─ Empregos_Var_Pct_AFL (já mapeada acima)
│  ├─ D_Calendario[Ano]
│  └─ D_Cnae[setor_afl]
└─ D_Cnae[setor_afl]
```

### Tip_Ind_Divisao_HTML
```
Tip_Ind_Divisao_HTML
├─ Emp_Divisao
│  ├─ Ano_Ref
│  │  └─ F_rais[ano]
│  ├─ Empregos_Ref
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Empregos
│  │  │  ├─ D_Cnae[divisao_afl]
│  │  │  ├─ D_Cnae[setor_afl]
│  │  │  ├─ D_Rank_Divisao[nm_divisao]
│  │  │  ├─ D_Rank_Divisao[setor_principal]
│  │  │  └─ F_rais[vinculos]
│  │  └─ D_Ano[ano]
│  ├─ Empregos_Ref_AFL
│  │  ├─ Empregos_Ref (já mapeada acima)
│  │  └─ D_GrupoSetor[grupo_setor]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ind_Ano
│  ├─ Ano_Ref (já mapeada acima)
│  └─ Ind_Atual
│     └─ D_Indicador[indicador]
├─ Ind_Rotulo
│  └─ Ind_Atual (já mapeada acima)
├─ Ind_Total_Divisoes
│  ├─ Ind_Valor_Div
│  │  ├─ Empregos (já mapeada acima)
│  │  ├─ Ind_Ano (já mapeada acima)
│  │  ├─ Ind_Valor_Ctx (…)
│  │  ├─ D_Ano[ano]
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ind_Valor_AFL
│  ├─ Ind_Valor_Ctx
│  │  ├─ Empregos (já mapeada acima)
│  │  ├─ Ind_Ano (já mapeada acima)
│  │  ├─ Ind_Atual (já mapeada acima)
│  │  ├─ D_Ano[ano]
│  │  ├─ D_Escolaridade[escolaridade_agrupada]
│  │  ├─ D_FaixaIdade[faixa_idade]
│  │  ├─ D_Raca[declarada]
│  │  ├─ D_Raca[grupo_raca]
│  │  ├─ D_Sexo[sexo]
│  │  ├─ F_rais[tipo_admissao]
│  │  └─ F_rais[trabalho_intermitente]
│  └─ D_GrupoSetor[grupo_setor]
├─ Ind_Valor_Div (já mapeada acima)
└─ D_Rank_Divisao[nm_divisao]
```

### Tip_Rem_Esc_Total_HTML
```
Tip_Rem_Esc_Total_HTML
├─ Tip_Rem_Esc_HTML
│  ├─ Empregos_Ref_AFL
│  │  ├─ Empregos_Ref (…)
│  │  └─ D_GrupoSetor[grupo_setor]
│  ├─ Rem_Esc_AFL
│  │  ├─ Remuneracao_Media_Ref_AFL (…)
│  │  └─ D_Escolaridade[escolaridade_agrupada]
│  ├─ Rem_Esc_Comp
│  │  ├─ Remuneracao_Media_Ref_Comparavel (…)
│  │  └─ D_Escolaridade[escolaridade_agrupada]
│  ├─ Rem_Esc_Sel
│  │  ├─ Remuneracao_Media_Ref (…)
│  │  └─ D_Escolaridade[escolaridade_agrupada]
│  ├─ D_Cnae[setor_afl]
│  └─ D_Escolaridade[escolaridade_agrupada]
└─ D_Cnae[setor_afl]
```

### Tip_Contrata_Pos_HTML
```
Tip_Contrata_Pos_HTML
├─ Ind_Ano
│  ├─ Ano_Ref
│  │  └─ F_rais[ano]
│  └─ Ind_Atual
│     └─ D_Indicador[indicador]
├─ Ind_Frase
│  └─ Ind_Atual (já mapeada acima)
├─ Ind_Posicao_AFL
│  ├─ Ind_Valor_Div
│  │  ├─ Empregos
│  │  │  ├─ D_Cnae[divisao_afl]
│  │  │  ├─ D_Cnae[setor_afl]
│  │  │  ├─ D_Rank_Divisao[nm_divisao]
│  │  │  ├─ D_Rank_Divisao[setor_principal]
│  │  │  └─ F_rais[vinculos]
│  │  ├─ Ind_Ano (já mapeada acima)
│  │  ├─ Ind_Valor_Ctx (…)
│  │  ├─ D_Ano[ano]
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ind_Rotulo
│  └─ Ind_Atual (já mapeada acima)
├─ Ind_Total_Divisoes
│  ├─ Ind_Valor_Div (já mapeada acima)
│  └─ D_Rank_Divisao[nm_divisao]
└─ Ind_Valor_AFL
   ├─ Ind_Valor_Ctx
   │  ├─ Empregos (já mapeada acima)
   │  ├─ Ind_Ano (já mapeada acima)
   │  ├─ Ind_Atual (já mapeada acima)
   │  ├─ D_Ano[ano]
   │  ├─ D_Escolaridade[escolaridade_agrupada]
   │  ├─ D_FaixaIdade[faixa_idade]
   │  ├─ D_Raca[declarada]
   │  ├─ D_Raca[grupo_raca]
   │  ├─ D_Sexo[sexo]
   │  ├─ F_rais[tipo_admissao]
   │  └─ F_rais[trabalho_intermitente]
   └─ D_GrupoSetor[grupo_setor]
```

### Tip_Ct_Mul_HTML
```
Tip_Ct_Mul_HTML
├─ Ano_Ref
│  └─ F_rais[ano]
├─ Ct_Mul_Div_Qtd
│  ├─ Ct_Mul_Qtd
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Empregos
│  │  │  ├─ D_Cnae[divisao_afl]
│  │  │  ├─ D_Cnae[setor_afl]
│  │  │  ├─ D_Rank_Divisao[nm_divisao]
│  │  │  ├─ D_Rank_Divisao[setor_principal]
│  │  │  └─ F_rais[vinculos]
│  │  ├─ D_Ano[ano]
│  │  └─ D_Sexo[sexo]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Mul_Div_Rep
│  ├─ Ct_Mul_Rep
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Empregos (já mapeada acima)
│  │  ├─ D_Ano[ano]
│  │  └─ D_Sexo[sexo]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Mul_Div_Sal
│  ├─ Ct_Mul_Sal
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Remuneracao_Media
│  │  │  ├─ F_rais[qtd_salario_valido]
│  │  │  └─ F_rais[soma_salario_valido]
│  │  ├─ D_Ano[ano]
│  │  └─ D_Sexo[sexo]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Mul_Div_Tot
│  ├─ Ct_Mul_Tot
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Empregos (já mapeada acima)
│  │  └─ D_Ano[ano]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Mul_Qtd (já mapeada acima)
├─ Ct_Mul_Rep (já mapeada acima)
├─ Ct_Mul_Sal (já mapeada acima)
├─ Ct_Mul_Tot (já mapeada acima)
├─ D_AflAtividade[nome]
├─ D_GrupoSetor[grupo_setor]
└─ D_Rank_Divisao[nm_divisao]
```

### Tip_Ct_Neg_HTML
```
Tip_Ct_Neg_HTML
├─ Ano_Ref
│  └─ F_rais[ano]
├─ Ct_Neg_Div_Qtd
│  ├─ Ct_Neg_Qtd
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Empregos
│  │  │  ├─ D_Cnae[divisao_afl]
│  │  │  ├─ D_Cnae[setor_afl]
│  │  │  ├─ D_Rank_Divisao[nm_divisao]
│  │  │  ├─ D_Rank_Divisao[setor_principal]
│  │  │  └─ F_rais[vinculos]
│  │  ├─ D_Ano[ano]
│  │  └─ D_Raca[grupo_raca]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Neg_Div_Rep
│  ├─ Ct_Neg_Rep
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Empregos (já mapeada acima)
│  │  ├─ D_Ano[ano]
│  │  ├─ D_Raca[declarada]
│  │  └─ D_Raca[grupo_raca]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Neg_Div_Sal
│  ├─ Ct_Neg_Sal
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Remuneracao_Media
│  │  │  ├─ F_rais[qtd_salario_valido]
│  │  │  └─ F_rais[soma_salario_valido]
│  │  ├─ D_Ano[ano]
│  │  └─ D_Raca[grupo_raca]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Neg_Div_Tot
│  ├─ Ct_Neg_Tot
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Empregos (já mapeada acima)
│  │  ├─ D_Ano[ano]
│  │  └─ D_Raca[declarada]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Neg_Qtd (já mapeada acima)
├─ Ct_Neg_Rep (já mapeada acima)
├─ Ct_Neg_Sal (já mapeada acima)
├─ Ct_Neg_Tot (já mapeada acima)
├─ D_AflAtividade[nome]
├─ D_GrupoSetor[grupo_setor]
└─ D_Rank_Divisao[nm_divisao]
```

### Tip_Ct_Esc_HTML
```
Tip_Ct_Esc_HTML
├─ Ano_Ref
│  └─ F_rais[ano]
├─ Ct_Esc_Div_Qtd
│  ├─ Ct_Esc_Qtd
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Empregos
│  │  │  ├─ D_Cnae[divisao_afl]
│  │  │  ├─ D_Cnae[setor_afl]
│  │  │  ├─ D_Rank_Divisao[nm_divisao]
│  │  │  ├─ D_Rank_Divisao[setor_principal]
│  │  │  └─ F_rais[vinculos]
│  │  ├─ D_Ano[ano]
│  │  ├─ D_Ct_Nivel[nivel]
│  │  └─ D_Escolaridade[escolaridade_agrupada]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Esc_Div_Rep
│  ├─ Ct_Esc_Rep
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Empregos (já mapeada acima)
│  │  ├─ D_Ano[ano]
│  │  ├─ D_Ct_Nivel[nivel]
│  │  └─ D_Escolaridade[escolaridade_agrupada]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Esc_Div_Sal
│  ├─ Ct_Esc_Sal
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Remuneracao_Media
│  │  │  ├─ F_rais[qtd_salario_valido]
│  │  │  └─ F_rais[soma_salario_valido]
│  │  ├─ D_Ano[ano]
│  │  ├─ D_Ct_Nivel[nivel]
│  │  └─ D_Escolaridade[escolaridade_agrupada]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Esc_Div_Tot
│  ├─ Ct_Esc_Tot
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Empregos (já mapeada acima)
│  │  └─ D_Ano[ano]
│  ├─ D_Cnae[divisao_afl]
│  ├─ D_Cnae[setor_afl]
│  ├─ D_GrupoSetor[grupo_setor]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ct_Esc_Qtd (já mapeada acima)
├─ Ct_Esc_Rep (já mapeada acima)
├─ Ct_Esc_Sal (já mapeada acima)
├─ Ct_Esc_Tot (já mapeada acima)
├─ D_AflAtividade[nome]
├─ D_Ct_Nivel[nivel]
├─ D_GrupoSetor[grupo_setor]
└─ D_Rank_Divisao[nm_divisao]
```

### Manchete_Emp_AFL_HTML
```
Manchete_Emp_AFL_HTML
├─ Ano_Ref
│  └─ F_rais[ano]
├─ Contexto_Emp_AFL
│  ├─ Ano_Ref (já mapeada acima)
│  ├─ D_AflAtividade[nome]
│  ├─ D_Escolaridade[escolaridade_agrupada]
│  ├─ D_Raca[raca_cor]
│  ├─ D_Sexo[sexo]
│  ├─ D_regiao[estado]
│  └─ D_regiao[uf]
├─ Emp_Sequencia_Altas_AFL
│  ├─ Ano_Inicio_Trecho
│  │  └─ Ano_Ref (já mapeada acima)
│  ├─ Ano_Ref (já mapeada acima)
│  ├─ Empregos
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_Rank_Divisao[nm_divisao]
│  │  ├─ D_Rank_Divisao[setor_principal]
│  │  └─ F_rais[vinculos]
│  ├─ D_Ano[ano]
│  └─ D_GrupoSetor[grupo_setor]
├─ Empregos_Ref
│  ├─ Ano_Ref (já mapeada acima)
│  ├─ Empregos (já mapeada acima)
│  └─ D_Ano[ano]
├─ Empregos_Var
│  ├─ Empregos_Ano_Anterior
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Comparavel_Ano_Anterior (…)
│  │  ├─ Empregos (já mapeada acima)
│  │  └─ D_Ano[ano]
│  └─ Empregos_Ref (já mapeada acima)
├─ Empregos_Var_Pct
│  ├─ Empregos_Ano_Anterior (já mapeada acima)
│  └─ Empregos_Var (já mapeada acima)
├─ D_regiao[estado]
└─ D_regiao[uf]
```

### Titulo_Emp_Var_AFL_HTML
```
Titulo_Emp_Var_AFL_HTML
├─ Ano_Ref
│  └─ F_rais[ano]
├─ Empregos_Var_Pct
│  ├─ Empregos_Ano_Anterior
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Comparavel_Ano_Anterior (…)
│  │  ├─ Empregos
│  │  │  ├─ D_Cnae[divisao_afl]
│  │  │  ├─ D_Cnae[setor_afl]
│  │  │  ├─ D_Rank_Divisao[nm_divisao]
│  │  │  ├─ D_Rank_Divisao[setor_principal]
│  │  │  └─ F_rais[vinculos]
│  │  └─ D_Ano[ano]
│  └─ Empregos_Var
│     ├─ Empregos_Ano_Anterior (já mapeada acima)
│     └─ Empregos_Ref (…)
├─ Empregos_Var_Pct_AFL
│  ├─ Empregos_Var_Pct (já mapeada acima)
│  └─ D_GrupoSetor[grupo_setor]
├─ Empregos_Var_Pct_Comparavel
│  ├─ Empregos_Var_Pct (já mapeada acima)
│  └─ D_GrupoSetor[grupo_setor]
└─ Setor_Emp_Total
   ├─ D_Cnae[divisao_afl]
   └─ D_Comparavel[comparavel_AFL_rotulo]
```

### Tip_Contrata_Max_Total_HTML
```
Tip_Contrata_Max_Total_HTML
├─ Ind_Ano
│  ├─ Ano_Ref
│  │  └─ F_rais[ano]
│  └─ Ind_Atual
│     └─ D_Indicador[indicador]
├─ Ind_Frase
│  └─ Ind_Atual (já mapeada acima)
├─ Ind_Maior_Divisao
│  ├─ Ind_Valor_Div
│  │  ├─ Empregos
│  │  │  ├─ D_Cnae[divisao_afl]
│  │  │  ├─ D_Cnae[setor_afl]
│  │  │  ├─ D_Rank_Divisao[nm_divisao]
│  │  │  ├─ D_Rank_Divisao[setor_principal]
│  │  │  └─ F_rais[vinculos]
│  │  ├─ Ind_Ano (já mapeada acima)
│  │  ├─ Ind_Valor_Ctx (…)
│  │  ├─ D_Ano[ano]
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  └─ D_Rank_Divisao[nm_divisao]
├─ Ind_Maior_Valor
│  ├─ Ind_Valor_Div (já mapeada acima)
│  └─ D_Rank_Divisao[nm_divisao]
└─ Ind_Rotulo
   └─ Ind_Atual (já mapeada acima)
```

### Ct_Mul_Ord
```
Ct_Mul_Ord
├─ Ct_Mul_Valor
│  ├─ Ct_Div_Emp
│  │  ├─ Empregos_Ref (…)
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  ├─ Ct_Mul_Div_Rep
│  │  ├─ Ct_Mul_Rep (…)
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  ├─ Ct_Mul_Div_Sal
│  │  ├─ Ct_Mul_Sal (…)
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  ├─ D_Ct_MetMul[metrica]
│  ├─ D_Ct_Modo[modo]
│  ├─ D_Ct_Setor[setor]
│  ├─ D_Rank_Divisao[nm_divisao]
│  └─ D_Rank_Divisao[setor_principal]
└─ D_Ct_Modo[modo]
```

### Ct_Neg_Ord
```
Ct_Neg_Ord
├─ Ct_Neg_Valor
│  ├─ Ct_Div_Emp
│  │  ├─ Empregos_Ref (…)
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  ├─ Ct_Neg_Div_Rep
│  │  ├─ Ct_Neg_Rep (…)
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  ├─ Ct_Neg_Div_Sal
│  │  ├─ Ct_Neg_Sal (…)
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  ├─ D_Ct_MetNeg[metrica]
│  ├─ D_Ct_Modo[modo]
│  ├─ D_Ct_Setor[setor]
│  ├─ D_Rank_Divisao[nm_divisao]
│  └─ D_Rank_Divisao[setor_principal]
└─ D_Ct_Modo[modo]
```

### Ct_Esc_Ord
```
Ct_Esc_Ord
├─ Ct_Esc_Valor
│  ├─ Ct_Div_Emp
│  │  ├─ Empregos_Ref (…)
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  ├─ Ct_Esc_Div_Rep
│  │  ├─ Ct_Esc_Rep (…)
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  ├─ Ct_Esc_Div_Sal
│  │  ├─ Ct_Esc_Sal (…)
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_GrupoSetor[grupo_setor]
│  │  └─ D_Rank_Divisao[nm_divisao]
│  ├─ D_Ct_MetEsc[metrica]
│  ├─ D_Ct_Modo[modo]
│  ├─ D_Ct_Setor[setor]
│  ├─ D_Rank_Divisao[nm_divisao]
│  └─ D_Rank_Divisao[setor_principal]
└─ D_Ct_Modo[modo]
```

### KPI_Emp_Total_HTML
```
KPI_Emp_Total_HTML
├─ Ano_Ref
│  └─ F_rais[ano]
├─ Empregos_Ref
│  ├─ Ano_Ref (já mapeada acima)
│  ├─ Empregos
│  │  ├─ D_Cnae[divisao_afl]
│  │  ├─ D_Cnae[setor_afl]
│  │  ├─ D_Rank_Divisao[nm_divisao]
│  │  ├─ D_Rank_Divisao[setor_principal]
│  │  └─ F_rais[vinculos]
│  └─ D_Ano[ano]
├─ Empregos_Var
│  ├─ Empregos_Ano_Anterior
│  │  ├─ Ano_Ref (já mapeada acima)
│  │  ├─ Comparavel_Ano_Anterior (…)
│  │  ├─ Empregos (já mapeada acima)
│  │  └─ D_Ano[ano]
│  └─ Empregos_Ref (já mapeada acima)
├─ Empregos_Var_Pct
│  ├─ Empregos_Ano_Anterior (já mapeada acima)
│  └─ Empregos_Var (já mapeada acima)
├─ Empregos_Var_Pct_AFL
│  ├─ Empregos_Var_Pct (já mapeada acima)
│  └─ D_GrupoSetor[grupo_setor]
└─ Empregos_Var_Pct_Comparavel
   ├─ Empregos_Var_Pct (já mapeada acima)
   └─ D_GrupoSetor[grupo_setor]
```


Outras 102 medidas-raiz têm árvore curta; veja **Usa** em [02 · Medidas](02-medidas.md).

---

## Reverse — quem depende das medidas-base

Medidas-base são as mais reusadas no modelo. Mexer nelas afeta várias outras a jusante.

### Ano_Ref (base)

**Usada por:**
- `Ano_Inicio_Trecho`
- `Comparavel_Ano_Anterior`
- `Contexto_Emp_AFL`
- `Contexto_Emp_Total`
- `Ct_Esc_Qtd`
- `Ct_Esc_Rep`
- `Ct_Esc_Sal`
- `Ct_Esc_Tot`
- `Ct_Mul_Qtd`
- `Ct_Mul_Rep`
- `Ct_Mul_Sal`
- `Ct_Mul_Tot`
- `Ct_Neg_Qtd`
- `Ct_Neg_Rep`
- `Ct_Neg_Sal`
- `Ct_Neg_Tot`
- `Emp_Contratos_HTML`
- `Emp_Divisao`
- `Emp_Sequencia_Altas_AFL`
- `Empregos_Ano_Anterior`
- … e mais 64

**Implicação:** mudar `Ano_Ref` afeta 84 outras medidas diretamente.

### Empregos_Ref (base)

**Usada por:**
- `Ct_Div_Emp`
- `Emp_CBO_Top`
- `Emp_Divisao`
- `Emp_UF_Pct_AFL`
- `Empregos_Ref_AFL`
- `Empregos_Ref_Comparavel`
- `Empregos_Var`
- `Esc_Comparacao_Pagina_HTML`
- `KPI_Emp_AFL_HTML`
- `KPI_Emp_Total_HTML`
- `Manchete_Emp_AFL_HTML`
- `Manchete_Emp_Total_HTML`
- `Manchete_Perfil_AFL_HTML`
- `Manchete_Perfil_Total_HTML`
- `Manchete_Salario_AFL_HTML`
- `Manchete_Salario_Total_HTML`
- `Perf_Ate24`
- `Perf_Intermitente`
- `Perf_MedioMais`
- `Perf_Mulheres`
- … e mais 20

**Implicação:** mudar `Empregos_Ref` afeta 40 outras medidas diretamente.

### Empregos (base)

**Usada por:**
- `Ct_Esc_Qtd`
- `Ct_Esc_Rep`
- `Ct_Esc_Tot`
- `Ct_Mul_Qtd`
- `Ct_Mul_Rep`
- `Ct_Mul_Tot`
- `Ct_Neg_Qtd`
- `Ct_Neg_Rep`
- `Ct_Neg_Tot`
- `Emp_Contratos_HTML`
- `Emp_Sequencia_Altas_AFL`
- `Empregos_Ano_Anterior`
- `Empregos_Ref`
- `Empregos_Ref_Todos`
- `Ind_Valor_Ano`
- `Ind_Valor_Ctx`
- `Ind_Valor_Div`
- `KPI_Ct_Esc_AFL_HTML`
- `KPI_Ct_Esc_Total_HTML`
- `Titulo_Emp_Contrato_HTML`

**Implicação:** mudar `Empregos` afeta 20 outras medidas diretamente.

### Remuneracao_Media_Ref (base)

**Usada por:**
- `KPI_RemMedia_AFL_HTML`
- `KPI_RemMedia_Total_HTML`
- `Manchete_Salario_Total_HTML`
- `Rem_Esc_Sel`
- `Rem_Razao_Raca`
- `Rem_Razao_Sexo`
- `Rem_UF_Geo`
- `Remuneracao_Media_Ref_AFL`
- `Remuneracao_Media_Ref_Comparavel`
- `Tip_CBO_HTML`
- `Tip_Rem_Ano_HTML`
- `Tip_Rem_Ano_Total_HTML`
- `Tip_Rem_Gap_Raca_HTML`
- `Tip_Rem_Gap_Sexo_HTML`
- `Tip_Rem_UF_HTML`
- `Titulo_Rem_UF_HTML`

**Implicação:** mudar `Remuneracao_Media_Ref` afeta 16 outras medidas diretamente.

### Empregos_Var_Pct (base)

**Usada por:**
- `Emp_Atividade_Var`
- `Empregos_Var_Pct_AFL`
- `Empregos_Var_Pct_Comparavel`
- `Empregos_Var_Pct_Sel_Pos`
- `Empregos_Var_Pct_Sel_Pre`
- `KPI_Emp_AFL_HTML`
- `KPI_Emp_Total_HTML`
- `Manchete_Emp_AFL_HTML`
- `Manchete_Emp_Total_HTML`
- `Tip_Emp_Ano_HTML`
- `Tip_Emp_Ano_Sem_Comparaveis_HTML`
- `Titulo_Emp_Var_AFL_HTML`
- `Titulo_Emp_Var_Total_HTML`

**Implicação:** mudar `Empregos_Var_Pct` afeta 13 outras medidas diretamente.

### Remuneracao_Media (base)

**Usada por:**
- `Ct_Esc_Sal`
- `Ct_Mul_Sal`
- `Ct_Neg_Sal`
- `KPI_Ct_Esc_AFL_HTML`
- `KPI_Ct_Esc_Total_HTML`
- `Rem_Media_AFL_Pos`
- `Rem_Media_AFL_Pre`
- `Rem_Media_Comp_Pos`
- `Rem_Media_Comp_Pre`
- `Rem_Media_Sel_Pos`
- `Rem_Media_Sel_Pre`
- `Remuneracao_Media_Ref`

**Implicação:** mudar `Remuneracao_Media` afeta 12 outras medidas diretamente.

### Empregos_Ref_AFL (base)

**Usada por:**
- `Emp_Divisao`
- `Emp_UF_Peso_AFL`
- `Emp_UF_Peso_Geo`
- `KPI_Peso_AFL_HTML`
- `KPI_Peso_Total_HTML`
- `Tip_Emp_Ano_HTML`
- `Tip_Emp_Ano_Sem_Comparaveis_HTML`
- `Tip_Emp_Atividade_HTML`
- `Tip_Emp_UF_HTML`
- `Tip_Ind_UF_HTML`
- `Tip_Rem_Esc_HTML`
- `Titulo_Emp_UF_Total_HTML`

**Implicação:** mudar `Empregos_Ref_AFL` afeta 12 outras medidas diretamente.

### Remuneracao_Media_Ref_AFL (base)

**Usada por:**
- `KPI_RemMedia_Total_HTML`
- `Manchete_Salario_AFL_HTML`
- `Manchete_Salario_Total_HTML`
- `Rem_Esc_AFL`
- `Rem_UF_Razao_Comp`
- `Tip_Rem_Ano_HTML`
- `Tip_Rem_Ano_Total_HTML`
- `Tip_Rem_UF_HTML`
- `Titulo_Rem_Esc_HTML`

**Implicação:** mudar `Remuneracao_Media_Ref_AFL` afeta 9 outras medidas diretamente.

### Perf_Mulheres (base)

**Usada por:**
- `KPI_Mulheres_AFL_HTML`
- `KPI_Mulheres_Total_HTML`
- `Manchete_Perfil_AFL_HTML`
- `Manchete_Perfil_Total_HTML`
- `Perf_Mulheres_AFL`
- `Perf_Mulheres_Comp`
- `Tip_CBO_HTML`
- `Titulo_CBO_HTML`

**Implicação:** mudar `Perf_Mulheres` afeta 8 outras medidas diretamente.

### Ind_Valor_Ctx (base)

**Usada por:**
- `Ind_Atividade_Lider`
- `Ind_Atividade_Lider_Valor`
- `Ind_UF_AFL_Dica`
- `Ind_Valor_AFL`
- `Ind_Valor_Comp`
- `Ind_Valor_Div`
- `Tip_Ind_Atividade_HTML`
- `Tip_Ind_UF_HTML`

**Implicação:** mudar `Ind_Valor_Ctx` afeta 8 outras medidas diretamente.

### Ind_Rotulo (base)

**Usada por:**
- `Tip_Contrata_Dif_HTML`
- `Tip_Contrata_Max_AFL_HTML`
- `Tip_Contrata_Max_Total_HTML`
- `Tip_Contrata_Pos_HTML`
- `Tip_Ind_Ano_HTML`
- `Tip_Ind_Atividade_HTML`
- `Tip_Ind_Divisao_HTML`
- `Tip_Ind_UF_HTML`

**Implicação:** mudar `Ind_Rotulo` afeta 8 outras medidas diretamente.

### Ind_Ano (base)

**Usada por:**
- `Ind_Valor_Ctx`
- `Ind_Valor_Div`
- `Tip_Contrata_Max_AFL_HTML`
- `Tip_Contrata_Max_Total_HTML`
- `Tip_Contrata_Pos_HTML`
- `Tip_Ind_Atividade_HTML`
- `Tip_Ind_Divisao_HTML`
- `Tip_Ind_UF_HTML`

**Implicação:** mudar `Ind_Ano` afeta 8 outras medidas diretamente.

### Remuneracao_Media_Ref_Comparavel (base)

**Usada por:**
- `KPI_RemMedia_AFL_HTML`
- `Manchete_Salario_AFL_HTML`
- `Rem_Esc_Comp`
- `Rem_UF_Razao_Comp`
- `Tip_Rem_Ano_HTML`
- `Tip_Rem_UF_HTML`
- `Titulo_Rem_Esc_HTML`

**Implicação:** mudar `Remuneracao_Media_Ref_Comparavel` afeta 7 outras medidas diretamente.

### Rem_Razao_Sexo (base)

**Usada por:**
- `Dif_Salarial_Sexo`
- `KPI_RazaoSexo_AFL_HTML`
- `KPI_RazaoSexo_Total_HTML`
- `Rem_Razao_Sexo_AFL`
- `Rem_Razao_Sexo_Comp`
- `Tip_RazaoSexo_HTML`
- `Tip_Rem_Gap_Sexo_HTML`

**Implicação:** mudar `Rem_Razao_Sexo` afeta 7 outras medidas diretamente.

### Rem_Razao_Raca (base)

**Usada por:**
- `Dif_Salarial_Raca`
- `KPI_RazaoRaca_AFL_HTML`
- `KPI_RazaoRaca_Total_HTML`
- `Rem_Razao_Raca_AFL`
- `Rem_Razao_Raca_Comp`
- `Tip_RazaoRaca_HTML`
- `Tip_Rem_Gap_Raca_HTML`

**Implicação:** mudar `Rem_Razao_Raca` afeta 7 outras medidas diretamente.

### Empregos_Var_Pct_AFL (base)

**Usada por:**
- `Empregos_Var_Pct_AFL_Pos`
- `Empregos_Var_Pct_AFL_Pre`
- `KPI_Emp_Total_HTML`
- `Tip_Emp_Ano_HTML`
- `Tip_Emp_Ano_Sem_Comparaveis_HTML`
- `Titulo_Emp_Var_AFL_HTML`
- `Titulo_Emp_Var_Total_HTML`

**Implicação:** mudar `Empregos_Var_Pct_AFL` afeta 7 outras medidas diretamente.

### Rem_Razao_Sexo_Comp (base)

**Usada por:**
- `Dif_Salarial_Sexo_Comp`
- `KPI_RazaoSexo_AFL_HTML`
- `Tip_RazaoSexo_HTML`
- `Tip_Rem_Gap_Sexo_HTML`
- `Titulo_Rem_Gap_HTML`

**Implicação:** mudar `Rem_Razao_Sexo_Comp` afeta 5 outras medidas diretamente.

### Rem_Razao_Sexo_AFL (base)

**Usada por:**
- `Dif_Salarial_Sexo_AFL`
- `KPI_RazaoSexo_Total_HTML`
- `Tip_RazaoSexo_HTML`
- `Tip_Rem_Gap_Sexo_HTML`
- `Titulo_Rem_Gap_HTML`

**Implicação:** mudar `Rem_Razao_Sexo_AFL` afeta 5 outras medidas diretamente.

### Rem_Razao_Raca_Comp (base)

**Usada por:**
- `Dif_Salarial_Raca_Comp`
- `KPI_RazaoRaca_AFL_HTML`
- `Tip_RazaoRaca_HTML`
- `Tip_Rem_Gap_Raca_HTML`
- `Titulo_Rem_Gap_HTML`

**Implicação:** mudar `Rem_Razao_Raca_Comp` afeta 5 outras medidas diretamente.

### Rem_Razao_Raca_AFL (base)

**Usada por:**
- `Dif_Salarial_Raca_AFL`
- `KPI_RazaoRaca_Total_HTML`
- `Tip_RazaoRaca_HTML`
- `Tip_Rem_Gap_Raca_HTML`
- `Titulo_Rem_Gap_HTML`

**Implicação:** mudar `Rem_Razao_Raca_AFL` afeta 5 outras medidas diretamente.

### Ind_Valor_Div (base)

**Usada por:**
- `Ind_Maior_Divisao`
- `Ind_Maior_Valor`
- `Ind_Posicao_AFL`
- `Ind_Total_Divisoes`
- `Tip_Ind_Divisao_HTML`

**Implicação:** mudar `Ind_Valor_Div` afeta 5 outras medidas diretamente.

### Ind_Atual (base)

**Usada por:**
- `Ind_Ano`
- `Ind_Frase`
- `Ind_Rotulo`
- `Ind_Valor_Ano`
- `Ind_Valor_Ctx`

**Implicação:** mudar `Ind_Atual` afeta 5 outras medidas diretamente.

### Empregos_Var (base)

**Usada por:**
- `Empregos_Var_Pct`
- `KPI_Emp_AFL_HTML`
- `KPI_Emp_Total_HTML`
- `Manchete_Emp_AFL_HTML`
- `Manchete_Emp_Total_HTML`

**Implicação:** mudar `Empregos_Var` afeta 5 outras medidas diretamente.

### Empregos_Ref_Comparavel (base)

**Usada por:**
- `Emp_UF_Peso_AFL`
- `KPI_Peso_AFL_HTML`
- `KPI_Peso_Total_HTML`
- `Tip_Emp_Ano_HTML`
- `Tip_Emp_UF_HTML`

**Implicação:** mudar `Empregos_Ref_Comparavel` afeta 5 outras medidas diretamente.

### Emp_Divisao (base)

**Usada por:**
- `Emp_Divisao_Top`
- `Emp_Posicao_AFL_Divisao`
- `Emp_Total_Divisoes`
- `Tip_Emp_Divisao_HTML`
- `Tip_Ind_Divisao_HTML`

**Implicação:** mudar `Emp_Divisao` afeta 5 outras medidas diretamente.

### Ct_Neg_Sal (base)

**Usada por:**
- `Ct_Neg_Div_Sal`
- `Ct_Neg_Valor_AFL`
- `KPI_Ct_Neg_AFL_HTML`
- `KPI_Ct_Neg_Total_HTML`
- `Tip_Ct_Neg_HTML`

**Implicação:** mudar `Ct_Neg_Sal` afeta 5 outras medidas diretamente.

### Ct_Neg_Rep (base)

**Usada por:**
- `Ct_Neg_Div_Rep`
- `Ct_Neg_Valor_AFL`
- `KPI_Ct_Neg_AFL_HTML`
- `KPI_Ct_Neg_Total_HTML`
- `Tip_Ct_Neg_HTML`

**Implicação:** mudar `Ct_Neg_Rep` afeta 5 outras medidas diretamente.

### Ct_Mul_Sal (base)

**Usada por:**
- `Ct_Mul_Div_Sal`
- `Ct_Mul_Valor_AFL`
- `KPI_Ct_Mul_AFL_HTML`
- `KPI_Ct_Mul_Total_HTML`
- `Tip_Ct_Mul_HTML`

**Implicação:** mudar `Ct_Mul_Sal` afeta 5 outras medidas diretamente.

### Ct_Mul_Rep (base)

**Usada por:**
- `Ct_Mul_Div_Rep`
- `Ct_Mul_Valor_AFL`
- `KPI_Ct_Mul_AFL_HTML`
- `KPI_Ct_Mul_Total_HTML`
- `Tip_Ct_Mul_HTML`

**Implicação:** mudar `Ct_Mul_Rep` afeta 5 outras medidas diretamente.

### Ano_Inicio_Trecho (base)

**Usada por:**
- `Emp_Sequencia_Altas_AFL`
- `KPI_Jovens_AFL_HTML`
- `KPI_Jovens_Total_HTML`
- `Perf_Idade_Inicio`
- `Titulo_Rem_Serie_HTML`

**Implicação:** mudar `Ano_Inicio_Trecho` afeta 5 outras medidas diretamente.

### Setor_Emp_Total (base)

**Usada por:**
- `Contexto_Emp_Total`
- `Manchete_Emp_Total_HTML`
- `Titulo_Emp_Var_AFL_HTML`
- `Titulo_Emp_Var_Total_HTML`

**Implicação:** mudar `Setor_Emp_Total` afeta 4 outras medidas diretamente.

### Perf_MedioMais (base)

**Usada por:**
- `KPI_Escol_AFL_HTML`
- `KPI_Escol_Total_HTML`
- `Perf_MedioMais_AFL`
- `Perf_MedioMais_Comp`

**Implicação:** mudar `Perf_MedioMais` afeta 4 outras medidas diretamente.

### Perf_Idade (base)

**Usada por:**
- `KPI_Jovens_AFL_HTML`
- `KPI_Jovens_Total_HTML`
- `Manchete_Perfil_AFL_HTML`
- `Manchete_Perfil_Total_HTML`

**Implicação:** mudar `Perf_Idade` afeta 4 outras medidas diretamente.

### Perf_Ate24 (base)

**Usada por:**
- `KPI_Jovens_AFL_HTML`
- `KPI_Jovens_Total_HTML`
- `Perf_Ate24_AFL`
- `Perf_Ate24_Comp`

**Implicação:** mudar `Perf_Ate24` afeta 4 outras medidas diretamente.

### Ind_Valor_AFL (base)

**Usada por:**
- `Tip_Contrata_Dif_HTML`
- `Tip_Contrata_Pos_HTML`
- `Tip_Ind_Atividade_HTML`
- `Tip_Ind_Divisao_HTML`

**Implicação:** mudar `Ind_Valor_AFL` afeta 4 outras medidas diretamente.

### Empregos_Var_Pct_Comparavel (base)

**Usada por:**
- `KPI_Emp_AFL_HTML`
- `KPI_Emp_Total_HTML`
- `Tip_Emp_Ano_HTML`
- `Titulo_Emp_Var_AFL_HTML`

**Implicação:** mudar `Empregos_Var_Pct_Comparavel` afeta 4 outras medidas diretamente.

### Emp_UF_Peso_AFL (base)

**Usada por:**
- `Emp_UF_Peso_Geo`
- `Tip_Emp_UF_HTML`
- `Titulo_Emp_UF_AFL_HTML`
- `Titulo_Emp_UF_Total_HTML`

**Implicação:** mudar `Emp_UF_Peso_AFL` afeta 4 outras medidas diretamente.

### Perf_Mulheres_Comp (base)

**Usada por:**
- `KPI_Mulheres_AFL_HTML`
- `KPI_Mulheres_Total_HTML`
- `Manchete_Perfil_AFL_HTML`

**Implicação:** mudar `Perf_Mulheres_Comp` afeta 3 outras medidas diretamente.

### Ind_Frase (base)

**Usada por:**
- `Tip_Contrata_Max_AFL_HTML`
- `Tip_Contrata_Max_Total_HTML`
- `Tip_Contrata_Pos_HTML`

**Implicação:** mudar `Ind_Frase` afeta 3 outras medidas diretamente.

### Empregos_Ref_Todos (base)

**Usada por:**
- `KPI_Peso_AFL_HTML`
- `KPI_Peso_Total_HTML`
- `Tip_Emp_Divisao_HTML`

**Implicação:** mudar `Empregos_Ref_Todos` afeta 3 outras medidas diretamente.

### Emp_Total_Divisoes (base)

**Usada por:**
- `Manchete_Emp_Total_HTML`
- `Tip_Emp_Divisao_HTML`
- `Titulo_Emp_Ranking_HTML`

**Implicação:** mudar `Emp_Total_Divisoes` afeta 3 outras medidas diretamente.

### Ct_Esc_Sal (base)

**Usada por:**
- `Ct_Esc_Div_Sal`
- `Ct_Esc_Valor_AFL`
- `Tip_Ct_Esc_HTML`

**Implicação:** mudar `Ct_Esc_Sal` afeta 3 outras medidas diretamente.

### Ct_Esc_Rep (base)

**Usada por:**
- `Ct_Esc_Div_Rep`
- `Ct_Esc_Valor_AFL`
- `Tip_Ct_Esc_HTML`

**Implicação:** mudar `Ct_Esc_Rep` afeta 3 outras medidas diretamente.

### Ct_Div_Emp (base)

**Usada por:**
- `Ct_Esc_Valor`
- `Ct_Mul_Valor`
- `Ct_Neg_Valor`

**Implicação:** mudar `Ct_Div_Emp` afeta 3 outras medidas diretamente.

### Contexto_Emp_Total (base)

**Usada por:**
- `Manchete_Emp_Total_HTML`
- `Manchete_Perfil_Total_HTML`
- `Manchete_Salario_Total_HTML`

**Implicação:** mudar `Contexto_Emp_Total` afeta 3 outras medidas diretamente.

### Contexto_Emp_AFL (base)

**Usada por:**
- `Manchete_Emp_AFL_HTML`
- `Manchete_Perfil_AFL_HTML`
- `Manchete_Salario_AFL_HTML`

**Implicação:** mudar `Contexto_Emp_AFL` afeta 3 outras medidas diretamente.


---

## Tabelas mais referenciadas

Sinaliza onde mora a "carne" do modelo — tabelas usadas por mais medidas têm maior peso na arquitetura.

1. `D_Cnae` — referenciada por 76 medidas
2. `D_GrupoSetor` — referenciada por 59 medidas
3. `D_Calendario` — referenciada por 38 medidas
4. `D_Rank_Divisao` — referenciada por 35 medidas
5. `D_Ano` — referenciada por 33 medidas

---

## Como usar essa info

- **Antes de refatorar uma medida-base** (ex: `Faturamento`), checa quem depende dela aqui — você pode estar quebrando 6 outras sem perceber
- **Em revisão de PR** que muda DAX, esse arquivo serve de "blast radius check"
- **Pra onboarding**, a árvore ajuda a entender o "esqueleto" de cálculo do modelo

---

*XPERIUN · `/pbi-doc`*
