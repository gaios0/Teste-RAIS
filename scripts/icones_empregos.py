"""Devolve os ícones (i) que faltam nos três cards de KPI dos fundos de Empregos (Todos e AFL).

Cada ícone é desenhado no centro do gatilho transparente que já existe na página (84 × 62 px), com o mesmo desenho dos demais cards
(lucide "info", 24 px, #434446). O fundo antigo é mantido; o novo vai com nome novo (cache do Desktop). Idempotente.
"""
import datetime
import json
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

import fundo_rais as fb
import nav_ranking as nav
import pbir_rais as pb

PAGINAS = {"c11": "a3d1f2c4e6b8097a1c11", "c12": "a3d1f2c4e6b8097a1c12"}


def gatilhos_kpi(pid):
    """Centros (px da página) dos gatilhos de informação da linha dos KPIs."""
    centros = []
    for f in (pb.DEF / "pages" / pid / "visuals").glob("*/visual.json"):
        v = json.loads(f.read_text(encoding="utf-8"))
        p = v["position"]
        if v["visual"]["visualType"] == "clusteredColumnChart" and round(p["width"]) == 84 and round(p["height"]) == 62 and p["y"] < 500:
            centros.append((round(p["x"] + p["width"] / 2, 1), round(p["y"] + p["height"] / 2, 1)))
    return sorted(centros)


def renderizar(centros, altura):
    corpo = "".join(fb.icone("info", cx - 12, cy - 12, 24, fb.K["tinta2"]) for cx, cy in centros)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fb.W} {altura}" width="{fb.W}" height="{altura}">'
           f'<rect width="{fb.W}" height="{altura}" fill="#FFFFFF"/>{corpo}</svg>')
    with tempfile.TemporaryDirectory() as d:
        s, p = Path(d) / "i.svg", Path(d) / "i.png"
        s.write_text(svg, encoding="utf-8")
        subprocess.run([fb.EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2", f"--screenshot={p}",
                        f"--window-size={fb.W},{altura}", s.as_uri()], capture_output=True, check=True)
        return np.asarray(Image.open(p).convert("RGB")).astype(int)


def main():
    carimbo = datetime.datetime.now().strftime("%Y%m%d%H%M")
    for suf, pid in PAGINAS.items():
        centros = gatilhos_kpi(pid)
        atual = nav.fundo_atual(pid)
        img = Image.open(nav.RECURSOS / atual).convert("RGB")
        a = np.asarray(img).astype(int)
        faltam = []
        for cx, cy in centros:
            reg = a[int((cy - 14) * 2):int((cy + 14) * 2), int((cx - 14) * 2):int((cx + 14) * 2)]
            if int((reg.sum(axis=2) < 450).sum()) < 100:
                faltam.append((cx, cy))
        print(suf, "gatilhos:", centros, "· sem ícone:", faltam)
        if not faltam:
            continue
        r = renderizar(faltam, img.height // 2)
        saida = np.minimum(a, r)                       # ícone escuro sobre branco: entra por cima, o resto do fundo fica igual
        novo = re.sub(r"\d+\.png$", f"{carimbo}.png", atual)
        Image.fromarray(saida.astype(np.uint8)).save(nav.RECURSOS / novo, optimize=True)
        pj = pb.DEF / "pages" / pid / "page.json"
        pj.write_text(pj.read_text(encoding="utf-8").replace(atual, novo), encoding="utf-8")
        nav.registrar(novo)
        print("  ", atual, "->", novo)


if __name__ == "__main__":
    main()
