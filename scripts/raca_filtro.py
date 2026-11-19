# -*- coding: utf-8 -*-
"""Filtro de raça com opções separadas: Negros (pretos + pardos), Preta, Parda, Branca, Amarela, Indígena, Não declarada.

- Tabela local D_RacaFiltro (opcao, raca_cor, ordem); "Negros" tem duas linhas (Preta e Parda).
- Relação muitos-para-muitos D_Raca[raca_cor] <- D_RacaFiltro[raca_cor] (a tabela nova filtra a D_Raca).
- Os 8 slicers de raça passam a usar D_RacaFiltro[opcao] (desfaz os dois níveis de raca_negros.py).
- REMOVEFILTERS(D_Raca) passa a limpar também D_RacaFiltro.
- Contexto_Emp_*: mostra a opção escolhida.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DEF = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition"
PAGES = RAIZ / "RAIS Emprego Formal.Report" / "definition" / "pages"
NEG = "Negros (pretos + pardos)"
LINHAS = [(NEG, "Preta", 1), (NEG, "Parda", 1), ("Preta", "Preta", 2), ("Parda", "Parda", 3), ("Branca", "Branca", 4),
          ("Amarela", "Amarela", 5), ("Indígena", "Indígena", 6), ("Não declarada", "Não Identificado", 7), ("Não declarada", "Campo Não Preenchido", 7)]

# ---- tabela
rows = ", ".join('{"%s", "%s", %d}' % r for r in LINHAS)
(DEF / "tables" / "D_RacaFiltro.tmdl").write_text(f"""/// Opções do filtro de raça. "{NEG}" filtra Preta e Parda juntas; as demais filtram a própria raça.
table D_RacaFiltro
	lineageTag: 3b9f6c2e-7a41-4d8e-b0c5-91e2f4a6d701

	column opcao
		dataType: string
		lineageTag: 3b9f6c2e-7a41-4d8e-b0c5-91e2f4a6d702
		summarizeBy: none
		sourceColumn: opcao
		sortByColumn: ordem

		annotation SummarizationSetBy = Automatic

	column raca_cor
		dataType: string
		isHidden
		lineageTag: 3b9f6c2e-7a41-4d8e-b0c5-91e2f4a6d703
		summarizeBy: none
		sourceColumn: raca_cor

		annotation SummarizationSetBy = Automatic

	column ordem
		dataType: int64
		isHidden
		formatString: 0
		lineageTag: 3b9f6c2e-7a41-4d8e-b0c5-91e2f4a6d704
		summarizeBy: none
		sourceColumn: ordem

		annotation SummarizationSetBy = Automatic

	partition D_RacaFiltro = m
		mode: import
		source =
				let
				    Fonte = #table(type table [opcao = text, raca_cor = text, ordem = Int64.Type], {{{rows}}})
				in
				    Fonte

	annotation PBI_ResultType = Table

""", encoding="utf-8", newline="\n")

model = DEF / "model.tmdl"
m = model.read_text(encoding="utf-8")
if "ref table D_RacaFiltro" not in m:
    m = m.replace("ref table D_regiao", "ref table D_regiao\nref table D_RacaFiltro")
    m = m.replace('"D_Ano"]', '"D_Ano","D_RacaFiltro"]')
    model.write_text(m, encoding="utf-8", newline="")

rel = DEF / "relationships.tmdl"
r = rel.read_text(encoding="utf-8")
if "D_RacaFiltro" not in r:
    r = r.rstrip("\n") + ("\n\nrelationship 3b9f6c2e-7a41-4d8e-b0c5-91e2f4a6d710\n\ttoCardinality: many\n"
                          "\tfromColumn: D_Raca.raca_cor\n\ttoColumn: D_RacaFiltro.raca_cor\n\n")
    rel.write_text(r, encoding="utf-8", newline="")

# ---- medidas
med = DEF / "tables" / "_medidas.tmdl"
t = med.read_text(encoding="utf-8")
n_rf = t.count("REMOVEFILTERS(D_Raca)")
t = t.replace("REMOVEFILTERS(D_Raca), REMOVEFILTERS(D_RacaFiltro)", "REMOVEFILTERS(D_Raca)")
t = t.replace("REMOVEFILTERS(D_Raca)", "REMOVEFILTERS(D_Raca), REMOVEFILTERS(D_RacaFiltro)")
novo = ('VAR Raca = IF(ISFILTERED(D_RacaFiltro[opcao]), CONCATENATEX(VALUES(D_RacaFiltro[opcao]), D_RacaFiltro[opcao], ", "), '
        'IF(ISFILTERED(D_Raca[raca_cor]), CONCATENATEX(VALUES(D_Raca[raca_cor]), D_Raca[raca_cor], ", "), ""))')
t, n_ctx = re.subn(r"VAR Raca = IF\(ISFILTERED\(D_Raca\[raca_cor\]\)[^\n]*", lambda _: novo, t)
med.write_text(t, encoding="utf-8", newline="")
print("REMOVEFILTERS:", n_rf, "| contexto:", n_ctx)

for g in RAIZ.glob("scripts/dax_*.py"):
    s = g.read_text(encoding="utf-8")
    if "REMOVEFILTERS(D_Raca)" in s and "D_RacaFiltro" not in s:
        g.write_text(s.replace("REMOVEFILTERS(D_Raca)", "REMOVEFILTERS(D_Raca), REMOVEFILTERS(D_RacaFiltro)"), encoding="utf-8", newline="")
        print("gerador:", g.name)

# ---- slicers
CAMPO = {"Column": {"Expression": {"SourceRef": {"Entity": "D_RacaFiltro"}}, "Property": "opcao"}}
n = 0
for vf in PAGES.glob("*/visuals/*/visual.json"):
    j = json.loads(vf.read_text(encoding="utf-8"))
    v = j.get("visual", {})
    q = v.get("query", {})
    proj = q.get("queryState", {}).get("Values", {}).get("projections", [])
    if v.get("visualType") != "slicer" or not any(p.get("queryRef", "").startswith("D_Raca.") for p in proj):
        continue
    q["queryState"]["Values"]["projections"] = [{"field": json.loads(json.dumps(CAMPO)), "queryRef": "D_RacaFiltro.opcao",
                                                 "nativeQueryRef": "opcao", "active": True}]
    q["sortDefinition"] = {"sort": [{"field": json.loads(json.dumps(CAMPO)), "direction": "Ascending"}], "isDefaultSort": True}
    vf.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    n += 1
print("slicers:", n)
