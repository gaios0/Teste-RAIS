"""DAX da aba Quem contrata (versão 2): perfil dos empregados (mulheres, negros e escolaridade) por setor e divisão
(Todos os setores) e pelos seis CNAEs do AFL (AFL).

Segue o protótipo aprovado: manchete, três KPIs (mulheres, negros, escolaridade), dois rankings por perfil e um ranking por
escolaridade. Cada ranking tem um botão que alterna UMA medida por vez: Representatividade (participação) ou Salário médio.

Tabelas locais desconectadas usadas pelos botões (ver contrata_v2.py): D_Ct_Modo, D_Ct_Setor, D_Ct_MetMul, D_Ct_MetNeg,
D_Ct_MetEsc e D_Ct_Nivel. Retorna tuplas (nome, doc, dax, pasta, formato, oculta) como as demais dax_*.py.

Números: estoque de vínculos em 31/12 (um único ano), remuneração média de dezembro em R$ nominais, negros = pretos + pardos
sobre quem declarou cor, piso de 50 mil empregos por divisão (o mesmo da versão anterior).
"""
from dax_rais import ANO_FIXO, AFL_ROTULO, G_AFL, kpi_html, num, pct, titulo_html
from dax_tooltips import CINZA, LARANJA, ROXO, linha, moeda, montar, pp

P = "Quem contrata"
PISO = 50000
AFL_COR = "#D97706"          # laranja do valor do AFL separado dos demais (mais escuro que o laranja de interface, #F58220)
PISO_TXT = "50.000"
A_ = ANO_FIXO.format(a="A")
PASTA_DADOS = f"{P}\\Perfil"

NIVEIS = {"Até fundamental": ["< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"],
          "Médio incompleto": ["Médio Incompleto"], "Médio completo": ["Médio Completo"],
          "Superior": ["Superior Incompleto", "Superior Completo"]}
MET = {"Mul": "D_Ct_MetMul", "Neg": "D_Ct_MetNeg", "Esc": "D_Ct_MetEsc"}
NOME_PERFIL = {"Mul": "mulheres", "Neg": "negros (pretos + pardos)", "Esc": "empregados do nível de escolaridade escolhido"}
PERFIS = {"Mul": ('KEEPFILTERS(D_Sexo[sexo] = "Mulher")', None),
          "Neg": ('KEEPFILTERS(D_Raca[grupo_raca] = "Negra")', 'KEEPFILTERS(D_Raca[declarada] = "Sim")')}
NIV_VAR = 'VAR Niv = COALESCE(SELECTEDVALUE(D_Ct_Nivel[nivel]), "Médio completo")\n'
SAL_VAR = 'VAR Sal = COALESCE(SELECTEDVALUE({met}[metrica]), "Representatividade") = "Salário médio"\n'
PIORES_VAR = 'VAR Piores = COALESCE(SELECTEDVALUE(D_Ct_Modo[modo]), "10 melhores divisões") = "10 piores divisões"\n'


def _lista(vals):
    return "{" + ", ".join(f'"{v}"' for v in vals) + "}"


def _filtro_esc(vals):
    return f"KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] IN {_lista(vals)})"


def _sw(inner):
    """SWITCH sobre o nível de escolaridade escolhido nos botões; inner(filtro) devolve a expressão de cada nível."""
    ramos = [f'"{k}", {inner(_filtro_esc(v))}' for k, v in NIVEIS.items() if k != "Médio completo"]
    return "SWITCH(Niv, " + ", ".join(ramos) + f", {inner(_filtro_esc(NIVEIS['Médio completo']))})"


def _pre(p):
    return "VAR A = [Ano_Ref]\n" + (NIV_VAR if p == "Esc" else "")


def _num(p, medida):
    """CALCULATE da medida restrita ao perfil (numerador)."""
    if p == "Esc":
        return _sw(lambda f: f"CALCULATE([{medida}], {A_}, {f})")
    return f"CALCULATE([{medida}], {A_}, {PERFIS[p][0]})"


def _den(p):
    """Total de empregos que serve de denominador da participação (negros: só quem declarou cor)."""
    d = PERFIS.get(p, (None, None))[1]
    return f"CALCULATE([Empregos], {A_}" + (f", {d}" if d else "") + ")"


def _div(medida):
    """Mesma medida, calculada para a divisão da categoria (ou para o conjunto AFL), sem os CNAEs do AFL nas divisões comuns."""
    return ("VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])\n"
            "RETURN IF(ISBLANK(Nome), BLANK(),\n"
            f"    IF(Nome = \"{AFL_ROTULO}\", CALCULATE([{medida}], {G_AFL}),\n"
            f"        CALCULATE([{medida}], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[divisao_afl] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = \"Não\"))))")


def medidas():
    m = []

    def add(nome, doc, dax, pasta, fmt=None, oculta=False, dyn=None):
        """dyn = expressão DAX do formato dinâmico (formatStringDefinition): o rótulo vira % ou R$ conforme o botão."""
        m.append((nome, doc, dax, pasta, fmt, oculta, dyn))

    def formato_botao(met):
        # VBA-style no modelo: "\R$ #,0" mostra R$ 2.486; "0.0%" mostra 54,2%
        return f'IF(COALESCE(SELECTEDVALUE({met}[metrica]), "Representatividade") = "Salário médio", "\\R$ #,0", "0.0%")'

    # ------------------------------------------------------------ base por perfil (contexto qualquer)
    for p in ("Mul", "Neg", "Esc"):
        quem = NOME_PERFIL[p]
        add(f"Ct_{p}_Qtd", f"Empregos em 31/12 do ano de referência: {quem}, no contexto.",
            _pre(p) + f"RETURN IF(NOT ISBLANK(A), {_num(p, 'Empregos')})", PASTA_DADOS, "#,0", True)
        add(f"Ct_{p}_Tot", f"Empregos em 31/12 do ano de referência que servem de denominador da participação de {quem}"
            + (" (só quem declarou cor)." if p == "Neg" else "."),
            _pre(p).replace(NIV_VAR, "") + f"RETURN IF(NOT ISBLANK(A), {_den(p)})", PASTA_DADOS, "#,0", True)
        add(f"Ct_{p}_Rep", f"Representatividade: participação de {quem} no total de empregos do contexto, em 31/12 do ano de referência.",
            _pre(p) + f"RETURN IF(NOT ISBLANK(A), DIVIDE({_num(p, 'Empregos')}, {_den(p)}))", PASTA_DADOS, "0.0%", True)
        add(f"Ct_{p}_Sal", f"Salário médio de dezembro (R$ nominais) de {quem} no contexto, no ano de referência.",
            _pre(p) + f"RETURN IF(NOT ISBLANK(A), {_num(p, 'Remuneracao_Media')})", PASTA_DADOS, "#,0.00", True)

    # ------------------------------------------------------------ mesmas medidas por divisão (Todos os setores)
    add("Ct_Div_Emp", "Empregos em 31/12 da divisão da categoria (ou do conjunto AFL), para o piso do ranking.", _div("Empregos_Ref"), PASTA_DADOS, "#,0", True)
    for p in ("Mul", "Neg", "Esc"):
        for k, rot in (("Rep", "representatividade"), ("Sal", "salário médio"), ("Qtd", "quantidade de empregos"), ("Tot", "denominador")):
            add(f"Ct_{p}_Div_{k}", f"{rot.capitalize()} ({NOME_PERFIL[p]}) da divisão da categoria; o item AFL usa os seis CNAEs.",
                _div(f"Ct_{p}_{k}"), PASTA_DADOS, {"Rep": "0.0%", "Sal": "#,0.00"}.get(k, "#,0"), True)

    # ------------------------------------------------------------ valor mostrado nos rankings (uma medida por vez, conforme o botão)
    for p in ("Mul", "Neg", "Esc"):
        met = MET[p]
        add(f"Ct_{p}_Valor", f"Valor do ranking por divisão ({NOME_PERFIL[p]}): representatividade OU salário médio, conforme o botão do gráfico. "
            f"Mostra as 10 melhores (ou 10 piores) divisões do setor escolhido, com piso de {PISO_TXT} empregos, e sempre o AFL (fora do cálculo).",
            "VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])\n"
            f"VAR EhAFL = Nome = \"{AFL_ROTULO}\"\n"
            + SAL_VAR.format(met=met) + PIORES_VAR +
            "VAR Setores = VALUES(D_Ct_Setor[setor])\n"
            "VAR NoSetor = CONTAINS(Setores, D_Ct_Setor[setor], SELECTEDVALUE(D_Rank_Divisao[setor_principal]))\n"
            f"VAR Meu = IF(NOT ISBLANK(Nome) && (EhAFL || NoSetor), IF(Sal, [Ct_{p}_Div_Sal], [Ct_{p}_Div_Rep]))\n"
            f"VAR Tab = FILTER(FILTER(ALL(D_Rank_Divisao[nm_divisao], D_Rank_Divisao[setor_principal]), D_Rank_Divisao[nm_divisao] <> \"{AFL_ROTULO}\" && D_Rank_Divisao[setor_principal] IN Setores), [Ct_Div_Emp] >= {PISO})\n"
            f"VAR Pos = IF(NOT(EhAFL) && NoSetor && NOT ISBLANK(Meu) && [Ct_Div_Emp] >= {PISO},\n"
            f"    IF(Piores, RANKX(Tab, IF(Sal, [Ct_{p}_Div_Sal], [Ct_{p}_Div_Rep]), , ASC, DENSE),\n"
            f"        RANKX(Tab, IF(Sal, [Ct_{p}_Div_Sal], [Ct_{p}_Div_Rep]), , DESC, DENSE)))\n"
            "RETURN IF(EhAFL, Meu, IF(NOT ISBLANK(Pos) && Pos <= 10, Meu))", f"{P}\\Ranking", None, False, formato_botao(met))
        add(f"Ct_{p}_Ord", "Chave de ordenação do ranking por divisão: o valor (ou o oposto nas 10 piores). O AFL fica na posição do seu valor, junto das demais divisões.",
            f"VAR V = [Ct_{p}_Valor]\n" + PIORES_VAR +
            "RETURN IF(ISBLANK(V), BLANK(), IF(Piores, -V, V))", f"{P}\\Ranking", "0.0000", True)
        # AFL: a categoria são os seis CNAEs (D_AflAtividade); o contexto já é o AFL
        add(f"Ct_{p}_Valor_AFL", f"Valor do ranking por CNAE do AFL ({NOME_PERFIL[p]}): representatividade OU salário médio, conforme o botão do gráfico.",
            SAL_VAR.format(met=met) + f"RETURN IF(Sal, [Ct_{p}_Sal], [Ct_{p}_Rep])", f"{P}\\Ranking", None, False, formato_botao(met))

    # ------------------------------------------------------------ manchete (muda conforme os botões de valor dos três gráficos)
    for u, tit_base, tit_sal, ctx in (
            ("Total", "Ranking dos setores: quem mais contrata por perfil dos empregados", "Ranking dos setores: salário médio por perfil dos empregados",
             "setores e divisões respeitam os filtros aplicados · AFL em destaque"),
            ("AFL", "Ranking do AFL: quem mais contrata por perfil dos empregados", "Ranking do AFL: salário médio por perfil dos empregados",
             "os seis CNAEs do AFL respeitam os filtros aplicados")):
        add(f"Manchete_Ct_{u}_HTML", f"Título e subtítulo da página Quem contrata ({u}); falam em salário médio quando os três gráficos estão nesse valor.",
            "VAR A = [Ano_Ref]\n"
            + "".join(SAL_VAR.format(met=MET[p]).replace("VAR Sal =", f"VAR Sal{p} =") for p in ("Mul", "Neg", "Esc")) +
            "VAR NSal = IF(SalMul, 1, 0) + IF(SalNeg, 1, 0) + IF(SalEsc, 1, 0)\n"
            f"VAR Titulo = IF(NSal = 3, \"{tit_sal}\", \"{tit_base}\")\n"
            "VAR Resumo = IF(NSal = 3, \"valores em salário médio de dezembro (R$ nominais)\", IF(NSal = 0, \"valores em representatividade (% dos empregos)\", \"valores conforme o botão de cada gráfico\"))\n"
            f"VAR Sub = IF(ISBLANK(A), \"Não há dados para os filtros selecionados\", \"Empregos em 31/12/\" & A & \" · \" & Resumo & \" · {ctx}\")\n"
            "RETURN \"<div role='group' aria-label='Quem mais contrata, por perfil dos empregados' style='width:100%;height:92px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;"
            "font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>\"\n"
            "    & \"<div style='font-size:34px;line-height:42px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>\" & Titulo & \"</div>\"\n"
            "    & \"<div style='margin-top:4px;font-size:22px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>\" & Sub & \"</div></div>\"",
            f"HTML\\{P}")
    # ------------------------------------------------------------ KPIs
    SET = ("VAR SetFiltro = TREATAS(VALUES(D_Ct_Setor[setor]), D_Cnae[setor_principal])\n"
           "VAR NSet = COUNTROWS(VALUES(D_Ct_Setor[setor]))\n"
           "VAR Onde = IF(NSet = 1, \"no setor selecionado\", IF(NSet = COUNTROWS(ALL(D_Ct_Setor[setor])), \"em todos os setores\", \"nos setores selecionados\"))\n")
    # KPIs de mulheres e negros: o valor grande é o SALÁRIO MÉDIO (rotulado ao lado) e a linha de baixo traz a REPRESENTATIVIDADE (rotulada)
    for p, rotulo, aria, base_txt in (("Mul", "Mulheres empregadas", "KPI de mulheres", "dos empregos"),
                                      ("Neg", "Negros (pretos + pardos)", "KPI de negros", "dos que declararam cor")):
        for u in ("Total", "AFL"):
            todos = u == "Total"
            sf = ", KEEPFILTERS(SetFiltro)" if todos else ""
            onde = "Onde" if todos else '"no AFL"'
            valor = moeda("Sal") + ' & "<span style=\'font-size:22px;font-weight:400;color:#434446;\'> salário médio</span>"'
            linha3 = ('IF(ISBLANK(Rep), "sem dados para os filtros escolhidos", "Representatividade: <b style=\'color:#1D1E21;\'>" & FORMAT(Rep, "0.0%", "pt-BR") & " '
                      + base_txt + '</b> " & ' + onde + ')')
            add(f"KPI_Ct_{p}_{u}_HTML", f"KPI de {NOME_PERFIL[p]} ({u}): salário médio (valor grande) e representatividade (linha de baixo), cada um rotulado.",
                (SET if todos else "") + f"VAR Rep = CALCULATE([Ct_{p}_Rep]{sf})\nVAR Sal = CALCULATE([Ct_{p}_Sal]{sf})\n" +
                kpi_html(aria, f'"{rotulo}"', valor, linha3, '"#434446"', None, True), f"HTML\\{P}\\KPIs")
    # KPI de escolaridade: fontes maiores e legenda explícita da ordem dos valores (% de participação · R$ de salário médio)
    for u in ("Total", "AFL"):
        todos = u == "Total"
        sf = ", KEEPFILTERS(SetFiltro)" if todos else ""
        v = (SET if todos else "") + "VAR A = [Ano_Ref]\n" + f"VAR T = CALCULATE([Empregos], {A_}{sf})\n"
        for k, nivel in (("MC", "Médio Completo"), ("SC", "Superior Completo"), ("FC", "Fundamental Completo"), ("MI", "Médio Incompleto")):
            f = f'KEEPFILTERS(D_Escolaridade[escolaridade_agrupada] = "{nivel}")'
            v += f"VAR R{k} = DIVIDE(CALCULATE([Empregos], {A_}{sf}, {f}), T)\n"
            v += f"VAR S{k} = CALCULATE([Remuneracao_Media], {A_}{sf}, {f})\n"

        def celula(rot, k):
            return ("\"<div style='min-width:0;'><div style='font-size:20px;line-height:24px;color:#434446;white-space:nowrap;'>" + rot + "</div>"
                    "<div style='font-size:26px;line-height:30px;font-weight:600;white-space:nowrap;'>\" & " + pct(f"R{k}") + " & \" · \" & " + moeda(f"S{k}") + " & \"</div></div>\"")
        add(f"KPI_Ct_Esc_{u}_HTML", f"KPI de escolaridade ({u}): participação (%) e salário médio (R$) de quatro níveis, em fontes maiores.",
            v + "RETURN IF(ISBLANK(A), \"\",\n"
            "    \"<div role='group' aria-label='Escolaridade: participação e salário médio' style='width:100%;height:172px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;"
            "background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>\"\n"
            "    & \"<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>Escolaridade</div>\"\n"
            "    & \"<div style='font-size:18px;line-height:22px;color:#434446;white-space:nowrap;'>participação (%) · salário médio (R$)</div>\"\n"
            "    & \"<div style='display:grid;grid-template-columns:1fr 1fr;gap:4px 14px;margin-top:6px;font-variant-numeric:tabular-nums;'>\"\n"
            "    & " + celula("Médio completo", "MC") + "\n    & " + celula("Superior completo", "SC") + "\n    & " + celula("Fundamental completo", "FC") + "\n    & "
            + celula("Médio incompleto", "MI") + "\n    & \"</div></div>\")", f"HTML\\{P}\\KPIs")

    # ------------------------------------------------------------ títulos dos cards (o 1º texto também muda com o botão de valor)
    for p, de_quem, entre, barra, rep_txt, sal_txt in (
            ("Mul", "de mulheres", "as mulheres", ROXO,
             "Representatividade: participação de mulheres no total de empregos {onde}. Valores absolutos no tooltip.",
             "Salário médio: remuneração média de dezembro das mulheres {onde}, em R$ nominais. Detalhes no tooltip."),
            ("Neg", "de negros", "os negros", "#434446",
             "Representatividade: participação de negros (pretos + pardos) entre quem declarou cor {onde}. Valores absolutos no tooltip.",
             "Salário médio: remuneração média de dezembro dos negros {onde}, em R$ nominais. Detalhes no tooltip.")):
        for u in ("Total", "AFL"):
            todos = u == "Total"
            onde = "na divisão" if todos else "em cada CNAE"
            if todos:
                l1 = (f'IF(Sal, IF(Piores, "Divisões com menor salário médio entre {entre}", "Divisões com maior salário médio entre {entre}"), '
                      f'IF(Piores, "Divisões com menor representatividade {de_quem}", "Divisões com maior representatividade {de_quem}"))')
            else:
                l1 = f'IF(Sal, "CNAEs com maior salário médio entre {entre}", "CNAEs com maior representatividade {de_quem}")'
            add(f"Titulo_Ct_{p}_{u}_HTML", f"Título do ranking ({NOME_PERFIL[p]}, {u}); muda com o botão Representatividade / Salário médio.",
                SAL_VAR.format(met=MET[p]) + (PIORES_VAR if todos else "") + f"VAR L1 = {l1}\n"
                f"VAR L2 = IF(Sal, \"{sal_txt.format(onde=onde)}\", \"{rep_txt.format(onde=onde)}\")\n" + titulo_html("L1", "L2", f'"{barra}"'), f"HTML\\{P}\\Títulos")
    for u in ("Total", "AFL"):
        todos = u == "Total"
        onde = "cada divisão" if todos else "cada CNAE do AFL"
        lugar = "divisão" if todos else "CNAE do AFL"
        add(f"Titulo_Ct_Esc_{u}_HTML", f"Título do ranking por escolaridade ({u}); muda com os botões de nível e de valor.",
            SAL_VAR.format(met=MET["Esc"]) + NIV_VAR +
            "VAR NomeNivel = SWITCH(Niv, \"Até fundamental\", \"até o fundamental completo\", \"Médio incompleto\", \"médio incompleto\", \"Superior\", \"superior (completo ou não)\", \"médio completo\")\n"
            f"VAR L1 = IF(Sal, \"Salário médio por {lugar} — escolaridade\", \"Representatividade por {lugar} — escolaridade\")\n"
            f"VAR L2 = \"Nível: \" & NomeNivel & \" · \" & IF(Sal, \"salário médio de dezembro dos empregados do nível em {onde} (R$ nominais)\", "
            f"\"participação do nível no total de empregos de {onde}\") & \". Valores absolutos no tooltip.\"\n"
            + titulo_html("L1", "L2", '"#F58220"'), f"HTML\\{P}\\Títulos")

    # ------------------------------------------------------------ tooltips dos rankings (página Canvas, valores absolutos)
    for p, rotulo_rep, extra in (("Mul", "Mulheres no total de empregos", ""), ("Neg", "Negros entre quem declarou cor", ""),
                                 ("Esc", "Nível no total de empregos", "")):
        vars_ = (NIV_VAR if p == "Esc" else "") + (
            "VAR EhAfl = ISFILTERED(D_AflAtividade[nome])\n"
            "VAR Nome = IF(EhAfl, SELECTEDVALUE(D_AflAtividade[nome]), SELECTEDVALUE(D_Rank_Divisao[nm_divisao]))\n"
            f"VAR Rep = IF(EhAfl, [Ct_{p}_Rep], [Ct_{p}_Div_Rep])\n"
            f"VAR Sal = IF(EhAfl, [Ct_{p}_Sal], [Ct_{p}_Div_Sal])\n"
            f"VAR Qtd = IF(EhAfl, [Ct_{p}_Qtd], [Ct_{p}_Div_Qtd])\n"
            f"VAR Tot = IF(EhAfl, [Ct_{p}_Tot], [Ct_{p}_Div_Tot])\n"
            f"VAR RepAfl = IF(EhAfl || Nome = \"{AFL_ROTULO}\", BLANK(), CALCULATE([Ct_{p}_Rep], {G_AFL}))\n"
            f"VAR SalAfl = IF(EhAfl || Nome = \"{AFL_ROTULO}\", BLANK(), CALCULATE([Ct_{p}_Sal], {G_AFL}))\n")
        sub = ('"Empregos em 31/12/" & [Ano_Ref]' if p != "Esc" else
               '"Empregos em 31/12/" & [Ano_Ref] & " · nível: " & SWITCH(Niv, "Até fundamental", "até o fundamental completo", "Médio incompleto", "médio incompleto", "Superior", "superior (completo ou não)", "médio completo")')
        add(f"Tip_Ct_{p}_HTML", f"Tooltip do ranking por perfil ({NOME_PERFIL[p]}): participação, salário médio, quantidades e referência do AFL.",
            montar(vars_, "Nome", sub,
                   [linha(ROXO if p == "Mul" else CINZA, f'"{rotulo_rep}"', pct("Rep"), num("Qtd") + ' & " de " & ' + num("Tot") + ' & " empregos"'),
                    linha(CINZA, '"Salário médio (dezembro, R$ nominais)"', moeda("Sal")),
                    linha(AFL_COR, '"AFL (referência)"', pct("RepAfl") + ' & " · " & ' + moeda("SalAfl"), None, "NOT ISBLANK(RepAfl)")],
                   'IF(ISBLANK(RepAfl) || ISBLANK(Rep), "", "Participação em relação ao AFL: " & ' + pp("Rep", "RepAfl") + ' & ".")'), "HTML\\Tooltips de gráficos")
    return m
