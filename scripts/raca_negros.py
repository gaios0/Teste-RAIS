# -*- coding: utf-8 -*-
"""Filtro de raça em dois níveis (grupo_raca > raca_cor) e definição de negros nas dicas (i).

- 8 slicers de D_Raca: entra D_Raca[grupo_raca] acima de D_Raca[raca_cor] (Negra > Preta, Parda).
- Contexto_Emp_*: com o grupo Negra inteiro selecionado, o texto mostra "negros (pretos + pardos)".
- D_Info e info_rais.py: "Negros = pretos + pardos." nas dicas que falam de negros.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SM = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables"
PAGES = RAIZ / "RAIS Emprego Formal.Report" / "definition" / "pages"
DEF = "Negros = pretos + pardos."

# ---- slicers
GRUPO = {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "D_Raca"}}, "Property": "grupo_raca"}},
         "queryRef": "D_Raca.grupo_raca", "nativeQueryRef": "grupo_raca", "active": True}
n_sl = 0
for vf in PAGES.glob("*/visuals/*/visual.json"):
    txt = vf.read_text(encoding="utf-8")
    j = json.loads(txt)
    v = j.get("visual", {})
    if v.get("visualType") != "slicer":
        continue
    proj = v.get("query", {}).get("queryState", {}).get("Values", {}).get("projections", [])
    refs = [p.get("queryRef") for p in proj]
    if "D_Raca.raca_cor" not in refs or "D_Raca.grupo_raca" in refs:
        continue
    proj.insert(0, json.loads(json.dumps(GRUPO)))
    for p in proj:
        p.pop("active", None)
    vf.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    n_sl += 1
print("slicers:", n_sl)

# ---- texto de contexto
med = SM / "_medidas.tmdl"
t = med.read_text(encoding="utf-8")
ant = 'VAR Raca = IF(ISFILTERED(D_Raca[raca_cor]), CONCATENATEX(VALUES(D_Raca[raca_cor]), D_Raca[raca_cor], ", "), "")'
novo = ('VAR Raca = IF(ISFILTERED(D_Raca[raca_cor]) || ISFILTERED(D_Raca[grupo_raca]), '
        'IF(SELECTEDVALUE(D_Raca[grupo_raca]) = "Negra" && COUNTROWS(VALUES(D_Raca[raca_cor])) = CALCULATE(DISTINCTCOUNT(D_Raca[raca_cor]), REMOVEFILTERS(D_Raca), D_Raca[grupo_raca] = "Negra"), '
        '"negros (pretos + pardos)", CONCATENATEX(VALUES(D_Raca[raca_cor]), D_Raca[raca_cor], ", ")), "")')
print("contexto:", t.count(ant))
med.write_text(t.replace(ant, novo), encoding="utf-8", newline="")

# ---- dicas (i)
P2_GAP = "100% = salários iguais. Comparar dentro da mesma escolaridade tira o efeito de diferenças de instrução."
P2_RANK = "Mostra as 10 maiores divisões e sempre o AFL, em laranja. Use o modo foco para ver mais."
info = SM / "D_Info.tmdl"
t = info.read_text(encoding="utf-8")
c = 0
for p in (P2_GAP, P2_RANK):
    t, k = re.subn(re.escape(f'"{p}", ""'), f'"{p}", "{DEF}"', t)
    c += k
t = t.replace("Negros = pretos e pardos.", DEF)
info.write_text(t, encoding="utf-8", newline="")
print("dicas:", c)

gen = RAIZ / "scripts" / "info_rais.py"
g = gen.read_text(encoding="utf-8")
for p in (P2_GAP, P2_RANK):
    if f'"{p}", "{DEF}"' not in g:
        g = g.replace(f'"{p}"]', f'"{p}", "{DEF}"]')
g = g.replace("Negros = pretos e pardos.", DEF)
gen.write_text(g, encoding="utf-8", newline="")
