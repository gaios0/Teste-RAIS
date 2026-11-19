# -*- coding: utf-8 -*-
"""Checagem estática: campos dos visuais e colunas citadas no DAX que não existem no modelo,
e textos que ainda falam de mediana ou de 2009."""
import json
import re
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SM = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition"
REP = RAIZ / "RAIS Emprego Formal.Report" / "definition"

campos = defaultdict(set)
for f in (SM / "tables").glob("*.tmdl"):
    t = f.read_text(encoding="utf-8")
    tab = re.search(r"^table ('?)(.+?)\1\s*$", t, re.M).group(2)
    for n in re.findall(r"^\t(?:column|measure) ('(?:[^']|'')+'|[^=\n]+?)(?:\s*=.*)?$", t, re.M):
        campos[tab].add(n.strip().strip("'"))
todas_medidas = {n for t in campos.values() for n in t}

paginas = {}
for p in (REP / "pages").iterdir():
    if (p / "page.json").exists():
        paginas[p.name] = json.loads((p / "page.json").read_text(encoding="utf-8")).get("displayName", p.name)


def andar(o, achou):
    if isinstance(o, dict):
        for k in ("Column", "Measure", "Aggregation", "HierarchyLevel"):
            if k in o and isinstance(o[k], dict):
                x = o[k]
                ent = x.get("Expression", {}).get("SourceRef", {}).get("Entity")
                if ent and "Property" in x:
                    achou.add((ent, x["Property"]))
        for v in o.values():
            andar(v, achou)
    elif isinstance(o, list):
        for v in o:
            andar(v, achou)


print("== Campos de visuais que não existem no modelo")
for vf in (REP / "pages").glob("*/visuals/*/visual.json"):
    achou = set()
    andar(json.loads(vf.read_text(encoding="utf-8")), achou)
    for ent, prop in sorted(achou):
        if prop not in campos.get(ent, set()):
            print(f"  {paginas[vf.parts[-4]]} | {vf.parts[-2]} | {ent}[{prop}]")

print("== Colunas citadas no DAX que não existem")
RE_STR = re.compile(r'"(?:[^"]|"")*"', re.S)
med = (SM / "tables" / "_medidas.tmdl").read_text(encoding="utf-8")
blocos = re.split(r"\n\tmeasure ", med)
for b in blocos[1:]:
    nome = b.split("=", 1)[0].strip()
    d = RE_STR.sub('""', b)
    for t, c in set(re.findall(r"('[^']+'|\b[A-Za-z_]\w*)\[([^\]]+)\]", d)):
        t = t.strip("'")
        if t in campos and c not in campos[t]:
            print(f"  {nome}: {t}[{c}]")

print("== Medidas que ainda usam mediana")
for b in blocos[1:]:
    nome = b.split("=", 1)[0].strip()
    if re.search(r"Mediana", RE_STR.sub('""', b)):
        print("  ", nome)
print("== Textos que falam de mediana ou de 2009")
for f in list((SM / "tables").glob("*.tmdl")):
    for i, l in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
        for s in re.findall(r'"([^"]*(?:mediana|2009)[^"]*)"', l, re.I):
            print(f"  {f.stem}:{i}: {s[:140]}")
