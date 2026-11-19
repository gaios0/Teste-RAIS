# RAIS Emprego Formal — Overview

> **Emprego formal no Brasil (RAIS/eSocial, 2009 em diante) com foco no AFL — alimentação fora do lar — comparado aos setores Comparáveis: quantos são, quem trabalha, quanto ganha e quem contrata.**
> Documentação gerada por Claude Code + `/pbi-doc` em 19 nov 2026

**Arquivo:** `RAIS Emprego Formal.pbip`

---

## Métricas

| Métrica | Valor |
|---|---|
| Tabelas reais | **22** (excluindo auto-date geradas) |
| Medidas | **221** |
| Relacionamentos | **11** |
| Colunas totais | **109** |
| Tamanho .pbip | **410 KB** |

---

## Inventário de tabelas

| Tabela | Tipo | Colunas | Medidas | Source |
|---|---|---|---|---|
| [`F_rais`](01-tabelas.md#f_rais) | Fato | 25 | 0 | DirectQuery · F_rais (Painel_RAIS) |
| [`D_AflAtividade`](01-tabelas.md#d_aflatividade) | Dimensão | 3 | 0 | Import · tabela digitada (#table) |
| [`D_Ano`](01-tabelas.md#d_ano) | Dimensão | 1 | 0 | Import · M (m) |
| [`D_Calendario`](01-tabelas.md#d_calendario) | Dimensão | 24 | 0 | Import · M gerado (calendário) |
| [`D_Cnae`](01-tabelas.md#d_cnae) | Dimensão | 8 | 0 | DirectQuery · D_Cnae (Painel_RAIS) |
| [`D_Comparavel`](01-tabelas.md#d_comparavel) | Dimensão | 2 | 0 | Import · tabela digitada (#table) |
| [`D_Escolaridade`](01-tabelas.md#d_escolaridade) | Dimensão | 2 | 0 | DirectQuery · D_Escolaridade (Painel_RAIS) |
| [`D_FaixaIdade`](01-tabelas.md#d_faixaidade) | Dimensão | 2 | 0 | DirectQuery · D_FaixaIdade (Painel_RAIS) |
| [`D_GrupoSetor`](01-tabelas.md#d_gruposetor) | Dimensão | 2 | 0 | DirectQuery · D_GrupoSetor (Painel_RAIS) |
| [`D_Raca`](01-tabelas.md#d_raca) | Dimensão | 4 | 0 | DirectQuery · D_Raca (Painel_RAIS) |
| [`D_regiao`](01-tabelas.md#d_regiao) | Dimensão | 4 | 0 | DirectQuery · D_regiao (Painel_RAIS) |
| [`D_Sexo`](01-tabelas.md#d_sexo) | Dimensão | 2 | 0 | DirectQuery · D_Sexo (Painel_RAIS) |
| [`D_Ct_MetEsc`](01-tabelas.md#d_ct_metesc) | Auxiliar | 2 | 0 | Import · tabela digitada (#table) |
| [`D_Ct_MetMul`](01-tabelas.md#d_ct_metmul) | Auxiliar | 2 | 0 | Import · tabela digitada (#table) |
| [`D_Ct_MetNeg`](01-tabelas.md#d_ct_metneg) | Auxiliar | 2 | 0 | Import · tabela digitada (#table) |
| [`D_Ct_Modo`](01-tabelas.md#d_ct_modo) | Auxiliar | 2 | 0 | Import · tabela digitada (#table) |
| [`D_Ct_Nivel`](01-tabelas.md#d_ct_nivel) | Auxiliar | 2 | 0 | Import · tabela digitada (#table) |
| [`D_Ct_Setor`](01-tabelas.md#d_ct_setor) | Auxiliar | 2 | 0 | Import · tabela digitada (#table) |
| [`D_Indicador`](01-tabelas.md#d_indicador) | Auxiliar | 3 | 0 | Import · tabela digitada (#table) |
| [`D_Info`](01-tabelas.md#d_info) | Auxiliar | 12 | 0 | Import · tabela digitada (#table) |
| [`D_Rank_Divisao`](01-tabelas.md#d_rank_divisao) | Auxiliar | 2 | 0 | Import · tabela digitada (#table) |
| [`_medidas`](01-tabelas.md#_medidas) | Medidas | 1 | 221 | Import · tabela digitada (#table) |

> **Tipo:** Fato (1+ por modelo) · Dimensão (descreve fato) · Medidas (só hospeda DAX) · Aux (parameter table, calculated, etc.)

---

## Fontes de dados

- **Modelo semântico do Power BI (DirectQuery para Analysis Services):** `Painel_RAIS`, workspace `Testes` (`powerbi://api.powerbi.com/v1.0/myorg/Testes`). Fonte de F_rais e das dimensões remotas.
- **Tabelas digitadas em M (`#table`)**: botões, parâmetros e textos das dicas.
- **M gerado**: calendário `D_Calendario`.

> **Atenção:** a fonte aponta para o workspace `Testes`. Ao publicar em outro workspace, troque o endereço em `expressions.tmdl`.

---

## Configurações relevantes do modelo

- **Culture:** pt-BR
- **Auto Date/Time:** ligado (nenhuma tabela LocalDateTable_* no modelo)
- **Modo de dados:** Composto: DirectQuery para AS + tabelas locais em import
- **Páginas do relatório:** 8 visíveis (Empregos · Todos os setores, Empregos · AFL, Quem trabalha · Todos os setores, Quem trabalha · AFL, Quanto ganha · Todos os setores, Quanto ganha · AFL, Ranking · Todos os setores, Ranking · AFL)
- **Páginas de dica (tooltip):** 28 ocultas
- **Pastas de medidas:** 41 displayFolders

---

## Próximas seções

- [01 · Tabelas](01-tabelas.md) — descrição + colunas tipadas + source M de cada tabela
- [02 · Medidas](02-medidas.md) — DAX completo + explicação PT de cada medida
- [03 · Relacionamentos](03-relacionamentos.md) — mapa visual + tabela detalhada
- [04 · Dependências](04-dependencias.md) — quem depende de quem entre as medidas

---

*XPERIUN · O Sistema Operacional dos Incomparáveis · `/pbi-doc`*
