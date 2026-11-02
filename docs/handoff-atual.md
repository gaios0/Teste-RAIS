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
