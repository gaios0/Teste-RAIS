"""DAX da aba Quem contrata: qual divisão (ou atividade do AFL) mais emprega mulheres, jovens, mais velhos, primeiro emprego etc.

O indicador vem do segmentador de botões (D_Indicador, local e desconectada). Um só cálculo-base (Ind_Valor_Ctx) vale para qualquer categoria do
contexto; o ranking de divisões o avalia por divisão (e pelo conjunto AFL). Piso de 50 mil empregos por divisão (a confirmar com a estatística).
"""
from dax_rais import (ANO_FIXO, AFL_ROTULO, G_AFL, G_COMP, chip_afl, chip_ref, esc, kpi_html, num, pct, titulo_html)

def kpi_v(*a, **k):
    """kpi_html precedido de uma VAR (medida sem VAR própria não pode começar com RETURN)."""
    return "VAR _A = [Ano_Ref]\n" + kpi_html(*a, **k)


P = "Quem contrata"
PISO = 50000
INDICADORES = ["Primeiro emprego", "Mulheres", "Até 24 anos", "55 anos ou mais", "Superior", "Negros", "Intermitente"]
FRASE = {"Primeiro emprego": "dos empregados estavam no primeiro emprego", "Mulheres": "dos empregados são mulheres", "Até 24 anos": "dos empregados têm até 24 anos",
         "55 anos ou mais": "dos empregados têm 55 anos ou mais", "Superior": "dos empregados têm superior (completo ou não)", "Negros": "dos empregados que declararam cor são negros",
         "Intermitente": "dos empregados têm contrato intermitente"}
LONGO = {"Primeiro emprego": "primeiro emprego", "Mulheres": "mulheres", "Até 24 anos": "jovens até 24 anos", "55 anos ou mais": "empregados com 55 anos ou mais",
         "Superior": "superior (completo ou não)", "Negros": "negros (entre quem declarou cor)", "Intermitente": "contrato intermitente"}
ATRIB = {   # indicador: (filtro do numerador, filtro do denominador ou None)
    "Primeiro emprego": ('KEEPFILTERS(F_rais[tipo_admissao] = "Primeiro Emprego")', None),
    "Mulheres": ('KEEPFILTERS(D_Sexo[sexo] = "Mulher")', None),
    "Até 24 anos": ('KEEPFILTERS(D_FaixaIdade[faixa_idade] IN {"14-17", "18-24"})', None),
    "55 anos ou mais": ('KEEPFILTERS(D_FaixaIdade[faixa_idade] IN {"55-64", "65+"})', None),
    "Superior": ('KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"})', None),
    "Negros": ('KEEPFILTERS(D_Raca[grupo_raca] = "Negra")', 'KEEPFILTERS(D_Raca[declarada] = "Sim")'),
    "Intermitente": ('KEEPFILTERS(F_rais[trabalho_intermitente] = "Sim")', None),
}


def valor(a_expr):
    """Participação do indicador escolhido no contexto, no ano calculado por a_expr (BLANK quando o indicador não existe no ano)."""
    ramos = ""
    for nome, (n, d) in ATRIB.items():
        den = f"CALCULATE([Empregos], {ANO_FIXO.format(a='A')}, {d})" if d else f"CALCULATE([Empregos], {ANO_FIXO.format(a='A')})"
        ramos += f"    \"{nome}\", DIVIDE(CALCULATE([Empregos], {ANO_FIXO.format(a='A')}, {n}), {den}),\n"
    return ("VAR Ind = [Ind_Atual]\nVAR A = " + a_expr + "\nRETURN IF(ISBLANK(A), BLANK(), SWITCH(Ind,\n" + ramos + "    BLANK()))")


def medidas():
    m = []

    def add(nome, doc, dax, pasta, fmt=None, oculta=False):
        m.append((nome, doc, dax, pasta, fmt, oculta))
    add("Ind_Atual", "Indicador escolhido nos botões (padrão: Mulheres).", 'COALESCE(SELECTEDVALUE(D_Indicador[indicador]), "Mulheres")', f"{P}\\Apoio", None, True)
    add("Ind_Rotulo", "Nome do indicador por extenso.", "SWITCH([Ind_Atual], " + ", ".join(f'"{k}", "{v}"' for k, v in LONGO.items()) + ', "")', f"{P}\\Apoio", None, True)
    add("Ind_Frase", "Frase do indicador para as manchetes.", "SWITCH([Ind_Atual], " + ", ".join(f'"{k}", "{v}"' for k, v in FRASE.items()) + ', "")', f"{P}\\Apoio", None, True)
    add("Ind_Ano", "Ano de cálculo do indicador no ranking: primeiro emprego só existe até 2021 (usa o menor entre o ano e 2021); intermitente, desde 2018.",
        "VAR A = [Ano_Ref]\nVAR Ind = [Ind_Atual]\nRETURN IF(ISBLANK(A), BLANK(), IF(Ind = \"Primeiro emprego\", MIN(A, 2021), IF(Ind = \"Intermitente\" && A < 2018, BLANK(), A)))", f"{P}\\Apoio", "0", True)
    add("Ind_Valor_Ctx", "Participação do indicador escolhido no contexto (categoria do visual, filtros e grupo), no ano do ranking.", valor("[Ind_Ano]"), f"{P}\\Indicadores", "0.0%")
    add("Ind_Valor_Ano", "Participação do indicador escolhido no ano do contexto (para séries; primeiro emprego só até 2021 e intermitente desde 2018).",
        valor("IF(([Ind_Atual] = \"Primeiro emprego\" && [Ano_Ref] > 2021) || ([Ind_Atual] = \"Intermitente\" && [Ano_Ref] < 2018), BLANK(), [Ano_Ref])"), f"{P}\\Indicadores", "0.0%")
    add("Ind_Valor_AFL", "Indicador escolhido, só do AFL.", f"CALCULATE([Ind_Valor_Ctx], {G_AFL})", f"{P}\\Indicadores", "0.0%")
    add("Ind_Valor_Comp", "Indicador escolhido, só dos Comparáveis.", f"CALCULATE([Ind_Valor_Ctx], {G_COMP})", f"{P}\\Indicadores", "0.0%")
    # série
    for suf, g, nome in (("AFL", G_AFL, "AFL"), ("Comp", G_COMP, "Comparáveis")):
        for tr, cond in (("Pre", "A < 2022"), ("Pos", "A >= 2022")):
            add(f"Ind_Serie_{suf}_{tr}", f"Indicador escolhido ao longo dos anos, {nome}, trecho {tr}.",
                f"VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A) && {cond}, CALCULATE([Ind_Valor_Ano], {g}))", f"{P}\\Séries", "0.0%")
    # ranking de divisões
    den = ("VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])\nVAR A = [Ind_Ano]\n"
           f"VAR Den = IF(Nome = \"{AFL_ROTULO}\", CALCULATE([Empregos], {G_AFL}, {ANO_FIXO.format(a='A')}),\n"
           "    CALCULATE([Empregos], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[nm_divisao] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = \"Não\"), " + ANO_FIXO.format(a="A") + "))\n"
           f"VAR Val = IF(Nome = \"{AFL_ROTULO}\", CALCULATE([Ind_Valor_Ctx], {G_AFL}),\n"
           "    CALCULATE([Ind_Valor_Ctx], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[nm_divisao] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = \"Não\")))\n")
    add("Ind_Valor_Div", f"Indicador escolhido por divisão (item AFL = seis CNAEs); só divisões com {PISO:,} empregos ou mais.".replace(",", "."),
        den + f"RETURN IF(ISBLANK(Nome) || ISBLANK(A) || Den < {PISO}, BLANK(), Val)", f"{P}\\Ranking", "0.0%")
    add("Ind_Divisao_Top", "Valor do ranking: as 10 maiores divisões no indicador e sempre o AFL; as demais voltam BLANK.",
        f"VAR EhAFL = SELECTEDVALUE(D_Rank_Divisao[nm_divisao]) = \"{AFL_ROTULO}\"\nVAR V = [Ind_Valor_Div]\n"
        "VAR R = IF(NOT ISBLANK(V), RANKX(ALLSELECTED(D_Rank_Divisao[nm_divisao]), [Ind_Valor_Div], , DESC, DENSE))\nRETURN IF(NOT ISBLANK(V) && (EhAFL || R <= 10), V)", f"{P}\\Ranking", "0.0%")
    add("Cor_Ind_Divisao", "Cor do ranking: AFL em laranja, demais em cinza.", f"IF(SELECTEDVALUE(D_Rank_Divisao[nm_divisao]) = \"{AFL_ROTULO}\", \"#F58220\", \"#DDDDDE\")", f"{P}\\Ranking", None, True)
    add("Ind_Posicao_AFL", "Posição do AFL entre todas as divisões no indicador escolhido.",
        "VAR T = FILTER(ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), \"@v\", [Ind_Valor_Div]), NOT ISBLANK([@v]))\n"
        f"VAR VA = MAXX(FILTER(T, [nm_divisao] = \"{AFL_ROTULO}\"), [@v])\nRETURN IF(NOT ISBLANK(VA), COUNTROWS(FILTER(T, [@v] > VA)) + 1)", f"{P}\\Ranking", "0", True)
    add("Ind_Total_Divisoes", "Quantidade de divisões com o indicador calculável.", "COUNTROWS(FILTER(ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), \"@v\", [Ind_Valor_Div]), NOT ISBLANK([@v])))", f"{P}\\Ranking", "0", True)
    add("Ind_Maior_Divisao", "Nome da divisão com o maior valor do indicador.",
        "VAR T = FILTER(ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), \"@v\", [Ind_Valor_Div]), NOT ISBLANK([@v]) && [nm_divisao] <> \"" + AFL_ROTULO + "\")\n"
        "RETURN CONCATENATEX(TOPN(1, T, [@v], DESC, [nm_divisao], ASC), [nm_divisao], \"\")", f"{P}\\Ranking", None, True)
    add("Ind_Maior_Valor", "Maior valor do indicador entre as divisões.",
        "VAR T = FILTER(ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), \"@v\", [Ind_Valor_Div]), NOT ISBLANK([@v]) && [nm_divisao] <> \"" + AFL_ROTULO + "\")\nRETURN MAXX(T, [@v])", f"{P}\\Ranking", "0.0%", True)
    # atividades do AFL (página AFL)
    add("Ind_Atividade_Lider", "Atividade do AFL com o maior valor do indicador.",
        "VAR T = FILTER(ADDCOLUMNS(VALUES(D_AflAtividade[nome]), \"@v\", [Ind_Valor_Ctx]), NOT ISBLANK([@v]))\nRETURN CONCATENATEX(TOPN(1, T, [@v], DESC, D_AflAtividade[nome], ASC), D_AflAtividade[nome], \"\")", f"{P}\\Atividades", None, True)
    add("Ind_Atividade_Lider_Valor", "Maior valor do indicador entre as atividades do AFL.",
        "VAR T = FILTER(ADDCOLUMNS(VALUES(D_AflAtividade[nome]), \"@v\", [Ind_Valor_Ctx]), NOT ISBLANK([@v]))\nRETURN MAXX(T, [@v])", f"{P}\\Atividades", "0.0%", True)
    # UFs (AFL)
    add("Ind_UF_Top", "Indicador escolhido por UF, só do AFL (10 maiores UFs; só UFs com 3 mil empregos do AFL ou mais).",
        f"VAR IA = [Ind_Ano]\nVAR Den = CALCULATE([Empregos], {G_AFL}, {ANO_FIXO.format(a='IA')})\nVAR V = IF(Den >= 3000, CALCULATE([Ind_Valor_Ctx], {G_AFL}))\n"
        "VAR R = IF(NOT ISBLANK(V), RANKX(ALLSELECTED(D_UF[uf]), CALCULATE([Ind_Valor_Ctx], " + G_AFL + "), , DESC, DENSE))\nRETURN IF(NOT ISBLANK(V) && R <= 10, V)", f"{P}\\UF", "0.0%")
    # títulos e KPIs
    for u in ("Total", "AFL"):
        pos = "VAR Pos = [Ind_Posicao_AFL]\nVAR N = [Ind_Total_Divisoes]\n"
        if u == "Total":
            add(f"Manchete_Contrata_{u}_HTML", "Manchete da aba Quem contrata (Todos os setores).",
                pos + "VAR A = [Ind_Ano]\nVAR Afl = [Ind_Valor_AFL]\nVAR Comp = [Ind_Valor_Comp]\nVAR Rot = [Ind_Rotulo]\nVAR Frase = [Ind_Frase]\n"
                "VAR Texto = IF(ISBLANK(Pos), \"O AFL não tem dados de \" & Rot & \" para os filtros escolhidos\", \"Em \" & Rot & \", o AFL é o \" & Pos & \"º entre as \" & N & \" divisões: \" & " + pct("Afl") + " & \" \" & Frase & \", contra \" & " + pct("Comp") + " & \" nos Comparáveis\")\n"
                "VAR Contexto = \"31/12/\" & A & IF([Ind_Atual] = \"Primeiro emprego\", \" (último ano com a informação)\", \"\") & \" · Brasil · divisões com \" & FORMAT(" + str(PISO) + ", \"#,0\", \"pt-BR\") & \" empregos ou mais · RAIS\"\n"
                "VAR Valido = NOT ISBLANK(A)\nRETURN IF(NOT Valido, \"<div role='text' style='width:100%;height:118px;font-family:Segoe UI,Arial,sans-serif;font-size:24px;color:#434446;'>Não há dados para os filtros selecionados.</div>\",\n"
                "    \"<div role='group' aria-label='Quem mais contrata' style='width:100%;height:118px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>\"\n"
                "        & \"<div style='height:48px;display:flex;align-items:center;white-space:nowrap;overflow:hidden;'><span style='min-width:0;font-size:36px;line-height:42px;font-weight:600;font-variant-numeric:tabular-nums;overflow:hidden;text-overflow:ellipsis;'>\" & " + esc("Texto") + " & \"</span></div>\"\n"
                "        & \"<div style='height:30px;margin:4px 0 0;font-size:24px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>\" & " + esc("Contexto") + " & \"</div></div>\")", f"HTML\\{P}")
        else:
            add(f"Manchete_Contrata_{u}_HTML", "Manchete da aba Quem contrata (AFL).",
                "VAR A = [Ind_Ano]\nVAR Afl = [Ind_Valor_AFL]\nVAR Comp = [Ind_Valor_Comp]\nVAR Rot = [Ind_Rotulo]\nVAR Frase = [Ind_Frase]\nVAR Lider = [Ind_Atividade_Lider]\nVAR VL = [Ind_Atividade_Lider_Valor]\n"
                "VAR Texto = IF(ISBLANK(A) || ISBLANK(Afl), \"O AFL não tem dados de \" & Rot & \" para os filtros escolhidos\", \"No AFL, \" & " + pct("Afl") + " & \" \" & Frase & \" (Comparáveis: \" & " + pct("Comp") + " & \"); a maior participação é em \" & Lider & \": \" & " + pct("VL") + ")\n"
                "VAR Contexto = \"31/12/\" & A & IF([Ind_Atual] = \"Primeiro emprego\", \" (último ano com a informação)\", \"\") & \" · Brasil · alimentação fora do lar (AFL) · RAIS\"\n"
                "RETURN IF(ISBLANK(A), \"<div role='text' style='width:100%;height:118px;font-family:Segoe UI,Arial,sans-serif;font-size:24px;color:#434446;'>Não há dados para os filtros selecionados.</div>\",\n"
                "    \"<div role='group' aria-label='Quem mais contrata' style='width:100%;height:118px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>\"\n"
                "        & \"<div style='height:48px;display:flex;align-items:center;white-space:nowrap;overflow:hidden;'><span style='min-width:0;font-size:36px;line-height:42px;font-weight:600;font-variant-numeric:tabular-nums;overflow:hidden;text-overflow:ellipsis;'>\" & " + esc("Texto") + " & \"</span></div>\"\n"
                "        & \"<div style='height:30px;margin:4px 0 0;font-size:24px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>\" & " + esc("Contexto") + " & \"</div></div>\")", f"HTML\\{P}")
        # KPIs
        if u == "Total":
            add(f"KPI_Contrata1_{u}_HTML", "KPI 1: posição do AFL no ranking de divisões.",
                pos + "VAR Afl = [Ind_Valor_AFL]\nVAR Comp = [Ind_Valor_Comp]\n" +
                kpi_html("KPI de posição do AFL", '"Posição do AFL entre as divisões"', 'IF(ISBLANK(Pos), "—", Pos & "º")', 'IF(ISBLANK(Pos), "sem dados no indicador", "de " & N & " divisões · " & [Ind_Rotulo])', '"#434446"', chip_afl(pct("Afl"))), f"HTML\\{P}\\KPIs")
        else:
            add(f"KPI_Contrata1_{u}_HTML", "KPI 1: valor do indicador no AFL.",
                "VAR Afl = [Ind_Valor_AFL]\nVAR Comp = [Ind_Valor_Comp]\n" +
                kpi_html("KPI do indicador no AFL", '"No AFL"', pct("Afl"), '[Ind_Rotulo]', '"#434446"', chip_ref(pct("Comp"))), f"HTML\\{P}\\KPIs")
        add(f"KPI_Contrata2_{u}_HTML", "KPI 2: diferença do AFL para os Comparáveis em pontos percentuais.",
            "VAR Afl = [Ind_Valor_AFL]\nVAR Comp = [Ind_Valor_Comp]\nVAR Dif = (Afl - Comp) * 100\n" +
            kpi_html("KPI de diferença para os Comparáveis", '"Diferença para os Comparáveis"', 'IF(ISBLANK(Dif), "—", IF(Dif > 0, "+", IF(Dif < 0, "−", "")) & FORMAT(ABS(Dif), "0.0", "pt-BR") & "<span style=\'font-size:28px;font-weight:400;\'> p.p.</span>")',
                     'IF(ISBLANK(Dif), "", IF(Dif > 0, "o AFL tem mais ", "o AFL tem menos ") & [Ind_Rotulo])', '"#434446"', chip_ref(pct("Comp"))), f"HTML\\{P}\\KPIs")
        if u == "Total":
            add(f"KPI_Contrata3_{u}_HTML", "KPI 3: maior valor do indicador entre as divisões.",
                kpi_v("KPI do maior valor", '"Maior valor entre as divisões"', pct("[Ind_Maior_Valor]"), "[Ind_Maior_Divisao]", '"#434446"'), f"HTML\\{P}\\KPIs")
        else:
            add(f"KPI_Contrata3_{u}_HTML", "KPI 3: maior valor do indicador entre as atividades do AFL.",
                kpi_v("KPI do maior valor", '"Maior valor entre as atividades"', pct("[Ind_Atividade_Lider_Valor]"), "[Ind_Atividade_Lider]", '"#434446"'), f"HTML\\{P}\\KPIs")
    # títulos dos cards
    add("Titulo_Contrata_Rank_Total_HTML", "Título do ranking de divisões.",
        "VAR Pos = [Ind_Posicao_AFL]\nVAR N = [Ind_Total_Divisoes]\nVAR Afl = [Ind_Valor_AFL]\nVAR Comp = [Ind_Valor_Comp]\n"
        "VAR L1 = IF(ISBLANK(Pos), \"O AFL não tem dados deste indicador\", \"O AFL é o \" & Pos & \"º entre \" & N & \" divisões em \" & [Ind_Rotulo])\n"
        "VAR L2 = IF(ISBLANK(Pos), \"\", \"AFL \" & " + pct("Afl") + " & \" × Comparáveis \" & " + pct("Comp") + " & \" · participação no emprego de cada divisão em \" & [Ind_Ano] & \" · piso de 50 mil empregos\")\n" + titulo_html("L1", "L2", '"#F58220"'), f"HTML\\{P}\\Títulos")
    add("Titulo_Contrata_Rank_AFL_HTML", "Título do ranking de atividades do AFL.",
        "VAR L1 = IF(ISBLANK([Ind_Atividade_Lider]), \"Sem dados para os filtros escolhidos\", [Ind_Atividade_Lider] & \" tem a maior participação de \" & [Ind_Rotulo] & \" entre as atividades do AFL\")\n"
        "VAR L2 = IF(ISBLANK([Ind_Atividade_Lider]), \"\", \"Participação no emprego de cada atividade (CNAE) do AFL em \" & [Ind_Ano])\n" + titulo_html("L1", "L2", '"#1D1E21"'), f"HTML\\{P}\\Títulos")
    add("Titulo_Contrata_Serie_HTML", "Título da série do indicador (AFL × Comparáveis).",
        "VAR A = [Ano_Ref]\nVAR I = [Ano_Inicio_Trecho]\n"
        "VAR L1 = IF(ISBLANK(A), \"Sem dados\", [Ind_Rotulo] & \": AFL × Comparáveis ao longo dos anos\")\n"
        "VAR L2 = IF(ISBLANK(A), \"\", IF([Ind_Atual] = \"Primeiro emprego\", \"Só existe até 2021 (o eSocial não registra o tipo de admissão)\", IF([Ind_Atual] = \"Intermitente\", \"Existe desde 2018 (reforma trabalhista)\", \"A linha não atravessa 2022 (nova fonte: eSocial)\")))\n" + titulo_html("L1", "L2", '"#F58220"'), f"HTML\\{P}\\Títulos")
    add("Titulo_Contrata_UF_HTML", "Título das UFs: onde o AFL tem a maior participação do indicador.",
        f"VAR T = FILTER(ADDCOLUMNS(VALUES(D_UF[uf]), \"@v\", [Ind_UF_Top]), NOT ISBLANK([@v]))\nVAR Lider1 = TOPN(1, T, [@v], DESC, D_UF[uf], ASC)\nVAR UF = CONCATENATEX(Lider1, D_UF[uf], \"\")\nVAR V = MAXX(Lider1, [@v])\n"
        "VAR L1 = IF(COUNTROWS(T) = 0, \"Sem dados para os filtros escolhidos\", \"Em \" & UF & \" o AFL tem a maior participação de \" & [Ind_Rotulo] & \": \" & " + pct("V") + ")\n"
        "VAR L2 = IF(COUNTROWS(T) = 0, \"\", \"Só dos empregos do AFL, por UF (10 maiores; UFs com 3 mil empregos do AFL ou mais)\")\n" + titulo_html("L1", "L2", '"#1D1E21"'), f"HTML\\{P}\\Títulos")
    # tabela dos 7 indicadores (AFL × Comparáveis)
    linhas = ""
    for nome, (n, d) in ATRIB.items():
        ano = "MIN(A, 2021)" if nome == "Primeiro emprego" else "A"
        cond = "A >= 2018" if nome == "Intermitente" else "TRUE()"
        for suf, g in (("A", G_AFL), ("C", G_COMP)):
            den = f"CALCULATE([Empregos], {g}, {ANO_FIXO.format(a=ano)}, {d})" if d else f"CALCULATE([Empregos], {g}, {ANO_FIXO.format(a=ano)})"
            linhas += f"VAR V{INDICADORES.index(nome)}{suf} = IF({cond}, DIVIDE(CALCULATE([Empregos], {g}, {ANO_FIXO.format(a=ano)}, {n}), {den}))\n"
    corpo = ""
    for i, nome in enumerate(INDICADORES):
        marca = f" (até 2021)" if nome == "Primeiro emprego" else (" (desde 2018)" if nome == "Intermitente" else "")
        corpo += (" & \"<tr><td style='padding:9px 0;border-top:1px solid #E8E8E9;'>" + nome + marca + "</td><td style='text-align:right;font-weight:600;border-top:1px solid #E8E8E9;'>\" & " + pct(f"V{i}A")
                  + " & \"</td><td style='text-align:right;color:#434446;border-top:1px solid #E8E8E9;'>\" & " + pct(f"V{i}C") + " & \"</td></tr>\"")
    add("Contrata_Tabela_HTML", "Tabela dos 7 indicadores: AFL × Comparáveis no ano de referência (primeiro emprego usa 2021).",
        "VAR A = [Ano_Ref]\n" + linhas + "RETURN IF(ISBLANK(A), \"\", \"<table style='width:100%;border-collapse:collapse;font-family:Segoe UI,Arial,sans-serif;font-size:21px;font-variant-numeric:tabular-nums;'><tr style='color:#434446;'>"
        "<th style='text-align:left;font-weight:600;padding-bottom:6px;'>Indicador</th><th style='text-align:right;font-weight:600;color:#B86218;'>AFL</th><th style='text-align:right;font-weight:600;'>Comparáveis</th></tr>\"" + corpo + " & \"</table>\")", f"HTML\\{P}")
    add("Titulo_Contrata_Tabela_HTML", "Título da tabela dos 7 indicadores.",
        "VAR L1 = \"O AFL em cada indicador, contra os Comparáveis\"\nVAR L2 = \"Participação nos empregos de 31/12/\" & [Ano_Ref] & \" (primeiro emprego: 2021)\"\n" + titulo_html("L1", "L2", '"#1D1E21"'), f"HTML\\{P}\\Títulos")
    return m
