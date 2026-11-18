"""Mostra qual página de tooltip e qual medida cada gráfico do Quanto ganha usa."""
import json
import sys

import pbir_rais as pb

for pg in sys.argv[1:]:
    print("===", pg)
    for f in sorted((pb.DEF / "pages" / pg / "visuals").glob("*/visual.json")):
        v = json.loads(f.read_text(encoding="utf-8"))
        tt = v["visual"].get("visualContainerObjects", {}).get("visualTooltip")
        if not tt or v["visual"]["visualType"] not in ("lineChart", "clusteredBarChart", "barChart"):
            continue
        sec = tt[0]["properties"]["section"]["expr"]["Literal"]["Value"].strip("'")
        if "show" in tt[0]["properties"] and tt[0]["properties"]["show"]["expr"]["Literal"]["Value"] == "false":
            continue
        pj = json.loads((pb.DEF / "pages" / sec / "page.json").read_text(encoding="utf-8"))
        vis = next((pb.DEF / "pages" / sec / "visuals").glob("*/visual.json"))
        med = json.loads(vis.read_text(encoding="utf-8"))["visual"]["query"]["queryState"]["content"]["projections"][0]["queryRef"]
        ys = [p["queryRef"] for p in v["visual"]["query"]["queryState"].get("Y", {}).get("projections", [])][:2]
        print(f"{v['visual']['visualType']:<18} {f.parent.name[:6]}  Y={ys}  -> {sec[-4:]} '{pj['displayName']}' medida {med}")
