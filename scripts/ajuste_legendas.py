"""Ajustes nas legendas desenhadas nos fundos (PNG):
  1. Empregos (Todos e AFL): remove a legenda do card da série (nada mais muda).
  2. Quanto ganha · AFL: o texto "Referência · média" da legenda vira "Comparáveis · média" (mesma fonte, tamanho e cor).
O PNG original de cada página é mantido; o ajuste vai para um arquivo novo (nome novo por causa do cache do Desktop) e é registrado.
Uso: python ajuste_legendas.py [--calibrar]
"""
import datetime
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

import fundo_rais as fb
import nav_ranking as nav
import pbir_rais as pb

PAGINA = {"emp_todos": "a3d1f2c4e6b8097a1c11", "emp_afl": "a3d1f2c4e6b8097a1c12", "ganha_afl": "a3d1f2c4e6b8097a1c32"}
COR_TEXTO = "#434446"


def renderizar(txt, esquerda, topo, tam, altura_pagina, familia="Segoe UI"):
    """Texto em HTML renderizado pelo Edge na mesma escala 2× dos fundos; devolve a imagem inteira da página."""
    html = (f"<!doctype html><meta charset='utf-8'><body style='margin:0;background:#fff'>"
            f"<div style=\"position:absolute;left:{esquerda}px;top:{topo}px;font:400 {tam}px '{familia}';line-height:1.2;color:{COR_TEXTO};white-space:nowrap\">{txt}</div></body>")
    with tempfile.TemporaryDirectory() as d:
        arq, png = Path(d) / "t.html", Path(d) / "t.png"
        arq.write_text(html, encoding="utf-8")
        subprocess.run([fb.EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2", f"--screenshot={png}",
                        f"--window-size={fb.W},{altura_pagina}", arq.as_uri()], capture_output=True, check=True)
        return Image.open(png).convert("RGB").copy()


def caixa(img, x0, y0, x1, y1, limiar=700):
    a = np.asarray(img).astype(int)[y0:y1, x0:x1]
    ys, xs = np.where(a.sum(axis=2) < limiar)
    return xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0


def novo_arquivo(pid, img, carimbo):
    atual = nav.fundo_atual(pid)
    novo = re.sub(r"\d+\.png$", f"{carimbo}.png", atual)
    img.save(nav.RECURSOS / novo, optimize=True)
    pj = pb.DEF / "pages" / pid / "page.json"
    pj.write_text(pj.read_text(encoding="utf-8").replace(atual, novo), encoding="utf-8")
    nav.registrar(novo)
    print(pid, atual, "->", novo)


def remover_legenda_empregos(carimbo):
    for chave in ("emp_todos", "emp_afl"):
        pid = PAGINA[chave]
        img = Image.open(nav.RECURSOS / nav.fundo_atual(pid)).convert("RGB")
        antes = caixa(img, 110, 1270, 2440, 1340)
        a = np.asarray(img).copy()
        a[1270:1340, 110:2440] = 255                     # só a faixa da legenda, dentro do card (largura útil do card, sem as bordas)
        print(chave, "legenda removida; caixa antes (x0, x1, y0, y1):", antes)
        novo_arquivo(pid, Image.fromarray(a), carimbo)


def trocar_referencia(carimbo, calibrar=False):
    pid = PAGINA["ganha_afl"]
    img = Image.open(nav.RECURSOS / nav.fundo_atual(pid)).convert("RGB")
    H = img.height // 2
    # texto original (2º item da legenda): região à direita do marcador tracejado
    x0, x1, y0, y1 = caixa(img, 1360, 1280, 1800, 1350)
    print("texto original (2x): x", x0, x1, "y", y0, y1, "largura", x1 - x0 + 1)
    melhor = None
    for tam in (17, 17.5, 18, 18.5, 19, 20, 21.333):
        r = renderizar("Referência · média", x0 / 2, 600, tam, H)
        b = caixa(r, 1200, 1100, 2400, 1500)
        dif = abs((b[1] - b[0]) - (x1 - x0))
        print(f"  tam {tam}: largura {b[1] - b[0] + 1}, altura {b[3] - b[2] + 1}")
        if melhor is None or dif < melhor[0]:
            melhor = (dif, tam, b)
    _, tam, b = melhor
    print("tamanho escolhido:", tam)
    if calibrar:
        return
    # alinha o topo e a esquerda do texto novo com os do original
    dx, dy = x0 - b[0], y0 - b[2]
    # mesma origem tipográfica do texto antigo (esquerda e linha de base), não a mesma caixa: "R" e "C" têm recuos diferentes
    r = renderizar("Comparáveis · média", x0 / 2 + dx / 2, 600 + dy / 2, tam, H)
    nb = caixa(r, 1200, 1100, 2400, 1500)
    print("texto novo (2x): x", nb[0], nb[1], "y", nb[2], nb[3])
    a = np.asarray(img).copy()
    a[1290:1350, x0 - 6:1800] = 255                        # apaga só o texto antigo (o marcador tracejado termina antes de x0)
    ar = np.asarray(r)
    janela = (slice(1290, 1350), slice(x0 - 6, 1800))
    a[janela] = np.minimum(a[janela], ar[janela])          # escuro sobre branco: o texto novo entra por cima
    novo_arquivo(pid, Image.fromarray(a), carimbo)


if __name__ == "__main__":
    carimbo = datetime.datetime.now().strftime("%Y%m%d%H%M")
    if "--calibrar" in sys.argv:
        trocar_referencia(carimbo, calibrar=True)
    else:
        remover_legenda_empregos(carimbo)
        trocar_referencia(carimbo)
