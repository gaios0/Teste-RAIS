# -*- coding: utf-8 -*-
"""Ranking (RAIS OFICIAL): "setores" -> "divisões" onde o ranking é por divisão CNAE.

- Manchete: "Ranking das divisões: média salarial e representatividade por perfil dos empregados."
  (AFL: "Ranking do AFL: média salarial e representatividade por perfil dos empregados.")
- Botões: "10 melhores divisões" / "10 piores divisões" (tabela D_Ct_Modo, medidas, filtro inicial do botão, geradores).
- Fundo de Ranking · Todos os setores: rótulo "Ranking dos setores" -> "Ranking das divisões".
"""
import datetime
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fundo_rais as fb
from texto_path import texto

RAIZ = Path(__file__).resolve().parent.parent
OF = RAIZ / "RAIS OFICIAL"
TAB = OF / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables"
REP = OF / "RAIS Emprego Formal.Report"
PAGES = REP / "definition" / "pages"
RECURSOS = REP / "StaticResources" / "RegisteredResources"
PID = "a3d1f2c4e6b8097a1c41"
MODO = "40980b2ae996c67d1cce"

TROCAS = [("10 melhores setores", "10 melhores divisões"), ("10 piores setores", "10 piores divisões")]
MANCHETES = [
    ('IF(NSal = 3, "Ranking dos setores: salário médio por perfil dos empregados", "Ranking dos setores: quem mais contrata por perfil dos empregados")',
     '"Ranking das divisões: média salarial e representatividade por perfil dos empregados."'),
    ('IF(NSal = 3, "Ranking do AFL: salário médio por perfil dos empregados", "Ranking do AFL: quem mais contrata por perfil dos empregados")',
     '"Ranking do AFL: média salarial e representatividade por perfil dos empregados."'),
]
cont = {}


def trocar_arquivo(p, pares, chave):
    t = p.read_text(encoding="utf-8")
    n = 0
    for a, b in pares:
        n += t.count(a)
        t = t.replace(a, b)
    p.write_text(t, encoding="utf-8", newline="")
    cont[chave] = cont.get(chave, 0) + n


# ---- modelo e visual
trocar_arquivo(TAB / "D_Ct_Modo.tmdl", TROCAS, "D_Ct_Modo")
trocar_arquivo(TAB / "_medidas.tmdl", TROCAS + MANCHETES, "_medidas")
trocar_arquivo(PAGES / PID / "visuals" / MODO / "visual.json", TROCAS, "botão")
# geradores antigos, para não voltar
for g, pares in (("contrata_v2.py", TROCAS + [('texto("Ranking dos setores"', 'texto("Ranking das divisões"')]), ("dax_contrata2.py", TROCAS)):
    trocar_arquivo(RAIZ / "scripts" / g, pares, g)
if cont["_medidas"] < 4:
    sys.exit(f"manchetes/medidas não achadas: {cont}")

# ---- fundo
pj = PAGES / PID / "page.json"
atual = re.search(r"'([^']+-bg\d+\.png)'", pj.read_text(encoding="utf-8")).group(1)
img = Image.open(RECURSOS / atual).convert("RGB")
a = np.asarray(img).astype(int)
pos = json.loads((PAGES / PID / "visuals" / MODO / "visual.json").read_text(encoding="utf-8"))["position"]
y0, y1 = int(pos["y"] * 2) + 4, int((pos["y"] + pos["height"]) * 2) - 4
x0, x1 = fb.M * 2 + 2, int(pos["x"] * 2) - 6
sub = a[y0:y1, x0:x1]
ys, xs = np.where(sub.sum(axis=2) < 600)
if len(xs) == 0:
    sys.exit("rótulo não achado no fundo")
caixa = (xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0)

plano = texto("Ranking das divisões", fb.M, pos["y"] + 32, 22, fb.K["tinta"], 600)
alt = img.height // 2
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fb.W} {alt}" width="{fb.W}" height="{alt}">'
       f'<rect width="{fb.W}" height="{alt}" fill="#FFFFFF"/>{plano}</svg>')
with tempfile.TemporaryDirectory() as d:
    s, p = Path(d) / "r.svg", Path(d) / "r.png"
    s.write_text(svg, encoding="utf-8")
    subprocess.run([fb.EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2", f"--screenshot={p}",
                    f"--window-size={fb.W},{alt}", s.as_uri()], capture_output=True, check=True)
    r = np.asarray(Image.open(p).convert("RGB")).astype(int)
nys, nxs = np.where(r[y0:y1, x0:x1].sum(axis=2) < 600)
fim = max(caixa[1], nxs.max() + x0)
if fim >= int(pos["x"] * 2) - 4:
    sys.exit("texto novo encosta nos botões")
jan = (slice(caixa[2] - 4, caixa[3] + 5), slice(caixa[0] - 4, fim + 5))
saida = a.copy()
fundo = a[caixa[2] - 6, caixa[0] - 6].copy()
saida[jan] = fundo
saida[jan] = np.minimum(saida[jan], r[jan])
carimbo = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
novo = re.sub(r"\d+\.png$", f"{carimbo}.png", atual)
Image.fromarray(saida.astype(np.uint8)).save(RECURSOS / novo, optimize=True)
rj = REP / "definition" / "report.json"
dj = json.loads(rj.read_text(encoding="utf-8"))
pk = next(x for x in dj["resourcePackages"] if x["name"] == "RegisteredResources")
if novo not in {i["name"] for i in pk["items"]}:
    pk["items"].append({"name": novo, "path": novo, "type": "Image"})
    pk["items"].sort(key=lambda i: i["name"].lower())
rj.write_text(json.dumps(dj, ensure_ascii=False, indent=2), encoding="utf-8")
pj.write_text(pj.read_text(encoding="utf-8").replace(atual, novo), encoding="utf-8", newline="\n")
Image.fromarray(saida[y0 - 20:y1 + 20, 0:1600].astype(np.uint8)).save(Path(tempfile.gettempdir()) / "ranking_rotulo.png")
print(cont, "fundo:", atual, "->", novo, "rótulo antigo", caixa, "fim novo", fim)
