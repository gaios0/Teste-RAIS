"""Tooltips explicativos (HTML) dos KPIs: o que o número significa, com um exemplo calculado com os valores da página.

Cada medida alimenta uma página de tooltip (600 × 450) criada por pagina_rais.py; o contexto de filtros vem do visual sobre o qual o mouse passa.
Retorna tuplas (nome, doc, dax, pasta, formato, oculta) como as demais; sempre começam com VAR (medida sem VAR não pode começar com RETURN).
"""
from dax_rais import esc, num, pct

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
    m = []

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
