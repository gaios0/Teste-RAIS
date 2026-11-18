"""Mostra onde Raca_HTML / Titulo_Raca_HTML filtram trabalho_intermitente e se algum visual ainda os usa."""
import json
import re

import pbir_rais as pb

t = (pb.RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl").read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n")
atual = None
for l in t:
    m = re.match(r"^\tmeasure (\w+)", l)
    if m:
        atual = m.group(1)
    if atual in ("Raca_HTML", "Titulo_Raca_HTML") and "trabalho_intermitente" in l:
        for mm in re.finditer(r".{0,160}F_rais\[trabalho_intermitente\].{0,120}", l):
            print(atual, "::", mm.group(0))
for suf in ("c21", "c22"):
    for f in (pb.DEF / "pages" / ("a3d1f2c4e6b8097a1" + suf) / "visuals").glob("*/visual.json"):
        s = f.read_text(encoding="utf-8")
        for nome in ("Raca_HTML", "Titulo_Raca_HTML", "Raca_RF_HTML"):
            if '"' + nome + '"' in s:
                print("visual", suf, f.parent.name[:6], nome)
