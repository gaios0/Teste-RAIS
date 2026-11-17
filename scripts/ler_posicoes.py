"""Lista as posições salvas das páginas Quem contrata (para ver o que foi movido à mão no Desktop)."""
import json
import sys
from pathlib import Path

import pbir_rais as pb

PAPEIS = ["manchete", "modo", "setor", "kpi0", "kpi1", "kpi2", "met_Mul", "met_Neg", "met_Esc", "nivel", "t_Mul", "t_Neg", "t_Esc", "ch_Mul", "ch_Neg", "ch_Esc"]
for pid in sys.argv[1:]:
    pasta = pb.DEF / "pages" / pid / "visuals"
    nomes = {pb.nome_visual(pid, "ct2_" + p): p for p in PAPEIS}
    linhas = []
    for d in pasta.iterdir():
        v = json.loads((d / "visual.json").read_text(encoding="utf-8"))
        pos = v["position"]
        papel = nomes.get(d.name, "")
        proj = [p["queryRef"] for p in v["visual"].get("query", {}).get("queryState", {}).get("Values", {}).get("projections", [])] or \
               [p["queryRef"] for p in v["visual"].get("query", {}).get("queryState", {}).get("Y", {}).get("projections", [])]
        linhas.append((pos["y"], pos["x"], papel or "-", v["visual"]["visualType"], pos["x"], pos["y"], pos["width"], pos["height"], pos["z"], (proj or [""])[0], d.name[:6]))
    print("=====", pid)
    for l in sorted(linhas):
        print("{:<9} {:<22} x={:>8.1f} y={:>8.1f} w={:>8.1f} h={:>8.1f} z={:>6}  {}  {}".format(l[2], l[3], l[4], l[5], l[6], l[7], l[8], l[9], l[10]))
