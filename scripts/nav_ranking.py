"""Renomeia a aba "Quem contrata" para "Ranking" em todas as páginas e ajusta os botões de navegação.

Os fundos das páginas Empregos, Quem trabalha e Quanto ganha foram ajustados à mão depois de gerados, então NÃO são regerados:
só a faixa de abas (primeiros 96 px) é redesenhada e colada no PNG já registrado (com nome novo, por causa do cache do Desktop).
As páginas de Ranking (c41/c42) usam contrata_v2.py, que já desenha a aba com o novo nome.

Uso: python nav_ranking.py --testar   (compara a faixa desenhada com a dos PNGs atuais, sem alterar nada)
     python nav_ranking.py            (aplica)
"""
import datetime
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

import fundo_rais as fb
import pbir_rais as pb

ANTIGO = ["Empregos", "Quem trabalha", "Quanto ganha", "Quem contrata"]
NOVO = ["Empregos", "Quem trabalha", "Quanto ganha", "Ranking"]
PAGINAS = {("Empregos", "Todos os setores"): "a3d1f2c4e6b8097a1c11", ("Empregos", "AFL"): "a3d1f2c4e6b8097a1c12",
           ("Quem trabalha", "Todos os setores"): "a3d1f2c4e6b8097a1c21", ("Quem trabalha", "AFL"): "a3d1f2c4e6b8097a1c22",
           ("Quanto ganha", "Todos os setores"): "a3d1f2c4e6b8097a1c31", ("Quanto ganha", "AFL"): "a3d1f2c4e6b8097a1c32",
           ("Quem contrata", "Todos os setores"): "a3d1f2c4e6b8097a1c41", ("Quem contrata", "AFL"): "a3d1f2c4e6b8097a1c42"}
ALTURA = 96            # px da faixa (as abas terminam em y=83; o rótulo dos filtros começa em y≈106)
RECURSOS = pb.REPORT / "StaticResources" / "RegisteredResources"


def faixa(tema, recorte, temas):
    """Faixa de abas (3840 × 192) desenhada pela mesma função do gerador original."""
    fb.TEMAS = temas
    plano = [e for e in fb.navegacao(tema, recorte)]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fb.W} {ALTURA}" width="{fb.W}" height="{ALTURA}">\n'
           f'<rect width="{fb.W}" height="{ALTURA}" fill="#FFFFFF"/>\n' + "\n".join(plano) + "\n</svg>\n")
    with tempfile.TemporaryDirectory() as d:
        arq, png = Path(d) / "faixa.svg", Path(d) / "faixa.png"
        arq.write_text(svg, encoding="utf-8")
        subprocess.run([fb.EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2", f"--screenshot={png}",
                        f"--window-size={fb.W},{ALTURA}", arq.as_uri()], capture_output=True, check=True)
        return Image.open(png).convert("RGB").copy()


def fundo_atual(pid):
    t = (pb.DEF / "pages" / pid / "page.json").read_text(encoding="utf-8")
    return re.search(r"'([^']+-bg\d+\.png)'", t).group(1)


def testar():
    for (tema, recorte), pid in PAGINAS.items():
        nome = fundo_atual(pid)
        atual = Image.open(RECURSOS / nome).convert("RGB").crop((0, 0, fb.W * 2, ALTURA * 2))
        ref = faixa(tema, recorte, ANTIGO)
        dif = ImageChops.difference(atual, ref).convert("L").point(lambda v: 255 if v > 40 else 0)
        print(f"{tema:<14} {recorte:<17} {nome:<40} pixels diferentes: {sum(1 for p in dif.getdata() if p)}")


def registrar(arq):
    rj = pb.DEF / "report.json"
    d = json.loads(rj.read_text(encoding="utf-8"))
    pacote = next(p for p in d["resourcePackages"] if p["name"] == "RegisteredResources")
    if arq not in {i["name"] for i in pacote["items"]}:
        pacote["items"].append({"name": arq, "path": arq, "type": "Image"})
        pacote["items"].sort(key=lambda i: i["name"].lower())
    rj.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def aplicar_fundos():
    carimbo = datetime.datetime.now().strftime("%Y%m%d%H%M")
    for (tema, recorte), pid in PAGINAS.items():
        if tema == "Quem contrata":
            continue                                   # as páginas de Ranking são refeitas por contrata_v2.py
        nome = fundo_atual(pid)
        img = Image.open(RECURSOS / nome).convert("RGB")
        img.paste(faixa(tema, recorte, NOVO), (0, 0))
        novo = re.sub(r"\d+\.png$", f"{carimbo}.png", nome)
        img.save(RECURSOS / novo, optimize=True)
        pj = pb.DEF / "pages" / pid / "page.json"
        t = pj.read_text(encoding="utf-8").replace(nome, novo)
        pj.write_text(t, encoding="utf-8")
        registrar(novo)
        print(pid, nome, "->", novo)


def botoes():
    """Texto dos botões de navegação (hover e press) e alt text: "Quem contrata" vira "Ranking"; o estado pressionado deixa de ser escuro."""
    laranja = pb.cor("#F58220")
    alterados = 0
    for pid in PAGINAS.values():
        for arq in (pb.DEF / "pages" / pid / "visuals").glob("*/visual.json"):
            v = json.loads(arq.read_text(encoding="utf-8"))
            if v["visual"]["visualType"] != "actionButton":
                continue
            link = v["visual"].get("visualContainerObjects", {}).get("visualLink", [{}])[0].get("properties", {})
            if "PageNavigation" not in json.dumps(link):
                continue                                # só os botões de abas (a faixa de informações tem outro papel)
            txt = arq.read_text(encoding="utf-8")
            txt = txt.replace("'Quem contrata'", "'Ranking'").replace("Ir para Quem contrata", "Ir para Ranking")
            v = json.loads(txt)
            obj = v["visual"]["objects"]
            for item in obj.get("fill", []):
                if item.get("selector", {}).get("id") == "press":
                    item["properties"]["fillColor"] = laranja               # antes #B86218 (marrom escuro)
            # Estado "selected": o botão fica selecionado no instante do clique, antes de a página trocar. Sem estilo para ele o Power BI
            # usa o padrão escuro (era o "preto" depois do clique). Os botões do RF já definem esse estado em laranja.
            obj["text"] = [i for i in obj["text"] if not (i.get("selector", {}).get("id") == "default" and i["properties"].get("show", {}).get("expr", {}).get("Literal", {}).get("Value") == "false")]
            obj["fill"] = [i for i in obj["fill"] if i.get("selector", {}).get("id") != "selected"]
            obj["fill"].append({"properties": {"fillColor": laranja, "transparency": pb.lit("0D")}, "selector": {"id": "selected"}})
            hover_txt = next(i for i in obj["text"] if i.get("selector", {}).get("id") == "hover")
            obj["text"] = [i for i in obj["text"] if i.get("selector", {}).get("id") != "selected"]
            obj["text"].append({"properties": json.loads(json.dumps(hover_txt["properties"])), "selector": {"id": "selected"}})
            pb.salvar(arq, v)
            alterados += 1
    print(alterados, "botões de navegação ajustados")


def nomes_internos():
    """displayName das páginas e dos tooltips (só aparece no editor)."""
    for pid in ("a3d1f2c4e6b8097a1c41", "a3d1f2c4e6b8097a1c42", "a3d1f2c4e6b8097a1c81", "a3d1f2c4e6b8097a1c82", "a3d1f2c4e6b8097a1c83"):
        pj = pb.DEF / "pages" / pid / "page.json"
        t = pj.read_text(encoding="utf-8")
        n = t.replace("Quem contrata ·", "Ranking ·").replace("Tooltip · Quem contrata", "Tooltip · Ranking")
        if n != t:
            pj.write_text(n, encoding="utf-8")


if __name__ == "__main__":
    if "--testar" in sys.argv:
        testar()
    else:
        aplicar_fundos()
        botoes()
        nomes_internos()
