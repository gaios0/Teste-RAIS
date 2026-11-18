"""Confere a presença dos ícones (i) nos fundos: conta pixels escuros dentro de cada posição de ícone (24 px, centro em centro_info)."""
import re
import sys

import numpy as np
from PIL import Image

import fundo_rais as fb
import nav_ranking as nav

pos = fb.posicoes_cartoes()


def contar(arq):
    a = np.asarray(Image.open(nav.RECURSOS / arq).convert("RGB")).astype(int)
    saida = {}
    for c in pos:
        cx, cy = fb.centro_info(c)
        reg = a[int((cy - 14) * 2):int((cy + 14) * 2), int((cx - 14) * 2):int((cx + 14) * 2)]
        saida[c] = int((reg.sum(axis=2) < 450).sum())
    return saida


alvos = sys.argv[1:] or [nav.fundo_atual("a3d1f2c4e6b8097a1" + s) for s in ("c11", "c12", "c21", "c31")]
for arq in alvos:
    print(arq, contar(arq))
