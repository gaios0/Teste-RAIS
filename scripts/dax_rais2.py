"""DAX das abas Quem trabalha, Quanto ganha e Quem contrata (etapa 2). Mesmos padrões de dax_rais.py (HTML escapado, KPIs de 156 px, AFL × Comparável).

Os textos DAX usam marcadores @...@ (e não f-strings) porque o DAX tem chaves de tabela ({"a", "b"}).
"""
from dax_rais import (ANO_FIXO, AFL_ROTULO, G_AFL, G_COMP, QUEBRA, chip_afl, chip_ref, esc, kpi_html, num, pct, titulo_html)

def kpi_v(*a, **k):
    """kpi_html precedido de uma VAR (medida sem VAR própria não pode começar com RETURN)."""
    return "VAR _A = [Ano_Ref]\n" + kpi_html(*a, **k)


P1, P2, P3 = "Quem trabalha", "Quanto ganha", "Quem contrata"
NAO_FAIXA = ["Não categorizado"]
ESC_FORA = ['"< 1 ano de estudo"', '"Ignorado/Faltante"']
ANOF = ANO_FIXO


def t(texto, **kw):
    for k, v in kw.items():
        texto = texto.replace(f"@{k}@", v)
    return texto


def pc(v, sinal=False):
    if v.startswith(("Perf_", "Rem_", "Pir_")):      # nome de medida, não de VAR
        v = f"[{v}]"
    return pct(v, sinal)


def manchete_corpo(texto_var, contexto_var, aria):
    return (
        "VAR Valido = NOT ISBLANK([Ano_Ref]) && NOT ISBLANK([Empregos_Ref])\nRETURN\n    IF(NOT Valido,\n"
        "        \"<div role='text' style='width:100%;height:118px;font-family:Segoe UI,Arial,sans-serif;font-size:24px;color:#434446;'>Não há dados para os filtros selecionados.</div>\",\n"
        f"        \"<div role='group' aria-label='{aria}' style='width:100%;height:118px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>\"\n"
        "            & \"<div style='height:48px;display:flex;align-items:center;white-space:nowrap;overflow:hidden;'><span style='min-width:0;font-size:36px;line-height:42px;font-weight:600;font-variant-numeric:tabular-nums;overflow:hidden;text-overflow:ellipsis;'>\" & "
        + esc(texto_var) + " & \"</span></div>\"\n"
        "            & \"<div style='height:30px;margin:4px 0 0;font-size:24px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>\" & " + esc(contexto_var) + " & \"</div>\"\n"
        "        & \"</div>\")")


PREP = ("VAR NUF = COUNTROWS(VALUES(D_UF[uf]))\nVAR Prep = IF(NOT ISFILTERED(D_UF[uf]) || NUF = COUNTROWS(ALL(D_UF[uf])), \"No Brasil\", "
        "IF(NUF = 1, \"Em \" & SELECTEDVALUE(D_UF[estado]), \"Nas \" & NUF & \" UFs escolhidas\"))\n")


# ====================================================================== QUEM TRABALHA
ATRIBUTOS = {   # nome: (filtro do numerador, filtro do denominador ou None, condição do ano ou None)
    "Mulheres": ('KEEPFILTERS(D_Sexo[sexo] = "Mulher")', None, None),
    "Ate24": ('KEEPFILTERS(D_FaixaIdade[faixa_idade] IN {"14-17", "18-24"})', None, None),
    "Acima55": ('KEEPFILTERS(D_FaixaIdade[faixa_idade] IN {"55-64", "65+"})', None, None),
    "MedioMais": ('KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Médio Completo", "Superior Incompleto", "Superior Completo"})', None, None),
    "Superior": ('KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {"Superior Incompleto", "Superior Completo"})', None, None),
    "Negros": ('KEEPFILTERS(D_Raca[grupo_raca] = "Negra")', 'KEEPFILTERS(D_Raca[declarada] = "Sim")', None),
    "Intermitente": ('KEEPFILTERS(F_rais[trabalho_intermitente] = "Sim")', None, "A >= 2018"),
    "Primeiro": ('KEEPFILTERS(F_rais[tipo_admissao] = "Primeiro Emprego")', None, "A <= 2021"),
}


def perfil(add):
    for nome, (num_f, den_f, cond) in ATRIBUTOS.items():
        corpo = ("VAR A = [Ano_Ref]\nVAR Num = CALCULATE([Empregos_Ref], @N@)\nVAR Den = " + ("CALCULATE([Empregos_Ref], @D@)" if den_f else "[Empregos_Ref]") + "\n"
                 "RETURN IF(ISBLANK(A) || NOT(@C@), BLANK(), DIVIDE(Num, Den))")
        corpo = t(corpo, N=num_f, D=den_f or "", C=cond or "TRUE()")
        add(f"Perf_{nome}", f"Participação ({nome}) nos empregos de 31/12 do ano de referência, no contexto da página.", corpo, f"{P1}\\Perfil", "0.0%")
        add(f"Perf_{nome}_AFL", f"Perf_{nome} só do AFL.", f"CALCULATE([Perf_{nome}], {G_AFL})", f"{P1}\\AFL", "0.0%")
        add(f"Perf_{nome}_Comp", f"Perf_{nome} só dos Comparáveis.", f"CALCULATE([Perf_{nome}], {G_COMP})", f"{P1}\\Comparável", "0.0%")
    add("Perf_Idade", "Idade média dos empregados em 31/12 do ano de referência.",
        "VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A), DIVIDE(CALCULATE(SUM(F_rais[soma_idade]), " + ANOF.format(a="A") + "), CALCULATE(SUM(F_rais[qtd_idade]), " + ANOF.format(a="A") + ")))",
        f"{P1}\\Perfil", "0.0")
    add("Perf_Idade_Inicio", "Idade média no primeiro ano do trecho comparável.",
        "VAR I = [Ano_Inicio_Trecho]\nRETURN IF(NOT ISBLANK(I), DIVIDE(CALCULATE(SUM(F_rais[soma_idade]), " + ANOF.format(a="I") + "), CALCULATE(SUM(F_rais[qtd_idade]), " + ANOF.format(a="I") + ")))",
        f"{P1}\\Perfil", "0.0")
    # pirâmide
    for nome, sexo, sinal in (("Mulheres", "Mulher", "-"), ("Homens", "Homem", "")):
        add(f"Pir_{nome}", f"Pirâmide etária: % de {nome.lower()} em cada faixa sobre o total de empregos do contexto (mulheres com sinal negativo).",
            t('VAR F = SELECTEDVALUE(D_FaixaIdade[faixa_idade])\nRETURN IF(ISBLANK(F) || F = "Não categorizado", BLANK(), @S@DIVIDE(CALCULATE([Empregos_Ref], KEEPFILTERS(D_Sexo[sexo] = "@X@")), CALCULATE([Empregos_Ref], REMOVEFILTERS(D_FaixaIdade))))', S=sinal, X=sexo),
            f"{P1}\\Pirâmide", "0.0%;0.0%;0.0%")
        add(f"Pir_{nome}_Comp", f"Pir_{nome} dos Comparáveis (referência no tooltip).", f"CALCULATE([Pir_{nome}], {G_COMP})", f"{P1}\\Pirâmide", "0.0%;0.0%;0.0%")
    add("Titulo_Pir_HTML", "Título da pirâmide: em quantas faixas de idade as mulheres são maioria.",
        "VAR T = ADDCOLUMNS(FILTER(VALUES(D_FaixaIdade[faixa_idade]), D_FaixaIdade[faixa_idade] <> \"Não categorizado\"), \"@m\", -[Pir_Mulheres], \"@h\", [Pir_Homens])\n"
        "VAR N = COUNTROWS(FILTER(T, NOT ISBLANK([@m]) && NOT ISBLANK([@h])))\nVAR NM = COUNTROWS(FILTER(T, [@m] > [@h]))\n"
        "VAR L1 = IF(N = 0, \"Sem dados para os filtros escolhidos\", IF(NM = N, \"As mulheres são maioria em todas as \" & N & \" faixas de idade\", IF(NM = 0, \"Os homens são maioria em todas as \" & N & \" faixas de idade\", \"As mulheres são maioria em \" & NM & \" das \" & N & \" faixas de idade\")))\n"
        "VAR L2 = IF(N = 0, \"\", \"% do total de empregos em 31/12/\" & [Ano_Ref] & \", por faixa de idade e sexo. O tooltip mostra os Comparáveis (referência)\")\n" + titulo_html("L1", "L2", '"#7F56D9"'), f"HTML\\{P1}\\Títulos")
    # escolaridade (HTML 100%)
    cores = ["#E0E7FF", "#A5B4FC", "#6366F1", "#312E81"]
    grupos = [("Até fundamental", '{"< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"}'), ("Médio incompleto", '{"Médio Incompleto"}'),
              ("Médio completo", '{"Médio Completo"}'), ("Superior", '{"Superior Incompleto", "Superior Completo"}')]
    vars_ = "VAR A = [Ano_Ref]\n"
    for suf, g in (("A", G_AFL), ("C", G_COMP)):
        vars_ += f"VAR Tot{suf} = CALCULATE([Empregos_Ref], {g}, REMOVEFILTERS(D_Escolaridade))\n"
        for i, (_, lista) in enumerate(grupos):
            vars_ += f"VAR E{i}{suf} = DIVIDE(CALCULATE([Empregos_Ref], {g}, REMOVEFILTERS(D_Escolaridade), D_Escolaridade[escolaridade_agrupada] IN {lista}), Tot{suf})\n"

    def barra(rot, suf):
        segs = ""
        for i, (_, _l) in enumerate(grupos):
            cor = cores[i]
            texto_cor = "#1D1E21" if i < 2 else "#FFFFFF"
            segs += (f" & \"<div style='width:\" & FORMAT(E{i}{suf} * 100, \"0.00\", \"en-US\") & \"%;background:{cor};color:{texto_cor};display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:600;overflow:hidden;'>\" & "
                     f"IF(E{i}{suf} >= 0.06, FORMAT(E{i}{suf}, \"0%\", \"pt-BR\"), \"\") & \"</div>\"")
        return ("\"<div style='display:flex;align-items:center;margin-top:14px;'><span style='flex:none;width:130px;font-size:21px;font-weight:600;'>" + rot + "</span><div style='flex:1;display:flex;height:48px;border-radius:4px;overflow:hidden;background:#EEEEEF;'>\""
                + segs + " & \"</div></div>\"")
    leg = "".join(f"<span style='margin-right:16px;white-space:nowrap;'><i style='display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:6px;vertical-align:-1px;background:{c};'></i>{n}</span>" for (n, _), c in zip(grupos, cores))
    add("Esc_Barras_HTML", "Escolaridade em barras 100% (AFL e Comparáveis), ignorando o filtro de escolaridade.",
        vars_ + "RETURN IF(ISBLANK(A) || TotA = 0, \"<div style='font-family:Segoe UI,Arial,sans-serif;font-size:21px;color:#434446;'>Sem dados para os filtros escolhidos.</div>\",\n"
        "    \"<div style='font-family:Segoe UI,Arial,sans-serif;font-variant-numeric:tabular-nums;color:#1D1E21;'>\" & " + barra("AFL", "A") + " & " + barra("Comparáveis", "C")
        + " & \"<div style='margin-top:18px;font-size:19px;line-height:30px;color:#434446;'>" + leg + "</div></div>\")", f"HTML\\{P1}")
    add("Titulo_Esc_HTML", "Título da escolaridade: ensino médio completo e superior, AFL × Comparáveis.",
        vars_ + "VAR L1 = IF(ISBLANK(A) || TotA = 0, \"Sem dados para os filtros escolhidos\", " + pc("E2A") + " & \" dos empregados do AFL têm o ensino médio completo\")\n"
        "VAR L2 = IF(ISBLANK(A) || TotA = 0, \"\", \"Superior (completo ou não): \" & " + pc("E3A") + " & \" no AFL e \" & " + pc("E3C") + " & \" nos Comparáveis\")\n" + titulo_html("L1", "L2", '"#312E81"'), f"HTML\\{P1}\\Títulos")
    # ocupações
    add("Emp_CBO_Top", "Empregos por ocupação (CBO); só as 8 maiores.",
        "VAR V = [Empregos_Ref]\nVAR R = IF(NOT ISBLANK(V), RANKX(ALLSELECTED(F_rais[cbo_2002]), [Empregos_Ref], , DESC, DENSE))\nRETURN IF(NOT ISBLANK(V) && R <= 8, V)", f"{P1}\\Ocupações", "#,0")
    add("Titulo_CBO_HTML", "Título das ocupações: a mais comum, seus empregos e % de mulheres.",
        "VAR T = FILTER(ADDCOLUMNS(VALUES(F_rais[cbo_2002]), \"@v\", [Empregos_Ref]), NOT ISBLANK([@v]))\nVAR Lider1 = TOPN(1, T, [@v], DESC, F_rais[cbo_2002], ASC)\nVAR Nome = CONCATENATEX(Lider1, F_rais[cbo_2002], \"\")\n"
        "VAR V = MAXX(Lider1, [@v])\nVAR Mul = CALCULATE([Perf_Mulheres], KEEPFILTERS(TREATAS({Nome}, F_rais[cbo_2002])))\n"
        "VAR L1 = IF(COUNTROWS(T) = 0, \"Sem dados para os filtros escolhidos\", Nome & \" é a ocupação mais comum: \" & " + num("V") + " & \" empregos\")\n"
        "VAR L2 = IF(COUNTROWS(T) = 0, \"\", \"Mulheres: \" & " + pc("Mul") + " & \" · ocupações (CBO) com mais empregos em 31/12/\" & [Ano_Ref])\n" + titulo_html("L1", "L2", '"#1D1E21"'), f"HTML\\{P1}\\Títulos")
    # raça + primeiro emprego + intermitente (HTML)
    cr = ["#D0D5DD", "#475467", "#98A2B3", "#1D1E21"]
    rac = [("Branca", "Branca"), ("Negra", "Negra"), ("Amarela", "Amarela"), ("Indígena", "Indígena")]
    vr = "VAR A = [Ano_Ref]\n"
    for suf, g in (("A", G_AFL), ("C", G_COMP)):
        vr += f"VAR Decl{suf} = CALCULATE([Empregos_Ref], {g}, REMOVEFILTERS(D_Raca), D_Raca[declarada] = \"Sim\")\nVAR TotR{suf} = CALCULATE([Empregos_Ref], {g}, REMOVEFILTERS(D_Raca))\n"
        for i, (_, gr) in enumerate(rac):
            vr += f"VAR R{i}{suf} = DIVIDE(CALCULATE([Empregos_Ref], {g}, REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = \"{gr}\", D_Raca[declarada] = \"Sim\"), Decl{suf})\n"
        vr += f"VAR Pri{suf} = CALCULATE([Perf_Primeiro], {g}, REMOVEFILTERS(D_Raca))\nVAR Int{suf} = CALCULATE([Perf_Intermitente], {g}, REMOVEFILTERS(D_Raca))\nVAR IntN{suf} = CALCULATE([Empregos_Ref], {g}, REMOVEFILTERS(D_Raca), F_rais[trabalho_intermitente] = \"Sim\")\n"

    def barra_r(rot, suf):
        segs = ""
        for i in range(4):
            cor = cr[i]
            tc = "#1D1E21" if i in (0, 2) else "#FFFFFF"
            segs += (f" & \"<div style='width:\" & FORMAT(R{i}{suf} * 100, \"0.00\", \"en-US\") & \"%;background:{cor};color:{tc};display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:600;overflow:hidden;'>\" & "
                     f"IF(R{i}{suf} >= 0.06, FORMAT(R{i}{suf}, \"0%\", \"pt-BR\"), \"\") & \"</div>\"")
        return ("\"<div style='display:flex;align-items:center;margin-top:12px;'><span style='flex:none;width:130px;font-size:21px;font-weight:600;'>" + rot + "</span><div style='flex:1;display:flex;height:44px;border-radius:4px;overflow:hidden;background:#EEEEEF;'>\""
                + segs + " & \"</div></div>\"")
    legr = "".join(f"<span style='margin-right:16px;white-space:nowrap;'><i style='display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:6px;vertical-align:-1px;background:{c};'></i>{n}{' (preta + parda)' if n == 'Negra' else ''}</span>" for (n, _), c in zip(rac, cr))
    add("Raca_HTML", "Cor/raça (sobre quem declarou) em barras 100%, AFL e Comparáveis, com primeiro emprego e intermitente.",
        vr + "RETURN IF(ISBLANK(A) || DeclA = 0, \"<div style='font-family:Segoe UI,Arial,sans-serif;font-size:21px;color:#434446;'>Sem dados para os filtros escolhidos.</div>\",\n"
        "    \"<div style='font-family:Segoe UI,Arial,sans-serif;font-variant-numeric:tabular-nums;color:#1D1E21;'>\" & " + barra_r("AFL", "A") + " & " + barra_r("Comparáveis", "C")
        + " & \"<div style='margin-top:12px;font-size:19px;line-height:28px;color:#434446;'>" + legr + "</div>\""
        " & \"<div style='margin-top:16px;border-top:1px solid #E8E8E9;padding-top:12px;font-size:21px;line-height:30px;'><b>Primeiro emprego</b> (só até 2021): \" & IF(ISBLANK(PriA), \"sem dados em \" & A, " + pc("PriA") + " & \" no AFL × \" & " + pc("PriC") + ")"
        " & \"<br><b>Intermitente</b> (desde 2018): \" & IF(ISBLANK(IntA), \"sem dados em \" & A, " + num("IntNA") + " & \" empregos, \" & " + pc("IntA") + " & \" × \" & " + pc("IntC") + ") & \"</div></div>\")", f"HTML\\{P1}")
    add("Titulo_Raca_HTML", "Título de cor/raça: % de negros entre quem declarou, AFL × Comparáveis.",
        vr + "VAR L1 = IF(ISBLANK(A) || DeclA = 0, \"Sem dados para os filtros escolhidos\", " + pc("R1A") + " & \" dos empregados do AFL que declararam cor são negros\")\n"
        "VAR L2 = IF(ISBLANK(A) || DeclA = 0, \"\", \"Comparáveis: \" & " + pc("R1C") + " & \" · declararam cor: \" & " + pc("DIVIDE(DeclA, TotRA)") + ")\n" + titulo_html("L1", "L2", '"#475467"'), f"HTML\\{P1}\\Títulos")
    # KPIs e manchetes
    for u in ("Total", "AFL"):
        extra_afl = lambda m: (chip_afl(pc(m + "_AFL")) + " & " + chip_ref(pc(m + "_Comp"))) if u == "Total" else chip_ref(pc(m + "_Comp"))
        add(f"KPI_Mulheres_{u}_HTML", "KPI de mulheres (% dos empregos), com chips.",
            kpi_v("KPI de participação de mulheres", '"Mulheres"', pc("Perf_Mulheres"), '"dos empregos em 31/12/" & [Ano_Ref]', '"#434446"', extra_afl("Perf_Mulheres")), f"HTML\\{P1}\\KPIs")
        add(f"KPI_Jovens_{u}_HTML", "KPI de empregados até 24 anos, com idade média.",
            "VAR Idade = [Perf_Idade]\nVAR IdadeI = [Perf_Idade_Inicio]\nVAR I = [Ano_Inicio_Trecho]\n" +
            kpi_html("KPI de jovens", '"Até 24 anos"', pc("Perf_Ate24"), "\"idade média \" & FORMAT(Idade, \"0.0\", \"pt-BR\") & \" anos\" & IF([Ano_Ref] > I, \" (\" & FORMAT(IdadeI, \"0.0\", \"pt-BR\") & \" em \" & I & \")\", \"\")", '"#434446"', extra_afl("Perf_Ate24")), f"HTML\\{P1}\\KPIs")
        add(f"KPI_Escol_{u}_HTML", "KPI de ensino médio completo ou mais, com superior.",
            kpi_v("KPI de escolaridade", '"Ensino médio completo ou mais"', pc("Perf_MedioMais"), "\"superior (completo ou não): \" & " + pc("Perf_Superior"), '"#434446"', extra_afl("Perf_MedioMais")), f"HTML\\{P1}\\KPIs")
        if u == "AFL":
            texto = PREP + "VAR Texto = Prep & \", \" & " + pc("Perf_Mulheres") + " & \" dos empregados do AFL são mulheres e \" & " + pc("Perf_Ate24") + " & \" têm até 24 anos\"\n"
        else:
            texto = (PREP + "VAR Texto = Prep & \", \" & " + pc("Perf_Mulheres") + " & \" dos empregados são mulheres e \" & " + pc("Perf_Ate24") + " & \" têm até 24 anos; no AFL, \" & " + pc("Perf_Mulheres_AFL") + " & \" e \" & " + pc("Perf_Ate24_AFL") + "\n")
        add(f"Manchete_Perfil_{u}_HTML", f"Manchete da página Quem trabalha · {u}.", texto + f"VAR Contexto = [Contexto_Emp_{u}]\n" + manchete_corpo("Texto", "Contexto", "Perfil dos empregados"), f"HTML\\{P1}")


# ====================================================================== QUANTO GANHA
def salario(add):
    # séries (média e mediana, AFL e Comparável, por trecho) para o gráfico de linhas; a mediana respeita UF, sexo e escolaridade
    for suf, g, nome in (("AFL", G_AFL, "AFL"), ("Comp", G_COMP, "Comparáveis")):
        for tr, cond in (("Pre", f"A < {QUEBRA}"), ("Pos", f"A >= {QUEBRA}")):
            add(f"Rem_Media_{suf}_{tr}", f"Remuneração média de dezembro do {nome}, trecho {tr}; BLANK fora do trecho.",
                f"VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A) && {cond}, CALCULATE([Remuneracao_Media], {g}, {ANOF.format(a='A')}))", f"{P2}\\Séries", "#,0")
            add(f"Rem_Mediana_{suf}_{tr}", f"Mediana da remuneração de dezembro do {nome}, trecho {tr}; BLANK fora do trecho ou quando a mediana não existe para os filtros.",
                f"VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A) && {cond}, [Remuneracao_Mediana_Ref_{'AFL' if suf == 'AFL' else 'Comparavel'}])", f"{P2}\\Séries", "#,0")
    # razões por sexo e cor (média de dezembro)
    def razao(nome, col, a, b, desc):
        for suf, g in (("", None), ("_AFL", G_AFL), ("_Comp", G_COMP)):
            interno = ("VAR A = [Ano_Ref]\nVAR Fora = ISBLANK(A) || (SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada]) IN {" + ", ".join(ESC_FORA) + "})\n"
                       "VAR Num = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(@T@), @C@ = \"@a@\")\nVAR Den = CALCULATE([Remuneracao_Media_Ref], REMOVEFILTERS(@T@), @C@ = \"@b@\")\n"
                       "RETURN IF(Fora, BLANK(), DIVIDE(Num, Den))")
            interno = t(interno, T=col.split("[")[0], C=col, a=a, b=b)
            add(f"Rem_Razao_{nome}{suf}", f"Razão da remuneração média ({desc}) no contexto{'' if not suf else ' do ' + suf[1:]}.",
                interno if not g else f"CALCULATE([Rem_Razao_{nome}], {g})", f"{P2}\\Razões", "0%")
    razao("Sexo", "D_Sexo[sexo]", "Mulher", "Homem", "mulheres ÷ homens")
    razao("Raca", "D_Raca[grupo_raca]", "Negra", "Branca", "negros ÷ brancos")
    # barras por escolaridade
    add("Rem_Esc_AFL", "Remuneração média de dezembro por escolaridade, AFL (categorias sem informação ficam BLANK).",
        "IF(SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada]) IN {" + ", ".join(ESC_FORA) + "}, BLANK(), [Remuneracao_Media_Ref_AFL])", f"{P2}\\Escolaridade", "#,0")
    add("Rem_Esc_Comp", "Remuneração média de dezembro por escolaridade, Comparáveis.",
        "IF(SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada]) IN {" + ", ".join(ESC_FORA) + "}, BLANK(), [Remuneracao_Media_Ref_Comparavel])", f"{P2}\\Escolaridade", "#,0")
    add("Rem_UF_Top", "Remuneração média de dezembro por UF (10 maiores).",
        "VAR V = [Remuneracao_Media_Ref]\nVAR R = IF(NOT ISBLANK(V), RANKX(ALLSELECTED(D_UF[uf]), [Remuneracao_Media_Ref], , DESC, DENSE))\nRETURN IF(NOT ISBLANK(V) && R <= 10, V)", f"{P2}\\UF", "#,0")
    add("Rem_UF_Razao_Comp", "Remuneração média do AFL na UF ÷ média dos Comparáveis na UF.", "DIVIDE([Remuneracao_Media_Ref_AFL], [Remuneracao_Media_Ref_Comparavel])", f"{P2}\\UF", "0%")
    for nome, txt in (("Sexo", "Mulheres ÷ homens"), ("Raca", "Negros ÷ brancos")):
        add(f"Rotulo_Gap_{nome}_HTML", f"Rótulo do gráfico de razão ({txt}).", f"\"<div style='font-family:Segoe UI,Arial,sans-serif;font-size:21px;font-weight:600;color:#1D1E21;'>{txt} · remuneração média de dezembro, por escolaridade</div>\"", f"HTML\\{P2}\\Títulos", None, True)
    # KPIs
    for u in ("Total", "AFL"):
        add(f"KPI_Mediana_{u}_HTML", "KPI de remuneração mediana de dezembro, com média, salários mínimos e chips.",
            ("VAR Med = [Remuneracao_Mediana_Ref]\n" if u == "Total" else "VAR Med = IF(ISFILTERED(D_AflAtividade[nome]), [Remuneracao_Mediana_Ref], COALESCE([Remuneracao_Mediana_Ref], [Remuneracao_Mediana_Ref_AFL]))\n") + "VAR Media = [Remuneracao_Media_Ref]\nVAR SM = [Remuneracao_Media_SM_Ref]\nVAR MedAFL = [Remuneracao_Mediana_Ref_AFL]\nVAR MedComp = [Remuneracao_Mediana_Ref_Comparavel]\n" +
            kpi_html("KPI de remuneração mediana", '"Remuneração mediana de dezembro"', 'IF(ISBLANK(Med), "—", "R$ " & FORMAT(Med, "#,0", "pt-BR"))',
                     'IF(ISBLANK(Med), "mediana só existe para setor, UF, sexo e escolaridade", "média R$ " & FORMAT(Media, "#,0", "pt-BR") & " · " & FORMAT(SM, "0.00", "pt-BR") & " salário mínimo")', '"#434446"',
                     (chip_afl('IF(ISBLANK(MedAFL), "—", "R$ " & FORMAT(MedAFL, "#,0", "pt-BR"))') + " & " if u == "Total" else "") + chip_ref('IF(ISBLANK(MedComp), "—", "R$ " & FORMAT(MedComp, "#,0", "pt-BR"))')), f"HTML\\{P2}\\KPIs")
        for nome, rot, quem, outro in (("Sexo", "Mulheres ganham, em média,", "Mulheres", "dos homens"), ("Raca", "Negros ganham, em média,", "Negros", "dos brancos")):
            m = f"Rem_Razao_{nome}"
            add(f"KPI_Razao{nome}_{u}_HTML", f"KPI da razão de remuneração ({quem} {outro}).",
                kpi_html(f"KPI de razão salarial ({quem})", f'"{rot}"', 'IF(ISBLANK([' + m + ']), "—", FORMAT([' + m + '], "0%", "pt-BR") & "<span style=\'font-size:24px;font-weight:400;\'> " & "' + outro + '" & "</span>")',
                         '"da remuneração média de dezembro"', '"#434446"',
                         (chip_afl(f'IF(ISBLANK([{m}_AFL]), "—", FORMAT([{m}_AFL], "0%", "pt-BR"))') + " & " if u == "Total" else "") + chip_ref(f'IF(ISBLANK([{m}_Comp]), "—", FORMAT([{m}_Comp], "0%", "pt-BR"))')), f"HTML\\{P2}\\KPIs")
        add(f"Manchete_Salario_{u}_HTML", f"Manchete da página Quanto ganha · {u}.",
            PREP + "VAR Med = [Remuneracao_Mediana_Ref]\nVAR Media = [Remuneracao_Media_Ref]\nVAR MedAFL = [Remuneracao_Mediana_Ref_AFL]\nVAR MedComp = [Remuneracao_Mediana_Ref_Comparavel]\nVAR A = [Ano_Ref]\n"
            + ("VAR Texto = Prep & \", metade do AFL ganhava até R$ \" & FORMAT(MedAFL, \"#,0\", \"pt-BR\") & \" em dez/\" & A & \": \" & FORMAT(DIVIDE(MedAFL, MedComp), \"0%\", \"pt-BR\") & \" da mediana dos Comparáveis\"\n"
               if u == "AFL" else
               "VAR Texto = Prep & IF(ISBLANK(Med), \", a remuneração média de dezembro de \" & A & \" foi R$ \" & FORMAT(Media, \"#,0\", \"pt-BR\"), \", metade dos empregados ganhava até R$ \" & FORMAT(Med, \"#,0\", \"pt-BR\") & \" em dez/\" & A) & IF(ISBLANK(MedAFL), \"\", \"; no AFL, R$ \" & FORMAT(MedAFL, \"#,0\", \"pt-BR\"))\n")
            + f"VAR Contexto = [Contexto_Emp_{u}] & \" · valores nominais\"\n" + manchete_corpo("Texto", "Contexto", "Remuneração dos empregados"), f"HTML\\{P2}")
    add("Titulo_Rem_Serie_HTML", "Título da série de remuneração: média do AFL como % da média dos Comparáveis no início e no fim do trecho.",
        "VAR A = [Ano_Ref]\nVAR I = [Ano_Inicio_Trecho]\n"
        f"VAR R0 = DIVIDE(CALCULATE([Remuneracao_Media], {G_AFL}, {ANOF.format(a='I')}), CALCULATE([Remuneracao_Media], {G_COMP}, {ANOF.format(a='I')}))\n"
        f"VAR R1 = DIVIDE(CALCULATE([Remuneracao_Media], {G_AFL}, {ANOF.format(a='A')}), CALCULATE([Remuneracao_Media], {G_COMP}, {ANOF.format(a='A')}))\n"
        "VAR L1 = IF(ISBLANK(A), \"Sem dados para os filtros escolhidos\", IF(A <= I, I & \" é o primeiro ano do trecho\", \"A média do AFL foi de \" & FORMAT(R0, \"0%\", \"pt-BR\") & \" para \" & FORMAT(R1, \"0%\", \"pt-BR\") & \" da média dos Comparáveis entre \" & I & \" e \" & A))\n"
        "VAR L2 = IF(ISBLANK(A), \"\", \"Remuneração de dezembro em R$ nominais (linha cheia = média, tracejada = mediana). 2021 e 2022 não se comparam (eSocial)\")\n" + titulo_html("L1", "L2", '"#F58220"'), f"HTML\\{P2}\\Títulos")
    add("Titulo_Rem_Esc_HTML", "Título da remuneração por escolaridade: quanto o AFL paga em relação aos Comparáveis com superior completo.",
        "VAR Sup = CALCULATE(DIVIDE([Remuneracao_Media_Ref_AFL], [Remuneracao_Media_Ref_Comparavel]), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = \"Superior Completo\"))\n"
        "VAR Med = CALCULATE(DIVIDE([Remuneracao_Media_Ref_AFL], [Remuneracao_Media_Ref_Comparavel]), KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = \"Médio Completo\"))\n"
        "VAR L1 = IF(ISBLANK(Sup), \"Sem dados para os filtros escolhidos\", \"Com superior completo, o AFL paga \" & FORMAT(Sup, \"0%\", \"pt-BR\") & \" da média dos Comparáveis\")\n"
        "VAR L2 = IF(ISBLANK(Sup), \"\", \"Com ensino médio completo: \" & FORMAT(Med, \"0%\", \"pt-BR\") & \". Remuneração média de dezembro (R$ nominais)\")\n" + titulo_html("L1", "L2", '"#1D1E21"'), f"HTML\\{P2}\\Títulos")
    add("Titulo_Rem_Gap_HTML", "Título das razões por sexo e cor, AFL × Comparáveis.",
        "VAR S = [Rem_Razao_Sexo_AFL]\nVAR SC = [Rem_Razao_Sexo_Comp]\nVAR R = [Rem_Razao_Raca_AFL]\nVAR RC = [Rem_Razao_Raca_Comp]\n"
        "VAR L1 = IF(ISBLANK(S) && ISBLANK(R), \"Sem dados para os filtros escolhidos\", \"A diferença salarial por sexo e por cor é menor no AFL do que nos Comparáveis\")\n"
        "VAR L2 = IF(L1 = \"Sem dados para os filtros escolhidos\", \"\", \"Sem filtro de escolaridade: mulheres ganham \" & FORMAT(S, \"0%\", \"pt-BR\") & \" do salário dos homens no AFL (\" & FORMAT(SC, \"0%\", \"pt-BR\") & \" nos Comparáveis); negros, \" & FORMAT(R, \"0%\", \"pt-BR\") & \" do dos brancos (\" & FORMAT(RC, \"0%\", \"pt-BR\") & \")\")\n"
        + titulo_html("L1", "L2", '"#1D1E21"'), f"HTML\\{P2}\\Títulos")
    add("Titulo_Rem_UF_HTML", "Título das UFs: maior média e maior distância para os Comparáveis.",
        "VAR T = FILTER(ADDCOLUMNS(VALUES(D_UF[uf]), \"@v\", [Remuneracao_Media_Ref], \"@r\", [Rem_UF_Razao_Comp]), NOT ISBLANK([@v]))\nVAR Lider1 = TOPN(1, T, [@v], DESC, D_UF[uf], ASC)\nVAR UF = CONCATENATEX(Lider1, D_UF[uf], \"\")\nVAR V = MAXX(Lider1, [@v])\n"
        "VAR Pior = TOPN(1, FILTER(T, NOT ISBLANK([@r])), [@r], ASC, D_UF[uf], ASC)\nVAR UFP = CONCATENATEX(Pior, D_UF[uf], \"\")\nVAR RP = MAXX(Pior, [@r])\n"
        "VAR L1 = IF(COUNTROWS(T) = 0, \"Sem dados para os filtros escolhidos\", IF(COUNTROWS(T) = 1, UF & \": R$ \" & FORMAT(V, \"#,0\", \"pt-BR\"), UF & \" paga a maior média: R$ \" & FORMAT(V, \"#,0\", \"pt-BR\")))\n"
        "VAR L2 = IF(COUNTROWS(T) < 2 || ISBLANK(RP), \"\", \"Maior distância para os Comparáveis: \" & UFP & \" (AFL \" & FORMAT(RP, \"0%\", \"pt-BR\") & \" da média comparável)\")\n" + titulo_html("L1", "L2", '"#1D1E21"'), f"HTML\\{P2}\\Títulos")


def medidas():
    m = []

    def add(nome, doc, dax, pasta, fmt=None, oculta=False):
        m.append((nome, doc, dax, pasta, fmt, oculta))
    perfil(add)
    salario(add)
    return m
