"""Textos dos (i) do painel RAIS: tabela D_Info (uma linha por cartão de cada página), no mesmo padrão do RF.

Cada cartão (KPI 1–3, L2A, L2B, L3A, L3B) de cada página recebe um (i) desenhado no fundo e um gatilho transparente; o tooltip compartilhado
(Info_Texto_HTML, 3 tamanhos) lê a linha da chave da página e do cartão. Cartões cujo tooltip precisa de números calculados (exemplos) usam páginas de
dica dedicadas (dax_dicas.py) e não entram aqui.
"""
CARTOES = ["K1", "K2", "K3", "L2A", "L2B", "L3A", "L3B"]
LARANJA, CINZA, VERDE, ROXO = "#F58220", "#434446", "#17B26A", "#7F56D9"
FUNDO = {LARANJA: "#FDF7F1", CINZA: "#F2F4F7", VERDE: "#ECFDF3", ROXO: "#F4EBFF"}

FONTE = "RAIS (Relação Anual de Informações Sociais), estoque de vínculos em 31 de dezembro; desde 2022 os dados vêm do eSocial."
QUEBRA = "Em 2022 a fonte passou a ser o eSocial e incluiu empregos que a RAIS antiga não captava: 2022 em diante não se compara com os anos anteriores, por isso as linhas são interrompidas."
COMP = "Comparáveis são os setores usados como referência para o AFL; AFL é o conjunto de seis atividades de alimentação fora do lar."

# (titulo, destaque, [parágrafos], cor)   -- chave: (tema, cartão)
T = {
    ("Empregos", "K1"): ("Empregos formais", "Vínculos de emprego ativos em 31 de dezembro do ano escolhido.",
                         [FONTE, "Conta vínculos, não pessoas: quem tem dois empregos formais aparece duas vezes.", "Os filtros da página (setor, divisão, UF, sexo, escolaridade, raça/cor) recortam o número."], VERDE),
    ("Empregos", "K2", ): ("Peso do AFL", "Quanto o AFL representa no emprego formal.",
                           ["Mostra o AFL como parte dos Comparáveis (AFL ÷ AFL + Comparáveis) e como parte de todo o emprego formal do país.", COMP], LARANJA),
    ("Empregos", "K3"): ("Crescimento médio ao ano", "Ritmo anual médio do emprego desde o início do período em análise.",
                         ["É a taxa composta: a taxa constante ao ano que levaria do emprego do início do trecho ao do ano escolhido.", QUEBRA], CINZA),
    ("Empregos", "L2A"): ("Variação anual do emprego", "Cada coluna é a variação do emprego de 31/12 sobre 31/12 do ano anterior.",
                          ["Passe o mouse sobre um ano para ver os empregos de cada grupo e a variação.", "2009 não tem ano anterior na série e 2022 não é comparável com 2021: essas colunas ficam vazias.", QUEBRA], LARANJA),
    ("Empregos", "L2B"): ("Tipos de contrato", "Participação de cada tipo de contrato nos empregos de 31/12.",
                          ["As categorias não se sobrepõem: cada vínculo entra em uma só (intermitente, aprendiz, tempo parcial, CLT por prazo indeterminado e prazo determinado ou temporário).", "Compara o AFL com os Comparáveis."], CINZA),
    ("Empregos", "L3A"): ("Ranking de empregos", "Quem mais emprega: divisões da CNAE (todos os setores) ou atividades do AFL.",
                          ["Divisão é o segundo nível da classificação CNAE (dois dígitos). O AFL aparece como um conjunto de seis atividades, em laranja.", "Use o modo foco (ícone no canto do gráfico) para ver todas as linhas."], LARANJA),
    ("Empregos", "L3B"): ("Empregos por UF", "Distribuição geográfica do emprego.",
                          ["Na página Todos os setores, mostra onde o AFL pesa mais no emprego dos Comparáveis; na página AFL, quanto cada UF concentra do emprego do AFL.",], CINZA),
    ("Quem trabalha", "K1"): ("Mulheres no emprego", "Percentual dos empregos de 31/12 ocupados por mulheres.",
                              [FONTE, "No AFL e nos Comparáveis aparecem como referência nos chips abaixo do número."], ROXO),
    ("Quem trabalha", "K2"): ("Jovens e idade média", "Percentual de empregados com até 24 anos (14 a 24).",
                              ["Abaixo do número, a idade média dos empregados no ano escolhido e no início do trecho.", "Idade registrada no vínculo em 31/12."], LARANJA),
    ("Quem trabalha", "K3"): ("Ensino médio ou mais", "Percentual dos empregados com ensino médio completo ou nível superior (completo ou não).",
                              ["Abaixo do número, a parcela com ensino superior (completo ou incompleto).", "Escolaridade declarada pelo empregador."], CINZA),
    ("Quem trabalha", "L2A"): ("Pirâmide por sexo e idade", "Cada barra é o percentual do total de empregos em uma faixa de idade e sexo.",
                               ["Mulheres à esquerda, homens à direita. As barras somam 100% do emprego do recorte.", "Passe o mouse para ver os Comparáveis como referência."], ROXO),
    ("Quem trabalha", "L2B"): ("Escolaridade", "Distribuição dos empregos por nível de escolaridade, AFL × Comparáveis.",
                               ["Quatro níveis: até fundamental, médio incompleto, médio completo e superior (completo ou não)."], CINZA),
    ("Quem trabalha", "L3A"): ("Ocupações (CBO)", "As ocupações com mais empregos, pela Classificação Brasileira de Ocupações.",
                               ["Mostra as primeiras ocupações; use o modo foco (ícone no canto do gráfico) para ver todas as ocupações do recorte.", "Passe o mouse para ver a participação de mulheres e a remuneração média de dezembro."], LARANJA),
    ("Quem trabalha", "L3B"): ("Cor ou raça", "Distribuição por cor ou raça entre os empregados que declararam.",
                               ["Até 2022, de 24% a 33% dos empregados não declaravam cor ou raça; os percentuais são calculados sobre quem declarou.", "Negros = pretos e pardos."], CINZA),
    ("Quanto ganha", "K1"): ("Remuneração mediana", "Metade dos empregados ganha menos que este valor e metade ganha mais.",
                             ["Remuneração de dezembro, em R$ nominais (sem correção pela inflação).", "A mediana existe para setor, UF, sexo e escolaridade; para outras combinações o painel mostra a média."], VERDE),
    ("Quanto ganha", "K2"): ("Mulheres ÷ homens", "Remuneração média das mulheres como percentual da dos homens.", ["100% significa salários iguais."], ROXO),
    ("Quanto ganha", "K3"): ("Negros ÷ brancos", "Remuneração média dos negros como percentual da dos brancos.", ["Só entram empregados que declararam cor ou raça."], LARANJA),
    ("Quanto ganha", "L2A"): ("Remuneração ao longo dos anos", "Linha cheia: média. Linha tracejada: mediana.",
                              ["Remuneração de dezembro em R$ nominais, sem correção pela inflação; a comparação entre anos distantes mistura inflação e ganho real.",
                               "A média usa só salários válidos (de 0,3 a 150 salários mínimos).", QUEBRA], LARANJA),
    ("Quanto ganha", "L2B"): ("Média por escolaridade", "Remuneração média de dezembro por nível de escolaridade.",
                              ["Compara o AFL com os Comparáveis (e, na página Todos os setores, com a seleção atual).", "Escolaridades sem informação ficam de fora."], CINZA),
    ("Quanto ganha", "L3A"): ("Diferenças por sexo e por cor", "Cada barra é a remuneração de um grupo como percentual da do outro, por escolaridade.",
                              ["Esquerda: salário das mulheres como % do dos homens. Direita: salário dos negros como % do dos brancos.", "100% = salários iguais. Comparar dentro da mesma escolaridade tira o efeito de diferenças de instrução."], ROXO),
    ("Quanto ganha", "L3B"): ("Remuneração por UF", "Remuneração média de dezembro nas 10 UFs com a maior média.",
                              ["Passe o mouse para ver quanto o AFL paga em relação aos Comparáveis na UF.", "Use o modo foco para ver todas as UFs."], CINZA),
    ("Quem contrata", "K1"): ("Posição no ranking", "Onde o AFL fica entre as divisões da CNAE no indicador escolhido.",
                              ["Só entram divisões com 50 mil empregos ou mais. Troque o indicador nos botões acima do ranking."], LARANJA),
    ("Quem contrata", "K2"): ("Diferença para os Comparáveis", "AFL menos Comparáveis, em pontos percentuais.", ["Ponto percentual é a diferença entre dois percentuais."], VERDE),
    ("Quem contrata", "K3"): ("Maior valor", "A divisão (ou atividade do AFL) com o maior valor do indicador.", ["Divisões com 50 mil empregos ou mais."], CINZA),
    ("Quem contrata", "L2A"): ("Ranking do indicador", "Participação do indicador escolhido em cada divisão, ou em cada atividade do AFL.",
                               ["Os sete botões trocam o indicador de toda a página: primeiro emprego (só até 2021), mulheres, até 24 anos, 55 anos ou mais, superior, negros e intermitente (desde 2018).",
                                "Mostra as 10 maiores divisões e sempre o AFL, em laranja. Use o modo foco para ver mais."], LARANJA),
    ("Quem contrata", "L2B"): ("Indicador ao longo dos anos", "Evolução do indicador escolhido, AFL × Comparáveis.",
                               ["Primeiro emprego só existe até 2021 (o eSocial não registra o tipo de admissão) e intermitente, desde 2018 (reforma trabalhista).", QUEBRA], CINZA),
    ("Quem contrata", "L3A"): ("Os sete indicadores", "Todos os indicadores lado a lado, no ano escolhido.",
                               ["Na página Todos os setores, a coluna Seleção atual mostra o recorte dos filtros (mercado inteiro, setores ou divisão)."], VERDE),
    ("Quem contrata", "L3B"): ("Indicador por UF", "Onde o indicador escolhido é maior.",
                               ["Só UFs com 3 mil empregos ou mais no recorte. Na página Todos os setores, o tooltip mostra o valor do AFL na UF."], CINZA),
}

# cartões que usam página de dica dedicada (números calculados) e, por isso, não entram no D_Info: (tema, recorte, cartão)
DEDICADOS = {("Quanto ganha", "Todos os setores", "K1"): "Tip_Mediana_HTML", ("Quanto ganha", "AFL", "K1"): "Tip_Mediana_HTML",
             ("Quanto ganha", "Todos os setores", "K2"): "Tip_RazaoSexo_HTML", ("Quanto ganha", "AFL", "K2"): "Tip_RazaoSexo_HTML",
             ("Quanto ganha", "Todos os setores", "K3"): "Tip_RazaoRaca_HTML", ("Quanto ganha", "AFL", "K3"): "Tip_RazaoRaca_HTML",
             ("Quem contrata", "Todos os setores", "K1"): "Tip_Contrata_Pos_HTML",
             ("Quem contrata", "Todos os setores", "K2"): "Tip_Contrata_Dif_HTML", ("Quem contrata", "AFL", "K2"): "Tip_Contrata_Dif_HTML",
             ("Quem contrata", "Todos os setores", "K3"): "Tip_Contrata_Max_Total_HTML", ("Quem contrata", "AFL", "K3"): "Tip_Contrata_Max_AFL_HTML"}


def chave(tema, recorte, cartao):
    return f"{tema}|{'AFL' if recorte == 'AFL' else 'Todos'}|{cartao}"


def classe(titulo, destaque, ps):
    n = len(titulo) + len(destaque) + sum(len(p) for p in ps)
    return "P" if n < 330 else ("M" if n < 560 else "G")


def linhas():
    """Linhas da D_Info: Chave, Classe, Titulo, Extra, Destaque, CorBorda, CorFundo, P1..P5."""
    saida = []
    for (tema, cartao), (titulo, destaque, ps, cor) in T.items():
        for rec in ("Todos os setores", "AFL"):
            if (tema, rec, cartao) in DEDICADOS:
                continue
            ps2 = list(ps) + [""] * (5 - len(ps))
            saida.append((chave(tema, rec, cartao), classe(titulo, destaque, ps), titulo, "", destaque, cor, FUNDO[cor], *ps2))
    return saida


COLUNAS = ["Chave", "Classe", "Titulo", "Extra", "Destaque", "CorBorda", "CorFundo", "P1", "P2", "P3", "P4", "P5"]
