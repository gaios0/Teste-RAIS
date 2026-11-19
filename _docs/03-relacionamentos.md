# RAIS Emprego Formal — Relacionamentos

Mapa visual + lista detalhada de relacionamentos entre tabelas.

> **Voltar pra:** [02 · Medidas](02-medidas.md) · **Próxima:** [04 · Dependências](04-dependencias.md)

---

## Diagrama

```
 ┌──────────────┐ N:N ┌───────────┐ N:1 ┌──────────┐
 │ D_Calendario │◄────│           │────►│ D_regiao │
 └──────┬───────┘     │           │     └──────────┘
        │ auto        │           │ N:1 ┌──────────┐
        ▼             │           │────►│ D_Sexo   │
 ┌──────────────┐     │  F_rais   │     └──────────┘
 │ D_Ano        │     │  (fato)   │ N:1 ┌────────────────┐
 └──────────────┘     │           │────►│ D_Escolaridade │
                      │           │     └────────────────┘
                      │           │ N:1 ┌──────────────┐
                      │           │────►│ D_FaixaIdade │
                      │           │     └──────────────┘
                      │           │ N:1 ┌──────────┐
                      │           │────►│ D_Raca   │
                      └─────┬─────┘     └──────────┘
                            │ N:1
                            ▼
                      ┌───────────┐ N:1 ┌──────────────┐
                      │  D_Cnae   │────►│ D_GrupoSetor │
                      └─────┬─────┘     └──────────────┘
                     N:1 │     │ 1:1
                         ▼     ▼
             ┌──────────────┐ ┌────────────────┐
             │ D_Comparavel │ │ D_AflAtividade │
             └──────────────┘ └────────────────┘

 Sem relação (parâmetros e textos): D_Indicador, D_Info, D_Rank_Divisao, D_Ct_*
```

---

## Tabela detalhada

| # | From | To | Cardinalidade | Direção | Ativo | Notas |
|---|---|---|---|---|---|---|
| 1 | `F_rais.cnae_fiscal` | `D_Cnae.cnae_fiscal` | N:1 | Única | ✓ | — |
| 2 | `F_rais.id_municipio` | `D_regiao.cod_municipio` | N:1 | Única | ✓ | — |
| 3 | `F_rais.sexo` | `D_Sexo.sexo` | N:1 | Única | ✓ | — |
| 4 | `F_rais.escolaridade_agrupada` | `D_Escolaridade.escolaridade_agrupada` | N:1 | Única | ✓ | — |
| 5 | `F_rais.faixa_idade` | `D_FaixaIdade.faixa_idade` | N:1 | Única | ✓ | — |
| 6 | `F_rais.raca_cor` | `D_Raca.raca_cor` | N:1 | Única | ✓ | — |
| 7 | `D_Cnae.grupo_setor` | `D_GrupoSetor.grupo_setor` | N:1 | Única | ✓ | — |
| 8 | `F_rais.ano` | `D_Calendario.Ano` | N:N | Única | ✓ | muitos-para-muitos, sem filtro de segurança |
| 9 | `D_Cnae.setor_comparavel_afl` | `D_Comparavel.comparavel_AFL` | N:1 | Única | ✓ | sem filtro de segurança |
| 10 | `D_Cnae.cnae_fiscal` | `D_AflAtividade.cnae_fiscal` | N:1 | Única | ✓ | sem filtro de segurança |
| 11 | `D_Calendario.Ano` | `D_Ano.ano` | N:1 | Única | ✓ | detectado automaticamente |

> **Notas:** sinalizar relacionamentos bi-direcionais, inativos, M:M, etc.

---

## Análise rápida

Esquema estrela com `F_rais` no centro e 11 relações. A fato filtra direto as dimensões de pessoa (sexo, idade, escolaridade, cor/raça), a geografia (`D_regiao`) e a atividade (`D_Cnae`). `D_Cnae` é um floco: dela saem `D_GrupoSetor`, `D_Comparavel` e `D_AflAtividade`. O tempo entra por `D_Calendario`, ligada a `F_rais[ano]` por uma relação muitos-para-muitos (um ano tem vários dias). Ficam sem relação as tabelas de parâmetro e de texto: `D_Ct_MetEsc`, `D_Ct_MetMul`, `D_Ct_MetNeg`, `D_Ct_Modo`, `D_Ct_Nivel`, `D_Ct_Setor`, `D_Indicador`, `D_Info`, `D_Rank_Divisao`. Nenhuma relação é bi-direcional e todas estão ativas.

> **Tom:** descrever, não opinar. Pra auditoria de qualidade dos relacionamentos (anti-patterns, bi-direcional desnecessário, etc.), use `/pbi-modelo-review`.

---

*XPERIUN · `/pbi-doc`*
