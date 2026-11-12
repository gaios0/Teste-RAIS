"""Tooltips explicativos (HTML) dos KPIs: o que o número significa, com um exemplo calculado com os valores da página.

Cada medida alimenta uma página de tooltip (600 × 450) criada por pagina_rais.py; o contexto de filtros vem do visual sobre o qual o mouse passa.
Retorna tuplas (nome, doc, dax, pasta, formato, oculta) como as demais; sempre começam com VAR (medida sem VAR não pode começar com RETURN).
"""
from dax_rais import esc, num, pct, titulo_html

P = "HTML\\Dicas"
ESTILO = "font-family:Segoe UI,Arial,sans-serif;padding:20px 24px;box-sizing:border-box;width:100%;height:100%;color:#1D1E21;"


def dica(variaveis, titulo, definicao, exemplo, nota=None):
    """Monta o DAX: variáveis (texto DAX com VARs) + HTML. titulo/definicao/exemplo/nota são expressões DAX de texto (já entre aspas ou concatenadas)."""
    corpo = ('"<div role=\'group\' style=\'' + ESTILO + '\'>"\n'
             ' & "<div style=\'font-size:23px;line-height:28px;font-weight:600;\'>" & ' + esc(titulo) + ' & "</div>"\n'
             ' & "<div style=\'margin-top:10px;font-size:19px;line-height:27px;color:#434446;\'>" & ' + esc(definicao) + ' & "</div>"\n'
             ' & "<div style=\'margin-top:16px;padding:12px 16px;background:#FDF7F1;border-left:4px solid #F58220;border-radius:6px;font-size:19px;line-height:28px;\'>'
             '<b>Exemplo</b><br>" & SUBSTITUTE(' + esc(exemplo) + ', "[[br]]", "<br>") & "</div>"\n')
    if nota:
        corpo += ' & "<div style=\'margin-top:14px;font-size:16px;line-height:22px;color:#667085;\'>" & ' + esc(nota) + ' & "</div>"\n'
    return variaveis + "RETURN\n    " + corpo + ' & "</div>"'


def r100(v):
    return f'"R$ " & FORMAT({v} * 100, "0", "pt-BR")'


def medidas():
    m = medidas_info()

    m.append(("Guia_Leitura_RAIS_HTML", "Guia de leitura e glossário compartilhado por todas as páginas do painel RAIS.", guia_leitura_rais(), "HTML\\Notas compartilhadas", None, False))

    def add(nome, doc, dax):
        m.append((nome, doc, dax, P, None, False))

    for nome, a, b, quem, outro, cor_txt in (("Sexo", "mulheres", "homens", "As mulheres", "os homens", "Todos os empregados, sem filtro de cor."),
                                              ("Raca", "negros (pretos e pardos)", "brancos", "Os negros", "os brancos", "Só entram empregados que declararam cor/raça.")):
        v = f"VAR R = [Rem_Razao_{nome}]\nVAR RA = [Rem_Razao_{nome}_AFL]\nVAR RC = [Rem_Razao_{nome}_Comp]\nVAR A = [Ano_Ref]\n"
        add(f"Tip_Razao{nome}_HTML", f"Tooltip do KPI de razão salarial ({a} ÷ {b}).",
            dica(v, f'"Como ler: {a} ÷ {b}"',
                 f'"Divide a remuneração média de dezembro de {a} pela de {b}, com os mesmos filtros da página. 100% significa salários iguais; abaixo de 100%, {quem.lower()} ganham menos."',
                 'IF(ISBLANK(R), "Sem dados para os filtros escolhidos.", "Para cada R$ 100 que ' + outro + ' recebem em média, ' + quem.lower() + ' recebem R$ " & FORMAT(R * 100, "0", "pt-BR") & " (" & FORMAT(R, "0%", "pt-BR") & ")."'
                 ' & IF(ISBLANK(RA) || ISBLANK(RC), "", "[[br]]No AFL: R$ " & FORMAT(RA * 100, "0", "pt-BR") & " · nos Comparáveis: R$ " & FORMAT(RC * 100, "0", "pt-BR") & "."))',
                 f'"Remuneração de dezembro de " & A & ", em R$ nominais. {cor_txt}"'))
    v = ("VAR Med = COALESCE([Remuneracao_Mediana_Ref], [Remuneracao_Mediana_Ref_AFL])\nVAR Media = [Remuneracao_Media_Ref]\nVAR A = [Ano_Ref]\n")
    add("Tip_Mediana_HTML", "Tooltip do KPI de mediana: diferença entre mediana e média.",
        dica(v, '"Mediana × média"',
             '"A mediana é o valor do meio: metade dos empregados ganha menos que ela e metade ganha mais. A média soma todas as remunerações e divide pelo número de empregados; costuma ser maior, porque poucos salários muito altos a puxam para cima."',
             'IF(ISBLANK(Med), "Para esta combinação de filtros a mediana não está disponível; ela existe para setor, UF, sexo e escolaridade.", "Em dezembro de " & A & ", metade ganhava até R$ " & FORMAT(Med, "#,0", "pt-BR") & "; a média foi R$ " & FORMAT(Media, "#,0", "pt-BR") & ".")',
             '"Valores nominais (sem correção pela inflação). Remuneração de dezembro."'))
    v = ("VAR Pos = [Ind_Posicao_AFL]\nVAR N = [Ind_Total_Divisoes]\nVAR Afl = [Ind_Valor_AFL]\nVAR Frase = [Ind_Frase]\nVAR Rot = [Ind_Rotulo]\nVAR A = [Ind_Ano]\n")
    add("Tip_Contrata_Pos_HTML", "Tooltip do KPI de posição do AFL no ranking de divisões.",
        dica(v, '"Posição do AFL no ranking"',
             '"As divisões da CNAE com 50 mil empregos ou mais são ordenadas pela participação de " & Rot & " entre os empregados. A 1ª posição é a divisão em que essa participação é a maior. O AFL entra no ranking como um conjunto de 6 atividades."',
             'IF(ISBLANK(Pos), "Sem dados para os filtros escolhidos.", "Em " & A & ", " & FORMAT(Afl, "0.0%", "pt-BR") & " " & Frase & " no AFL. Ele é o " & Pos & "º entre " & N & " divisões" & IF(Pos > 1, ": " & (Pos - 1) & " divisões têm participação maior.", ": nenhuma divisão tem participação maior."))',
             '"O indicador muda conforme o botão escolhido acima do ranking."'))
    v = ("VAR Afl = [Ind_Valor_AFL]\nVAR Comp = [Ind_Valor_Comp]\nVAR Dif = (Afl - Comp) * 100\nVAR Rot = [Ind_Rotulo]\n")
    add("Tip_Contrata_Dif_HTML", "Tooltip do KPI de diferença em pontos percentuais.",
        dica(v, '"O que é ponto percentual (p.p.)"',
             '"É a diferença entre dois percentuais. Não é uma variação percentual: indo de 39,6% para 55,6%, a diferença é de 16,0 pontos percentuais, e não de 16%."',
             'IF(ISBLANK(Dif), "Sem dados para os filtros escolhidos.", "AFL " & FORMAT(Afl, "0.0%", "pt-BR") & " − Comparáveis " & FORMAT(Comp, "0.0%", "pt-BR") & " = " & IF(Dif > 0, "+", IF(Dif < 0, "−", "")) & FORMAT(ABS(Dif), "0.0", "pt-BR") & " p.p. (" & Rot & ")")',
             '"Comparáveis: setores usados como referência para o AFL."'))
    v = ("VAR Divisao = [Ind_Maior_Divisao]\nVAR Valor = [Ind_Maior_Valor]\nVAR Frase = [Ind_Frase]\nVAR Rot = [Ind_Rotulo]\nVAR A = [Ind_Ano]\n")
    add("Tip_Contrata_Max_Total_HTML", "Tooltip do KPI de maior valor entre as divisões.",
        dica(v, '"Maior valor entre as divisões"',
             '"É a divisão da CNAE com a maior participação de " & Rot & " entre os empregados, considerando só divisões com 50 mil empregos ou mais."',
             'IF(ISBLANK(Valor), "Sem dados para os filtros escolhidos.", "Em " & A & ", em " & Divisao & ", " & FORMAT(Valor, "0.0%", "pt-BR") & " " & Frase & ".")',
             '"Nome oficial da divisão CNAE."'))
    v = ("VAR Lider = [Ind_Atividade_Lider]\nVAR Valor = [Ind_Atividade_Lider_Valor]\nVAR Frase = [Ind_Frase]\nVAR Rot = [Ind_Rotulo]\nVAR A = [Ind_Ano]\n")
    add("Tip_Contrata_Max_AFL_HTML", "Tooltip do KPI de maior valor entre as atividades do AFL.",
        dica(v, '"Maior valor entre as atividades"',
             '"É a atividade (CNAE) do AFL com a maior participação de " & Rot & " entre os seus empregados."',
             'IF(ISBLANK(Valor), "Sem dados para os filtros escolhidos.", "Em " & A & ", " & Lider & ": " & FORMAT(Valor, "0.0%", "pt-BR") & " " & Frase & ".")',
             '"O AFL reúne seis atividades: restaurantes, lanchonetes, bares com e sem entretenimento, padarias (revenda) e alimentos preparados para consumo domiciliar."'))
    return m


def guia_leitura_rais():
    """Texto fixo do guia superior; não depende dos filtros da página."""
    return (
        "VAR _A = 0\nRETURN\n"
        "    \"<div role='note' aria-label='Guia de leitura e glossário do painel RAIS' style='width:1040px;height:900px;box-sizing:border-box;padding:22px 26px;background:#FFFFFF;border:1px solid #D9DDE5;border-top:6px solid #F58220;border-radius:8px;color:#434446;font-family:Segoe UI,Arial,sans-serif;font-size:17px;line-height:23px;overflow:hidden;'>\"\n"
        "    & \"<div style='font-size:25px;line-height:31px;font-weight:700;color:#1D1E21;'>INFORMAÇÕES PARA LEITURA</div>\"\n"
        "    & \"<div style='font-size:18px;line-height:25px;color:#667085;margin-top:3px;margin-bottom:16px;'>Um guia rápido para explorar o painel de emprego formal e interpretar os indicadores da RAIS.</div>\"\n"
        "    & \"<div style='display:flex;gap:14px;margin-bottom:19px;'><div style='flex:1;min-width:0;padding:13px 16px;background:#FDF7F1;border-radius:6px;'><strong style='display:block;color:#B86218;margin-bottom:5px;'>Passe o mouse para descobrir mais</strong>Gráficos, números, manchetes e ícones ⓘ têm explicações adicionais. Mantenha o cursor sobre a informação; não é preciso clicar.</div><div style='flex:1;min-width:0;padding:13px 16px;background:#FDF7F1;border-radius:6px;'><strong style='display:block;color:#B86218;margin-bottom:5px;'>Explore os recortes</strong>Use os filtros, clique nas barras e consulte as abas para alternar tema e universo. Limpar filtros volta à leitura inicial da página.</div></div>\"\n"
        "    & \"<div style='font-size:15px;line-height:21px;font-weight:700;letter-spacing:1px;color:#B86218;margin-bottom:12px;'>GLOSSÁRIO · MEDIDAS E CONCEITOS</div>\"\n"
        "    & \"<div style='display:flex;gap:28px;'><div style='flex:1;min-width:0;'><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>RAIS / estoque de empregos</strong> — Retrato dos vínculos formais ativos em 31 de dezembro. Conta vínculos, não pessoas: quem tem dois empregos aparece duas vezes.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Ano de referência e defasagem</strong> — A RAIS é anual e divulgada com defasagem. O filtro Ano define o retrato de 31/12 usado nos indicadores.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Quebra da série em 2022</strong> — Desde 2022, a fonte é o eSocial, que ampliou a cobertura. Por isso, 2022 em diante não deve ser comparado diretamente com anos anteriores; as séries são interrompidas.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>AFL</strong> — Alimentação Fora do Lar: conjunto de seis CNAEs definidos no painel. Nos rankings, aparece como grupo próprio.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Comparáveis ao AFL</strong> — Atividades usadas como referência para comparar o AFL. A comparação-padrão é AFL × Comparáveis.</div></div>\"\n"
        "    & \"<div style='flex:1;min-width:0;'><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Todos os setores / AFL</strong> — A primeira visão mostra o contexto de mercado e a seleção dos filtros; a aba AFL restringe o painel às seis atividades de alimentação fora do lar.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Remuneração</strong> — Salário de dezembro, em R$ nominais (sem correção pela inflação). A média considera salários válidos de 0,3 a 150 salários mínimos; a mediana só existe para alguns recortes.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Percentuais e p.p.</strong> — Todo percentual informa uma parcela do universo mostrado. Pontos percentuais (p.p.) são diferença entre percentuais: de 30% para 35% = 5 p.p.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>Cor ou raça</strong> — Os percentuais consideram somente quem declarou a informação. Pretos e pardos formam o grupo de negros.</div><div style='margin-bottom:10px;'><strong style='color:#1D1E21;'>CNAE / divisão</strong> — CNAE é a classificação da atividade econômica; divisão é um agrupamento de CNAEs. Os nomes dos rankings seguem essa classificação.</div></div></div>\"\n"
        "    & \"<div style='margin-top:4px;padding-top:11px;border-top:1px solid #E6E8ED;font-size:16px;line-height:22px;color:#667085;'><strong>Antes de comparar:</strong> confira ano, localidade, filtros e a nota metodológica da página. Ela indica quando há quebra de série, universo restrito ou dado indisponível.</div></div>\""
    )


def medidas_info():
    m = []
    m.append(("Info_Texto_HTML", "Cartão do (i): lê a linha da D_Info escolhida pela categoria do gatilho.",
              "VAR Chave = SELECTEDVALUE(D_Info[Chave])\nVAR Titulo = SELECTEDVALUE(D_Info[Titulo], \"\")\nVAR Extra = SELECTEDVALUE(D_Info[Extra], \"\")\n"
              "VAR Destaque = SELECTEDVALUE(D_Info[Destaque], \"\")\nVAR Borda = SELECTEDVALUE(D_Info[CorBorda], \"#1D1E21\")\nVAR Fundo = SELECTEDVALUE(D_Info[CorFundo], \"#F7F7F7\")\n"
              "VAR P1 = SELECTEDVALUE(D_Info[P1], \"\")\nVAR P2 = SELECTEDVALUE(D_Info[P2], \"\")\nVAR P3 = SELECTEDVALUE(D_Info[P3], \"\")\nVAR P4 = SELECTEDVALUE(D_Info[P4], \"\")\nVAR P5 = SELECTEDVALUE(D_Info[P5], \"\")\n"
              "VAR Corpo = IF(P1 = \"\", \"\", \"<div>\" & P1 & \"</div>\") & IF(P2 = \"\", \"\", \"<div style='margin-top:8px;'>\" & P2 & \"</div>\") & IF(P3 = \"\", \"\", \"<div style='margin-top:8px;'>\" & P3 & \"</div>\")"
              " & IF(P4 = \"\", \"\", \"<div style='margin-top:8px;'>\" & P4 & \"</div>\") & IF(P5 = \"\", \"\", \"<div style='margin-top:8px;'>\" & P5 & \"</div>\")\n"
              "RETURN IF(ISBLANK(Chave) || Titulo = \"\", \"<div role='note' style='font-family:Segoe UI,Arial,sans-serif;font-size:21px;color:#434446;padding:12px;'>Texto indisponível.</div>\",\n"
              "    \"<div role='note' style='width:100%;height:100%;box-sizing:border-box;margin:0;padding:12px 14px;background:#FFFFFF;color:#1D1E21;font-family:Segoe UI,Arial,sans-serif;overflow:hidden;'>\"\n"
              "    & \"<div style='font-size:24px;line-height:30px;font-weight:600;margin-bottom:8px;'>\" & Titulo & \"</div>\" & Extra\n"
              "    & IF(Destaque = \"\", \"\", \"<div style='padding:7px 9px;border-left:4px solid \" & Borda & \";border-radius:0 6px 6px 0;background:\" & Fundo & \";font-size:21px;line-height:27px;margin-bottom:8px;'>\" & Destaque & \"</div>\")\n"
              "    & \"<div style='font-size:21px;line-height:28px;color:#434446;'>\" & Corpo & \"</div></div>\")", "HTML\\Notas compartilhadas", None, False))
    # título do gráfico de variação anual do emprego (substitui o índice base 100)
    base = ("VAR A = [Ano_Ref]\nVAR VA = [Empregos_Var_Pct_AFL]\nVAR VC = [Empregos_Var_Pct_Comparavel]\nVAR VS = [Empregos_Var_Pct]\n"
            "VAR Nome = IF([Setor_Emp_Total] = \"todos os setores\", \"o mercado formal\", [Setor_Emp_Total])\n")
    sem = "IF(A = 2022, \"2022 não pode ser comparado com 2021 (nova fonte: eSocial)\", \"2009 é o primeiro ano da série: não há ano anterior\")"
    l2 = ("VAR L2 = IF(ISBLANK(A), \"\", \"Variação do emprego em 31/12 sobre 31/12 do ano anterior. Escolha o ano no filtro Ano; 2022 não tem comparação (nova fonte: eSocial)\")\n")
    m.append(("Titulo_Emp_Var_AFL_HTML", "Título da variação anual do emprego (página AFL).",
              base + "VAR L1 = IF(ISBLANK(A), \"Sem dados para os filtros escolhidos\", IF(ISBLANK(VA), " + sem + ", \"Em \" & A & \", o emprego do AFL \" & IF(VA >= 0, \"subiu \", \"caiu \") & "
              + pct("ABS(VA)") + " & IF(ISBLANK(VC), \"\", \" (Comparáveis: \" & " + pct("VC", True) + " & \")\")))\n" + l2 + titulo_html("L1", "L2", '"#F58220"'), "HTML\\Empregos\\Títulos", None, False))
    m.append(("Titulo_Emp_Var_Total_HTML", "Título da variação anual do emprego (página Todos os setores).",
              base + "VAR L1 = IF(ISBLANK(A), \"Sem dados para os filtros escolhidos\", IF(ISBLANK(VA), " + sem + ", \"Em \" & A & \": AFL \" & " + pct("VA", True)
              + " & \", \" & Nome & \" \" & " + pct("VS", True) + "))\n" + l2 + titulo_html("L1", "L2", '"#F58220"'), "HTML\\Empregos\\Títulos", None, False))
    return m
