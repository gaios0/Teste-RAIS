"""Cores usadas nos gráficos de cada página (literais, tema e medidas de cor), para achar onde está o laranja do AFL."""
import json
import re

import pbir_rais as pb

TIPOS = ("lineChart", "clusteredBarChart", "barChart", "clusteredColumnChart", "columnChart", "areaChart")
for f in sorted((pb.DEF / "pages").glob("*/visuals/*/visual.json")):
    t = f.read_text(encoding="utf-8")
    v = json.loads(t)
    tipo = v["visual"]["visualType"]
    if tipo not in TIPOS:
        continue
    if v["position"]["y"] == 0 and v["position"]["height"] == 30:
        continue          # gatilho transparente do guia de leitura
    if v["visual"].get("objects", {}).get("dataPoint", [{}])[0].get("properties", {}).get("fillTransparency"):
        continue          # gatilhos (i) transparentes
    pid = f.parts[-4][-4:]
    ys = []
    for k, q in v["visual"].get("query", {}).get("queryState", {}).items():
        for p in q["projections"]:
            if k in ("Y", "Y2"):
                ys.append(p["queryRef"].replace("_medidas.", ""))
    hexes = sorted(set(re.findall(r"'(#[0-9A-Fa-f]{6})'", t)))
    tema = sorted(set(re.findall(r'"ColorId":\s*(\d+)', t)))
    medcor = sorted(set(re.findall(r'"Property":\s*"(Cor_\w+)"', t)))
    print(f"{pid} {tipo:<20} Y={','.join(ys)[:70]:<70} hex={hexes} tema={tema} medida_cor={medcor}")
