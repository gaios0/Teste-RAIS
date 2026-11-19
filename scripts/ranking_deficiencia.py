# -*- coding: utf-8 -*-
"""Ranking por deficiência nas páginas Ranking (Todos os setores e AFL), igual ao ranking de escolaridade.

- Tabelas de botão: D_Ct_Def (Física, Auditiva, Visual, Intelectual, Múltipla, Reabilitado) e D_Ct_MetDef
  (Representatividade | Salário médio).
- Medidas Ct_Def_* copiadas das Ct_Esc_*, com o filtro F_rais[tipo_deficiencia] no lugar da escolaridade.
- Visuais: título, botões de métrica e de tipo e gráfico, copiados do bloco de escolaridade e postos logo abaixo.
- Tooltip: página nova (cópia da Dica do ranking de escolaridade) com Tip_Ct_Def_HTML.
- Página 603 px mais alta; o fundo ganha um cartão igual ao da escolaridade, com 6 caixas de botão.
"""
import copy
import datetime
import json
import re
import uuid
from pathlib import Path

import numpy as np
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
SM = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition"
REP = RAIZ / "RAIS Emprego Formal.Report"
PAGES = REP / "definition" / "pages"
RECURSOS = REP / "StaticResources" / "RegisteredResources"
MED = SM / "tables" / "_medidas.tmdl"

TIPOS = ["Física", "Auditiva", "Visual", "Intelectual", "Múltipla", "Reabilitado"]
GAP = 36                    # px (2x) entre o cartão de escolaridade e o novo
DESLOC = None               # px (1x), calculado pelo tamanho do cartão
TIP_ESC = "a3d1f2c4e6b8097a1c83"
TIP_DEF = "a3d1f2c4e6b8097a1c84"
PAGINAS = {
    "a3d1f2c4e6b8097a1c41": {"bloco": ["258e64cb8dd615900fa7", "fff52f52fa8d255d1168", "d6fa105d5eb65c9d58f9", "f92aadf28ecec02e1212"],
                             "nivel": "d6fa105d5eb65c9d58f9", "cartao": (2428, 3597)},
    "a3d1f2c4e6b8097a1c42": {"bloco": ["aa8cea2b410b41c34648", "0912d5e6645f7d26d1af", "e1580b685112322cc23e", "9a06c45be25765da0c06"],
                             "nivel": "e1580b685112322cc23e", "cartao": (2180, 3349)},
}


def tag():
    return str(uuid.uuid4())


def nome_visual():
    return uuid.uuid4().hex[:20]


# ---------------------------------------------------------------- tabelas de botão
def tabela(nome, col, valores):
    linhas = ", ".join('{"%s", "%d"}' % (v, i) for i, v in enumerate(valores, 1))
    return f"""table {nome}
	lineageTag: {tag()}

	column {col}
		dataType: string
		lineageTag: {tag()}
		summarizeBy: none
		sourceColumn: {col}
		sortByColumn: ordem

		annotation SummarizationSetBy = Automatic

	column ordem
		dataType: string
		isHidden
		lineageTag: {tag()}
		summarizeBy: none
		sourceColumn: ordem

		annotation SummarizationSetBy = Automatic

	partition {nome} = m
		mode: import
		source =
				let
				    Fonte = #table(type table [{col} = text, ordem = text], {{{linhas}}})
				in
				    Fonte

	annotation PBI_ResultType = Table

"""


def tabelas():
    (SM / "tables" / "D_Ct_Def.tmdl").write_text(tabela("D_Ct_Def", "tipo", TIPOS), encoding="utf-8", newline="\n")
    (SM / "tables" / "D_Ct_MetDef.tmdl").write_text(tabela("D_Ct_MetDef", "metrica", ["Representatividade", "Salário médio"]), encoding="utf-8", newline="\n")
    m = (SM / "model.tmdl").read_text(encoding="utf-8")
    for n in ("D_Ct_Def", "D_Ct_MetDef"):
        if f"ref table {n}\n" not in m + "\n":
            m = m.replace("ref table D_Ct_Modo", f"ref table D_Ct_Modo\nref table {n}")
            m = m.replace('"D_Ct_Nivel",', f'"D_Ct_Nivel","{n}",')
    (SM / "model.tmdl").write_text(m, encoding="utf-8", newline="")


# ---------------------------------------------------------------- medidas
ANO = "REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A"
NOME_TIPO = ('SWITCH(SELECTEDVALUE(D_Ct_Def[tipo]), "Física", "física", "Auditiva", "auditiva", "Visual", "visual", '
             '"Intelectual", "intelectual", "Múltipla", "múltipla", "Reabilitado", "reabilitado", "todos os tipos")')
NOVAS = {
    "Ct_Def_Tipo": ("Valor de F_rais[tipo_deficiencia] do botão de tipo do ranking por deficiência (vazio quando nada está escolhido: soma todos os tipos).",
                    'VAR T = SELECTEDVALUE(D_Ct_Def[tipo])\nRETURN IF(T = "Intelectual", "Intelectual (Mental)", T)', None, "Quem contrata\\Perfil"),
    "Ct_Def_Qtd": ("Empregos em 31/12 do ano de referência com o tipo de deficiência escolhido, no contexto.",
                   f"VAR A = [Ano_Ref]\nVAR T = [Ct_Def_Tipo]\nRETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], {ANO}, KEEPFILTERS(FILTER(ALL(F_rais[tipo_deficiencia], F_rais[indicador_portador_deficiencia]), IF(ISBLANK(T), F_rais[indicador_portador_deficiencia] = "Sim", F_rais[tipo_deficiencia] = T)))))", "#,0", "Quem contrata\\Perfil"),
    "Ct_Def_Tot": ("Empregos em 31/12 do ano de referência que servem de denominador da representatividade por deficiência.",
                   f"VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], {ANO}))", "#,0", "Quem contrata\\Perfil"),
    "Ct_Def_Rep": ("Representatividade: participação do tipo de deficiência escolhido no total de empregos do contexto, em 31/12 do ano de referência.",
                   "DIVIDE([Ct_Def_Qtd], [Ct_Def_Tot])", "0.0%", "Quem contrata\\Perfil"),
    "Ct_Def_Sal": ("Salário médio de dezembro dos empregados com o tipo de deficiência escolhido, no contexto.",
                   f"VAR A = [Ano_Ref]\nVAR T = [Ct_Def_Tipo]\nRETURN IF(NOT ISBLANK(A), CALCULATE([Remuneracao_Media], {ANO}, KEEPFILTERS(FILTER(ALL(F_rais[tipo_deficiencia], F_rais[indicador_portador_deficiencia]), IF(ISBLANK(T), F_rais[indicador_portador_deficiencia] = "Sim", F_rais[tipo_deficiencia] = T)))))", "#,0.00", "Quem contrata\\Perfil"),
}


def bloco_medida(nome, desc, dax, fmt, pasta, hidden=True, fsd=None):
    corpo = "\n".join("\t\t\t" + l for l in dax.split("\n"))
    s = f"\t/// {desc}\n\tmeasure {nome} =\n{corpo}\n"
    if fmt:
        s += f"\t\tformatString: {fmt}\n"
    if hidden:
        s += "\t\tisHidden\n"
    s += f"\t\tdisplayFolder: {pasta}\n\t\tlineageTag: {tag()}\n"
    if fsd:
        s += f"\n\t\tformatStringDefinition = {fsd}\n"
    return s + "\n"


def bloco_de(t, nome):
    m = re.search(r"(?ms)^(\t///[^\n]*\n)*\tmeasure " + re.escape(nome) + r" =\n.*?(?=^\t(?:///|measure |column |partition ))", t)
    return m.group(0)


def copiar(t, nome_esc, nome_def, trocas):
    b = bloco_de(t, nome_esc)
    for a, n in trocas:
        b = b.replace(a, n)
    b = b.replace(f"measure {nome_esc} =", f"measure {nome_def} =")
    return re.sub(r"lineageTag: [0-9a-f-]+", lambda _: f"lineageTag: {tag()}", b)


def medidas():
    t = MED.read_text(encoding="utf-8")
    if "measure Ct_Def_Valor =" in t:
        print("medidas já existem")
        return
    novo = "".join(bloco_medida(n, *v) for n, v in NOVAS.items())
    base = [("Ct_Esc_", "Ct_Def_"), ("D_Ct_MetEsc", "D_Ct_MetDef"), ("nível de escolaridade escolhido", "tipo de deficiência escolhido")]
    for n in ("Div_Rep", "Div_Sal", "Div_Qtd", "Div_Tot", "Valor", "Ord", "Valor_AFL"):
        novo += copiar(t, f"Ct_Esc_{n}", f"Ct_Def_{n}", base).rstrip("\n") + "\n\n"
    tit = base + [('VAR Niv = COALESCE(SELECTEDVALUE(D_Ct_Nivel[nivel]), "Médio completo")\n', ""),
                  ('VAR NomeNivel = SWITCH(Niv, "Até fundamental", "até o fundamental completo", "Médio incompleto", "médio incompleto", "Superior", "superior (completo ou não)", "médio completo")',
                   f"VAR NomeTipo = {NOME_TIPO}"),
                  ("— escolaridade", "— deficiência"), ('"Nível: " & NomeNivel', '"Tipo: " & NomeTipo'),
                  ("dos empregados do nível em cada", "dos empregados com esse tipo de deficiência em cada"),
                  ("participação do nível no total", "participação do tipo no total"),
                  ("Título do ranking por escolaridade", "Título do ranking por deficiência"), ("botões de nível", "botões de tipo")]
    novo += copiar(t, "Titulo_Ct_Esc_Total_HTML", "Titulo_Ct_Def_Total_HTML", tit).rstrip("\n") + "\n\n"
    novo += copiar(t, "Titulo_Ct_Esc_AFL_HTML", "Titulo_Ct_Def_AFL_HTML", tit).rstrip("\n") + "\n\n"
    tip = base + [('VAR Niv = COALESCE(SELECTEDVALUE(D_Ct_Nivel[nivel]), "Médio completo")', f"VAR NomeTipo = {NOME_TIPO}"),
                  ('" · nível: " & SWITCH(Niv, "Até fundamental", "até o fundamental completo", "Médio incompleto", "médio incompleto", "Superior", "superior (completo ou não)", "médio completo")',
                   '" · deficiência: " & NomeTipo'),
                  ("Nível no total de empregos", "Tipo no total de empregos")]
    b = copiar(t, "Tip_Ct_Esc_HTML", "Tip_Ct_Def_HTML", tip)
    if "D_Ct_Nivel" in b or "Niv" in re.sub(r"Nivel_", "", b.split("RETURN")[1]):
        raise SystemExit("tooltip: sobrou referência ao nível")
    novo += b.rstrip("\n") + "\n\n"
    for n in ("Titulo_Ct_Def_Total_HTML", "Titulo_Ct_Def_AFL_HTML"):
        if "D_Ct_Nivel" in bloco_de(novo + "\tmeasure X =\n", n):
            raise SystemExit(f"{n}: sobrou referência ao nível")
    ancora = re.search(r"(?m)^\tpartition _medidas", t).start()
    t = t[:ancora] + novo + t[ancora:]
    MED.write_text(t, encoding="utf-8", newline="")
    print("medidas novas:", len(re.findall(r"(?m)^\tmeasure ", novo)))


# ---------------------------------------------------------------- fundo
def fundo_atual(pid):
    t = (PAGES / pid / "page.json").read_text(encoding="utf-8")
    return re.search(r"'([^']+-bg\d+\.png)'", t).group(1)


def novo_fundo(pid, cfg, carimbo):
    global DESLOC
    atual = fundo_atual(pid)
    a = np.asarray(Image.open(RECURSOS / atual).convert("RGB")).copy()
    y0, y1 = cfg["cartao"]
    cartao = a[y0:y1 + 1].copy()
    # caixa de botões de nível (4 caixas) -> 6 caixas
    nv = json.loads((PAGES / pid / "visuals" / cfg["nivel"] / "visual.json").read_text(encoding="utf-8"))["position"]
    ym = int(nv["y"] * 2 + 48) - y0
    linha = cartao[ym]
    escuros = np.where(linha.sum(axis=1) < 750)[0]
    x_esq, x_dir = 112, 3726
    div = [x for x in escuros if x_esq + 10 < x < x_dir - 10]
    larg = 3
    col = cartao[:, div[0]]
    ys = np.where(col[ym - 60:ym + 60].sum(axis=1) < 750)[0] + ym - 60
    top, bot = ys.min() + 1, ys.max()          # só o miolo (as bordas de cima e de baixo ficam)
    tira = cartao[top:bot, div[0]:div[0] + larg].copy()
    for x in sorted(set(div)):
        cartao[top:bot, x] = 255
    passo = (x_dir + 2 - x_esq) / 6
    for k in range(1, 6):
        x = int(round(x_esq + k * passo)) - 1
        cartao[top:bot, x:x + larg] = tira
    branco = np.full((GAP, a.shape[1], 3), 255, dtype=a.dtype)
    saida = np.vstack([a[:y1 + 1], branco, cartao, a[y1 + 1:]])
    DESLOC = (GAP + cartao.shape[0]) // 2
    novo = re.sub(r"\d+\.png$", f"{carimbo}.png", atual)
    Image.fromarray(saida.astype(np.uint8)).save(RECURSOS / novo, optimize=True)
    return atual, novo, saida.shape[0] // 2


def registrar(arq):
    rj = REP / "definition" / "report.json"
    d = json.loads(rj.read_text(encoding="utf-8"))
    pacote = next(p for p in d["resourcePackages"] if p["name"] == "RegisteredResources")
    if arq not in {i["name"] for i in pacote["items"]}:
        pacote["items"].append({"name": arq, "path": arq, "type": "Image"})
        pacote["items"].sort(key=lambda i: i["name"].lower())
    rj.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------- visuais
TROCAS_VIS = [('"Entity": "D_Ct_MetEsc"', '"Entity": "D_Ct_MetDef"'), ("D_Ct_MetEsc.", "D_Ct_MetDef."),
              ('"Entity": "D_Ct_Nivel"', '"Entity": "D_Ct_Def"'), ("D_Ct_Nivel.nivel", "D_Ct_Def.tipo"),
              ('"Property": "nivel"', '"Property": "tipo"'), ('"nativeQueryRef": "nivel"', '"nativeQueryRef": "tipo"'),
              ("'Médio incompleto'", "'Física'"), ("'Médio completo'", "'Física'"), ("'Superior'", "'Física'"), ("'Até fundamental'", "'Física'"),
              ("Ct_Esc_", "Ct_Def_"), ("Titulo_Ct_Esc_", "Titulo_Ct_Def_"), (TIP_ESC, TIP_DEF)]


def visuais(pid, cfg):
    mapa = {v: nome_visual() for v in cfg["bloco"]}
    for antigo, novo in mapa.items():
        txt = (PAGES / pid / "visuals" / antigo / "visual.json").read_text(encoding="utf-8")
        for a, b in TROCAS_VIS:
            txt = txt.replace(a, b)
        j = json.loads(txt)
        j["name"] = novo
        j["position"]["y"] = j["position"]["y"] + DESLOC
        j["position"]["z"] = j["position"]["z"] + 100
        j["position"]["tabOrder"] = j["position"].get("tabOrder", j["position"]["z"]) + 100
        sg = j.get("visual", {}).get("syncGroup")
        if sg:
            sg["groupName"] = sg["groupName"] + "_def"
        d = PAGES / pid / "visuals" / novo
        d.mkdir()
        (d / "visual.json").write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return mapa


def pagina(pid, mapa, atual, novo_bg, altura):
    pj = PAGES / pid / "page.json"
    j = json.loads(pj.read_text(encoding="utf-8"))
    j["height"] = altura
    txt = json.dumps(j, ensure_ascii=False, indent=2).replace(atual, novo_bg)
    j = json.loads(txt)
    inter = j.get("visualInteractions", [])
    extra = []
    for it in inter:
        if it["source"] in mapa or it["target"] in mapa:
            n = dict(it, source=mapa.get(it["source"], it["source"]), target=mapa.get(it["target"], it["target"]))
            extra.append(n)
    # os botões novos não filtram nada fora do bloco novo, como os de escolaridade
    j["visualInteractions"] = inter + [e for e in extra if e not in inter]
    pj.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return len(extra)


def tooltip():
    src, dst = PAGES / TIP_ESC, PAGES / TIP_DEF
    if dst.exists():
        return
    dst.mkdir()
    pj = json.loads((src / "page.json").read_text(encoding="utf-8"))
    pj["name"] = TIP_DEF
    pj["displayName"] = pj["displayName"].replace("escolaridade", "deficiência").replace("Escolaridade", "Deficiência")
    if pj["displayName"] == json.loads((src / "page.json").read_text(encoding="utf-8"))["displayName"]:
        pj["displayName"] += " (deficiência)"
    mapa = {}
    for v in (src / "visuals").iterdir():
        n = nome_visual()
        mapa[v.name] = n
        txt = (v / "visual.json").read_text(encoding="utf-8").replace("Tip_Ct_Esc_HTML", "Tip_Ct_Def_HTML")
        j = json.loads(txt)
        j["name"] = n
        (dst / "visuals" / n).mkdir(parents=True)
        (dst / "visuals" / n / "visual.json").write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    txt = json.dumps(pj, ensure_ascii=False, indent=2)
    for a, b in mapa.items():
        txt = txt.replace(a, b)
    (dst / "page.json").write_text(txt + "\n", encoding="utf-8", newline="\n")
    pp = PAGES / "pages.json"
    p = json.loads(pp.read_text(encoding="utf-8"))
    if TIP_DEF not in p["pageOrder"]:
        p["pageOrder"].insert(p["pageOrder"].index(TIP_ESC) + 1, TIP_DEF)
    pp.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    print("tooltip:", pj["displayName"])


if __name__ == "__main__":
    tabelas()
    medidas()
    tooltip()
    carimbo = datetime.datetime.now().strftime("%Y%m%d%H%M")
    for pid, cfg in PAGINAS.items():
        atual, novo_bg, altura = novo_fundo(pid, cfg, carimbo)
        registrar(novo_bg)
        mapa = visuais(pid, cfg)
        k = pagina(pid, mapa, atual, novo_bg, altura)
        print(f"{pid}: fundo {novo_bg}, altura {altura}, +{DESLOC}px, visuais {list(mapa.values())}, interações {k}")
