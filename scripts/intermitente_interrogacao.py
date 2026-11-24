# -*- coding: utf-8 -*-
"""RAIS OFICIAL: rótulo do filtro "Intermitente" vira "Intermitente ?" no fundo das 8 páginas.

O rótulo antigo fica como está; só o "?" é desenhado logo depois, com a mesma fonte, tamanho e espessura
(espessura calibrada pela "tinta" do rótulo antigo, como em filtro_intermitente.py)."""
import datetime
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from filtro_intermitente import renderizar, caixa, tinta  # noqa: E402

OF = Path(__file__).resolve().parent.parent / "RAIS OFICIAL" / "RAIS Emprego Formal.Report"
PAGES = OF / "definition" / "pages"
RECURSOS = OF / "StaticResources" / "RegisteredResources"
PAGINAS = ["c11", "c12", "c21", "c22", "c31", "c32", "c41", "c42"]
OX, OY, ALT = 100, 60, 100          # origem do texto de teste (px da página) e altura da tela de teste
carimbo = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
cache = {}
# fundos de antes do "?" (o script pode ser repetido sem acumular)
ORIGEM = {"c11": "empregos-todos-bg202611181407.png", "c12": "empregos-afl-bg202611181407.png", "c21": "trabalha-todos-bg202611181341.png",
          "c22": "trabalha-afl-bg202611181341.png", "c31": "ganha-todos-bg202611181341.png", "c32": "ganha-afl-bg202611181341.png",
          "c41": "contrata-todos-bg20261124144651.png", "c42": "contrata-afl-bg20261119151532.png"}


def teste(txt, borda):
    if (txt, borda) not in cache:
        cache[(txt, borda)] = renderizar(txt, OX, OY, borda, ALT)
    return cache[(txt, borda)]


novos = []
for suf in PAGINAS:
    pid = "a3d1f2c4e6b8097a1" + suf
    pos = None
    for vf in (PAGES / pid / "visuals").glob("*/visual.json"):
        t = vf.read_text(encoding="utf-8")
        if '"visualType": "slicer"' in t and "trabalho_intermitente" in t:
            pos = json.loads(t)["position"]
    if pos is None:
        sys.exit(f"{suf}: filtro Intermitente não achado")
    pj = PAGES / pid / "page.json"
    atual = re.search(r"'([^']+-bg\d+\.png)'", pj.read_text(encoding="utf-8")).group(1)
    base = ORIGEM[suf]
    a = np.asarray(Image.open(RECURSOS / base).convert("RGB")).astype(int)
    x0, x1 = int(pos["x"] * 2) - 10, int((pos["x"] + pos["width"]) * 2)
    y0, y1 = int((pos["y"] - 34) * 2), int(pos["y"] * 2) - 4
    v = caixa(a, x0, y0, x1, y1)
    ref = tinta(a, v)
    # espessura: a que deixa "Intermitente" com a mesma tinta e largura do rótulo antigo
    melhor = None
    for borda in (0, 0.3, 0.5, 0.7, 0.9, 1.1):
        r = teste("Intermitente", borda)
        b = caixa(r, 0, 0, 1000, ALT * 2)
        erro = abs(tinta(r, b) - ref) / ref + abs((b[1] - b[0]) - (v[1] - v[0])) / (v[1] - v[0])
        if melhor is None or erro < melhor[0]:
            melhor = (erro, borda, b)
    _, borda, b = melhor
    r2 = teste("Intermitente ?", borda)
    b2 = caixa(r2, 0, 0, 1000, ALT * 2)
    dx, dy = v[0] - b[0], v[3] - b[3]                 # alinha pela esquerda e pela base do rótulo antigo
    ini = b[1] + 3                                    # o "?" começa depois do fim do "e"
    janela = r2[b2[2] - 2:b2[3] + 3, ini:b2[1] + 3]
    ty, tx = b2[2] - 2 + dy, ini + dx
    if tx + janela.shape[1] >= x1:
        sys.exit(f"{suf}: o '?' passa da caixa do filtro")
    saida = a.copy()
    alvo = saida[ty:ty + janela.shape[0], tx:tx + janela.shape[1]]
    saida[ty:ty + janela.shape[0], tx:tx + janela.shape[1]] = np.minimum(alvo, janela)
    novo = re.sub(r"\d+\.png$", f"{carimbo}.png", base)
    Image.fromarray(saida.astype(np.uint8)).save(RECURSOS / novo, optimize=True)
    pj.write_text(pj.read_text(encoding="utf-8").replace(atual, novo), encoding="utf-8", newline="\n")
    novos.append(novo)
    if suf == "c41":
        Image.fromarray(saida[y0 - 10:y1 + 120, x0 - 20:x1 + 20].astype(np.uint8)).save(Path(sys.argv[1]) if len(sys.argv) > 1 else RECURSOS / "_previa.png")
    print(f"{suf}: rótulo {v}, borda {borda}, {atual} -> {novo}")

rj = OF / "definition" / "report.json"
d = json.loads(rj.read_text(encoding="utf-8"))
pk = next(p for p in d["resourcePackages"] if p["name"] == "RegisteredResources")
for n in novos:
    if n not in {i["name"] for i in pk["items"]}:
        pk["items"].append({"name": n, "path": n, "type": "Image"})
pk["items"].sort(key=lambda i: i["name"].lower())
rj.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

# tira as imagens da versão sem espaço (162903), que nenhuma página usa mais
for p in RECURSOS.glob("*-bg20261124162903.png"):
    p.unlink()
d = json.loads(rj.read_text(encoding="utf-8"))
pk = next(p for p in d["resourcePackages"] if p["name"] == "RegisteredResources")
pk["items"] = [i for i in pk["items"] if not i["name"].endswith("-bg20261124162903.png")]
rj.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")