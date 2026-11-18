"""Troca o filtro "Contrato" (F_rais[modalidade_contrato]) pelo filtro "Intermitente" (F_rais[trabalho_intermitente]) nas oito páginas.

 1. Segmentadores: mesmo visual (posição, estilo, sincronização), só muda o campo, o título e o grupo de sincronização.
 2. Fundos de Empregos, Quem trabalha e Quanto ganha: o rótulo "Contrato" é apagado e "Intermitente" é desenhado no mesmo lugar, com a
    mesma espessura de letra (o original era mais encorpado que o Open Sans 600: a espessura é calibrada pela "tinta" do texto antigo).
    Os fundos de Ranking (c41/c42) são refeitos por contrata_v2.py.
Os fundos de partida são os anteriores a ESTA troca (último arquivo da página com carimbo menor que ANTES_DE), então o script pode ser
repetido sem acumular alterações. Uso: python filtro_intermitente.py
"""
import datetime
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

import fundo_rais as fb
import nav_ranking as nav
import pbir_rais as pb
from texto_path import texto

PAGINAS = ["c11", "c12", "c21", "c22", "c31", "c32", "c41", "c42"]
COR = "#434446"
ANTES_DE = 202611181338           # carimbo da primeira troca; os fundos de partida são os anteriores a ele


def segmentadores():
    for suf in PAGINAS:
        pid = "a3d1f2c4e6b8097a1" + suf
        achou = False
        for f in (pb.DEF / "pages" / pid / "visuals").glob("*/visual.json"):
            t = f.read_text(encoding="utf-8")
            if "modalidade_contrato" in t and '"visualType": "slicer"' in t:
                novo = t.replace("modalidade_contrato", "trabalho_intermitente").replace("'Contrato'", "'Intermitente'").replace("rais_contrato", "rais_intermitente")
                f.write_text(novo, encoding="utf-8")
                achou = True
                print(suf, "segmentador trocado:", f.parent.name[:8])
        if not achou:
            ok = any("trabalho_intermitente" in f.read_text(encoding="utf-8") for f in (pb.DEF / "pages" / pid / "visuals").glob("*/visual.json"))
            print(suf, "segmentador já é Intermitente" if ok else "ATENÇÃO: segmentador não encontrado")


def renderizar(txt, x, y_base, borda, altura):
    """Open Sans 600 com contorno opcional (borda, em px da página) para engrossar o traço."""
    plano = texto(txt, x, y_base, fb.PT(18), COR, 600)
    if borda:
        plano = plano.replace("/>", f' stroke="{COR}" stroke-width="{borda}" stroke-linejoin="round"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fb.W} {altura}" width="{fb.W}" height="{altura}">'
           f'<rect width="{fb.W}" height="{altura}" fill="#FFFFFF"/>{plano}</svg>')
    with tempfile.TemporaryDirectory() as d:
        s, p = Path(d) / "r.svg", Path(d) / "r.png"
        s.write_text(svg, encoding="utf-8")
        subprocess.run([fb.EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2", f"--screenshot={p}",
                        f"--window-size={fb.W},{altura}", s.as_uri()], capture_output=True, check=True)
        return np.asarray(Image.open(p).convert("RGB")).astype(int)


def caixa(a, x0, y0, x1, y1, limiar=700):
    sub = a[y0:y1, x0:x1]
    ys, xs = np.where(sub.sum(axis=2) < limiar)
    return xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0


def tinta(a, caixa_):
    x0, x1, y0, y1 = caixa_
    return int((765 - a[y0 - 6:y1 + 7, x0 - 6:x1 + 7].sum(axis=2)).clip(0).sum())


def fonte_de_partida(pid):
    """Último fundo da página anterior à troca (mesma família de nome, carimbo de 12 dígitos menor que ANTES_DE)."""
    atual = nav.fundo_atual(pid)
    familia = re.sub(r"\d+\.png$", "", atual)
    candidatos = []
    for p in nav.RECURSOS.glob(familia + "[0-9]*.png"):
        n = re.search(r"(\d+)\.png$", p.name).group(1)
        if len(n) == 12 and int(n) < ANTES_DE:
            candidatos.append((int(n), p.name))
    return max(candidatos)[1]


def fundos():
    carimbo = datetime.datetime.now().strftime("%Y%m%d%H%M")
    for suf in PAGINAS:
        if suf in ("c41", "c42"):
            continue
        pid = "a3d1f2c4e6b8097a1" + suf
        atual = nav.fundo_atual(pid)
        origem = fonte_de_partida(pid)
        img = Image.open(nav.RECURSOS / origem).convert("RGB")
        a = np.asarray(img).astype(int)
        altura = img.height // 2
        x0, x1, y0, y1 = caixa(a, 3120, 190, 3840, 270)
        cx = (x0, x1, y0, y1)
        ref = tinta(a, cx)
        print(f"{suf}: partida {origem}; rótulo 'Contrato' x {x0}-{x1} y {y0}-{y1}, tinta {ref}")
        # calibra o contorno: "Contrato" refeito com cada espessura, comparado com o original (tinta e largura)
        melhor = None
        for borda in (0, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3):
            r = renderizar("Contrato", 1600, 124, borda, altura)
            b = caixa(r, 3100, 190, 3840, 270)
            erro = abs(tinta(r, b) - ref) / ref + abs((b[1] - b[0]) - (x1 - x0)) / (x1 - x0)
            if melhor is None or erro < melhor[0]:
                melhor = (erro, borda, b)
        _, borda, b = melhor
        ox = 1600 + (x0 - b[0]) / 2                     # mesma origem à esquerda e mesma linha de base do texto antigo
        oy = 124 + (y1 - b[3]) / 2
        r = renderizar("Intermitente", ox, oy, borda, altura)
        nb = caixa(r, 3100, 190, 3840, 270)
        print(f"   contorno {borda}; 'Intermitente' x {nb[0]}-{nb[1]} y {nb[2]}-{nb[3]}")
        saida = a.copy()
        janela = (slice(y0 - 8, y1 + 8), slice(x0 - 8, nb[1] + 12))
        saida[janela] = 255
        saida[janela] = np.minimum(saida[janela], r[janela])
        novo = re.sub(r"\d+\.png$", f"{carimbo}.png", origem)
        Image.fromarray(saida.astype(np.uint8)).save(nav.RECURSOS / novo, optimize=True)
        pj = pb.DEF / "pages" / pid / "page.json"
        pj.write_text(pj.read_text(encoding="utf-8").replace(atual, novo), encoding="utf-8")
        nav.registrar(novo)
        print("  ", atual, "->", novo)


if __name__ == "__main__":
    segmentadores()
    fundos()
