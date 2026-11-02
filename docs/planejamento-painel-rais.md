# Painel RAIS · Emprego Formal — estudo inicial e proposta (02/11/2026)

## O que existe
- `RAIS Emprego Formal.pbip`: relatório (1 página em branco) + modelo local **composto**, com todas as tabelas em DirectQuery para o modelo publicado `Painel_RAIS` (workspace Testes). Não há medidas; dá para criar medidas e tabelas importadas no modelo local.
- `Painéis AFL — Congresso Nacional Nov 26.docx`: 10 perguntas do Painel 2 (RAIS) e a ressalva da defasagem de um ano.

## Modelo
| Tabela | Conteúdo |
|---|---|
| `F_rais` | Estoque de vínculos ativos em 31/12, **agregado**: `vinculos`, `soma_salario_valido`, `qtd_salario_valido`, `soma_sm_valido`, `soma_idade`, `qtd_idade`. Dimensões: ano, UF, município, CNAE subclasse (e nomes), grupo de setor, sexo, faixa etária, escolaridade, raça/cor, CBO 2002, categoria de vínculo, natureza, modalidade de contrato, tipo de admissão, intermitente, parcial, horas contratuais, deficiência, âmbito |
| `F_Mediana` | Mediana salarial **pré-calculada** por ano × grupo de setor (AFL, Comparável, Demais, Todos) × UF (+ Todos) × sexo (+ Todos) × escolaridade (+ Todos). Sem raça e sem CNAE |
| `D_Ano` | 2009–2025, com a coluna `base`: RAIS declaratória até 2021, **eSocial a partir de 2022** |
| `D_Cnae` | 1.359 subclasses; `setor_afl` (6 CNAEs do AFL, iguais aos do RF), `setor_comparavel_afl`, `grupo_setor` (AFL · Comparável · Demais), `setor_principal` (5 setores) |
| `D_Sexo`, `D_FaixaIdade` (7 faixas), `D_Escolaridade` (7 níveis), `D_Raca` (com `grupo_raca` Negra = preta + parda e `declarada`), `D_UF`, `D_GrupoSetor` | ordenadas por `ordem` |

Conferência: o estoque bate com os números oficiais da RAIS (41,2 mi em 2009; 52,8 mi em 2022; 60,7 mi em 2025).

## Números de partida (AFL)
| Ano | Empregos AFL | % do emprego formal | Remuneração média (nominal) | Em salários mínimos | % mulheres | Idade média |
|---|---|---|---|---|---|---|
| 2009 | 1.017.895 | 2,5% | R$ 717 | 1,54 | 51,2% | 31,7 |
| 2019 | 1.563.255 | 3,3% | R$ 1.610 | 1,61 | 53,6% | 33,5 |
| 2020 | 1.290.855 | 2,8% | R$ 1.512 | 1,45 | 53,5% | 34,0 |
| 2025 | 1.768.754 | 2,9% | R$ 2.315 | 1,53 | 55,6% | 35,1 |

- Mediana do AFL em 2025: R$ 2.037 (Comparáveis R$ 2.471; Todos R$ 2.744).
- Ocupações do AFL em 2025: atendente de lanchonete (309.619), auxiliar nos serviços de alimentação (261.087), cozinheiro geral (209.383), garçom (162.430).
- Intermitente no AFL: 17.463 vínculos em 2025 (1,0%).

## Achados que mudam a análise
1. **Quebra de fonte em 2022 (eSocial).** O estoque total sobe 8,3% de 2021 para 2022 e o do AFL, 17,9%: parte é recuperação pós-pandemia, parte é mudança de captação. A série precisa marcar 2022 e a variação 2021→2022 não pode ser lida como crescimento puro.
2. **Primeiro emprego só existe até 2021.** No eSocial o tipo de admissão "Primeiro Emprego" praticamente some (2022: 1 vínculo no AFL; 2023+: vazio). A pergunta só tem resposta para 2009–2021.
3. **Raça/cor sem informação muda com o tempo.** Não declarada: 24–33% dos vínculos até 2022; 10% em 2023; 3–5% em 2024–2025. Comparar composição racial ao longo dos anos sem tratar isso mostra uma "mudança" que é de preenchimento. Proposta: percentuais sobre os declarados + aviso da cobertura.
4. **Remuneração está em reais correntes.** O modelo não tem deflator; o documento pede R$ reais. Proposta: tabela local com o IPCA (IBGE) e valores a preços do último ano. A remuneração em salários mínimos já existe e serve de segunda leitura.
5. **Comparação justa.** O total inclui o setor público (12,6 milhões de vínculos estatutários em 2025), que paga mais e não existe no AFL. Remuneração e perfil do AFL devem ser comparados com os **Comparáveis** (ou com o setor privado), não com o total.
6. **Intermitente começa em 2017–2018** (reforma trabalhista); antes é "não categorizado".
7. **Mediana tem recortes limitados** (setor, UF, sexo, escolaridade). Com outros filtros (raça, CNAE, faixa etária) a mediana não existe; a página precisa dizer isso.

## Quebra de série em 2022 (nota técnica do MTE, RAIS 2022)
Fonte: `apresentacao_rais-2022_nota_tecnica.pdf` (gov.br/trabalho-e-emprego).
- Migração para o eSocial em grupos: grupos 1 e 2 (não optantes do Simples) desde o ano-base 2019; **grupo 3 (optantes do Simples, entidades sem fins lucrativos, pessoas físicas) no ano-base 2022**, 77% dos estabelecimentos e 35% dos vínculos; grupo 4 (órgãos públicos) no ano-base 2023.
- Estoque 2022 = 52.790.864: 48.728.871 já existiam na RAIS 2021, **2.266.347 são crescimento real** e **1.795.646 são aumento de cobertura** (empresas pequenas que não declaravam; 80% dos "incluídos" tinham até 4 empregados). Variação observada 2021→2022: +4.061.993 (+8,3%); real: cerca de +4,7%.
- O MTE diz que 2022 não é diretamente comparável com a série anterior e não publica série retropolada; prevê novo impacto em 2023 com o setor público.
- Consequência para o AFL: o setor é quase todo Simples e de empresas pequenas, então o efeito tende a ser maior que a média (observado: +17,9% de 2021 para 2022). O setor público (2023) não afeta o AFL, mas afeta "Todos os setores".

### Tratamento proposto
1. **Duas séries:** 2009–2021 (RAIS declaratória) e 2022–2025 (eSocial), lado a lado no mesmo eixo, com marca visual da quebra e nota fixa no fundo.
2. **Nenhuma comparação atravessa a quebra:** "% sobre o ano anterior" de 2022 volta BLANK (como 2006 no RF); crescimento acumulado e médio ao ano partem do início do trecho do ano escolhido (2009 ou 2022); recordes e sequências nas manchetes só dentro do trecho.
3. **Todos os setores em 2023:** aviso da entrada do setor público (ou comparação só com o setor privado).
4. **Perfil e remuneração:** percentuais e médias também sofrem com a entrada de empresas pequenas (perfil mais jovem e salário menor); comparações 2021 × 2022 ficam marcadas, e o (i) explica.
5. **Estimativa opcional do efeito no AFL:** comparar a variação da RAIS 2021→2022 do AFL com o saldo do Novo CAGED de 2022, como o próprio MTE fez para o total (depende do painel do CAGED).

## Calendário
Padrão do time (M do D_Calendario, mesmo das outras bases), como tabela importada no modelo local:
- intervalo de 01/01/2009 a 31/12 do ano corrente (a fato é DirectQuery e só tem `ano`, então o M não lê a data mínima/máxima dela);
- relação **muitos-para-muitos** `D_Calendario[Ano]` → `F_rais[ano]` e `F_Mediana[ano]` (filtro do calendário para a fato); a referência de estoque é 31/12 de cada ano;
- colunas extras: `Fonte RAIS` (RAIS declaratória até 2021, eSocial desde 2022) e `Trecho da série` (2009–2021 / 2022 em diante), para medidas e notas;
- `D_Ano` fica como está (vem do modelo publicado); os visuais usam o calendário, para alinhar com o RF e o CAGED (mensal).

## Proposta de estrutura (mesmo sistema visual do RF)
Navegação **Tema × Recorte** = 6 páginas; o ano é segmentador (padrão: último ano, 2025) e as séries mostram 2009–2025 com 2022 marcado.

| Tema | Pergunta | KPIs | Linha 2 | Capítulo 2 |
|---|---|---|---|---|
| **Empregos** | Quantos e se cresceu | Empregos em 31/12 (+ variação sobre o ano anterior) · participação no emprego formal (Todos: chip AFL) · crescimento médio ao ano | Estoque ano a ano (rótulo = % sobre o ano anterior; 2022 marcado) + composição por tipo de contrato/jornada | Ranking de divisões (AFL laranja, top 10) ou atividades do AFL + UF |
| **Quem trabalha** | Perfil | % mulheres · idade média (ou % até 24 anos) · % com médio completo ou mais (chip AFL) | Pirâmide etária por sexo + escolaridade | Raça/cor (sobre declarados) + ocupações principais (CBO) · primeiro emprego (até 2021) e intermitente (desde 2018) |
| **Quanto ganha** | Remuneração | Média e mediana em R$ reais (+ em salários mínimos) · razão mulheres/homens · razão negros/brancos | Série real da média e da mediana + por escolaridade | Diferença por sexo e cor (dentro da mesma escolaridade, para não confundir com composição) + por UF |

Manchetes no padrão do RF: sequência ("o emprego do AFL cresce há N anos"), contexto (pandemia de 2020, quebra de 2022) e comparação justa (AFL × Comparáveis por % e razão).

## Decisões (Sabino, 02/11/2026)
- **Estrutura:** 6 páginas (Empregos, Quem trabalha, Quanto ganha × Todos os setores, AFL), ano como segmentador.
- **Remuneração:** salário de **dezembro** (`salario_mensal` da linha mes = 'Dezembro' da gold, estoque em 31/12), **R$ nominais, sem deflação**. Média = `soma_salario_valido ÷ qtd_salario_valido` (regra de 0,3 a 150 SM; os vínculos fora da regra continuam no estoque). Mediana da `F_Mediana`. Rodapé das páginas de salário: **"Valores nominais, remuneração de dezembro"**.
- **Comparação:** a correta é sempre **AFL × Comparável** (`D_GrupoSetor[grupo_setor]`; Comparável já exclui o AFL); sem "Demais" e sem total do setor privado como referência. A página Todos os setores tem a caixa "Só os comparáveis ao AFL", como no RF, e toda comparação mostra os dois números (contra todos e contra Comparável), indicando que a correta é contra Comparável.
- **Primeiro emprego:** só existe até 2021 (a página diz isso).
- **Git:** repositório local; linha de base `1e574ff`, branch `feature/fundacao-modelo`.

## Fundação do modelo (scripts/modelo_base.py) — testada nas medidas
- `D_Calendario` (M padrão do time, 2009 → fim do ano corrente, + `Fonte RAIS` e `Trecho da Série`), relações muitos-para-muitos com `F_rais[ano]` e `F_Mediana[ano]`.
- `_medidas`: `Ano_Ref`, `Ano_Inicio_Trecho`, `Fonte_RAIS_Ref`, `Empregos`, `Empregos_Ref`, `Empregos_Ano_Anterior` (BLANK em 2009 e 2022), `Empregos_Var`, `Empregos_Var_Pct`, `Empregos_Inicio_Trecho`, `Empregos_Cresc_Medio_Ano` (dentro do trecho), `Remuneracao_Media`, `Remuneracao_Media_Ref`, `Remuneracao_Media_SM_Ref`, `Mediana_Disponivel`, `Remuneracao_Mediana_Ref` (F_Mediana com "Todos" nas dimensões sem filtro; BLANK com raça, idade, CNAE, município ou atributos do vínculo) e as versões `_AFL` / `_Comparavel`.
- Teste (`scripts/testar_base.py`), 2025: 60.688.704 empregos (+5,0% sobre 2024; +4,8% ao ano desde 2022); AFL 1.768.754 (+2,9%; +3,3% ao ano desde 2022) e Comparável 26.116.280; remuneração média AFL R$ 2.315,43 × Comparável R$ 3.627,69; mediana AFL R$ 2.037,27 × Comparável R$ 2.470,97. 2022 sem variação (quebra).
