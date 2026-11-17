"""Quem contrata v2: refaz SÓ as duas páginas da aba (Todos os setores e AFL) no desenho do protótipo aprovado.

Não usa pagina_rais.py nem modelo_base.py de propósito: os dois regravam o projeto inteiro e apagariam os ajustes manuais já
salvos nas outras páginas. Este script mexe apenas em:
  - tables/_medidas.tmdl (acrescenta/atualiza as medidas Ct_*, KPI_Ct_*, Titulo_Ct_*, Manchete_Ct_*, Tip_Ct_*),
  - seis tabelas locais desconectadas D_Ct_* (botões) + model.tmdl (refs),
  - páginas a3d1f2c4e6b8097a1c41 e ...c42, seus fundos e três páginas de tooltip (c81, c82, c83).
Idempotente: pode ser rodado de novo. Nada é enviado ao Git.
"""
import copy
import datetime
import json
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import dax_contrata2
import fundo_rais as fb
import pbir_rais as pb
from texto_path import texto

RAIZ = Path(__file__).resolve().parents[1]
DEF_MODELO = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition"
TAB = DEF_MODELO / "tables"
RECURSOS = pb.REPORT / "StaticResources" / "RegisteredResources"
LARANJA, ROXO, GRAFITE = "#F58220", "#7F56D9", "#434446"
FMT_VALOR = '[<=1]0.0%;"R$ "#,0'
ID = {"Todos os setores": "a3d1f2c4e6b8097a1c41", "AFL": "a3d1f2c4e6b8097a1c42"}
TIP = {"Mul": "a3d1f2c4e6b8097a1c81", "Neg": "a3d1f2c4e6b8097a1c82", "Esc": "a3d1f2c4e6b8097a1c83"}
NOTA_QUEBRA = ("A RAIS passou a vir do eSocial em 2022 e incluiu empregos de empresas pequenas que ficavam de fora: "
               "2022 em diante não se compara com os anos anteriores.")
NOTA = {"Todos os setores": ("Valores nominais, remuneração média de dezembro. Percentual de negros sobre quem declarou cor. "
                             "Divisões com menos de 50 mil empregos ficam fora do ranking. " + NOTA_QUEBRA),
        "AFL": "Valores nominais, remuneração média de dezembro. Percentual de negros sobre quem declarou cor. " + NOTA_QUEBRA}

# ------------------------------------------------------------------ tabelas locais dos botões
TABELAS = {
    "D_Ct_Modo": ("modo", [("10 melhores setores", "1"), ("10 piores setores", "2")]),
    "D_Ct_Setor": ("setor", [("Agropecuária", "1"), ("Comércio", "2"), ("Construção", "3"), ("Indústria", "4"), ("Serviços", "5")]),
    "D_Ct_MetMul": ("metrica", [("Representatividade", "1"), ("Salário médio", "2")]),
    "D_Ct_MetNeg": ("metrica", [("Representatividade", "1"), ("Salário médio", "2")]),
    "D_Ct_MetEsc": ("metrica", [("Representatividade", "1"), ("Salário médio", "2")]),
    "D_Ct_Nivel": ("nivel", [("Até fundamental", "1"), ("Médio incompleto", "2"), ("Médio completo", "3"), ("Superior", "4")]),
}


def _crlf(t, original):
    return t.replace("\n", "\r\n") if "\r\n" in original else t


def tabela_tmdl(nome, col, linhas):
    arq = TAB / f"{nome}.tmdl"
    tags = {}
    if arq.exists():
        t = arq.read_text(encoding="utf-8")
        tags = {m.group(1): m.group(2) for m in re.finditer(r"\tcolumn (\w+)\n(?:.*\n)*?\t\tlineageTag: ([0-9a-f-]+)", t)}
        tag_tab = re.search(r"^\tlineageTag: ([0-9a-f-]+)", t, re.M).group(1)
    else:
        tag_tab = str(uuid.uuid4())
    corpo = ", ".join("{" + ", ".join('"' + v + '"' for v in l) + "}" for l in linhas)
    L = [f"table {nome}", f"\tlineageTag: {tag_tab}", ""]
    for c in (col, "ordem"):
        L += [f"\tcolumn {c}", "\t\tdataType: string", f"\t\tlineageTag: {tags.get(c, str(uuid.uuid4()))}", "\t\tsummarizeBy: none", f"\t\tsourceColumn: {c}"]
        if c == col:
            L.append("\t\tsortByColumn: ordem")
        L += ["", "\t\tannotation SummarizationSetBy = Automatic", ""]
    L += [f"\tpartition {nome} = m", "\t\tmode: import", "\t\tsource =", "\t\t\t\tlet",
          f"\t\t\t\t    Fonte = #table(type table [{col} = text, ordem = text], {{{corpo}}})", "\t\t\t\tin", "\t\t\t\t    Fonte", "",
          "\tannotation PBI_ResultType = Table", ""]
    arq.write_text("\r\n".join(L), encoding="utf-8", newline="")


def registrar_tabelas():
    for nome, (col, linhas) in TABELAS.items():
        tabela_tmdl(nome, col, linhas)
    arq = DEF_MODELO / "model.tmdl"
    t = arq.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in t else "\n"
    for nome in TABELAS:
        if f"ref table {nome}{nl}" not in t:
            t = t.replace(f"ref table D_Info{nl}", f"ref table D_Info{nl}ref table {nome}{nl}", 1)
    m = re.search(r"annotation PBI_QueryOrder = (\[.*?\])", t)
    ordem = json.loads(m.group(1))
    for nome in TABELAS:
        if nome not in ordem:
            ordem.append(nome)
    t = t[:m.start(1)] + json.dumps(ordem, ensure_ascii=False, separators=(",", ":")) + t[m.end(1):]
    arq.write_text(t, encoding="utf-8", newline="")


# ------------------------------------------------------------------ medidas
def bloco_medida(nome, doc, dax, pasta, fmt, oculta, tag, dyn=None):
    L = [f"\t/// {doc}"]
    if "\n" in dax:
        L.append(f"\tmeasure {nome} =")
        L += ["\t\t\t" + l for l in dax.split("\n")]
    else:
        L.append(f"\tmeasure {nome} = {dax}")
    if fmt:
        L.append(f"\t\tformatString: {fmt}")
    if oculta:
        L.append("\t\tisHidden")
    L.append(f"\t\tdisplayFolder: {pasta}")
    L.append(f"\t\tlineageTag: {tag}")
    if dyn:        # formatStringDefinition é um objeto filho no TMDL: vem depois das propriedades, separado por linha em branco (como o Desktop grava)
        L.append("")
        L.append(f"\t\tformatStringDefinition = {dyn}")
    return "\n".join(L) + "\n\n"


def gravar_medidas():
    arq = TAB / "_medidas.tmdl"
    original = arq.read_bytes().decode("utf-8")     # bytes: read_text converteria CRLF e perderia o estilo do arquivo
    t = original.replace("\r\n", "\n")
    novas = dax_contrata2.medidas()
    nomes = [x[0] for x in novas]
    assert len(nomes) == len(set(nomes)), "medida duplicada"
    existentes = set(re.findall(r"^\tmeasure (\w+)", t, re.M))
    # nomes novos não podem colidir com medidas de outros módulos: só podem ser substituídas as nossas (prefixos Ct_)
    colisao = [n for n in nomes if n in existentes and not re.match(r"(Ct_|KPI_Ct_|Titulo_Ct_|Manchete_Ct_|Tip_Ct_)", n)]
    assert not colisao, f"colisão com medidas existentes: {colisao}"
    # remove, linha a linha, os blocos antigos das nossas medidas (doc, declaração, corpo, propriedades e objetos filhos)
    tags, saida, linhas, i, alvo = {}, [], t.split("\n"), 0, set(nomes)
    while i < len(linhas):
        m = re.match(r"^\tmeasure (\w+)", linhas[i])
        if m and m.group(1) in alvo:
            while saida and saida[-1].startswith("\t///"):
                saida.pop()
            i += 1
            # O Desktop grava objetos filhos (formatStringDefinition) depois de uma linha em branco: a linha em branco faz parte
            # do bloco enquanto a próxima linha não vazia ainda estiver mais indentada (2 tabs). Sem isso sobravam filhos soltos.
            while i < len(linhas):
                if linhas[i].startswith("\t\t"):
                    tg = re.match(r"\t\tlineageTag: ([0-9a-f-]+)", linhas[i])
                    if tg:
                        tags[m.group(1)] = tg.group(1)
                    i += 1
                elif linhas[i] == "":
                    k = i
                    while k < len(linhas) and linhas[k] == "":
                        k += 1
                    if k < len(linhas) and linhas[k].startswith("\t\t"):
                        i = k
                    else:
                        i = k                     # engole as linhas em branco depois do bloco (evita acumular vazios a cada regravação)
                        break
                else:
                    break
            continue
        saida.append(linhas[i])
        i += 1
    t = "\n".join(saida)
    ponto = t.index("\tcolumn Coluna\n")
    blocos = "".join(bloco_medida(n, d, x, p, f, o, tags.get(n, str(uuid.uuid4())), y) for n, d, x, p, f, o, y in novas)
    t = t[:ponto] + blocos + t[ponto:]
    conferir_formato_dinamico(t, set(nomes))
    arq.write_bytes(_crlf(t, original).encode("utf-8"))
    return len(novas)


def conferir_formato_dinamico(t, meus):
    """formatStringDefinition só pode existir 1 vez por medida e só nas nossas (o Desktop recusa o projeto se sobrar linha solta)."""
    atual, cont = None, {}
    for l in t.split("\n"):
        m = re.match(r"^\tmeasure (\w+)", l)
        if m:
            atual = m.group(1)
        elif l.startswith("\t\tformatStringDefinition"):
            cont[atual] = cont.get(atual, 0) + 1
    ruins = {k: v for k, v in cont.items() if v > 1 or k not in meus}
    assert not ruins, f"formatStringDefinition fora do lugar: {ruins}"


# ------------------------------------------------------------------ geometria
def layout(todos):
    """Posições (px) de cada bloco da página."""
    L = {"todos": todos}
    L["linhaA"], L["linhaB"] = 304, 364
    L["kpi_y"] = 436 if todos else 312
    L["kpi_h"] = 190
    L["card_y"] = L["kpi_y"] + L["kpi_h"] + 24
    L["card_h"] = 540            # mesma altura dos cards nas duas versões
    L["esc_y"] = L["card_y"] + L["card_h"] + 24
    L["esc_h"] = 580
    L["nota_y"] = L["esc_y"] + L["esc_h"] + 24
    L["H"] = L["nota_y"] + fb.NOTA_H + 24
    L["modo"] = (270, L["linhaA"], 420)           # x, y, largura (2 botões de 210)
    L["setor"] = (270, L["linhaB"], 850)          # 5 botões de 170
    return L


def caixas_filtro(todos):
    itens = [("Ano", 140), ("Setores" if todos else "CNAE AFL", 360), ("Localização", None), ("Sexo", None), ("Escolaridade", None), ("Raça/cor", None), ("Contrato", None)]
    resto = (fb.W - 2 * fb.M - (len(itens) - 1) * fb.G - sum(w for _, w in itens if w)) / sum(1 for _, w in itens if not w)
    x, pos = fb.M, {}
    for nome, w in itens:
        w = w or resto
        pos[nome] = (round(x, 1), round(w, 1))
        x += w + fb.G
    return pos


def cards_geom(L):
    """(x, y, w, h) dos cards de ranking e do card de escolaridade."""
    mul = (fb.cx(0), L["card_y"], fb.cw(6), L["card_h"])
    neg = (fb.cx(6), L["card_y"], fb.cw(6), L["card_h"])
    esc = (fb.cx(0), L["esc_y"], fb.cw(12), L["esc_h"])
    return {"Mul": mul, "Neg": neg, "Esc": esc}


MET_W, NIVEL_W = 340, 680


def trilhos(L):
    """Posições (x, y, w, nº de botões) dos botões de cada card."""
    g = cards_geom(L)
    t = {}
    for p in ("Mul", "Neg"):
        x, y, w, h = g[p]
        t["met_" + p] = (x + w - 24 - MET_W, y + 20, MET_W, 2)
    x, y, w, h = g["Esc"]
    t["nivel"] = (x + w - 24 - NIVEL_W, y + 16, NIVEL_W, 4)
    t["met_Esc"] = (x + w - 24 - MET_W, y + 72, MET_W, 2)
    if L["todos"]:
        t["modo"] = (*L["modo"], 2)
        t["setor"] = (*L["setor"], 5)
    return t


# ------------------------------------------------------------------ fundo (SVG → PNG)
def card_acento_esq(x, y, w, h, cor, idx):
    s = fb.card(x, y, w, h)
    s.append(f'<clipPath id="kc{idx}"><rect x="{fb.R(x) + .5}" y="{fb.R(y) + .5}" width="{fb.R(w) - 1}" height="{fb.R(h) - 1}" rx="8"/></clipPath>')
    s.append(f'<rect x="{fb.R(x)}" y="{fb.R(y)}" width="5" height="{fb.R(h)}" fill="{cor}" clip-path="url(#kc{idx})"/>')
    return s


def svg_fundo(L, t=None):
    """t = posições (x, y, largura, nº de botões) dos trilhos; por padrão as do layout original, mas o fundo deve seguir as dos visuais salvos."""
    todos = L["todos"]
    fb.TEMAS = ["Empregos", "Quem trabalha", "Quanto ganha", "Ranking"]      # a aba "Quem contrata" passou a se chamar "Ranking"
    s = [fb.navegacao("Ranking", "Todos os setores" if todos else "AFL")]
    for nome, (x, w) in caixas_filtro(todos).items():
        s.append([texto(nome, x, fb.FL_ROT, fb.PT(18), fb.K["tinta2"], 600),
                  f'<rect x="{fb.R(x) + .5}" y="{fb.FL_Y + .5}" width="{fb.R(w) - 1}" height="{fb.FL_H - 1}" rx="4" fill="{fb.K["card"]}" stroke="{fb.K["borda"]}"/>'])
    t = t or trilhos(L)
    if todos:
        s.append([texto("Ranking dos setores", fb.M, t["modo"][1] + 32, 22, fb.K["tinta"], 600),
                  texto("AFL não entra neste cálculo.", t["modo"][0] + t["modo"][2] + 24, t["modo"][1] + 31, 20, fb.K["tinta2"], 400),
                  texto("Setor selecionado", fb.M, t["setor"][1] + 32, 22, fb.K["tinta"], 600)])
        s.append(fb.trilho_setores(*t["modo"][:3], n=2))
        s.append(fb.trilho_setores(*t["setor"][:3], n=5))
    for i, (x, cor) in enumerate(zip((fb.cx(0), fb.cx(4), fb.cx(8)), (ROXO, GRAFITE, LARANJA))):
        s.append(card_acento_esq(x, L["kpi_y"], fb.cw(4), L["kpi_h"], cor, i))
    for p, (x, y, w, h) in cards_geom(L).items():
        s.append(fb.card(x, y, w, h))
    for k in ("met_Mul", "met_Neg", "nivel", "met_Esc"):
        s.append(fb.trilho_setores(*t[k][:3], n=t[k][3]))
    fb.NOTA_Y = L["nota_y"]            # fb.nota() lê a posição da nota deste módulo
    s.append(fb.nota(NOTA["Todos os setores" if todos else "AFL"]))
    plano = [e for grupo in s for e in (grupo if isinstance(grupo, list) else [grupo])]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fb.W} {L["H"]}" width="{fb.W}" height="{L["H"]}">\n{fb.DEFS}\n'
            f'<rect width="{fb.W}" height="{L["H"]}" fill="#FFFFFF"/>\n' + "\n".join(plano) + "\n</svg>\n")


def gravar_fundo(L, nome, t=None):
    fb.SAIDA.mkdir(parents=True, exist_ok=True)
    arq = fb.SAIDA / f"{nome}-bg.svg"
    arq.write_text(svg_fundo(L, t), encoding="utf-8")
    png = fb.SAIDA / f"{nome}-bg.png"
    subprocess.run([fb.EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2", f"--screenshot={png}",
                    f"--window-size={fb.W},{L['H']}", arq.as_uri()], capture_output=True, check=True)
    return png


def registrar_fundo(png, nome):
    """Copia o PNG com nome novo (o Desktop cacheia pelo nome) e registra no report.json."""
    arq = f"{nome}-bg{datetime.datetime.now():%Y%m%d%H%M}.png"
    shutil.copyfile(png, RECURSOS / arq)
    rj = pb.DEF / "report.json"
    d = json.loads(rj.read_text(encoding="utf-8"))
    pacote = next(p for p in d["resourcePackages"] if p["name"] == "RegisteredResources")
    if arq not in {i["name"] for i in pacote["items"]}:
        pacote["items"].append({"name": arq, "path": arq, "type": "Image"})
        pacote["items"].sort(key=lambda i: i["name"].lower())
    rj.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return arq


# ------------------------------------------------------------------ páginas
def preservados(pasta):
    """Visuais que continuam como estão (abas, faixa de leitura, limpar filtros, segmentadores): devolve {nome: json}."""
    manter = {}
    for d in pasta.iterdir():
        v = json.loads((d / "visual.json").read_text(encoding="utf-8"))
        tipo, pos = v["visual"]["visualType"], v["position"]
        proj = [p["queryRef"] for p in v["visual"].get("query", {}).get("queryState", {}).get("Values", {}).get("projections", [])]
        if tipo in ("actionButton", "image") or (pos["y"] == 0 and pos["height"] == 30):
            manter[d.name] = v
        elif tipo == "slicer" and proj and proj[0] in FILTROS:
            manter[d.name] = v
    return manter


FILTROS = {"D_Calendario.Ano": "Ano", "D_Comparavel.comparavel_AFL_rotulo": "Setores", "D_AflAtividade.nome": "CNAE AFL", "D_UF.estado": "Localização",
           "D_Sexo.sexo": "Sexo", "D_Escolaridade.escolaridade_agrupada": "Escolaridade", "D_Raca.raca_cor": "Raça/cor", "F_rais.modalidade_contrato": "Contrato"}


def montar_pagina(recorte):
    todos = recorte == "Todos os setores"
    pid = ID[recorte]
    pasta = pb.DEF / "pages" / pid
    L = layout(todos)
    sufixo = "todos" if todos else "afl"
    manter = preservados(pasta / "visuals")
    # apaga o que não é preservado
    for d in (pasta / "visuals").iterdir():
        if d.name not in manter:
            shutil.rmtree(d)
    caixas = caixas_filtro(todos)
    for nome, v in manter.items():
        proj = v["visual"]["query"]["queryState"]["Values"]["projections"][0]["queryRef"] if v["visual"]["visualType"] == "slicer" else None
        if proj:
            x, w = caixas[FILTROS[proj]]
            if FILTROS[proj] == "Setores":
                v["position"].update({"x": x, "width": w, "y": 136, "height": 48})
            else:
                v["position"].update({"x": x - 4, "width": w + 8, "y": 132, "height": 52})
        pb.salvar(pasta / "visuals" / nome / "visual.json", v)
    z = [1000]

    def prox():
        z[0] += 100
        return z[0]

    def n(papel):
        return pb.nome_visual(pid, "ct2_" + papel)

    def gravar(papel, v):
        pb.salvar(pasta / "visuals" / v["name"] / "visual.json", v)

    u = "Total" if todos else "AFL"
    gravar("manchete", pb.html(n("manchete"), (fb.M, 196, fb.W - 2 * fb.M, 92, prox()), f"Manchete_Ct_{u}_HTML"))
    t = trilhos(L)
    if todos:
        gravar("modo", pb.botoes_setor(n("modo"), (*t["modo"][:3], 48, prox()), "D_Ct_Modo", "modo", n=2, inicial="10 melhores setores", fonte=16))
        gravar("setor", pb.botoes_setor(n("setor"), (*t["setor"][:3], 48, prox()), "D_Ct_Setor", "setor", n=5, inicial="Serviços", fonte=16))
    # KPIs
    for i, m in enumerate((f"KPI_Ct_Mul_{u}_HTML", f"KPI_Ct_Neg_{u}_HTML", f"KPI_Ct_Esc_{u}_HTML")):
        gravar(f"kpi{i}", pb.html(n(f"kpi{i}"), (fb.cx(4 * i) + 28, L["kpi_y"] + 9, fb.cw(4) - 52, 172, prox()), m))
    # cards de ranking
    g = cards_geom(L)
    for p in ("Mul", "Neg", "Esc"):
        x, y, w, h = g[p]
        met = t["met_" + p]
        gravar("met_" + p, pb.botoes_setor(n("met_" + p), (*met[:3], 48, prox()), f"D_Ct_Met{p}", "metrica", n=2, inicial="Representatividade", fonte=16))
        if p == "Esc":
            niv = t["nivel"]
            gravar("nivel", pb.botoes_setor(n("nivel"), (*niv[:3], 48, prox()), "D_Ct_Nivel", "nivel", n=4, inicial="Médio completo", fonte=16))
            larg_titulo, topo = w - 48 - NIVEL_W - 24, 136
        else:
            larg_titulo, topo = w - 48 - MET_W - 16, 124
        gravar("t_" + p, pb.html(n("t_" + p), (x + 24, y + 16, larg_titulo, 100, prox()), f"Titulo_Ct_{p}_{u}_HTML"))
        pos = (x + 16, y + topo, w - 32, h - topo - 16, prox())
        if todos:
            v = pb.barras(n("ch_" + p), pos, pb.coluna("D_Rank_Divisao", "nm_divisao"), f"Ct_{p}_Valor", "Valor", None, cor_por_medida="Cor_Ind_Divisao",
                          tooltips=[(f"Ct_{p}_Ord", "Ordem", "0.0000")], foco=True, espaco=10, fonte=16)
            v["visual"]["query"]["sortDefinition"] = {"sort": [{"field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_medidas"}}, "Property": f"Ct_{p}_Ord"}},
                                                                 "direction": "Descending"}]}
        else:
            v = pb.barras(n("ch_" + p), pos, pb.coluna("D_AflAtividade", "nome"), f"Ct_{p}_Valor_AFL", "Valor", None, cor_fixa=LARANJA, espaco=14, fonte=16)
        v["visual"]["visualContainerObjects"]["visualTooltip"] = [{"properties": {"section": pb.lit(f"'{TIP[p]}'"), "type": pb.lit("'Canvas'"), "show": pb.lit("true")}}]
        gravar("ch_" + p, v)
    # página
    pg = json.loads((pasta / "page.json").read_text(encoding="utf-8"))
    png = gravar_fundo(L, f"contrata-{sufixo}")
    arq = registrar_fundo(png, f"contrata-{sufixo}")
    pg["height"] = L["H"]
    img = pg["objects"]["background"][0]["properties"]["image"]["image"]
    img["name"]["expr"]["Literal"]["Value"] = f"'{arq}'"
    img["url"]["expr"]["ResourcePackageItem"]["ItemName"] = arq
    pg.pop("visualInteractions", None)
    pb.salvar(pasta / "page.json", pg)
    print(recorte, pid, "visuais:", len(list((pasta / "visuals").iterdir())), "· fundo", arq, "· altura", L["H"])


def paginas_tooltip():
    nomes = {"Mul": "mulheres", "Neg": "negros", "Esc": "escolaridade"}
    for p, pid in TIP.items():
        destino = pb.DEF / "pages" / pid
        if destino.exists():
            shutil.rmtree(destino)
        pagina, vis, v = pb.pagina_tooltip(pid, f"Tooltip · Quem contrata · {nomes[p]}", f"Tip_Ct_{p}_HTML", 640, 400)
        pb.salvar(destino / "page.json", pagina)
        pb.salvar(destino / "visuals" / v / "visual.json", vis)
    pj = pb.DEF / "pages" / "pages.json"
    d = json.loads(pj.read_text(encoding="utf-8"))
    for pid in TIP.values():
        if pid not in d["pageOrder"]:
            d["pageOrder"].append(pid)
    pj.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


PAPEIS = ["manchete", "modo", "setor", "kpi0", "kpi1", "kpi2", "met_Mul", "met_Neg", "met_Esc", "nivel", "t_Mul", "t_Neg", "t_Esc", "ch_Mul", "ch_Neg", "ch_Esc"]
N_BOTOES = {"modo": 2, "setor": 5, "met_Mul": 2, "met_Neg": 2, "met_Esc": 2, "nivel": 4}


def _arq_visual(pid, papel):
    return pb.DEF / "pages" / pid / "visuals" / pb.nome_visual(pid, "ct2_" + papel) / "visual.json"


def ler_posicoes(pid):
    """{papel: (x, y, w, h)} salvo nos visuais da página (inclui o que foi movido à mão no Desktop)."""
    out = {}
    for papel in PAPEIS:
        arq = _arq_visual(pid, papel)
        if arq.exists():
            p = json.loads(arq.read_text(encoding="utf-8"))["position"]
            out[papel] = (p["x"], p["y"], p["width"], p["height"])
    return out


def _origem(papel, L):
    g = cards_geom(L)
    if papel.startswith("kpi"):
        return fb.cx(4 * int(papel[3])), L["kpi_y"]
    for p in ("Mul", "Neg", "Esc"):
        if papel.endswith("_" + p) or (p == "Esc" and papel == "nivel"):
            return g[p][0], g[p][1]
    return 0, 0


def trilhos_salvos(pid):
    """Posições dos botões como estão nos visuais salvos (o fundo desenha a borda exatamente aí)."""
    pos = ler_posicoes(pid)
    return {k: (round(pos[k][0], 1), round(pos[k][1], 1), round(pos[k][2], 1), n) for k, n in N_BOTOES.items() if k in pos}


def barras_laranja_afl():
    """Barras dos CNAEs do AFL em laranja. O seletor por 'metadata' não pegou no Desktop (barras saíam pretas); o curinga de ponto de dados pega."""
    for papel in ("ch_Mul", "ch_Neg", "ch_Esc"):
        arq = _arq_visual(ID["AFL"], papel)
        v = json.loads(arq.read_text(encoding="utf-8"))
        v["visual"]["objects"]["dataPoint"] = [{"properties": {"fill": pb.cor(LARANJA)}, "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}}]
        pb.salvar(arq, v)


def fonte_maior_escolaridade(tamanho=18):
    """Eixo e rótulos do gráfico do card de escolaridade em fonte maior (só mexe no tamanho; o resto do visual fica como está)."""
    for pid in ID.values():
        arq = _arq_visual(pid, "ch_Esc")
        v = json.loads(arq.read_text(encoding="utf-8"))
        for obj in ("categoryAxis", "labels"):
            for item in v["visual"]["objects"].get(obj, []):
                if "fontSize" in item["properties"]:
                    item["properties"]["fontSize"] = pb.lit(f"{tamanho}D")
        pb.salvar(arq, v)


def sem_formato_fixo(pid):
    """Tira o formato fixo dos gráficos de ranking: quem formata o rótulo é o formato dinâmico da medida (% ou R$ conforme o botão)."""
    for papel in ("ch_Mul", "ch_Neg", "ch_Esc"):
        arq = _arq_visual(pid, papel)
        v = json.loads(arq.read_text(encoding="utf-8"))
        for proj in v["visual"]["query"]["queryState"]["Y"]["projections"]:
            proj.pop("format", None)
        pb.salvar(arq, v)


def replicar_no_afl():
    """Aplica na página AFL as mesmas mudanças de posição/tamanho feitas à mão em Todos os setores (relativas a cada card)."""
    Lt, La = layout(True), layout(False)
    todos = ler_posicoes(ID["Todos os setores"])
    pid_a = ID["AFL"]
    for papel, (x, y, w, h) in todos.items():
        if papel in ("modo", "setor"):
            continue                                  # só existem em Todos os setores
        ox, oy = _origem(papel, Lt)
        ax, ay = _origem(papel, La)
        nx, ny = ax + (x - ox), ay + (y - oy)
        if papel.startswith("ch_"):                   # o gráfico vai até 16 px do fim do card, como em Todos os setores
            fim = (La["esc_y"] + La["esc_h"]) if papel == "ch_Esc" else (La["card_y"] + La["card_h"])
            h = fim - 16 - ny
        arq = _arq_visual(pid_a, papel)
        v = json.loads(arq.read_text(encoding="utf-8"))
        v["position"].update({"x": round(nx, 1), "y": round(ny, 1), "width": round(w, 1), "height": round(h, 1)})
        pb.salvar(arq, v)


def atualizar_fundo(recorte):
    pid = ID[recorte]
    todos = recorte == "Todos os setores"
    L = layout(todos)
    pj = pb.DEF / "pages" / pid / "page.json"
    pg = json.loads(pj.read_text(encoding="utf-8"))
    if todos:
        L["H"] = pg["height"]                         # respeita a altura que está salva na página
    nome = "contrata-" + ("todos" if todos else "afl")
    png = gravar_fundo(L, nome, trilhos_salvos(pid))
    arq = registrar_fundo(png, nome)
    pg["height"] = L["H"]
    img = pg["objects"]["background"][0]["properties"]["image"]["image"]
    img["name"]["expr"]["Literal"]["Value"] = f"'{arq}'"
    img["url"]["expr"]["ResourcePackageItem"]["ItemName"] = arq
    pb.salvar(pj, pg)
    print(recorte, "fundo", arq, "· altura", L["H"])


def ajustar():
    """Fluxo padrão depois que a página foi ajustada à mão: não recria visuais; atualiza medidas, replica posições no AFL e redesenha as bordas."""
    print(gravar_medidas(), "medidas gravadas em _medidas.tmdl")
    replicar_no_afl()
    barras_laranja_afl()
    fonte_maior_escolaridade()
    for pid in ID.values():
        sem_formato_fixo(pid)
    for recorte in ID:
        atualizar_fundo(recorte)


def main():
    if "--so-medidas" in sys.argv:
        print(gravar_medidas(), "medidas gravadas em _medidas.tmdl")
        return
    if "--recriar" not in sys.argv:
        ajustar()
        return
    # recria TUDO do zero (descarta posições ajustadas à mão): só use no começo
    print(registrar_tabelas() or "tabelas locais gravadas")
    print(gravar_medidas(), "medidas gravadas em _medidas.tmdl")
    for recorte in ID:
        montar_pagina(recorte)
    barras_laranja_afl()
    paginas_tooltip()
    print("tooltips:", ", ".join(TIP.values()))


if __name__ == "__main__":
    main()
