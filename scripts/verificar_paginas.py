"""Verificação estrutural de qualquer página: JSONs válidos e toda medida usada pelos visuais existe em _medidas.tmdl.
Uso: python verificar_paginas.py c12 c32 ...  (sufixo do id da página; sem argumentos, confere as oito páginas de conteúdo)."""
import json
import re
import sys
from pathlib import Path

import pbir_rais as pb

RAIZ = Path(__file__).resolve().parents[1]
t = (RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl").read_bytes().decode("utf-8")
med = set(re.findall(r"^\tmeasure (\w+)", t, re.M))
alvo = sys.argv[1:] or ["c11", "c12", "c21", "c22", "c31", "c32", "c41", "c42"]
for suf in alvo:
    pid = "a3d1f2c4e6b8097a1" + suf
    falta, n = set(), 0
    for f in (pb.DEF / "pages" / pid / "visuals").glob("*/visual.json"):
        s = f.read_text(encoding="utf-8")
        json.loads(s)
        n += 1
        for pr in re.findall(r'"Entity":\s*"_medidas"\s*\}\s*\},\s*"Property":\s*"(\w+)"', s):
            if pr not in med:
                falta.add(pr)
    json.loads((pb.DEF / "pages" / pid / "page.json").read_text(encoding="utf-8"))
    print(suf, n, "visuais · medidas ausentes:", sorted(falta) or "nenhuma")
