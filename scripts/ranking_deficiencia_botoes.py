# -*- coding: utf-8 -*-
"""Botões de tipo do ranking por deficiência: 6 colunas e 79,4 px de altura (ajuste feito à mão na página AFL),
levado para Todos os setores, e moldura do fundo esticada até a nova altura nas duas páginas."""
import datetime
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image

import ranking_deficiencia as rd

SLICERS = {"a3d1f2c4e6b8097a1c41": "eadb381b34bf47a4b3e7", "a3d1f2c4e6b8097a1c42": "98121d3878b84b11b8f1"}
REF = SLICERS["a3d1f2c4e6b8097a1c42"]
X_LINHA = 400          # coluna (2x) no meio de uma caixa: só as linhas de cima e de baixo da moldura são escuras
CANTO = 12             # linhas (2x) de cada ponta da moldura que ficam como estão (cantos arredondados)

ref = json.loads((rd.PAGES / "a3d1f2c4e6b8097a1c42" / "visuals" / REF / "visual.json").read_text(encoding="utf-8"))
ALTURA = ref["position"]["height"]
carimbo = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
ALTURA_ANTIGA = 47.911023220948749
ORIGEM = {"a3d1f2c4e6b8097a1c41": "contrata-todos-bg202611191503.png", "a3d1f2c4e6b8097a1c42": "contrata-afl-bg202611191503.png"}

for pid, vid in SLICERS.items():
    vf = rd.PAGES / pid / "visuals" / vid / "visual.json"
    txt = vf.read_text(encoding="utf-8")
    j = json.loads(txt)
    if pid != "a3d1f2c4e6b8097a1c42":
        j["position"]["height"] = ALTURA
        txt = json.dumps(j, ensure_ascii=False, indent=2) + "\n"
        txt = re.sub(r'"Value": "4L"', '"Value": "6L"', txt)
        vf.write_text(txt, encoding="utf-8", newline="\n")
    y, h = j["position"]["y"], ALTURA
    atual = rd.fundo_atual(pid)
    origem = ORIGEM[pid]
    a = np.asarray(Image.open(rd.RECURSOS / origem).convert("RGB")).copy()
    col = a[int(2 * y) - 6:int(2 * y) + 110, X_LINHA]
    ys = np.where(col.sum(axis=1) < 760)[0] + int(2 * y) - 6
    top, bot = int(ys.min()), int(ys.max())
    novo_bot = bot + int(round(2 * (h - ALTURA_ANTIGA)))
    alt = novo_bot - top + 1
    cima = a[top:top + CANTO].copy()
    baixo = a[bot - CANTO + 1:bot + 1].copy()
    meio = a[(top + bot) // 2].copy()
    bloco = np.vstack([cima, np.repeat(meio[None], alt - 2 * CANTO, axis=0), baixo])
    a[top:novo_bot + 1] = bloco
    novo = re.sub(r"\d+\.png$", f"{carimbo}.png", origem)
    Image.fromarray(a.astype(np.uint8)).save(rd.RECURSOS / novo, optimize=True)
    rd.registrar(novo)
    pj = rd.PAGES / pid / "page.json"
    pj.write_text(pj.read_text(encoding="utf-8").replace(atual, novo), encoding="utf-8", newline="\n")
    print(f"{pid}: moldura {top}-{bot} -> {top}-{novo_bot} (2x); fundo {novo}")
