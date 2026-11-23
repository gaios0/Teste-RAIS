# Painel RAIS · Emprego Formal (Observatório Abrasel)

Painel Power BI sobre o emprego formal no Brasil (RAIS, e eSocial desde 2022), com foco no **AFL** (alimentação fora do lar: seis atividades da CNAE) comparado aos setores **Comparáveis**.

## Onde está o painel

| Pasta | O que é |
|---|---|
| `RAIS OFICIAL/` | **Versão oficial.** Projeto PBIP (`RAIS Emprego Formal.pbip`): relatório em PBIR e modelo em TMDL. |
| `scripts/` | Scripts Python e PowerShell que geram e ajustam páginas, medidas e fundos. |
| `docs/` | Planejamento, handoff, fundos (`docs/fundos/`) e prévias (`docs/previa/`). |
| `_docs/` | Documentação do modelo gerada pela skill `pbi-doc` (`index.html` + 5 markdowns). |
| `assets/` | Imagens de apoio. |

Abra `RAIS OFICIAL/RAIS Emprego Formal.pbip` no Power BI Desktop. Na primeira abertura, clique em **Atualizar agora**: as tabelas locais (calendário, botões, textos) não ficam salvas no PBIP.

## Fonte de dados

- Modelo semântico `Painel_RAIS`, workspace `Testes`, lido em **DirectQuery para Analysis Services** (`expressions.tmdl`).
- A fato `F_rais` traz os vínculos ativos em 31/12, já agregados: `vinculos`, somas de salário e de idade válidos.
- Tabelas locais em M: calendário, botões, parâmetros e textos das dicas (i).

## Páginas

| Tema | Páginas |
|---|---|
| Empregos | Todos os setores · AFL |
| Quem trabalha | Todos os setores · AFL |
| Quanto ganha | Todos os setores · AFL |
| Ranking | Todos os setores · AFL |

As demais 29 páginas são ocultas: tooltips e dicas (i).

A página **Ranking** tem quatro rankings por divisão CNAE, com botões de valor (Representatividade ou Salário médio): mulheres, negros, escolaridade (por nível) e **deficiência** (Física, Auditiva, Visual, Intelectual, Múltipla, Reabilitado). Sem nível ou tipo escolhido, o ranking soma todos. Só entram divisões com 50 mil empregos ou mais; o AFL aparece sempre, em laranja.

## Modelo

- 28 tabelas (sem as de data automática) e 236 medidas, em `RAIS OFICIAL/RAIS Emprego Formal.SemanticModel/definition/`.
- Todas as medidas ficam na tabela `_medidas`, em pastas (displayFolder).
- Esquema estrela: `F_rais` no centro; `D_Cnae` liga a `D_GrupoSetor`, `D_Comparavel` e `D_AflAtividade`; `D_Calendario` liga a `F_rais[ano]` (muitos-para-muitos) e `D_Ano` filtra o calendário.

## Regras de cálculo

- **Ano de referência (`Ano_Ref`)**: o ano do filtro de ano (ou do eixo do gráfico); sem filtro, o último ano da base. Os outros filtros não trocam o ano: sem dados, o número fica vazio.
- **`D_Ano`** vai de 2009 ao ano corrente e cresce sozinha.
- **Quebra de 2022**: a fonte passa a ser o eSocial. A variação de 2022 sobre 2021 fica vazia e as linhas não atravessam a quebra. Primeiro emprego só existe até 2021; intermitente, desde 2018.
- **Remuneração**: salário de dezembro, R$ nominais, sem correção pela inflação; média = soma ÷ quantidade de salários válidos. Não há mediana (a base atual não tem a `F_Mediana`).
- **Totais das participações** deixam de fora o que não tem informação, para as faixas somarem 100%:
  - cor/raça: só quem declarou (`D_Raca[declarada] = "Sim"`);
  - escolaridade: sem `Ignorado/Faltante`;
  - faixa de idade: sem `Não categorizado`.
- **Negros = pretos + pardos.** O filtro de raça tem opções separadas: Negros (pretos + pardos), Preta, Parda, Branca, Amarela, Indígena e Não declarada (tabela `D_RacaFiltro`).
- Comparação de referência sempre **AFL × Comparáveis**.

## Scripts úteis

Rode a partir da raiz do repositório.

| Comando | O que faz |
|---|---|
| `python scripts/checar_painel.py` | Confere se os campos dos visuais e as colunas do DAX existem no modelo. Só lê. |
| `python scripts/limpar_medidas.py` | Lista medidas que nenhum visual ou tooltip usa (`--aplicar` apaga). |
| `python scripts/gerar_doc_pbi.py` | Gera de novo a documentação em `_docs/`. |
| `powershell -File scripts/validar_tmdl.ps1` | Carrega o modelo TMDL e mostra erros de estrutura. |
| `powershell -File scripts/dax_local.ps1 -Port <porta> -File <consulta.dax>` | Roda uma consulta DAX no modelo aberto no Desktop. Só lê. |

Atenção: vários scripts (`scripts/validar_tmdl.ps1`, `scripts/gerar_doc_pbi.py`, `scripts/limpar_medidas.py`, `scripts/checar_painel.py`) ainda apontam para o PBIP na raiz do repositório. Para usar no `RAIS OFICIAL/`, troque o caminho no começo do script. Os geradores antigos (`dax_*.py`, `ajustes_rais.py`, `modelo_base.py`) ainda têm medidas removidas: depois de rodar um deles, rode `limpar_medidas.py`.

## Como trabalhar

1. Feche o Power BI Desktop **sem salvar** antes de rodar um script que muda o PBIP, e abra de novo depois. Se salvar com a versão antiga aberta, o Desktop apaga as mudanças.
2. Mudanças vão para um branch `feature/...` e entram na `main` por pull request.
3. Detalhes de layout, cores e textos: `docs/handoff-atual.md`, `docs/planejamento-painel-rais.md` e o playbook em `.kiro/skills/playbook/`.
