# 04 · Regras de conteúdo e de dados

## Comunicação

- **Público:** executivos e imprensa leigos. Manchetes compreensíveis, sem jargão. Explique siglas (p.p., CBO, CNAE) no (i) ou no texto.
- **Manchete = afirmação com número**, não rótulo. Ex.: "No Brasil, o empregado tem em média 39,4 anos e 45,7% são mulheres; no AFL, 35,1 anos e 55,6%". Aceita até 2 linhas; nada de reticências no meio da frase.
- **Não deixe a página falar de um só tema sem avisar.** Em painéis com seletor de indicador (botões), a manchete e o título do ranking dizem qual indicador está ativo e mandam trocar nos botões.
- **Não escreva conclusão fixa em título dinâmico** ("a diferença é menor no AFL"): derive a frase dos números ou use texto neutro ("Mulheres ganham 87% do salário dos homens no AFL (Comparáveis: 79%)").
- **Percentual sempre com denominador claro** (título, subtítulo ou tooltip).
- **Diferença entre percentuais em pontos percentuais (p.p.)**, nunca "x%".
- Números em rankings **completos** (sem abreviar para mil/milhão), salvo decisão contrária.
- Nomes **oficiais** das divisões CNAE; abrevie só visualmente quando indispensável (o tooltip traz o nome inteiro).

## Dados

- **Estoque mensal/anual usa uma única competência.** Nunca some fotografias de períodos diferentes.
- **Quebra de série:** quando a fonte muda (RAIS declaratória → eSocial em 2022), as séries são interrompidas e a nota de rodapé explica. Não ligue os pontos, não calcule variação entre os dois lados, e declare "2022 não é comparável com 2021".
- **Valores monetários:** diga se são nominais ou reais. No RAIS, remuneração de **dezembro em R$ nominais**, sem correção pela inflação; rodapé: "Valores nominais, remuneração de dezembro". Média = soma ÷ quantidade de salários válidos (0,3 a 150 salários mínimos); a mediana vem pré-calculada por ano × setor × UF × sexo × escolaridade, e quando a combinação de filtros não permite, o painel mostra a média e avisa.
- **Piso estatístico em rankings** (RAIS: divisões com 50 mil empregos ou mais; UFs com 3 mil; municípios com 100 a 300). O piso é uma decisão a confirmar com a estatística e deve aparecer no texto.
- **Categorias sem informação** (ex.: raça/cor não declarada: 24 a 33% até 2022) ficam fora do percentual, e o texto diz "entre quem declarou".
- **Indicadores que só existem em parte da série** (primeiro emprego até 2021; trabalho intermitente desde 2018) declaram isso no gráfico/título e no (i).

## Universo AFL e Comparáveis

- **AFL** = conjunto de exatamente seis CNAEs: `4721102`, `5611201`, `5611203`, `5611204`, `5611205`, `5620104`. **Não pertencem:** `4721101` e `5611202`. A classificação mora na dimensão de CNAE (`D_CNAE`/`D_Cnae`) e em `dimensoes/tab_CNAE_Nova_com_setores (1).csv`; não recodifique.
- **Comparáveis** = setores de referência para o AFL (coluna `setor_comparavel_afl`). A comparação padrão é sempre **AFL × Comparáveis**. "Demais setores" e total privado só entram quando a pergunta exigir.
- No ranking de divisões, "AFL · conjunto de 6 CNAEs" é categoria sintética; a divisão ALIMENTAÇÃO mantém o nome oficial e contém os demais CNAEs da divisão 56; **sem dupla contagem**.
- Páginas em duas versões: **Todos os setores** (contexto de mercado, com "Seleção atual") e **AFL** (só o AFL, com Comparáveis de referência). **Revise a página "Todos os setores" gráfico a gráfico:** um gráfico que só repete o AFL ali é um erro de recorte (já ocorreu nos gráficos de UF, de série e de tabela).

## RAIS: o que o leitor precisa saber

- Estoque de vínculos em 31/12; conta **vínculos, não pessoas**; inclui setor público no total.
- Defasagem: o dado de um ano só sai cerca de um ano depois.
- Fonte desde 2022: eSocial (aumentou a cobertura; a nota técnica do MTE estima que boa parte do salto de 2022 é cobertura, não emprego novo). O grupo público entra em 2023.
- Idade, escolaridade e cor/raça são declaradas no vínculo.

## Cores com significado

Ver `01`. Resumo: laranja = AFL/ação; verde = positivo; vermelho = negativo; cinza = referência/neutro; roxo = mulheres. Uma cor, um significado.
