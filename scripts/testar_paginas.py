"""Testa as medidas das páginas contra o modelo aberto (consultas simples; as medidas já estão no modelo carregado).

Uso: python scripts/testar_paginas.py emp
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PS1 = Path(tempfile.gettempdir()) / "dax_decada.ps1"


def definicoes():
    """Todas as medidas do projeto como DEFINE MEASURE (sobrescrevem as do modelo carregado)."""
    import modelo_base as mb
    blocos = [f"MEASURE _medidas[{nome}] =\n{dax}" for nome, _, dax, _, _, _ in mb.medidas()]
    tabela = ""
    if os.environ.get("RAIS_SEM_D_INDICADOR") == "1":        # antes de reabrir o PBIP, a tabela local ainda não existe no modelo carregado
        linhas = ", ".join(f'{{"{n}", "{i + 1}"}}' for i, n in enumerate(mb.INDICADORES))
        tabela = f'TABLE D_Indicador = DATATABLE("indicador", STRING, "ordem", STRING, {{{linhas}}})\n'
    return "DEFINE\n" + tabela + "\n".join(blocos) + "\n"


def rodar(consultas):
    d = definicoes()
    consultas = [c.split("\n", 1)[0] + "\n" + d + c.split("\n", 1)[1] for c in consultas]
    arq = Path(tempfile.gettempdir()) / "consultas_rais.dax"
    arq.write_text("\n###\n".join(consultas), encoding="utf-8", newline="\n")
    r = subprocess.run(["powershell", "-NoProfile", "-File", str(PS1), "-File", str(arq)], capture_output=True, text=True, encoding="utf-8")
    return r.stdout.replace("\r", "")


def texto(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " | ", html)).strip()


def emp():
    A = "D_Calendario[Ano] = 2025"
    q = []
    for u in ("Total", "AFL"):
        extra = ', D_Cnae[setor_afl] = "Sim"' if u == "AFL" else ""
        for n in (f"Manchete_Emp_{u}_HTML", f"KPI_Emp_{u}_HTML", f"KPI_Peso_{u}_HTML", f"KPI_Cresc_{u}_HTML", f"Contexto_Emp_{u}"):
            q.append(f"-- {u} {n}\nEVALUATE ROW(\"t\", CALCULATE([{n}], {A}{extra}))")
    q.append(f"-- Titulo serie\nEVALUATE ROW(\"t\", CALCULATE([Titulo_Emp_Serie_HTML], {A}))")
    q.append(f"-- Titulo contrato\nEVALUATE ROW(\"t\", CALCULATE([Titulo_Emp_Contrato_HTML], {A}))")
    q.append(f"-- Contratos\nEVALUATE ROW(\"t\", CALCULATE([Emp_Contratos_HTML], {A}))")
    q.append(f"-- Titulo ranking\nEVALUATE ROW(\"t\", CALCULATE([Titulo_Emp_Ranking_HTML], {A}))")
    q.append(f"-- Titulo atividades\nEVALUATE ROW(\"t\", CALCULATE([Titulo_Emp_Atividades_HTML], {A}, D_Cnae[setor_afl] = \"Sim\"))")
    q.append(f"-- Titulo UF AFL\nEVALUATE ROW(\"t\", CALCULATE([Titulo_Emp_UF_AFL_HTML], {A}, D_Cnae[setor_afl] = \"Sim\"))")
    q.append(f"-- Titulo UF Total\nEVALUATE ROW(\"t\", CALCULATE([Titulo_Emp_UF_Total_HTML], {A}))")
    q.append("-- serie indices\nEVALUATE SUMMARIZECOLUMNS(D_Calendario[Ano], \"afl_pre\", [Emp_Indice_AFL_Pre], \"afl_pos\", [Emp_Indice_AFL_Pos], \"comp_pre\", [Emp_Indice_Comp_Pre], \"comp_pos\", [Emp_Indice_Comp_Pos]) ORDER BY D_Calendario[Ano]")
    q.append("-- ranking divisoes\nEVALUATE TOPN(12, SUMMARIZECOLUMNS(D_Rank_Divisao[nm_divisao], D_Calendario[Ano], KEEPFILTERS(TREATAS({2025}, D_Calendario[Ano])), \"v\", [Emp_Divisao_Top]), [v], DESC)")
    q.append("-- ranking filtro comparavel\nEVALUATE TOPN(4, SUMMARIZECOLUMNS(D_Rank_Divisao[nm_divisao], KEEPFILTERS(TREATAS({2025}, D_Calendario[Ano])), KEEPFILTERS(TREATAS({\"Sim\"}, D_Comparavel[comparavel_AFL])), \"v\", [Emp_Divisao_Top]), [v], DESC)")
    q.append("-- atividades\nEVALUATE SUMMARIZECOLUMNS(D_AflAtividade[nome], KEEPFILTERS(TREATAS({2025}, D_Calendario[Ano])), \"v\", [Empregos_Ref], \"var\", [Emp_Atividade_Var])")
    q.append("-- uf\nEVALUATE TOPN(5, SUMMARIZECOLUMNS(D_UF[uf], KEEPFILTERS(TREATAS({2025}, D_Calendario[Ano])), KEEPFILTERS(TREATAS({\"Sim\"}, D_Cnae[setor_afl])), \"v\", [Emp_UF_Top], \"peso\", [Emp_UF_Peso_Top]), [v], DESC)")
    return q


def perfil():
    A = "D_Calendario[Ano] = 2025"
    q = []
    for u in ("Total", "AFL"):
        extra = ', D_Cnae[setor_afl] = "Sim"' if u == "AFL" else ""
        for n in (f"Manchete_Perfil_{u}_HTML", f"KPI_Mulheres_{u}_HTML", f"KPI_Jovens_{u}_HTML", f"KPI_Escol_{u}_HTML"):
            q.append(f"-- {u} {n}\nEVALUATE ROW(\"t\", CALCULATE([{n}], {A}{extra}))")
    for n in ("Titulo_Pir_HTML", "Esc_Barras_HTML", "Titulo_Esc_HTML", "Titulo_CBO_HTML", "Raca_HTML", "Titulo_Raca_HTML"):
        q.append(f"-- {n}\nEVALUATE ROW(\"t\", CALCULATE([{n}], {A}, D_Cnae[setor_afl] = \"Sim\"))")
    q.append('-- piramide\nEVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_FaixaIdade[faixa_idade], "m", [Pir_Mulheres], "h", [Pir_Homens], "mc", [Pir_Mulheres_Comp], "hc", [Pir_Homens_Comp]), D_Calendario[Ano] = 2025, D_Cnae[setor_afl] = "Sim")')
    q.append('-- cbo\nEVALUATE TOPN(10, CALCULATETABLE(SUMMARIZECOLUMNS(F_rais[cbo_2002], "v", [Emp_CBO_Top], "m", [Perf_Mulheres], "r", [Remuneracao_Media_Ref]), D_Calendario[Ano] = 2025, D_Cnae[setor_afl] = "Sim"), [v], DESC)')
    return q


def salario():
    A = "D_Calendario[Ano] = 2025"
    q = []
    for u in ("Total", "AFL"):
        extra = ', D_Cnae[setor_afl] = "Sim"' if u == "AFL" else ""
        for n in (f"Manchete_Salario_{u}_HTML", f"KPI_Mediana_{u}_HTML", f"KPI_RazaoSexo_{u}_HTML", f"KPI_RazaoRaca_{u}_HTML"):
            q.append(f"-- {u} {n}\nEVALUATE ROW(\"t\", CALCULATE([{n}], {A}{extra}))")
    for n in ("Titulo_Rem_Serie_HTML", "Titulo_Rem_Esc_HTML", "Titulo_Rem_Gap_HTML", "Titulo_Rem_UF_HTML", "Rotulo_Gap_Sexo_HTML"):
        q.append(f"-- {n}\nEVALUATE ROW(\"t\", CALCULATE([{n}], {A}))")
    q.append('-- serie\nEVALUATE SUMMARIZECOLUMNS(D_Calendario[Ano], "ma_pre", [Rem_Media_AFL_Pre], "ma_pos", [Rem_Media_AFL_Pos], "md_pre", [Rem_Mediana_AFL_Pre], "md_pos", [Rem_Mediana_AFL_Pos], "mc_pos", [Rem_Media_Comp_Pos], "mdc_pos", [Rem_Mediana_Comp_Pos]) ORDER BY D_Calendario[Ano]')
    q.append('-- esc\nEVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_Escolaridade[escolaridade_agrupada], "afl", [Rem_Esc_AFL], "comp", [Rem_Esc_Comp], "rs_afl", [Rem_Razao_Sexo_AFL], "rs_comp", [Rem_Razao_Sexo_Comp], "rr_afl", [Rem_Razao_Raca_AFL], "rr_comp", [Rem_Razao_Raca_Comp]), D_Calendario[Ano] = 2025)')
    q.append('-- uf\nEVALUATE TOPN(5, CALCULATETABLE(SUMMARIZECOLUMNS(D_UF[uf], "v", [Rem_UF_Top], "r", [Rem_UF_Razao_Comp]), D_Calendario[Ano] = 2025, D_Cnae[setor_afl] = "Sim"), [v], DESC)')
    return q


def contrata():
    A = "D_Calendario[Ano] = 2025"
    q = []
    for u in ("Total", "AFL"):
        extra = ', D_Cnae[setor_afl] = "Sim"' if u == "AFL" else ""
        for n in (f"Manchete_Contrata_{u}_HTML", f"KPI_Contrata1_{u}_HTML", f"KPI_Contrata2_{u}_HTML", f"KPI_Contrata3_{u}_HTML"):
            q.append(f"-- {u} {n}\nEVALUATE ROW(\"t\", CALCULATE([{n}], {A}{extra}))")
    for n in ("Titulo_Contrata_Rank_Total_HTML", "Titulo_Contrata_Rank_AFL_HTML", "Titulo_Contrata_Serie_HTML", "Titulo_Contrata_UF_HTML", "Contrata_Tabela_HTML"):
        q.append(f"-- {n}\nEVALUATE ROW(\"t\", CALCULATE([{n}], {A}, D_Cnae[setor_afl] = \"Sim\"))")
    q.append('-- ranking divisoes (mulheres)\nEVALUATE TOPN(12, SUMMARIZECOLUMNS(D_Rank_Divisao[nm_divisao], KEEPFILTERS(TREATAS({2025}, D_Calendario[Ano])), "v", [Ind_Divisao_Top]), [v], DESC)')
    q.append('-- ranking divisoes (primeiro emprego)\nEVALUATE TOPN(6, SUMMARIZECOLUMNS(D_Rank_Divisao[nm_divisao], KEEPFILTERS(TREATAS({2021}, D_Calendario[Ano])), KEEPFILTERS(TREATAS({"Primeiro emprego"}, D_Indicador[indicador])), "v", [Ind_Divisao_Top]), [v], DESC)')
    q.append('-- atividades (jovens)\nEVALUATE SUMMARIZECOLUMNS(D_AflAtividade[nome], KEEPFILTERS(TREATAS({2025}, D_Calendario[Ano])), KEEPFILTERS(TREATAS({"Até 24 anos"}, D_Indicador[indicador])), "v", [Ind_Valor_Ctx])')
    q.append('-- uf (mulheres)\nEVALUATE TOPN(5, SUMMARIZECOLUMNS(D_UF[uf], KEEPFILTERS(TREATAS({2025}, D_Calendario[Ano])), "v", [Ind_UF_Top]), [v], DESC)')
    q.append('-- serie (mulheres)\nEVALUATE SUMMARIZECOLUMNS(D_Calendario[Ano], "a_pre", [Ind_Serie_AFL_Pre], "a_pos", [Ind_Serie_AFL_Pos], "c_pre", [Ind_Serie_Comp_Pre], "c_pos", [Ind_Serie_Comp_Pos]) ORDER BY D_Calendario[Ano]')
    return q


def ajustes():
    A = "D_Calendario[Ano] = 2025"
    q = []
    for n in ("Tip_RazaoSexo_HTML", "Tip_RazaoRaca_HTML", "Tip_Mediana_HTML", "Tip_Contrata_Pos_HTML", "Tip_Contrata_Dif_HTML", "Tip_Contrata_Max_Total_HTML", "Contrata_Tabela_Total_HTML",
              "Manchete_Perfil_Total_HTML", "Titulo_Rem_Gap_HTML", "Titulo_Rem_Esc_HTML", "Titulo_Contrata_UF_Total_HTML", "KPI_Contrata2_Total_HTML", "KPI_Contrata1_Total_HTML",
              "Titulo_Contrata_Serie_HTML", "Titulo_Contrata_Rank_Total_HTML", "Manchete_Contrata_Total_HTML"):
        q.append(f"-- {n}\nEVALUATE ROW(\"t\", CALCULATE([{n}], {A}))")
    for n in ("Tip_Contrata_Max_AFL_HTML", "Manchete_Perfil_AFL_HTML"):
        q.append(f"-- {n}\nEVALUATE ROW(\"t\", CALCULATE([{n}], {A}, D_Cnae[setor_afl] = \"Sim\"))")
    q.append('-- uf todos\nEVALUATE TOPN(5, CALCULATETABLE(SUMMARIZECOLUMNS(D_UF[uf], "v", [Ind_UF_Todos_Top], "a", [Ind_UF_AFL_Dica]), D_Calendario[Ano] = 2025), [v], DESC)')
    q.append('-- serie sel\nEVALUATE TOPN(3, SUMMARIZECOLUMNS(D_Calendario[Ano], "p", [Ind_Serie_Sel_Pre], "q", [Ind_Serie_Sel_Pos], "m", [Rem_Media_Sel_Pos]), D_Calendario[Ano], DESC)')
    q.append('-- esc sel\nEVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_Escolaridade[escolaridade_agrupada], "s", [Rem_Esc_Sel]), D_Calendario[Ano] = 2025)')
    return q


def main():
    alvo = sys.argv[1:] or ["emp"]
    consultas = {"ajustes": ajustes, "emp": emp, "perfil": perfil, "salario": salario, "contrata": contrata}
    saida = rodar([c for a in alvo for c in consultas[a]()])
    for bloco in saida.split("--- ")[1:]:
        cab = bloco.split("\n")[0]
        corpo = bloco[len(cab):].strip()
        erro = "ERRO" in corpo[:200]
        print(("!! " if erro else "## ") + cab)
        print("   " + (corpo[:160].replace("\n", " ") if erro else texto(corpo)[:900]))


if __name__ == "__main__":
    main()
