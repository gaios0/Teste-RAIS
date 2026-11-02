"""Testa as medidas das páginas contra o modelo aberto (consultas simples; as medidas já estão no modelo carregado).

Uso: python scripts/testar_paginas.py emp
"""
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
    return "DEFINE\n" + "\n".join(blocos) + "\n"


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


def main():
    saida = rodar(emp() if "emp" in sys.argv[1:] or not sys.argv[1:] else [])
    for bloco in saida.split("--- ")[1:]:
        cab = bloco.split("\n")[0]
        corpo = bloco[len(cab):].strip()
        erro = "ERRO" in corpo[:200]
        print(("!! " if erro else "## ") + cab)
        print("   " + (corpo[:700] if erro else texto(corpo)[:900]))


if __name__ == "__main__":
    main()
