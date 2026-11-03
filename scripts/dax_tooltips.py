"""Tooltips de página dos gráficos nativos (análise e contexto do ponto sobrevoado), no padrão visual do RF (design system v3).

O contexto de filtros do ponto (ano, UF, faixa de idade, divisão...) chega à página de tooltip; cada medida monta um cartão HTML: título do ponto,
linhas AFL / Comparáveis / Seleção atual (esta só fora da página AFL) e uma frase de leitura. Retorna (nome, doc, dax, pasta, formato, oculta).
"""
from dax_rais import G_AFL, G_COMP, esc, num, pct

P = "HTML\\Tooltips de gráficos"
LARANJA, CINZA, SEL, ROXO, VERDE = "#F58220", "#434446", "#98A2B3", "#7F56D9", "#17B26A"
EH_AFL = 'SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim"'


def txt(e):
    return esc(e)


def cab(titulo, sub):
    return ('"<div style=\'font-size:24px;line-height:30px;font-weight:600;\'>" & ' + txt(titulo) + ' & "</div>"'
            ' & "<div style=\'font-size:18px;line-height:24px;color:#667085;margin-top:2px;\'>" & ' + txt(sub) + ' & "</div>"')


def linha(cor, rotulo, valor, detalhe=None, mostrar="TRUE()"):
    """Linha com marcador de cor, rótulo, valor em destaque e detalhe opcional; some quando `mostrar` é falso."""
    det = (' & IF(ISBLANK(' + detalhe + '), "", "<div style=\'font-size:17px;color:#667085;margin-left:20px;\'>" & ' + txt(detalhe) + ' & "</div>")') if detalhe else ""
    return ('IF(' + mostrar + ', "<div style=\'margin-top:12px;\'><div style=\'display:flex;justify-content:space-between;align-items:baseline;font-size:20px;\'><span>'
            '<span style=\'display:inline-block;width:12px;height:12px;border-radius:3px;background:' + cor + ';margin-right:8px;\'></span>" & ' + txt(rotulo) + ' & "</span>'
            '<b style=\'font-size:22px;font-variant-numeric:tabular-nums;\'>" & ' + txt(valor) + ' & "</b></div>"' + det + ' & "</div>", "")')


def nota(expr):
    return ('IF(' + expr + ' = "", "", "<div style=\'margin-top:14px;padding:9px 12px;border-left:4px solid #F58220;border-radius:0 6px 6px 0;background:#FDF7F1;font-size:18px;line-height:25px;\'>" & ' + txt(expr) + ' & "</div>")')


def montar(vars_, titulo, sub, linhas_, frase="\"\""):
    corpo = ' & '.join([cab(titulo, sub)] + linhas_ + [nota("Leitura")])
    return (vars_ + "VAR Leitura = " + frase + "\nRETURN\n    \"<div role='group' style='font-family:Segoe UI,Arial,sans-serif;padding:18px 22px;box-sizing:border-box;color:#1D1E21;background:#FFFFFF;'>\" & "
            + corpo + ' & "</div>"')


def moeda(v):
    return f'IF(ISBLANK({v}), "—", "R$ " & FORMAT({v}, "#,0", "pt-BR"))'


def pp(a, b):
    """Diferença em pontos percentuais entre duas razões/percentuais (texto com sinal)."""
    return f'IF(ISBLANK({a}) || ISBLANK({b}), "", IF({a} >= {b}, "+", "−") & FORMAT(ABS({a} - {b}) * 100, "0.0", "pt-BR") & " p.p.")'


def medidas():
    m = []

    def add(nome, doc, dax):
        m.append((nome, doc, dax, P, None, False))

    # ---- Empregos: ano
    v = ("VAR A = SELECTEDVALUE(D_Calendario[Ano])\nVAR EA = [Empregos_Ref_AFL]\nVAR VA = [Empregos_Var_Pct_AFL]\nVAR EC = [Empregos_Ref_Comparavel]\nVAR VC = [Empregos_Var_Pct_Comparavel]\n"
         "VAR ES = [Empregos_Ref]\nVAR VS = [Empregos_Var_Pct]\nVAR PaginaAFL = " + EH_AFL + "\n")
    add("Tip_Emp_Ano_HTML", "Tooltip do ano na variação anual do emprego: empregos e variação do AFL, Comparáveis e seleção atual.",
        montar(v, '"31/12/" & A', 'IF(ISBLANK(VA), IF(A = 2022, "Sem comparação com 2021: nova fonte (eSocial)", "Primeiro ano da série"), "Variação sobre 31/12/" & (A - 1))',
               [linha(LARANJA, '"AFL"', num("EA"), f'IF(ISBLANK(VA), BLANK(), {pct("VA", True)})'), linha(CINZA, '"Comparáveis"', num("EC"), f'IF(ISBLANK(VC), BLANK(), {pct("VC", True)})'),
                linha(SEL, '"Seleção atual"', num("ES"), f'IF(ISBLANK(VS), BLANK(), {pct("VS", True)})', "NOT PaginaAFL")],
               'IF(ISBLANK(VA) || ISBLANK(VC), "", "Em " & A & ", o emprego do AFL " & IF(VA >= VC, "cresceu mais", "cresceu menos") & " que o dos Comparáveis (" & ' + pp("VA", "VC") + ' & ").")'))
    # ---- Empregos: divisão (Todos os setores)
    v = ("VAR N = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])\nVAR E = [Emp_Divisao]\nVAR Tot = [Empregos_Ref_Todos]\nVAR Pos = IF(NOT ISBLANK(E), RANKX(ALL(D_Rank_Divisao[nm_divisao]), [Emp_Divisao], , DESC, DENSE))\n"
         "VAR NDiv = [Emp_Total_Divisoes]\nVAR Peso = DIVIDE(E, Tot)\n")
    add("Tip_Emp_Divisao_HTML", "Tooltip da divisão no ranking de empregos: empregos, peso no emprego formal e posição.",
        montar(v, "N", '"Empregos em 31/12/" & [Ano_Ref]',
               [linha(CINZA, '"Empregos"', num("E")), linha(CINZA, '"Peso no emprego formal"', pct("Peso")), linha(CINZA, '"Posição no ranking"', 'IF(ISBLANK(Pos), "—", Pos & "º de " & NDiv)')],
               'IF(ISBLANK(Pos), "", IF(N = "AFL · conjunto de 6 CNAEs", "O AFL reúne seis atividades de alimentação fora do lar; as demais barras são divisões da CNAE.", "Divisão da CNAE (dois dígitos)."))'))
    # ---- Empregos: atividade (AFL)
    v = ("VAR N = SELECTEDVALUE(D_AflAtividade[nome])\nVAR E = [Empregos_Ref]\nVAR Tot = [Empregos_Ref_AFL]\nVAR Peso = DIVIDE(E, Tot)\nVAR Var = [Emp_Atividade_Var]\n"
         "VAR Pos = IF(NOT ISBLANK(E), RANKX(ALL(D_AflAtividade[nome]), [Empregos_Ref], , DESC, DENSE))\n")
    add("Tip_Emp_Atividade_HTML", "Tooltip da atividade do AFL: empregos, peso no AFL, variação e posição.",
        montar(v, "N", '"Empregos em 31/12/" & [Ano_Ref]',
               [linha(LARANJA, '"Empregos"', num("E"), f'IF(ISBLANK(Var), BLANK(), {pct("Var", True)} & " sobre o ano anterior")'), linha(LARANJA, '"Peso nos empregos do AFL"', pct("Peso")),
                linha(CINZA, '"Posição entre as atividades"', 'IF(ISBLANK(Pos), "—", Pos & "ª de 6")')]))
    # ---- Empregos: UF
    v = ("VAR UFNome = SELECTEDVALUE(D_UF[estado], SELECTEDVALUE(D_UF[uf]))\nVAR Mun = SELECTEDVALUE(F_rais[municipio])\nVAR UF = IF(ISBLANK(Mun), UFNome, Mun & \" · \" & SELECTEDVALUE(D_UF[uf]))\nVAR EA = [Empregos_Ref_AFL]\nVAR EC = [Empregos_Ref_Comparavel]\nVAR Peso = [Emp_UF_Peso_AFL]\n"
         "VAR ParteBR = DIVIDE(EA, CALCULATE([Empregos_Ref_AFL], REMOVEFILTERS(D_UF)))\n")
    add("Tip_Emp_UF_HTML", "Tooltip da UF: empregos do AFL e dos Comparáveis, peso do AFL e parte do AFL do país.",
        montar(v, "UF", '"Empregos em 31/12/" & [Ano_Ref]',
               [linha(LARANJA, '"AFL"', num("EA"), f'"Parte do AFL do país: " & {pct("ParteBR")}'), linha(CINZA, '"Comparáveis"', num("EC")), linha(CINZA, '"Peso do AFL nos Comparáveis"', pct("Peso"))],
               'IF(ISBLANK(Peso), "", "A cada 100 empregos de AFL + Comparáveis em " & UF & ", " & FORMAT(Peso * 100, "0", "pt-BR") & " são do AFL.")'))
    # ---- Quem trabalha: pirâmide
    v = ("VAR F = SELECTEDVALUE(D_FaixaIdade[faixa_idade])\nVAR E = [Empregos_Ref]\n"
         "VAR Mul = DIVIDE(CALCULATE([Empregos_Ref], KEEPFILTERS(D_Sexo[sexo] = \"Mulher\")), E)\n"
         "VAR MulC = CALCULATE(DIVIDE(CALCULATE([Empregos_Ref], KEEPFILTERS(D_Sexo[sexo] = \"Mulher\")), [Empregos_Ref]), " + G_COMP + ")\n"
         "VAR MulA = CALCULATE(DIVIDE(CALCULATE([Empregos_Ref], KEEPFILTERS(D_Sexo[sexo] = \"Mulher\")), [Empregos_Ref]), " + G_AFL + ")\n"
         "VAR TotFaixa = DIVIDE(E, CALCULATE([Empregos_Ref], REMOVEFILTERS(D_FaixaIdade)))\n")
    add("Tip_Pir_HTML", "Tooltip da pirâmide: empregos da faixa, peso da faixa e participação de mulheres (recorte, AFL e Comparáveis).",
        montar(v, '"Faixa de " & F & " anos"', '"Empregos em 31/12/" & [Ano_Ref]',
               [linha(CINZA, '"Empregos da faixa"', num("E"), f'"Peso da faixa no recorte: " & {pct("TotFaixa")}'), linha(ROXO, '"Mulheres na faixa (recorte)"', pct("Mul")),
                linha(LARANJA, '"Mulheres na faixa · AFL"', pct("MulA"), None, "NOT(" + EH_AFL + ")"), linha(CINZA, '"Mulheres na faixa · Comparáveis"', pct("MulC"))],
               'IF(ISBLANK(Mul), "", IF(Mul > 0.5, "As mulheres são maioria nesta faixa.", "Os homens são maioria nesta faixa."))'))
    # ---- Quem trabalha: ocupação (CBO)
    v = ("VAR O = SELECTEDVALUE(F_rais[cbo_2002])\nVAR E = [Empregos_Ref]\nVAR Peso = DIVIDE(E, CALCULATE([Empregos_Ref], REMOVEFILTERS(F_rais[cbo_2002])))\nVAR Mul = [Perf_Mulheres]\n"
         "VAR R = [Remuneracao_Media_Ref]\nVAR RGeral = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(F_rais[cbo_2002]))\nVAR Razao = DIVIDE(R, RGeral)\n")
    add("Tip_CBO_HTML", "Tooltip da ocupação (CBO): empregos, peso no recorte, mulheres e remuneração média.",
        montar(v, "O", '"Empregos em 31/12/" & [Ano_Ref]',
               [linha(CINZA, '"Empregos"', num("E"), f'"Peso no recorte: " & {pct("Peso")}'), linha(ROXO, '"Mulheres"', pct("Mul")),
                linha(VERDE, '"Remuneração média de dezembro"', moeda("R"), 'IF(ISBLANK(Razao), BLANK(), FORMAT(Razao, "0%", "pt-BR") & " da média do recorte")')],
               'IF(ISBLANK(Razao), "", IF(Razao >= 1, "Paga acima da média do recorte.", "Paga abaixo da média do recorte."))'))
    # ---- Quanto ganha: ano
    v = ("VAR A = SELECTEDVALUE(D_Calendario[Ano])\nVAR MA = [Remuneracao_Media_Ref_AFL]\nVAR MdA = [Remuneracao_Mediana_Ref_AFL]\nVAR MC = [Remuneracao_Media_Ref_Comparavel]\n"
         "VAR MdC = [Remuneracao_Mediana_Ref_Comparavel]\nVAR MS = [Remuneracao_Media_Ref]\nVAR Razao = DIVIDE(MA, MC)\nVAR PaginaAFL = " + EH_AFL + "\n")
    add("Tip_Rem_Ano_HTML", "Tooltip do ano na série de remuneração: média e mediana do AFL e dos Comparáveis.",
        montar(v, '"Dezembro de " & A', '"Remuneração de dezembro, R$ nominais"',
               [linha(LARANJA, '"AFL · média"', moeda("MA"), f'"Mediana " & {moeda("MdA")}'), linha(CINZA, '"Comparáveis · média"', moeda("MC"), f'"Mediana " & {moeda("MdC")}'),
                linha(SEL, '"Seleção atual · média"', moeda("MS"), None, "NOT PaginaAFL")],
               'IF(ISBLANK(Razao), "", "O AFL pagou, em média, " & FORMAT(Razao, "0%", "pt-BR") & " do que pagaram os Comparáveis. Valores nominais: não descontam a inflação.")'))
    # ---- Quanto ganha: escolaridade
    v = ("VAR E = SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada])\nVAR MA = [Rem_Esc_AFL]\nVAR MC = [Rem_Esc_Comp]\nVAR MS = [Rem_Esc_Sel]\nVAR Razao = DIVIDE(MA, MC)\n"
         "VAR NA = [Empregos_Ref_AFL]\nVAR PaginaAFL = " + EH_AFL + "\n")
    add("Tip_Rem_Esc_HTML", "Tooltip da escolaridade: média do AFL, dos Comparáveis e da seleção, e empregos do AFL.",
        montar(v, "E", '"Remuneração média de dezembro, R$ nominais"',
               [linha(LARANJA, '"AFL"', moeda("MA"), f'"Empregos do AFL: " & {num("NA")}'), linha(CINZA, '"Comparáveis"', moeda("MC")), linha(SEL, '"Seleção atual"', moeda("MS"), None, "NOT PaginaAFL")],
               'IF(ISBLANK(Razao), "", "Nesta escolaridade o AFL paga " & FORMAT(Razao, "0%", "pt-BR") & " da média dos Comparáveis.")'))
    # ---- Quanto ganha: razões (sexo e raça)
    for nome, a, b, ca, cb in (("Sexo", "mulheres", "homens", "Mulher", "Homem"), ("Raca", "negros", "brancos", "Negra", "Branca")):
        col = "D_Sexo[sexo]" if nome == "Sexo" else "D_Raca[grupo_raca]"
        tab = col.split("[")[0]
        def media(g, c):
            return f"CALCULATE([Remuneracao_Media_Ref], {g + ', ' if g else ''}REMOVEFILTERS({tab}), {col} = \"{c}\")"
        v = (f"VAR E = SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada])\nVAR RA = [Rem_Razao_{nome}_AFL]\nVAR RC = [Rem_Razao_{nome}_Comp]\nVAR RS = [Rem_Razao_{nome}]\n"
             f"VAR AA = {media(G_AFL, ca)}\nVAR AB = {media(G_AFL, cb)}\nVAR CA = {media(G_COMP, ca)}\nVAR CB = {media(G_COMP, cb)}\nVAR PaginaAFL = " + EH_AFL + "\n")
        add(f"Tip_Rem_Gap_{nome}_HTML", f"Tooltip da razão {a} ÷ {b} por escolaridade: razão e salários médios de cada grupo no AFL e nos Comparáveis.",
            montar(v, "E", f'"Salário dos {a} como % do dos {b}"',
                   [linha(LARANJA, '"AFL"', pct("RA"), f'"{a.capitalize()} " & {moeda("AA")} & " · {b} " & {moeda("AB")}'),
                    linha(CINZA, '"Comparáveis"', pct("RC"), f'"{a.capitalize()} " & {moeda("CA")} & " · {b} " & {moeda("CB")}'),
                    linha(SEL, '"Seleção atual"', pct("RS"), None, "NOT PaginaAFL")],
                   'IF(ISBLANK(RA) || ISBLANK(RC), "", "A diferença no AFL é " & IF(RA >= RC, "menor", "maior") & " que nos Comparáveis (" & ' + pp("RA", "RC") + ' & "). 100% = salários iguais.")'))
    # ---- Quanto ganha: UF
    v = ("VAR UFNome = SELECTEDVALUE(D_UF[estado], SELECTEDVALUE(D_UF[uf]))\nVAR Mun = SELECTEDVALUE(F_rais[municipio])\nVAR UF = IF(ISBLANK(Mun), UFNome, Mun & \" · \" & SELECTEDVALUE(D_UF[uf]))\nVAR M = [Remuneracao_Media_Ref]\nVAR MA = [Remuneracao_Media_Ref_AFL]\nVAR MC = [Remuneracao_Media_Ref_Comparavel]\nVAR Razao = [Rem_UF_Razao_Comp]\n"
         "VAR PaginaAFL = " + EH_AFL + "\n")
    add("Tip_Rem_UF_HTML", "Tooltip da UF na remuneração: média do recorte, do AFL e dos Comparáveis.",
        montar(v, "UF", '"Remuneração média de dezembro, R$ nominais"',
               [linha(SEL, '"Recorte da página"', moeda("M"), None, "NOT PaginaAFL"), linha(LARANJA, '"AFL"', moeda("MA")), linha(CINZA, '"Comparáveis"', moeda("MC"))],
               'IF(ISBLANK(Razao), "", "Em " & UF & " o AFL paga " & FORMAT(Razao, "0%", "pt-BR") & " da média dos Comparáveis.")'))
    # ---- Quem contrata: divisão, atividade, ano, UF
    v = ("VAR N = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])\nVAR V = [Ind_Valor_Div]\nVAR Afl = [Ind_Valor_AFL]\nVAR E = [Emp_Divisao]\nVAR Rot = [Ind_Rotulo]\n"
         "VAR Pos = IF(NOT ISBLANK(V), RANKX(ALL(D_Rank_Divisao[nm_divisao]), [Ind_Valor_Div], , DESC, DENSE))\nVAR NDiv = [Ind_Total_Divisoes]\n")
    add("Tip_Ind_Divisao_HTML", "Tooltip da divisão no ranking de contratação: valor do indicador, posição e diferença para o AFL.",
        montar(v, "N", '"Participação de " & Rot & " em " & [Ind_Ano]',
               [linha(CINZA, '"Na divisão"', pct("V"), f'"Posição: " & IF(ISBLANK(Pos), "—", Pos & "º de " & NDiv)'), linha(LARANJA, '"No AFL"', pct("Afl")), linha(CINZA, '"Empregos da divisão"', num("E"))],
               'IF(ISBLANK(V) || ISBLANK(Afl), "", IF(N = "AFL · conjunto de 6 CNAEs", "É o conjunto de seis atividades do AFL.", "O AFL está " & ' + pp("Afl", "V") + ' & " em relação a esta divisão."))'))
    v = ("VAR N = SELECTEDVALUE(D_AflAtividade[nome])\nVAR V = [Ind_Valor_Ctx]\nVAR Afl = [Ind_Valor_AFL]\nVAR E = [Empregos_Ref]\nVAR Rot = [Ind_Rotulo]\n")
    add("Tip_Ind_Atividade_HTML", "Tooltip da atividade do AFL: valor do indicador e comparação com o AFL inteiro.",
        montar(v, "N", '"Participação de " & Rot & " em " & [Ind_Ano]',
               [linha(LARANJA, '"Na atividade"', pct("V")), linha(CINZA, '"No AFL inteiro"', pct("Afl")), linha(CINZA, '"Empregos da atividade"', num("E"))],
               'IF(ISBLANK(V) || ISBLANK(Afl), "", "A atividade está " & ' + pp("V", "Afl") + ' & " em relação à média do AFL.")'))
    v = ("VAR A = SELECTEDVALUE(D_Calendario[Ano])\nVAR VA = CALCULATE([Ind_Valor_Ano], " + G_AFL + ")\nVAR VC = CALCULATE([Ind_Valor_Ano], " + G_COMP + ")\nVAR VS = [Ind_Valor_Ano]\nVAR Rot = [Ind_Rotulo]\n"
         "VAR PaginaAFL = " + EH_AFL + "\n")
    add("Tip_Ind_Ano_HTML", "Tooltip do ano na série do indicador de contratação.",
        montar(v, '"31/12/" & A', '"Participação de " & Rot',
               [linha(LARANJA, '"AFL"', pct("VA")), linha(CINZA, '"Comparáveis"', pct("VC")), linha(SEL, '"Seleção atual"', pct("VS"), None, "NOT PaginaAFL")],
               'IF(ISBLANK(VA) || ISBLANK(VC), "Sem dados para este indicador neste ano.", "O AFL está " & ' + pp("VA", "VC") + ' & " em relação aos Comparáveis.")'))
    v = ("VAR UFNome = SELECTEDVALUE(D_UF[estado], SELECTEDVALUE(D_UF[uf]))\nVAR Mun = SELECTEDVALUE(F_rais[municipio])\nVAR UF = IF(ISBLANK(Mun), UFNome, Mun & \" · \" & SELECTEDVALUE(D_UF[uf]))\nVAR V = [Ind_Valor_Ctx]\nVAR VA = [Ind_UF_AFL_Dica]\nVAR E = [Empregos_Ref]\nVAR EA = [Empregos_Ref_AFL]\nVAR Rot = [Ind_Rotulo]\n"
         "VAR PaginaAFL = " + EH_AFL + "\n")
    add("Tip_Ind_UF_HTML", "Tooltip da UF na contratação: valor do indicador no recorte e no AFL da UF.",
        montar(v, "UF", '"Participação de " & Rot & " em " & [Ind_Ano]',
               [linha(SEL, '"Recorte da página"', pct("V"), f'"Empregos: " & {num("E")}', "NOT PaginaAFL"), linha(LARANJA, '"AFL"', pct("VA"), f'"Empregos do AFL: " & {num("EA")}')],
               'IF(ISBLANK(V) || ISBLANK(VA) || PaginaAFL, "", "O AFL está " & ' + pp("VA", "V") + ' & " em relação ao recorte nesta UF.")'))
    return m


TOOLTIPS = {   # medida → (id da página, largura, altura)
    "Tip_Emp_Ano_HTML": ("a3d1f2c4e6b8097a1c71", 560, 400), "Tip_Emp_Divisao_HTML": ("a3d1f2c4e6b8097a1c72", 600, 380), "Tip_Emp_Atividade_HTML": ("a3d1f2c4e6b8097a1c73", 600, 380),
    "Tip_Emp_UF_HTML": ("a3d1f2c4e6b8097a1c74", 600, 400), "Tip_Pir_HTML": ("a3d1f2c4e6b8097a1c75", 600, 440), "Tip_CBO_HTML": ("a3d1f2c4e6b8097a1c76", 620, 420),
    "Tip_Rem_Ano_HTML": ("a3d1f2c4e6b8097a1c77", 600, 420), "Tip_Rem_Esc_HTML": ("a3d1f2c4e6b8097a1c78", 600, 400), "Tip_Rem_Gap_Sexo_HTML": ("a3d1f2c4e6b8097a1c79", 640, 440),
    "Tip_Rem_Gap_Raca_HTML": ("a3d1f2c4e6b8097a1c7a", 640, 440), "Tip_Rem_UF_HTML": ("a3d1f2c4e6b8097a1c7b", 600, 360), "Tip_Ind_Divisao_HTML": ("a3d1f2c4e6b8097a1c7c", 620, 420),
    "Tip_Ind_Atividade_HTML": ("a3d1f2c4e6b8097a1c7d", 600, 380), "Tip_Ind_Ano_HTML": ("a3d1f2c4e6b8097a1c7e", 560, 380), "Tip_Ind_UF_HTML": ("a3d1f2c4e6b8097a1c7f", 600, 360),
}
