"""Laranja do AFL mais escuro (#F58220 -> AFL_ESCURO) onde ele representa o valor do AFL separado dos demais.

Muda: gráficos (barras e linhas do AFL), medidas de cor do ranking, marcadores e chips "AFL" de tooltips/KPIs e as legendas desenhadas nos fundos.
Não muda: o laranja de interface (abas, botões, acentos de KPI e de título, destaque da frase de leitura, sublinhado da aba ativa).
Idempotente. Uso: python afl_cor.py
"""
import datetime
import json
import re
from pathlib import Path

import sys

import numpy as np
from PIL import Image
from scipy import ndimage

import nav_ranking as nav
import pbir_rais as pb

ANTIGO = "#F58220"
AFL_ESCURO = "#D97706"                 # âmbar escuro (a 1ª tentativa, #D95F02, foi recusada)
TENTATIVAS_ANTERIORES = ["#D95F02"]    # trocadas pela cor atual se ainda estiverem no projeto
RAIZ = Path(__file__).resolve().parents[1]
TMDL = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl"
GRAFICOS = ("lineChart", "clusteredBarChart", "barChart", "clusteredColumnChart")


def medidas():
    """Só os usos que representam o AFL: cor do item AFL nos rankings, marcador de legenda dos tooltips e borda do chip AFL."""
    t = TMDL.read_bytes().decode("utf-8")
    regras = [(r'("AFL · conjunto de 6 CNAEs", ")' + ANTIGO + '"', r"\g<1>" + AFL_ESCURO + '"'),
              (r"(border-radius:3px;background:)" + ANTIGO + ";", r"\g<1>" + AFL_ESCURO + ";"),
              (r"(padding:1px 9px;border:1px solid )" + ANTIGO + ";", r"\g<1>" + AFL_ESCURO + ";")]
    total = 0
    for padrao, subst in regras:
        t, n = re.subn(padrao, subst, t, flags=re.I)
        total += n
    for antes in TENTATIVAS_ANTERIORES:
        t, n = re.subn(re.escape(antes), AFL_ESCURO, t, flags=re.I)
        total += n
    TMDL.write_bytes(t.encode("utf-8"))
    print("medidas:", total, "trocas")


def graficos():
    n = 0
    for f in sorted((pb.DEF / "pages").glob("*/visuals/*/visual.json")):
        t = f.read_text(encoding="utf-8")
        trocar = [ANTIGO] + TENTATIVAS_ANTERIORES
        if not any(c.lower() in t.lower() for c in trocar):
            continue
        if json.loads(t)["visual"]["visualType"] not in GRAFICOS:
            continue
        f.write_text(re.sub("|".join(re.escape(c) for c in trocar), AFL_ESCURO, t, flags=re.I), encoding="utf-8")
        n += 1
        print("  gráfico:", f.parts[-4][-4:], f.parts[-2][:6])
    print("gráficos:", n)


def recolorir(img):
    """Troca o laranja só nos marcadores de legenda (fundo branco): preserva o anti-aliasing pela proporção de laranja de cada pixel.

    Um marcador é um componente pequeno (até 70 × 20 px na página) com miolo sólido; barras de acento de título/KPI (longas) e as
    franjas coloridas do texto (sem miolo sólido) ficam como estão.
    """
    a = np.asarray(img.convert("RGB")).astype(np.int32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    rb = r - b
    with np.errstate(divide="ignore", invalid="ignore"):
        razao = np.where(rb > 0, (g - b) / np.maximum(rb, 1), 0)
    candidatos = (r >= 238) & (rb >= 25) & (np.abs(razao - 0.46) < 0.035)
    candidatos[:200, :] = False              # faixa de abas (sublinhado da aba ativa é laranja de interface)
    alfa = np.clip(rb / 213.0, 0, 1)
    rotulos, n = ndimage.label(candidatos, structure=np.ones((3, 3)))
    mascara = np.zeros_like(candidatos)
    for i, caixa in enumerate(ndimage.find_objects(rotulos), start=1):
        h, w = caixa[0].stop - caixa[0].start, caixa[1].stop - caixa[1].start
        comp = rotulos[caixa] == i
        miolo = int((comp & (alfa[caixa] >= 0.9)).sum())
        if miolo >= 20 and w <= 140 and h <= 40:
            mascara[caixa] |= comp
    novo = np.array([int(AFL_ESCURO[i:i + 2], 16) for i in (1, 3, 5)])
    saida = a.copy()
    for c in range(3):
        saida[..., c] = np.where(mascara, np.round(255 - alfa * (255 - novo[c])), a[..., c])
    return Image.fromarray(saida.astype(np.uint8)), int(mascara.sum())


def fundos(origem=None):
    """origem = carimbo do fundo ainda sem recolorir (ex.: 202611171414). Sem ele, parte do fundo registrado agora."""
    carimbo = datetime.datetime.now().strftime("%Y%m%d%H%M")
    for (tema, recorte), pid in nav.PAGINAS.items():
        if tema == "Quem contrata":
            continue                          # as páginas de Ranking não têm legenda laranja
        atual = nav.fundo_atual(pid)
        nome = re.sub(r"\d+\.png$", f"{origem}.png", atual) if origem else atual
        img, n = recolorir(Image.open(nav.RECURSOS / nome))
        pj = pb.DEF / "pages" / pid / "page.json"
        if n < 50:                            # nada a recolorir: a página volta a apontar para o fundo de origem
            pj.write_text(pj.read_text(encoding="utf-8").replace(atual, nome), encoding="utf-8")
            print(pid, nome, "sem legenda laranja")
            continue
        novo = re.sub(r"\d+\.png$", f"{carimbo}.png", nome)
        img.save(nav.RECURSOS / novo, optimize=True)
        pj.write_text(pj.read_text(encoding="utf-8").replace(atual, novo), encoding="utf-8")
        nav.registrar(novo)
        print(pid, nome, "->", novo, f"({n} pixels)")


if __name__ == "__main__":
    medidas()
    graficos()
    fundos(sys.argv[sys.argv.index("--origem") + 1] if "--origem" in sys.argv else None)
