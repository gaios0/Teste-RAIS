"""Inventário de onde o laranja do AFL (#F58220) aparece: visuais (por página e tipo) e medidas (por nome)."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import pbir_rais as pb

RAIZ = Path(__file__).resolve().parents[1]
COR = re.compile(r"#F58220", re.I)
print("== visuais")
tot = defaultdict(Counter)
for f in sorted((pb.DEF / "pages").glob("*/visuals/*/visual.json")):
    t = f.read_text(encoding="utf-8")
    n = len(COR.findall(t))
    if not n:
        continue
    v = json.loads(t)
    tipo = v["visual"]["visualType"]
    if tipo in ("actionButton", "image"):
        continue
    pid = f.parts[-4][-4:]
    props = sorted(set(re.findall(r'"(fill|markerColor|color|fontColor|fillColor|lineColor)"\s*:', t)))
    medida = ""
    try:
        medida = next(iter(v["visual"]["query"]["queryState"]["Y"]["projections"]))["queryRef"]
    except Exception:
        try:
            medida = next(iter(v["visual"]["query"]["queryState"]["content"]["projections"]))["queryRef"]
        except Exception:
            pass
    print(f"  {pid} {tipo:<22} {n:>2}x  {medida}")
print("== medidas (tmdl)")
texto = (RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl").read_bytes().decode("utf-8").replace("\r\n", "\n")
atual, cont = None, Counter()
for l in texto.split("\n"):
    m = re.match(r"^\tmeasure (\w+)", l)
    if m:
        atual = m.group(1)
    if atual and COR.search(l):
        cont[atual] += len(COR.findall(l))
for k, v in sorted(cont.items()):
    print(f"  {v:>2}x {k}")
print("total medidas com a cor:", len(cont))
