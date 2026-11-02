# -*- coding: utf-8 -*-
"""Converte texto em <path> (contorno da fonte) para o fundo passar no validador (sem <text>).
Fonte: Open Sans 400/600 (OFL, @fontsource/open-sans 5.2.5), o substituto aberto mais próximo do Segoe UI."""
from functools import lru_cache
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

from pathlib import Path
_DIR = Path(__file__).resolve().parents[1] / "assets" / "fontes"
FONTES = {400: str(_DIR / "open-sans-latin-400-normal.woff"), 600: str(_DIR / "open-sans-latin-600-normal.woff")}


@lru_cache(maxsize=None)
def _fonte(peso):
    f = TTFont(FONTES[peso]); return f, f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm


def largura(txt, tam, peso=400):
    f, gs, cmap, hmtx, upm = _fonte(peso)
    return sum(hmtx[cmap.get(ord(c), ".notdef")][0] for c in txt) * tam / upm


def texto(txt, x, y, tam, cor, peso=400, ancora="start"):
    """y = linha de base. ancora: start | middle | end."""
    f, gs, cmap, hmtx, upm = _fonte(peso)
    esc = tam / upm; w = largura(txt, tam, peso)
    x0 = x - (w / 2 if ancora == "middle" else w if ancora == "end" else 0)
    pen = SVGPathPen(gs); cur = 0
    for c in txt:
        g = cmap.get(ord(c), ".notdef")
        gs[g].draw(TransformPen(pen, (esc, 0, 0, -esc, x0 + cur * esc, y)))
        cur += hmtx[g][0]
    return f'<path d="{pen.getCommands()}" fill="{cor}"/>'
