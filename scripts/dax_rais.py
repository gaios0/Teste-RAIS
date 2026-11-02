"""DAX das páginas do painel RAIS (HTML dos KPIs, manchetes e títulos; séries, rankings e tooltips).

Etapa 1: tema Empregos (Todos os setores e AFL). Segue o padrão das medidas HTML do RF (dax_ativas_decada / dax_movimentacoes):
  - todo texto dinâmico passa por esc() antes de entrar no HTML;
  - KPIs de 156 px, manchete de 118 px, títulos com barra à esquerda;
  - a comparação de referência é sempre AFL × Comparável (chip cinza "Comparáveis x · ref.").
Retorna tuplas (nome, doc, dax, pasta, formato, oculta) iguais às de modelo_base.medidas().
"""

QUEBRA = 2022
INICIO = 2009
AFL_ROTULO = "AFL · conjunto de 6 CNAEs"
ANO_FIXO = "REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = {a}"
G_AFL = 'REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "AFL"'
G_COMP = 'REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = "Comparável"'
G_TODOS = "REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), REMOVEFILTERS(D_Comparavel), REMOVEFILTERS(D_AflAtividade)"


def esc(x):
    """Escapa texto dinâmico antes de inseri-lo no HTML."""
    return ('SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(' + x + ', "&", "&amp;"), "<", "&lt;"), ">", "&gt;"), '
            'UNICHAR(34), "&quot;"), UNICHAR(39), "&#39;")')


# ------------------------------------------------------------------ peças de HTML
def chip_afl(txt):
    return ('"<span style=\'display:inline-block;padding:1px 9px;border:1px solid #F58220;border-radius:6px;background:#FDF7F1;color:#B86218;'
            'font-size:20px;line-height:26px;font-weight:600;\'>AFL " & ' + txt + ' & "</span>"')


def chip_ref(txt):
    return ('"<span style=\'display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;'
            'font-size:20px;line-height:26px;font-weight:600;\'>Comparáveis " & ' + txt + ' & " <span style=\'font-weight:400;font-size:17px;color:#434446;\'>· ref.</span></span>"')


def kpi_html(aria, rotulo, valor, linha3, cor3='"#434446"', chips=None):
    """KPI de 156 px: rótulo, valor, linha de comparação e (opcional) chips."""
    extra = (' & "<div style=\'display:flex;gap:8px;margin-top:3px;white-space:nowrap;\'>" & ' + chips + ' & "</div>"') if chips else ""
    return (
        "RETURN\n"
        f"    \"<div role='group' aria-label='{aria}' style='width:100%;height:156px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;"
        "background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>\"\n"
        "        & \"<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>\" & " + rotulo + " & \"</div>\"\n"
        "        & \"<div style='margin-top:2px;font-size:53px;line-height:58px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap;'>\" & " + valor + " & \"</div>\"\n"
        "        & \"<div style='margin-top:3px;font-size:22px;line-height:26px;color:\" & " + cor3 + " & \";white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>\" & " + linha3 + " & \"</div>\""
        + extra + "\n        & \"</div>\"")


def titulo_html(l1, l2, cor_barra='"#1D1E21"', detalhe=None):
    """Título-afirmação de card: barra à esquerda, L1 semibold 24 px e L2 20 px (padrão do RF)."""
    det = f" title='\" & {esc(detalhe)} & \"'" if detalhe else ""
    return (
        "RETURN\n"
        f"    \"<div role='heading' aria-level='3'{det} style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:4px 56px 4px 0;display:flex;align-items:flex-start;gap:10px;"
        "background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;'>\"\n"
        "        & \"<span aria-hidden='true' style='flex:none;width:4px;align-self:stretch;min-height:28px;border-radius:2px;background:\" & " + cor_barra + " & \";'></span>\"\n"
        "        & \"<span style='display:block;min-width:0;max-height:100%;overflow:hidden;font-variant-numeric:tabular-nums;'>\"\n"
        "        & \"<span style='display:block;font-size:24px;line-height:28px;font-weight:600;color:#1D1E21;'>\" & " + esc(l1) + " & \"</span>\"\n"
        "        & IF(" + l2 + " = \"\", \"\", \"<span style='display:block;font-size:20px;line-height:26px;color:#434446;'>\" & " + esc(l2) + " & \"</span>\") & \"</span></div>\"")


def seta(v):
    return (f'VAR Icone = SWITCH(TRUE(), {v} > 0, "▲", {v} < 0, "▼", "●")\n'
            f'VAR Cor = SWITCH(TRUE(), {v} > 0, "#137547", {v} < 0, "#B42318", "#434446")\n')


FMT_PCT = 'FORMAT({v}, "0.0%", "pt-BR")'


def pct(v, sinal=False):
    s = f'IF(ISBLANK({v}), "—", ' + (f'IF({v} > 0, "+", IF({v} < 0, "−", "")) & FORMAT(ABS({v}), "0.0%", "pt-BR")' if sinal else f'FORMAT({v}, "0.0%", "pt-BR")') + ")"
    return s


def num(v):
    return f'FORMAT({v}, "#,0", "pt-BR")'


# ------------------------------------------------------------------ medidas
def medidas():
    m = []

    def add(nome, doc, dax, pasta, fmt=None, oculta=False):
        m.append((nome, doc, dax, pasta, fmt, oculta))

    P = "Empregos"
    # --- base de grupos e ranking
    add("Emp_Grupo_AFL_Ano", "Empregos do AFL em 31/12 do ano da variável A (para uso em tabelas de anos).", f"VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], {G_AFL}, {ANO_FIXO.format(a='A')}))", f"{P}\\Apoio", "#,0", True)
    add("Empregos_Ref_Todos", "Empregos do ano de referência ignorando setor, comparabilidade e atividade (mantém UF, sexo, escolaridade e raça).",
        f"VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], {G_TODOS}, {ANO_FIXO.format(a='A')}))", f"{P}\\Apoio", "#,0")
    add("Emp_Sequencia_Altas_AFL", "Quantos anos seguidos o emprego do AFL subiu, terminando no ano de referência e sem atravessar a quebra de 2022.",
        "VAR A = [Ano_Ref]\nVAR I = [Ano_Inicio_Trecho]\n"
        "VAR T = ADDCOLUMNS(GENERATESERIES(I + 1, MAX(A, I + 1)), \"@var\", VAR y = [Value] RETURN\n"
        f"    CALCULATE([Empregos], {G_AFL}, {ANO_FIXO.format(a='y')}) - CALCULATE([Empregos], {G_AFL}, {ANO_FIXO.format(a='y - 1')}))\n"
        "VAR UltimaNaoAlta = MAXX(FILTER(T, [@var] <= 0), [Value])\n"
        "RETURN IF(A > I, A - COALESCE(UltimaNaoAlta, I), 0)", f"{P}\\Apoio", "0", True)

    # --- séries (índice base 100 no primeiro ano do trecho; Pré = 2009–2021, Pós = 2022 em diante, para a linha não atravessar a quebra)
    for sufixo, g, nome in (("AFL", G_AFL, "AFL"), ("Comp", G_COMP, "Comparável")):
        for trecho, cond, rot in (("Pre", f"A < {QUEBRA}", "2009–2021"), ("Pos", f"A >= {QUEBRA}", "2022 em diante")):
            add(f"Emp_Indice_{sufixo}_{trecho}", f"Índice de empregos do {nome} (base 100 = primeiro ano do trecho), trecho {rot}; BLANK fora do trecho.",
                "VAR A = [Ano_Ref]\nVAR I = [Ano_Inicio_Trecho]\n"
                f"VAR Fim = CALCULATE([Empregos], {g}, {ANO_FIXO.format(a='A')})\n"
                f"VAR Base = CALCULATE([Empregos], {g}, {ANO_FIXO.format(a='I')})\n"
                f"RETURN IF(NOT ISBLANK(A) && {cond} && Base > 0, DIVIDE(Fim, Base) * 100)", f"{P}\\Séries", "0.0")

    # --- KPIs
    def var_linha(u):
        """Linha de variação do KPI de empregos (sobre o ano anterior, ou aviso quando não há comparação)."""
        grupo = "[Empregos_Ref]"
        return (
            "VAR A = [Ano_Ref]\nVAR Valor = [Empregos_Ref]\nVAR Variacao = [Empregos_Var]\nVAR VarPct = [Empregos_Var_Pct]\n" + seta("Variacao") +
            "VAR Linha = IF(NOT ISBLANK(Variacao), Icone & \" \" & IF(Variacao > 0, \"+\", IF(Variacao < 0, \"−\", \"\")) & " + num("ABS(Variacao)") + " & \" (\" & " + pct("VarPct", True) + " & \") sobre \" & (A - 1),\n"
            f"    IF(A = {QUEBRA}, \"2022 não se compara com 2021 (nova fonte: eSocial)\", \"Primeiro ano da série\"))\n"
            "VAR CorLinha = IF(ISBLANK(Variacao), \"#434446\", Cor)\n")

    add("KPI_Emp_AFL_HTML", "KPI de empregos (página AFL): estoque em 31/12 com variação e referência dos comparáveis.",
        var_linha("AFL") + "VAR VarComp = [Empregos_Var_Pct_Comparavel]\n" +
        kpi_html("KPI de empregos formais", '"Empregos em 31/12/" & A', num("Valor"), "Linha", "CorLinha", chip_ref(pct("VarComp", True))), f"HTML\\{P}\\KPIs")
    add("KPI_Emp_Total_HTML", "KPI de empregos (página Todos os setores): estoque em 31/12 com variação, chip AFL e referência dos comparáveis.",
        var_linha("Total") + "VAR VarAFL = [Empregos_Var_Pct_AFL]\nVAR VarComp = [Empregos_Var_Pct_Comparavel]\n" +
        kpi_html("KPI de empregos formais", '"Empregos em 31/12/" & A', num("Valor"), "Linha", "CorLinha", chip_afl(pct("VarAFL", True)) + " & " + chip_ref(pct("VarComp", True))), f"HTML\\{P}\\KPIs")

    add("KPI_Peso_AFL_HTML", "KPI de peso (página AFL): AFL ÷ (AFL + comparáveis) e participação em todo o emprego formal.",
        "VAR Afl = [Empregos_Ref_AFL]\nVAR Comp = [Empregos_Ref_Comparavel]\nVAR Todos = [Empregos_Ref_Todos]\n"
        "VAR Peso = DIVIDE(Afl, Afl + Comp)\nVAR PesoTodos = DIVIDE(Afl, Todos)\n" +
        kpi_html("KPI de peso do AFL", '"Peso nos empregos comparáveis"', 'IF(ISBLANK(Peso), "—", FORMAT(Peso, "0.0%", "pt-BR"))',
                 '"dos empregos do AFL + comparáveis"', '"#434446"', '"<span style=\'font-size:21px;color:#434446;\'>" & ' + pct("PesoTodos") + ' & " de todo o emprego formal</span>"'), f"HTML\\{P}\\KPIs")
    add("KPI_Peso_Total_HTML", "KPI de peso (página Todos os setores): AFL ÷ todo o emprego formal e AFL ÷ (AFL + comparáveis).",
        "VAR Afl = [Empregos_Ref_AFL]\nVAR Comp = [Empregos_Ref_Comparavel]\nVAR Todos = [Empregos_Ref_Todos]\n"
        "VAR Peso = DIVIDE(Afl, Todos)\nVAR PesoComp = DIVIDE(Afl, Afl + Comp)\n" +
        kpi_html("KPI de peso do AFL", '"Peso do AFL"', 'IF(ISBLANK(Peso), "—", FORMAT(Peso, "0.0%", "pt-BR"))', '"de todo o emprego formal"', '"#434446"',
                 '"<span style=\'display:inline-block;padding:1px 9px;border:1px solid #434446;border-radius:6px;background:#F2F4F7;color:#1D1E21;font-size:20px;line-height:26px;font-weight:600;\'>" & '
                 + pct("PesoComp") + ' & " do AFL + comparáveis <span style=\'font-weight:400;font-size:17px;color:#434446;\'>· ref.</span></span>"'), f"HTML\\{P}\\KPIs")

    def cresc(u):
        return ("VAR A = [Ano_Ref]\nVAR I = [Ano_Inicio_Trecho]\nVAR Cresc = [Empregos_Cresc_Medio_Ano]\nVAR CrescComp = [Empregos_Cresc_Medio_Ano_Comparavel]\nVAR CrescAfl = [Empregos_Cresc_Medio_Ano_AFL]\n"
                "VAR Seq = [Emp_Sequencia_Altas_AFL]\n")
    add("KPI_Cresc_AFL_HTML", "KPI de crescimento médio ao ano no trecho (página AFL), com referência dos comparáveis.",
        cresc("AFL") + "VAR Linha = IF(A > I, IF(Seq >= 2, Seq & \" altas seguidas\", IF(Seq = 1, \"alta no último ano\", \"queda no último ano\")), \"Primeiro ano do trecho: ainda sem crescimento a medir\")\n" +
        kpi_html("KPI de crescimento médio ao ano", '"Crescimento médio ao ano desde " & I', 'IF(ISBLANK(Cresc), "—", ' + pct("Cresc", True) + ')', "Linha", '"#434446"', chip_ref(pct("CrescComp", True))), f"HTML\\{P}\\KPIs")
    add("KPI_Cresc_Total_HTML", "KPI de crescimento médio ao ano no trecho (página Todos os setores), com chips AFL e comparáveis.",
        cresc("Total") + "VAR Linha = IF(A > I, \"por ano, de \" & I & \" a \" & A, \"Primeiro ano do trecho: ainda sem crescimento a medir\")\n" +
        kpi_html("KPI de crescimento médio ao ano", '"Crescimento médio ao ano desde " & I', 'IF(ISBLANK(Cresc), "—", ' + pct("Cresc", True) + ')', "Linha", '"#434446"',
                 chip_afl(pct("CrescAfl", True)) + " & " + chip_ref(pct("CrescComp", True))), f"HTML\\{P}\\KPIs")

    # --- contexto e manchete
    contexto_comum = (
        "VAR A = [Ano_Ref]\nVAR TemUF = ISFILTERED(D_UF[uf])\nVAR NUF = COUNTROWS(VALUES(D_UF[uf]))\n"
        "VAR Local = IF(NOT TemUF || NUF = COUNTROWS(ALL(D_UF[uf])), \"Brasil\", IF(NUF = 1, SELECTEDVALUE(D_UF[estado]), NUF & \" UFs\"))\n"
        "VAR Sexo = IF(ISFILTERED(D_Sexo[sexo]), CONCATENATEX(VALUES(D_Sexo[sexo]), D_Sexo[sexo], \", \"), \"\")\n"
        "VAR Esc = IF(ISFILTERED(D_Escolaridade[escolaridade_agrupada]), CONCATENATEX(VALUES(D_Escolaridade[escolaridade_agrupada]), D_Escolaridade[escolaridade_agrupada], \", \"), \"\")\n"
        "VAR Raca = IF(ISFILTERED(D_Raca[raca_cor]), CONCATENATEX(VALUES(D_Raca[raca_cor]), D_Raca[raca_cor], \", \"), \"\")\n")
    partes = ('VAR Partes = FILTER(UNION(ROW("@o", 1, "@t", "31/12/" & A), ROW("@o", 2, "@t", Local), ROW("@o", 3, "@t", Setor), ROW("@o", 4, "@t", Sexo),\n'
              '    ROW("@o", 5, "@t", Esc), ROW("@o", 6, "@t", Raca), ROW("@o", 7, "@t", "RAIS (" & IF(A >= 2022, "eSocial", "declaratória") & ")")), NOT ISBLANK([@t]) && [@t] <> "")\n'
              'VAR Texto = CONCATENATEX(Partes, [@t], " · ", [@o], ASC)\n')
    add("Contexto_Emp_Total", "Linha de contexto da página Empregos · Todos os setores.",
        contexto_comum + 'VAR Setor = IF(ISFILTERED(D_Comparavel[comparavel_AFL]), "setores comparáveis ao AFL", "todos os setores")\n' + partes + "RETURN IF(ISBLANK(A), \"\", Texto)", f"{P}\\Apoio", None, True)
    add("Contexto_Emp_AFL", "Linha de contexto da página Empregos · AFL.",
        contexto_comum + 'VAR Setor = IF(ISFILTERED(D_AflAtividade[nome]) && COUNTROWS(VALUES(D_AflAtividade[nome])) < COUNTROWS(ALL(D_AflAtividade[nome])), CONCATENATEX(VALUES(D_AflAtividade[nome]), D_AflAtividade[nome], ", "), "alimentação fora do lar (AFL)")\n'
        + partes + "RETURN IF(ISBLANK(A), \"\", Texto)", f"{P}\\Apoio", None, True)

    def manchete(u):
        topo = ("VAR A = [Ano_Ref]\nVAR NUF = COUNTROWS(VALUES(D_UF[uf]))\nVAR Prep = IF(NOT ISFILTERED(D_UF[uf]) || NUF = COUNTROWS(ALL(D_UF[uf])), \"No Brasil\", IF(NUF = 1, \"Em \" & SELECTEDVALUE(D_UF[estado]), \"Nas \" & NUF & \" UFs escolhidas\"))\n"
                "VAR Valor = [Empregos_Ref]\nVAR Variacao = [Empregos_Var]\nVAR VarPct = [Empregos_Var_Pct]\nVAR Seq = [Emp_Sequencia_Altas_AFL]\nVAR Contexto = [Contexto_Emp_" + u + "]\n")
        if u == "Total":
            fecho = ('VAR Pos = [Emp_Posicao_AFL_Divisao]\nVAR Divs = [Emp_Total_Divisoes]\n'
                     'VAR Texto = Prep & ", o emprego formal fechou " & A & " com " & ' + num("Valor") + ' & " vínculos" & IF(ISBLANK(Pos), "", "; o AFL é a " & Pos & "ª maior divisão entre " & Divs)\n')
        else:
            fecho = ('VAR Fecho = SWITCH(TRUE(), ISBLANK(Variacao), IF(A = ' + str(QUEBRA) + ', "primeiro ano da fonte eSocial", "primeiro ano da série"),\n'
                     '    Variacao > 0, IF(Seq >= 2, Seq & "ª alta seguida", "alta de " & ' + pct("VarPct") + '), Variacao < 0, "queda de " & ' + pct("ABS(VarPct)") + ' & " sobre " & (A - 1), "estável")\n'
                     'VAR Texto = Prep & ", o AFL fechou " & A & " com " & ' + num("Valor") + ' & " empregos formais: " & Fecho\n')
        return (topo + fecho + "VAR Valido = NOT ISBLANK(A) && NOT ISBLANK(Valor)\nRETURN\n    IF(NOT Valido,\n"
                "        \"<div role='text' style='width:100%;height:118px;font-family:Segoe UI,Arial,sans-serif;font-size:24px;color:#434446;'>Não há dados para os filtros selecionados.</div>\",\n"
                "        \"<div role='group' aria-label='Resumo do emprego formal' style='width:100%;height:118px;box-sizing:border-box;margin:0;padding:0;overflow:hidden;background:transparent;font-family:Segoe UI,Arial,sans-serif;color:#1D1E21;'>\"\n"
                "            & \"<div style='height:48px;display:flex;align-items:center;white-space:nowrap;overflow:hidden;'><span style='min-width:0;font-size:36px;line-height:42px;font-weight:600;font-variant-numeric:tabular-nums;overflow:hidden;text-overflow:ellipsis;'>\" & " + esc("Texto") + " & \"</span></div>\"\n"
                "            & \"<div style='height:30px;margin:4px 0 0;font-size:24px;line-height:30px;color:#434446;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>\" & " + esc("Contexto") + " & \"</div>\"\n"
                "        & \"</div>\")")
    add("Manchete_Emp_Total_HTML", "Manchete da página Empregos · Todos os setores.", manchete("Total"), f"HTML\\{P}")
    add("Manchete_Emp_AFL_HTML", "Manchete da página Empregos · AFL.", manchete("AFL"), f"HTML\\{P}")

    # --- título da série (índice)
    serie = ("VAR A = [Ano_Ref]\nVAR I = [Ano_Inicio_Trecho]\nVAR Afl = [Empregos_Ref_AFL]\nVAR Comp = [Empregos_Ref_Comparavel]\n"
             f"VAR AflI = CALCULATE([Empregos], {G_AFL}, {ANO_FIXO.format(a='I')})\nVAR CompI = CALCULATE([Empregos], {G_COMP}, {ANO_FIXO.format(a='I')})\n"
             "VAR CAfl = DIVIDE(Afl, AflI) - 1\nVAR CComp = DIVIDE(Comp, CompI) - 1\n"
             f"VAR Afl19 = CALCULATE([Empregos], {G_AFL}, {ANO_FIXO.format(a='2019')})\nVAR Afl20 = CALCULATE([Empregos], {G_AFL}, {ANO_FIXO.format(a='2020')})\n"
             f"VAR Comp19 = CALCULATE([Empregos], {G_COMP}, {ANO_FIXO.format(a='2019')})\nVAR Comp20 = CALCULATE([Empregos], {G_COMP}, {ANO_FIXO.format(a='2020')})\n"
             "VAR L1 = IF(ISBLANK(A), \"Sem dados para os filtros escolhidos\", IF(A <= I, I & \" é o primeiro ano do trecho: ainda não há crescimento a comparar\",\n"
             "    \"Desde \" & I & \", o emprego do AFL cresceu \" & " + pct("CAfl") + " & \" e o dos comparáveis, \" & " + pct("CComp") + "))\n"
             "VAR L2 = IF(ISBLANK(A), \"\", IF(A >= " + str(QUEBRA) + ", \"Índice de empregos em 31/12, base 100 = 31/12/\" & I & \". 2021 e os anos anteriores ficam no trecho anterior (nova fonte: eSocial)\",\n"
             "    \"Índice de empregos em 31/12, base 100 = 31/12/\" & I & IF(Afl19 > 0 && Afl20 > 0 && Comp19 > 0, \". Em 2020 o AFL perdeu \" & " + pct("ABS(DIVIDE(Afl20, Afl19) - 1)") + " & \" dos empregos; os comparáveis, \" & " + pct("ABS(DIVIDE(Comp20, Comp19) - 1)") + ", \"\")))\n")
    add("Titulo_Emp_Serie_HTML", "Título do gráfico de série (índice): crescimento desde o início do trecho, AFL × comparáveis.",
        serie + titulo_html("L1", "L2", '"#F58220"'), f"HTML\\{P}\\Títulos")

    # --- contratos (tabela AFL × Comparáveis, categorias exclusivas)
    def cat_sum(g, cat):
        base = f"CALCULATE([Empregos], {g}, {ANO_FIXO.format(a='A')}, "
        cond = {"clt": 'F_rais[trabalho_intermitente] <> "Sim", F_rais[modalidade_contrato] <> "Aprendiz", F_rais[trabalho_parcial] <> "Sim", F_rais[modalidade_contrato] = "CLT Prazo Indeterminado"',
                "det": 'F_rais[trabalho_intermitente] <> "Sim", F_rais[modalidade_contrato] <> "Aprendiz", F_rais[trabalho_parcial] <> "Sim", '
                       'F_rais[modalidade_contrato] IN {"CLT Prazo Determinado", "Contrato por Prazo Determinado", "Temporário", "Contrato Temporário"}',
                "inter": 'F_rais[trabalho_intermitente] = "Sim"',
                "parc": 'F_rais[trabalho_intermitente] <> "Sim", F_rais[modalidade_contrato] <> "Aprendiz", F_rais[trabalho_parcial] = "Sim"',
                "apr": 'F_rais[trabalho_intermitente] <> "Sim", F_rais[modalidade_contrato] = "Aprendiz"'}[cat]
        return base + cond + ")"
    cats = [("clt", "CLT por prazo indeterminado"), ("det", "Prazo determinado ou temporário"), ("inter", "Intermitente"), ("parc", "Parcial"), ("apr", "Aprendiz")]
    vars_ = "VAR A = [Ano_Ref]\n"
    for sufixo, g in (("A", G_AFL), ("C", G_COMP)):
        vars_ += f"VAR Tot{sufixo} = CALCULATE([Empregos], {g}, {ANO_FIXO.format(a='A')})\n"
        for k, _ in cats:
            vars_ += f"VAR {k}{sufixo} = {cat_sum(g, k)}\n"
    def linha(k, rot):
        return ("\"<tr><td style='padding:9px 0;border-top:1px solid #E8E8E9;'>" + rot + "</td><td style='text-align:right;font-weight:600;border-top:1px solid #E8E8E9;'>\" & "
                f"IF(ISBLANK(TotA) || TotA = 0, \"—\", FORMAT(DIVIDE({k}A, TotA), \"0.0%\", \"pt-BR\")) & \"</td><td style='text-align:right;color:#434446;border-top:1px solid #E8E8E9;'>\" & "
                f"IF(ISBLANK(TotC) || TotC = 0, \"—\", FORMAT(DIVIDE({k}C, TotC), \"0.0%\", \"pt-BR\")) & \"</td></tr>\"")
    corpo = " & ".join(linha(k, r) for k, r in cats)
    add("Emp_Contratos_HTML", "Tabela de contratos: AFL × Comparáveis, em % dos empregos de 31/12 do ano de referência (categorias exclusivas, na ordem intermitente, aprendiz, parcial, CLT, prazo determinado).",
        vars_ + "RETURN IF(ISBLANK(A) || TotA = 0, \"<div style='font-family:Segoe UI,Arial,sans-serif;font-size:21px;color:#434446;'>Sem dados para os filtros escolhidos.</div>\",\n"
        "    \"<table style='width:100%;border-collapse:collapse;font-family:Segoe UI,Arial,sans-serif;font-size:21px;font-variant-numeric:tabular-nums;'><tr style='color:#434446;'>"
        "<th style='text-align:left;font-weight:600;padding-bottom:6px;'>Contrato</th><th style='text-align:right;font-weight:600;color:#B86218;'>AFL</th><th style='text-align:right;font-weight:600;'>Comparáveis</th></tr>\" & " + corpo + " & \"</table>\")",
        f"HTML\\{P}")
    add("Titulo_Emp_Contrato_HTML", "Título do card de contratos: % de CLT por prazo indeterminado no AFL e o contraste com os comparáveis.",
        vars_ + "VAR PA = DIVIDE(cltA, TotA)\nVAR PC = DIVIDE(cltC, TotC)\nVAR DA = DIVIDE(detA, TotA)\nVAR DC = DIVIDE(detC, TotC)\n"
        "VAR L1 = IF(ISBLANK(A) || TotA = 0, \"Sem dados para os filtros escolhidos\", " + pct("PA") + " & \" dos empregos do AFL são CLT por prazo indeterminado\")\n"
        "VAR L2 = IF(L1 = \"Sem dados para os filtros escolhidos\", \"\", \"Prazo determinado ou temporário: \" & " + pct("DA") + " & \" no AFL e \" & " + pct("DC") + " & \" nos comparáveis\")\n"
        + titulo_html("L1", "L2", '"#1D1E21"'), f"HTML\\{P}\\Títulos")

    # --- ranking de divisões (Todos os setores): D_Rank_Divisao é local e desconectada
    add("Emp_Divisao", "Empregos em 31/12 da divisão de D_Rank_Divisao no ano de referência; o item AFL usa os seis CNAEs e as divisões não incluem os CNAEs do AFL.",
        "VAR Nome = SELECTEDVALUE(D_Rank_Divisao[nm_divisao])\nVAR A = [Ano_Ref]\n"
        f"RETURN IF(ISBLANK(Nome) || ISBLANK(A), BLANK(), IF(Nome = \"{AFL_ROTULO}\", [Empregos_Ref_AFL],\n"
        "    CALCULATE([Empregos_Ref], REMOVEFILTERS(D_GrupoSetor), KEEPFILTERS(D_Cnae[nm_divisao] = Nome), KEEPFILTERS(D_Cnae[setor_afl] = \"Não\"))))", f"{P}\\Ranking", "#,0")
    add("Emp_Divisao_Top", "Valor do ranking: as 10 maiores divisões em empregos e sempre o AFL; as demais voltam BLANK.",
        f"VAR EhAFL = SELECTEDVALUE(D_Rank_Divisao[nm_divisao]) = \"{AFL_ROTULO}\"\nVAR Valor = [Emp_Divisao]\n"
        "VAR Posicao = IF(NOT ISBLANK(Valor), RANKX(ALLSELECTED(D_Rank_Divisao[nm_divisao]), [Emp_Divisao], , DESC, DENSE))\nRETURN IF(NOT ISBLANK(Valor) && (EhAFL || Posicao <= 10), Valor)", f"{P}\\Ranking", "#,0")
    add("Cor_Emp_Divisao", "Cor do ranking: AFL em laranja, demais divisões em cinza neutro.", f"IF(SELECTEDVALUE(D_Rank_Divisao[nm_divisao]) = \"{AFL_ROTULO}\", \"#F58220\", \"#DDDDDE\")", f"{P}\\Ranking", None, True)
    add("Emp_Posicao_AFL_Divisao", "Posição do AFL entre todas as divisões em empregos (ignora os botões de setor).",
        "VAR Divs = ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), \"@v\", [Emp_Divisao])\nVAR Validas = FILTER(Divs, NOT ISBLANK([@v]))\n"
        f"VAR ValorAFL = MAXX(FILTER(Validas, [nm_divisao] = \"{AFL_ROTULO}\"), [@v])\nRETURN IF(NOT ISBLANK(ValorAFL), COUNTROWS(FILTER(Validas, [@v] > ValorAFL)) + 1)", f"{P}\\Ranking", "0", True)
    add("Emp_Total_Divisoes", "Quantidade de divisões com empregos no contexto (ignora os botões de setor).",
        "COUNTROWS(FILTER(ADDCOLUMNS(ALL(D_Rank_Divisao[nm_divisao]), \"@v\", [Emp_Divisao]), NOT ISBLANK([@v])))", f"{P}\\Ranking", "0", True)
    add("Titulo_Emp_Ranking_HTML", "Título do ranking de divisões: posição do AFL em empregos e em crescimento.",
        "VAR Pos = [Emp_Posicao_AFL_Divisao]\nVAR N = [Emp_Total_Divisoes]\n"
        "VAR L1 = IF(ISBLANK(Pos), \"O AFL não tem empregos para os filtros escolhidos\", IF(Pos = 1, \"O AFL é a maior divisão do emprego formal entre as \" & N, \"O AFL é a \" & Pos & \"ª maior divisão do emprego formal entre as \" & N))\n"
        "VAR L2 = IF(ISBLANK(Pos), \"\", \"O gráfico mostra as 10 maiores divisões e o AFL, em empregos de 31/12/\" & [Ano_Ref] & \". Compare por participação, nunca o AFL contra o total.\")\n"
        + titulo_html("L1", "L2", '"#F58220"'), f"HTML\\{P}\\Títulos")

    # --- atividades do AFL (página AFL)
    add("Emp_Atividade_Var", "Variação % dos empregos da atividade do AFL sobre o ano anterior (BLANK quando não há ano comparável).",
        "[Empregos_Var_Pct]", f"{P}\\Atividades", "+0.0%;-0.0%;0.0%")
    add("Titulo_Emp_Atividades_HTML", "Título das atividades do AFL: atividade líder e peso nos empregos do AFL.",
        "VAR T = FILTER(ADDCOLUMNS(VALUES(D_AflAtividade[nome]), \"@v\", [Empregos_Ref]), NOT ISBLANK([@v]))\nVAR Tot = SUMX(T, [@v])\n"
        "VAR Lider = TOPN(1, T, [@v], DESC, D_AflAtividade[nome], ASC)\nVAR Nome = CONCATENATEX(Lider, D_AflAtividade[nome], \"\")\nVAR Peso = DIVIDE(MAXX(Lider, [@v]), Tot)\n"
        "VAR L1 = IF(Tot = 0, \"Sem dados para os filtros escolhidos\", IF(COUNTROWS(T) = 1, Nome & \" reúne todos os empregos do filtro\", Nome & \" concentra \" & " + pct("Peso") + " & \" dos empregos do AFL\"))\n"
        "VAR L2 = IF(Tot = 0, \"\", \"Empregos em 31/12/\" & [Ano_Ref] & \" nas 6 atividades (CNAEs) do AFL\")\n" + titulo_html("L1", "L2", '"#1D1E21"'), f"HTML\\{P}\\Títulos")

    # --- UF
    add("Emp_UF_Top", "Empregos por UF (as 10 maiores); as demais voltam BLANK.",
        "VAR Valor = [Empregos_Ref]\nVAR Posicao = IF(NOT ISBLANK(Valor), RANKX(ALLSELECTED(D_UF[uf]), [Empregos_Ref], , DESC, DENSE))\nRETURN IF(NOT ISBLANK(Valor) && Posicao <= 10, Valor)", f"{P}\\UF", "#,0")
    add("Emp_UF_Peso_AFL", "Peso do AFL nos empregos comparáveis da UF: AFL ÷ (AFL + comparáveis).", "DIVIDE([Empregos_Ref_AFL], [Empregos_Ref_AFL] + [Empregos_Ref_Comparavel])", f"{P}\\UF", "0.0%")
    add("Emp_UF_Peso_Top", "Peso do AFL nos empregos comparáveis, só nas 10 UFs com mais empregos do AFL.",
        "VAR Valor = [Emp_UF_Peso_AFL]\nVAR Posicao = IF(NOT ISBLANK([Empregos_Ref_AFL]), RANKX(ALLSELECTED(D_UF[uf]), [Empregos_Ref_AFL], , DESC, DENSE))\nRETURN IF(NOT ISBLANK(Valor) && Posicao <= 10, Valor)", f"{P}\\UF", "0.0%")
    add("Titulo_Emp_UF_AFL_HTML", "Título das UFs (página AFL): UF líder e participação nos empregos do AFL, com a UF onde o AFL mais pesa.",
        "VAR T = FILTER(ADDCOLUMNS(VALUES(D_UF[uf]), \"@v\", [Empregos_Ref], \"@p\", [Emp_UF_Peso_AFL]), NOT ISBLANK([@v]))\nVAR Tot = SUMX(T, [@v])\n"
        "VAR Lider = TOPN(1, T, [@v], DESC, D_UF[uf], ASC)\nVAR UF = CONCATENATEX(Lider, D_UF[uf], \"\")\nVAR Mais = TOPN(1, T, [@p], DESC, D_UF[uf], ASC)\nVAR UFMais = CONCATENATEX(Mais, D_UF[uf], \"\")\nVAR PMais = MAXX(Mais, [@p])\n"
        "VAR L1 = IF(Tot = 0, \"Sem dados para os filtros escolhidos\", IF(COUNTROWS(T) = 1, UF & \" reúne os empregos do filtro\", UF & \" tem \" & " + pct("DIVIDE(MAXX(Lider, [@v]), Tot)") + " & \" dos empregos do AFL\"))\n"
        "VAR L2 = IF(Tot = 0 || COUNTROWS(T) = 1, \"\", \"Onde o AFL pesa mais: \" & UFMais & \" (\" & " + pct("PMais") + " & \" dos empregos comparáveis)\")\n" + titulo_html("L1", "L2", '"#1D1E21"'), f"HTML\\{P}\\Títulos")
    add("Titulo_Emp_UF_Total_HTML", "Título das UFs (página Todos os setores): UF onde o AFL mais pesa no emprego comparável.",
        "VAR T = FILTER(ADDCOLUMNS(VALUES(D_UF[uf]), \"@a\", [Empregos_Ref_AFL], \"@p\", [Emp_UF_Peso_AFL]), NOT ISBLANK([@a]))\n"
        "VAR Mais = TOPN(1, T, [@p], DESC, D_UF[uf], ASC)\nVAR UFMais = CONCATENATEX(Mais, D_UF[uf], \"\")\nVAR PMais = MAXX(Mais, [@p])\n"
        "VAR L1 = IF(COUNTROWS(T) = 0, \"Sem dados para os filtros escolhidos\", IF(COUNTROWS(T) = 1, \"Peso do AFL nos empregos comparáveis\", \"Em \" & UFMais & \", o AFL é \" & " + pct("PMais") + " & \" do emprego comparável\"))\n"
        "VAR L2 = IF(COUNTROWS(T) = 0, \"\", \"Peso do AFL nos empregos comparáveis, nas 10 UFs com mais empregos do AFL\")\n" + titulo_html("L1", "L2", '"#1D1E21"'), f"HTML\\{P}\\Títulos")
    add("Info_Gatilho_Valor", "Valor constante usado pelos mini-gráficos transparentes que abrem tooltips (botões ⓘ).", "1", "Base\\Apoio", "0", True)
    return m
