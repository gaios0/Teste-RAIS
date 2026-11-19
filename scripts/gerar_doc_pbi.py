# -*- coding: utf-8 -*-
"""Gera a documentação do painel RAIS (skill /pbi-doc): _docs/00..04 *.md + _docs/index.html.

Só lê o SemanticModel e o Report. Uso: python scripts/gerar_doc_pbi.py
"""
import html
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SM = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition"
REP = RAIZ / "RAIS Emprego Formal.Report" / "definition"
SKILL = RAIZ / ".kiro" / "skills" / "pbi-doc" / "templates"
OUT = RAIZ / "_docs"

PROJETO = "RAIS Emprego Formal"
ARQUIVO = "RAIS Emprego Formal.pbip"
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
HOJE = date.today()
TS = f"{HOJE.day} {MESES[HOJE.month - 1]} {HOJE.year}"
TAGLINE = ("Emprego formal no Brasil (RAIS/eSocial, 2009 em diante) com foco no AFL — alimentação fora do lar — "
           "comparado aos setores Comparáveis: quantos são, quem trabalha, quanto ganha e quem contrata.")

# Papel de cada tabela (escrito à mão a partir das colunas, das relações e do uso nas medidas).
INFO_TAB = {
    "F_rais": ("Fato", "Fato principal: vínculos de emprego da RAIS já agregados, com contagem e somas de salário e idade.",
               "1 linha = combinação de ano × município × CNAE × CBO × atributos do vínculo e do trabalhador (sexo, idade, escolaridade, cor/raça…).",
               "Os números do painel saem daqui: `vinculos` (empregos em 31/12), `soma_salario_valido` / `qtd_salario_valido` (remuneração média) e `soma_idade` / `qtd_idade` (idade média). Lida em DirectQuery no modelo `Painel_RAIS`."),
    "D_Cnae": ("Dimensão", "Classificação CNAE das atividades, com a divisão e o grupo de setor (AFL, Comparável…).",
               "1 linha por subclasse CNAE (`cnae_fiscal`).",
               "Liga a fato aos setores. `grupo_setor` filtra D_GrupoSetor, `setor_comparavel_afl` filtra D_Comparavel e `cnae_fiscal` filtra D_AflAtividade."),
    "D_GrupoSetor": ("Dimensão", "Grupo de setor usado em todo o painel (AFL × Comparável × demais).", "1 linha por grupo de setor.",
                     "Base dos filtros AFL e Comparáveis em quase todas as medidas `_AFL` e `_Comparavel`."),
    "D_Sexo": ("Dimensão", "Sexo do trabalhador, com ordem de exibição.", "1 linha por sexo.", "Usada nos KPIs e gráficos de mulheres e na razão salarial por sexo."),
    "D_Escolaridade": ("Dimensão", "Escolaridade agrupada em quatro níveis, com ordem.", "1 linha por nível de escolaridade.", "Eixo dos gráficos de escolaridade e da razão salarial por escolaridade."),
    "D_FaixaIdade": ("Dimensão", "Faixa de idade do trabalhador, com ordem.", "1 linha por faixa de idade.", "Eixo da pirâmide etária e base do indicador de jovens."),
    "D_Raca": ("Dimensão", "Cor ou raça, agrupada em negros, brancos e outros, com a marca de declarada.", "1 linha por cor/raça.", "Base dos percentuais por cor (só sobre quem declarou) e da razão salarial negros × brancos."),
    "D_regiao": ("Dimensão", "Geografia: município, estado e sigla da UF.", "1 linha por município (`cod_municipio`).", "Mapas e rankings por UF, com drill para município."),
    "D_Calendario": ("Dimensão", "Calendário diário de 2009 até o fim do ano corrente, com a fonte da RAIS e o trecho da série.",
                     "1 linha por dia.", "Liga-se a `F_rais[ano]` por uma relação muitos-para-muitos. `Fonte RAIS` e `Trecho da Série` separam a RAIS antiga (até 2021) do eSocial (2022 em diante)."),
    "D_Ano": ("Dimensão", "Lista de anos, ligada ao calendário.", "1 linha por ano.", "Relação detectada automaticamente com `D_Calendario[Ano]`."),
    "D_Comparavel": ("Dimensão", "Rótulo de exibição do setor comparável ao AFL.", "1 linha por setor comparável.", "Filtrada por `D_Cnae[setor_comparavel_afl]`."),
    "D_AflAtividade": ("Dimensão", "As seis atividades do AFL, por código CNAE, com ordem.", "1 linha por CNAE do AFL.", "Botões e rankings da página AFL."),
    "D_Rank_Divisao": ("Auxiliar", "Lista de divisões CNAE usada no eixo dos rankings.", "1 linha por divisão.", "Tabela local (import), sem relação: as medidas filtram a fato com ela."),
    "D_Indicador": ("Auxiliar", "Os sete indicadores da página Quem contrata (botões).", "1 linha por indicador.", "Tabela de parâmetro: a escolha troca o indicador de toda a página."),
    "D_Info": ("Auxiliar", "Textos dos ícones de informação (i) de cada visual.", "1 linha por chave `Página|Setor|Visual`.", "As medidas `Info_*` e as dicas leem esta tabela pela `Chave`."),
    "D_Ct_Modo": ("Auxiliar", "Botões do ranking: 10 melhores ou 10 piores setores.", "1 linha por opção.", "Tabela de parâmetro da página de ranking."),
    "D_Ct_Setor": ("Auxiliar", "Botões de setor da página de ranking.", "1 linha por opção.", "Tabela de parâmetro da página de ranking."),
    "D_Ct_MetMul": ("Auxiliar", "Botões de métrica do bloco de mulheres (representatividade ou salário médio).", "1 linha por métrica.", "Troca a métrica e o formato das medidas `Ct_Mul_*`."),
    "D_Ct_MetNeg": ("Auxiliar", "Botões de métrica do bloco de negros (representatividade ou salário médio).", "1 linha por métrica.", "Troca a métrica e o formato das medidas `Ct_Neg_*`."),
    "D_Ct_MetEsc": ("Auxiliar", "Botões de métrica do bloco de escolaridade (representatividade ou salário médio).", "1 linha por métrica.", "Troca a métrica e o formato das medidas `Ct_Esc_*`."),
    "D_Ct_Nivel": ("Auxiliar", "Botões de nível de escolaridade da página de ranking.", "1 linha por nível.", "Tabela de parâmetro da página de ranking."),
    "_medidas": ("Medidas", "Tabela que só hospeda as medidas DAX do painel.", "Sem linhas de dados.", "Todas as medidas ficam aqui, organizadas por pastas (displayFolder)."),
}
ORDEM_TIPO = {"Fato": 0, "Dimensão": 1, "Auxiliar": 2, "Medidas": 3}
BADGE = {"Fato": "fato", "Dimensão": "dim", "Auxiliar": "aux", "Medidas": "med"}


def esc(s):
    return html.escape(str(s), quote=True)


def slug(s):
    s = re.sub(r"[^\w]+", "-", s.lower()).strip("-")
    return s or "x"


def tira_aspas(n):
    n = n.strip()
    return n[1:-1].replace("''", "'") if n.startswith("'") and n.endswith("'") else n


# ---------------------------------------------------------------- leitura do TMDL
def ler_tabela(path):
    linhas = path.read_text(encoding="utf-8").split("\n")
    nome = tira_aspas(linhas[0][len("table "):])
    tab = {"nome": nome, "desc": "", "colunas": [], "medidas": [], "particao": None}
    desc = []
    atual = None      # dict do objeto (coluna/medida/partição)
    modo = None       # "expr" | "fsd" | "src" | None
    for ln in linhas[1:]:
        if ln.startswith("\t///"):
            desc.append(ln[4:].strip())
            continue
        m = re.match(r"^\t(measure|column|partition) (.+?)(?: = ?(.*))?$", ln)
        if m and not ln.startswith("\t\t"):
            tipo, n, resto = m.groups()
            if tipo == "partition":
                n, resto = n, resto
                atual = {"nome": tira_aspas(n), "tipo": (resto or "").strip(), "modo": "", "fonte": [], "entity": "", "exprsrc": ""}
                tab["particao"] = atual
                modo = None
            else:
                atual = {"nome": tira_aspas(n), "desc": " ".join(desc), "expr": [], "props": {}, "calc": resto is not None}
                if resto:
                    atual["expr"].append(resto.strip())
                (tab["medidas"] if tipo == "measure" else tab["colunas"]).append(atual)
                modo = "expr" if resto is not None else None
            desc = []
            continue
        if ln.strip() == "" and modo not in ("expr", "fsd", "src"):
            continue
        if not ln.startswith("\t"):
            atual, modo = None, None
            continue
        if ln.startswith("\t") and not ln.startswith("\t\t"):
            atual, modo, desc = None, None, []   # annotation/propriedade da tabela
            continue
        if atual is None:
            continue
        if ln.startswith("\t\t\t") or (ln.strip() == "" and modo in ("expr", "fsd", "src")):
            if modo == "expr":
                atual["expr"].append(ln[3:] if ln.startswith("\t\t\t") else "")
            elif modo == "fsd":
                atual["props"]["formatStringDefinition"] = (atual["props"].get("formatStringDefinition", "") + " " + ln.strip()).strip()
            elif modo == "src":
                atual["fonte"].append(ln[4:] if ln.startswith("\t\t\t\t") else ln.strip())
            elif "entity" in atual:
                kv = ln.strip().split(":", 1)
                if kv[0] == "entityName":
                    atual["entity"] = kv[1].strip()
                elif kv[0] == "expressionSource":
                    atual["exprsrc"] = kv[1].strip()
            continue
        p = ln.strip()
        if "entity" in atual:   # partição
            if p.startswith("mode:"):
                atual["modo"] = p.split(":", 1)[1].strip()
            modo = "src" if p.startswith("source =") else None
            continue
        if p.startswith("formatStringDefinition ="):
            atual["props"]["formatStringDefinition"] = p.split("=", 1)[1].strip()
            modo = "fsd"
            continue
        modo = None
        if ":" in p:
            k, v = p.split(":", 1)
            atual["props"][k.strip()] = v.strip()
        else:
            atual["props"][p] = True
    tab["desc"] = tab["desc"] or ""
    for o in tab["medidas"] + tab["colunas"]:
        while o["expr"] and not o["expr"][-1].strip():
            o["expr"].pop()
        o["dax"] = "\n".join(o["expr"]).strip("\n")
    return tab


def ler_relacoes():
    rels, atual = [], None
    for ln in (SM / "relationships.tmdl").read_text(encoding="utf-8").split("\n"):
        if ln.startswith("relationship "):
            atual = {"id": ln.split(" ", 1)[1], "fromCardinality": "many", "toCardinality": "one",
                     "crossFilteringBehavior": "oneDirection", "isActive": "true"}
            rels.append(atual)
        elif atual is not None and ln.startswith("\t") and ":" in ln:
            k, v = ln.strip().split(":", 1)
            atual[k.strip()] = v.strip()
    for r in rels:
        r["fromTab"], r["fromCol"] = r["fromColumn"].split(".", 1)
        r["toTab"], r["toCol"] = r["toColumn"].split(".", 1)
    return rels


tabelas = [ler_tabela(p) for p in sorted((SM / "tables").glob("*.tmdl"))
           if not p.stem.startswith(("LocalDateTable_", "DateTableTemplate_"))]
tabelas.sort(key=lambda t: (ORDEM_TIPO[INFO_TAB.get(t["nome"], ("Auxiliar",))[0]], t["nome"].lower()))
relacoes = ler_relacoes()
modelo_txt = (SM / "model.tmdl").read_text(encoding="utf-8")
expr_txt = (SM / "expressions.tmdl").read_text(encoding="utf-8")

medidas = [dict(m, host=t["nome"]) for t in tabelas for m in t["medidas"]]
NOMES_MED = {m["nome"] for m in medidas}
NOMES_TAB = {t["nome"] for t in tabelas}
COLS = {(t["nome"], c["nome"]) for t in tabelas for c in t["colunas"]}

# páginas do relatório e uso das medidas nos visuais
paginas = []
uso_visual = defaultdict(set)
pj = json.loads((REP / "pages" / "pages.json").read_text(encoding="utf-8"))
for pid in pj.get("pageOrder", []):
    pdir = REP / "pages" / pid
    if not (pdir / "page.json").exists():
        continue
    pg = json.loads((pdir / "page.json").read_text(encoding="utf-8"))
    nome_pg = pg.get("displayName", pid)
    paginas.append((nome_pg, pg.get("visibility", "") == "HiddenInViewMode"))
    for vf in pdir.glob("visuals/*/visual.json"):
        for prop in set(re.findall(r'"Property":\s*"([^"]+)"', vf.read_text(encoding="utf-8"))):
            if prop in NOMES_MED:
                uso_visual[prop].add(nome_pg)


# ---------------------------------------------------------------- análise do DAX
RE_TOKEN = re.compile(r'"(?:[^"]|"")*"|//[^\n]*|--[^\n]*|/\*.*?\*/', re.S)
RE_COLREF = re.compile(r"('(?:[^']|'')+'|[A-Za-z_][\w]*)\s*\[([^\]]+)\]")
RE_BARE = re.compile(r"\[([^\]]+)\]")


def limpar(dax):
    return RE_TOKEN.sub(lambda m: '""' if m.group(0).startswith('"') else " ", dax)


def refs(dax):
    d = limpar(dax)
    meds, cols, tabs = set(), set(), set()
    for t, c in RE_COLREF.findall(d):
        t = tira_aspas(t)
        if t in NOMES_TAB:
            if (t, c) in COLS:
                cols.add(f"{t}[{c}]")
                tabs.add(t)
            elif c in NOMES_MED:
                meds.add(c)
    resto = RE_COLREF.sub(" ", d)
    for c in RE_BARE.findall(resto):
        if c in NOMES_MED:
            meds.add(c)
    for t in NOMES_TAB:
        if re.search(r"(?<![\w'])" + re.escape(t) + r"(?![\w\[])", resto) or f"'{t}'" in resto:
            tabs.add(t)
    return meds, cols, tabs


for m in medidas:
    m["usa_med"], m["usa_col"], m["usa_tab"] = refs(m["dax"])
    m["usa_med"].discard(m["nome"])
usada_por = defaultdict(set)
for m in medidas:
    for u in m["usa_med"]:
        usada_por[u].add(m["nome"])
POR_NOME = {m["nome"]: m for m in medidas}

KEYWORDS = {"VAR", "RETURN", "TRUE", "FALSE", "IN", "NOT", "AND", "OR", "ASC", "DESC", "DEFINE", "EVALUATE", "BLANK"}
RE_HL = re.compile(r'(?P<s>"(?:[^"]|"")*")|(?P<c>//[^\n]*|--[^\n]*|/\*.*?\*/)|(?P<w>[A-Za-z_][\w.]*)(?P<p>\s*\()?', re.S)


def realce(dax):
    out, pos = [], 0
    for m in RE_HL.finditer(dax):
        out.append(esc(dax[pos:m.start()]))
        pos = m.end()
        if m.group("s"):
            out.append(f'<span class="s">{esc(m.group("s"))}</span>')
        elif m.group("c"):
            out.append(f'<span class="c">{esc(m.group("c"))}</span>')
        else:
            w, p = m.group("w"), m.group("p") or ""
            if w.upper() in KEYWORDS and w.upper() not in ("TRUE", "FALSE", "BLANK", "NOT") or (w.upper() in ("TRUE", "FALSE", "BLANK", "NOT") and not p):
                out.append(f'<span class="k">{esc(w)}</span>{esc(p)}')
            elif p:
                out.append(f'<span class="f">{esc(w)}</span>{esc(p)}')
            else:
                out.append(esc(w))
    out.append(esc(dax[pos:]))
    return "".join(out)


FUNCS = [
    ("CALCULATE", "usa `CALCULATE` para trocar o filtro antes de calcular"),
    ("REMOVEFILTERS", "limpa filtros com `REMOVEFILTERS`"),
    ("ALLSELECTED", "respeita só a seleção da página com `ALLSELECTED`"),
    ("TREATAS", "aplica filtro virtual com `TREATAS`"),
    ("SELECTEDVALUE", "lê a escolha do usuário com `SELECTEDVALUE`"),
    ("ISFILTERED", "muda de comportamento conforme o que está filtrado (`ISFILTERED`)"),
    ("ISINSCOPE", "muda conforme o nível do visual (`ISINSCOPE`)"),
    ("SWITCH", "escolhe o resultado com `SWITCH`"),
    ("DIVIDE", "divide com `DIVIDE`, que devolve BLANK quando o divisor é zero"),
    ("RANKX", "calcula posição com `RANKX`"),
    ("TOPN", "pega os primeiros com `TOPN`"),
    ("SUMX", "soma linha a linha com `SUMX`"),
    ("AVERAGEX", "tira média linha a linha com `AVERAGEX`"),
    ("MAXX", "pega o maior valor de uma lista com `MAXX`"),
    ("MINX", "pega o menor valor de uma lista com `MINX`"),
    ("ADDCOLUMNS", "monta uma tabela virtual com `ADDCOLUMNS`"),
    ("SUMMARIZE", "agrupa com `SUMMARIZE`"),
    ("LOOKUPVALUE", "busca um valor em outra tabela com `LOOKUPVALUE`"),
    ("CONCATENATEX", "junta textos com `CONCATENATEX`"),
    ("FORMAT", "formata números como texto em pt-BR com `FORMAT`"),
]


def como_funciona(m):
    d = limpar(m["dax"])
    up = d.upper()
    partes = []
    vars_ = re.findall(r"\bVAR\s+([A-Za-z_]\w*)", m["dax"])
    if "<div" in m["dax"] or "<span" in m["dax"]:
        partes.append("Monta um texto HTML para um visual de HTML (cards, títulos, tooltips)")
    if vars_:
        lista = ", ".join(f"`{v}`" for v in vars_[:8]) + ("…" if len(vars_) > 8 else "")
        partes.append(f"Guarda {len(vars_)} variável(is) ({lista}) e devolve o resultado no `RETURN`")
    acoes = [txt for f, txt in FUNCS if re.search(r"\b" + f + r"\s*\(", up)]
    if acoes:
        partes.append("; ".join(acoes[:6]))
    if not partes:
        partes.append("Expressão direta, sem variáveis")
    alvos = sorted(set(re.findall(r"REMOVEFILTERS\s*\(\s*('?[\w ]+'?(?:\[[^\]]+\])?)", d)))
    txt = ". ".join(p[0].upper() + p[1:] for p in partes) + "."
    if alvos:
        txt += " Filtros limpos: " + ", ".join(f"`{tira_aspas(a)}`" for a in alvos[:6]) + "."
    return txt


PREFIXOS = [("KPI_", "Card de KPI em HTML."), ("Tip_", "Tooltip em HTML."), ("Titulo_", "Título de visual em HTML."),
            ("Manchete_", "Manchete da página em HTML."), ("Rotulo_", "Rótulo de visual em HTML."), ("Info_", "Ícone de informação (i) do visual."),
            ("Cor_", "Cor usada na formatação condicional."), ("Dif_", "Diferença entre grupos."), ("Rem_", "Remuneração para um visual."),
            ("Emp_", "Empregos para um visual."), ("Ct_", "Valor da página de ranking (Quem contrata)."), ("Ind_", "Indicador da página Quem contrata.")]


def o_que_faz(m):
    if m["desc"]:
        return m["desc"], False
    for p, t in PREFIXOS:
        if m["nome"].startswith(p):
            return t, True
    return "Medida de apoio usada por outras medidas.", True


def pasta(m):
    return m["props"].get("displayFolder", "").strip() or "Sem pasta"


def fmt(m):
    if "formatString" in m["props"]:
        return m["props"]["formatString"]
    if "formatStringDefinition" in m["props"]:
        return "dinâmico"
    return "—"


# ---------------------------------------------------------------- dados derivados
n_col = sum(len(t["colunas"]) for t in tabelas)
tam = sum(p.stat().st_size for p in SM.rglob("*") if p.is_file())
TAM = f"{tam / 1024:.0f} KB" if tam < 1024 * 1024 else f"{tam / 1024 / 1024:.1f} MB"
grupos = defaultdict(list)
for m in medidas:
    grupos[pasta(m)].append(m)
pastas = sorted(grupos, key=lambda p: (p == "Sem pasta", p.lower()))
for p in pastas:
    grupos[p].sort(key=lambda m: m["nome"].lower())
base_rank = sorted(((len(usada_por[n]), n) for n in usada_por), reverse=True)
ANCORAS = {n for _, n in base_rank[:6]}
raizes = [m["nome"] for m in medidas if not usada_por.get(m["nome"])]
uso_tab = defaultdict(int)
for m in medidas:
    for t in m["usa_tab"]:
        uso_tab[t] += 1
top_tab = sorted(uso_tab.items(), key=lambda kv: -kv[1])[:5]
src_as = re.search(r'AnalysisServices\.Database\("([^"]+)",\s*"([^"]+)"\)', expr_txt)
WS_URL, WS_DB = (src_as.group(1), src_as.group(2)) if src_as else ("?", "?")
WS_NOME = WS_URL.rsplit("/", 1)[-1]


def origem(t):
    p = t["particao"]
    if not p:
        return "—"
    if p["tipo"] == "entity":
        return f"DirectQuery · {p['entity']} ({WS_DB})"
    corpo = "\n".join(p["fonte"])
    if "#table(" in corpo:
        return "Import · tabela digitada (#table)"
    if "List.Dates" in corpo or "Date" in corpo and t["nome"] == "D_Calendario":
        return "Import · M gerado (calendário)"
    return f"Import · M ({p['tipo']})"


def resumo_m(t):
    p = t["particao"]
    if not p:
        return ""
    if p["tipo"] == "entity":
        return (f"// partição entity, modo {p['modo']}\n// entidade: {p['entity']}\n"
                f"// fonte: {p['exprsrc']} → AnalysisServices.Database(\"{WS_URL}\", \"{WS_DB}\")")
    linhas = [re.sub(r"\{\{.*\}\}", "{{ … linhas digitadas … }}", l) if len(l) > 160 else l for l in p["fonte"]]
    if len(linhas) > 15:
        linhas = linhas[:12] + [f"    // … {len(linhas) - 14} linhas omitidas …"] + linhas[-2:]
    return "\n".join(linhas)


def papel_col(t, c):
    n = c["nome"]
    rel_from = {(r["fromTab"], r["fromCol"]): r for r in relacoes}
    rel_to = {(r["toTab"], r["toCol"]): r for r in relacoes}
    if c["calc"]:
        return "Calculada"
    if (t["nome"], n) in rel_from:
        r = rel_from[(t["nome"], n)]
        return f"Chave estrangeira → {r['toTab']}"
    if (t["nome"], n) in rel_to:
        return "Chave primária" if rel_to[(t["nome"], n)]["toCardinality"] == "one" else "Chave (lado muitos)"
    if c["props"].get("dataType") in ("int64", "double", "decimal") and t["nome"].startswith("F_"):
        return "Métrica"
    return "Atributo"


def notas_col(c):
    n = []
    if c["props"].get("isHidden"):
        n.append("oculta")
    sc = c["props"].get("sourceColumn")
    if sc and tira_aspas(sc) != c["nome"]:
        n.append(f"origem: `{tira_aspas(sc)}`")
    if c["props"].get("sortByColumn"):
        n.append(f"ordena por `{c['props']['sortByColumn']}`")
    if c["props"].get("formatString"):
        n.append(f"formato `{c['props']['formatString']}`")
    if c["desc"]:
        n.append(c["desc"])
    return "; ".join(n) or "—"


def card(r):
    a = "N" if r["fromCardinality"] == "many" else "1"
    b = "N" if r["toCardinality"] == "many" else "1"
    return f"{a}:{b}"


def notas_rel(r):
    n = []
    if card(r) == "N:N":
        n.append("muitos-para-muitos")
    if r["crossFilteringBehavior"] == "bothDirections":
        n.append("bi-direcional")
    if r["isActive"] == "false":
        n.append("inativo")
    if r["id"].startswith("AutoDetected"):
        n.append("detectado automaticamente")
    if r.get("securityFilteringBehavior") == "none":
        n.append("sem filtro de segurança")
    return ", ".join(n) or "—"


def arvore(nome, prof, vistos, pref="", max_prof=3):
    linhas = []
    m = POR_NOME[nome]
    filhos = sorted(m["usa_med"]) + sorted(m["usa_col"])
    for i, f in enumerate(filhos):
        ult = i == len(filhos) - 1
        ramo = "└─ " if ult else "├─ "
        if f in POR_NOME:
            if f in vistos:
                linhas.append((pref + ramo, f, "dim", " (já mapeada acima)"))
            elif prof >= max_prof and POR_NOME[f]["usa_med"]:
                linhas.append((pref + ramo, f, "branch", " (…)"))
            else:
                vistos.add(f)
                linhas.append((pref + ramo, f, "branch", ""))
                linhas += arvore(f, prof + 1, vistos, pref + ("   " if ult else "│  "), max_prof)
        else:
            linhas.append((pref + ramo, f, "leaf", ""))
    return linhas


def tamanho_arvore(n, vistos=None):
    vistos = vistos if vistos is not None else set()
    for f in POR_NOME[n]["usa_med"]:
        if f not in vistos:
            vistos.add(f)
            tamanho_arvore(f, vistos)
    return len(vistos)


raizes_top = sorted(raizes, key=lambda n: -tamanho_arvore(n))
raizes_html = raizes_top[:6]

# ---------------------------------------------------------------- markdown
def ler_tpl(nome):
    t = (SKILL / nome).read_text(encoding="utf-8")
    return re.sub(r"^<!--.*?-->\s*", "", t, flags=re.S)


def preencher(t, mapa):
    for k, v in mapa.items():
        t = t.replace("{{" + k + "}}", str(v))
    return t


GLOBAIS = {"PROJECT_NAME": PROJETO, "PROJECT_FILENAME": ARQUIVO, "TIMESTAMP": TS, "PROJECT_TAGLINE": TAGLINE,
           "TABLES_COUNT": len(tabelas), "MEASURES_COUNT": len(medidas), "RELATIONSHIPS_COUNT": len(relacoes),
           "COLUMNS_COUNT": n_col, "SIZE": TAM}

inv_md = "\n".join(f"| [`{t['nome']}`](01-tabelas.md#{slug(t['nome'])}) | {INFO_TAB[t['nome']][0]} | {len(t['colunas'])} | {len(t['medidas'])} | {origem(t)} |" for t in tabelas)
fontes_md = (f"- **Modelo semântico do Power BI (DirectQuery para Analysis Services):** `{WS_DB}`, workspace `{WS_NOME}` (`{WS_URL}`). "
             f"Fonte de F_rais e das dimensões remotas.\n- **Tabelas digitadas em M (`#table`)**: botões, parâmetros e textos das dicas.\n"
             f"- **M gerado**: calendário `D_Calendario`.")
avisos_md = (f"> **Atenção:** a fonte aponta para o workspace `{WS_NOME}`. Ao publicar em outro workspace, troque o endereço em `expressions.tmdl`.")
auto_dt = "ligado" if "__PBI_TimeIntelligenceEnabled = 1" in modelo_txt else "desligado"
cult = re.search(r"culture:\s*(\S+)", modelo_txt).group(1)
pag_vis = [p for p, h in paginas if not h]
pag_dica = [p for p, h in paginas if h]
config = [("Culture", cult), ("Auto Date/Time", auto_dt + " (nenhuma tabela LocalDateTable_* no modelo)"),
          ("Modo de dados", "Composto: DirectQuery para AS + tabelas locais em import"),
          ("Páginas do relatório", f"{len(pag_vis)} visíveis ({', '.join(pag_vis)})"),
          ("Páginas de dica (tooltip)", f"{len(pag_dica)} ocultas"),
          ("Pastas de medidas", f"{len(pastas)} displayFolders")]
config_md = "\n".join(f"- **{k}:** {v}" for k, v in config)

blocos = []
for t in tabelas:
    tipo, tag, gran, desc = INFO_TAB[t["nome"]]
    b = [f"## {t['nome']}", "", f"> {tag}", f"> **Tipo:** {tipo} · **Origem:** {origem(t)}", "", "### Descrição", desc + (f" {t['desc']}" if t["desc"] else ""), "",
         "### Granularidade", gran, ""]
    if t["colunas"]:
        b += ["### Colunas", "", "| Coluna | Tipo | Papel | Notas |", "|---|---|---|---|"]
        b += [f"| `{c['nome']}` | {c['props'].get('dataType', '—')} | {papel_col(t, c)} | {notas_col(c)} |" for c in t["colunas"]]
        b.append("")
    if t["medidas"]:
        b += ["### Medidas hospedadas", ""]
        b += [f"- [{p}](02-medidas.md#{slug(p)}) — {sum(1 for m in grupos[p] if m['host'] == t['nome'])} medidas" for p in pastas]
        b.append("")
    if t["particao"] and t["nome"] != "_medidas":
        b += ["### Source M (resumo)", "```m", resumo_m(t), "```", ""]
    b.append("---")
    blocos.append("\n".join(b))

grupos_md = []
for p in pastas:
    g = [f"## {p}", "", f"{len(grupos[p])} medidas.", ""]
    for m in grupos[p]:
        txt, inf = o_que_faz(m)
        g += [f"### {m['nome']}", "", f"`{m['host']}.{m['nome']}` · formato `{fmt(m)}`", "",
              "**O que faz:**", txt + (" *(inferido do nome; não há descrição no TMDL)*" if inf else ""), "",
              "**DAX:**", "```dax", m["dax"], "```", "", "**Como funciona:**", como_funciona(m), ""]
        usa = [f"`{u}`" for u in sorted(m["usa_med"])] + [f"`{c}`" for c in sorted(m["usa_col"])]
        g.append("**Usa:** " + (", ".join(usa) or "—"))
        g.append("**É usada por:** " + (", ".join(f"`{u}`" for u in sorted(usada_por[m["nome"]])) or "nenhuma medida (medida-raiz)"))
        if uso_visual.get(m["nome"]):
            g.append("**Aparece nas páginas:** " + ", ".join(sorted(uso_visual[m["nome"]])))
        g += ["", "---", ""]
    grupos_md.append("\n".join(g))

DIAGRAMA = r"""
 ┌──────────────┐ N:N ┌───────────┐ N:1 ┌──────────┐
 │ D_Calendario │◄────│           │────►│ D_regiao │
 └──────┬───────┘     │           │     └──────────┘
        │ auto        │           │ N:1 ┌──────────┐
        ▼             │           │────►│ D_Sexo   │
 ┌──────────────┐     │  F_rais   │     └──────────┘
 │ D_Ano        │     │  (fato)   │ N:1 ┌────────────────┐
 └──────────────┘     │           │────►│ D_Escolaridade │
                      │           │     └────────────────┘
                      │           │ N:1 ┌──────────────┐
                      │           │────►│ D_FaixaIdade │
                      │           │     └──────────────┘
                      │           │ N:1 ┌──────────┐
                      │           │────►│ D_Raca   │
                      └─────┬─────┘     └──────────┘
                            │ N:1
                            ▼
                      ┌───────────┐ N:1 ┌──────────────┐
                      │  D_Cnae   │────►│ D_GrupoSetor │
                      └─────┬─────┘     └──────────────┘
                     N:1 │     │ 1:1
                         ▼     ▼
             ┌──────────────┐ ┌────────────────┐
             │ D_Comparavel │ │ D_AflAtividade │
             └──────────────┘ └────────────────┘

 Sem relação (parâmetros e textos): D_Indicador, D_Info, D_Rank_Divisao, D_Ct_*
""".strip("\n")

rel_md = "\n".join(f"| {i} | `{r['fromColumn']}` | `{r['toColumn']}` | {card(r)} | {'**Ambas**' if r['crossFilteringBehavior'] == 'bothDirections' else 'Única'} | {'✓' if r['isActive'] != 'false' else '✗'} | {notas_rel(r)} |"
                   for i, r in enumerate(relacoes, 1))
sem_rel = sorted(t["nome"] for t in tabelas if t["nome"] not in {r["fromTab"] for r in relacoes} | {r["toTab"] for r in relacoes} and t["nome"] != "_medidas")
REL_ANALISE = (f"Esquema estrela com `F_rais` no centro e {len(relacoes)} relações. A fato filtra direto as dimensões de pessoa (sexo, idade, escolaridade, cor/raça), "
               "a geografia (`D_regiao`) e a atividade (`D_Cnae`). `D_Cnae` é um floco: dela saem `D_GrupoSetor`, `D_Comparavel` e `D_AflAtividade`. "
               "O tempo entra por `D_Calendario`, ligada a `F_rais[ano]` por uma relação muitos-para-muitos (um ano tem vários dias). "
               f"Ficam sem relação as tabelas de parâmetro e de texto: {', '.join(f'`{s}`' for s in sem_rel)}. Nenhuma relação é bi-direcional e todas estão ativas.")

arv_md = []
for n in raizes_top[:15]:
    ls = arvore(n, 1, set())
    arv_md.append(f"### {n}\n```\n{n}\n" + "\n".join(p + f + s for p, f, _, s in ls) + "\n```")
arv_md.append(f"\nOutras {len(raizes) - 15} medidas-raiz têm árvore curta; veja **Usa** em [02 · Medidas](02-medidas.md).")
rev_md = []
for k, n in base_rank:
    if k < 3:
        break
    lst = sorted(usada_por[n])
    rev_md.append(f"### {n} (base)\n\n**Usada por:**\n" + "\n".join(f"- `{u}`" for u in lst[:20]) + (f"\n- … e mais {len(lst) - 20}" if len(lst) > 20 else "")
                  + f"\n\n**Implicação:** mudar `{n}` afeta {len(lst)} outras medidas diretamente.\n")
top_md = "\n".join(f"{i}. `{t}` — referenciada por {k} medidas" for i, (t, k) in enumerate(top_tab, 1))

OUT.mkdir(exist_ok=True)
saidas = {
    "00-overview.md": preencher(ler_tpl("00-overview.md"), dict(GLOBAIS, INVENTORY_TABLE_MD=inv_md, DATA_SOURCES_LIST=fontes_md, WARNINGS_BLOCK=avisos_md, CONFIG_LIST_MD=config_md)),
    "01-tabelas.md": preencher(ler_tpl("01-tabelas.md"), dict(GLOBAIS, TABLES_BLOCKS_MD="\n\n".join(blocos))),
    "02-medidas.md": preencher(ler_tpl("02-medidas.md"), dict(GLOBAIS, MEASURE_GROUPS_MD="\n".join(grupos_md))),
    "03-relacionamentos.md": preencher(ler_tpl("03-relacionamentos.md"), dict(GLOBAIS, REL_DIAGRAM_ASCII=DIAGRAMA, REL_TABLE_MD_ROWS=rel_md, REL_ANALYSIS=REL_ANALISE)),
    "04-dependencias.md": preencher(ler_tpl("04-dependencias.md"), dict(GLOBAIS, DEP_TREES_MD="\n\n".join(arv_md), DEP_REVERSE_MD="\n".join(rev_md), TOP_TABLES_MD=top_md)),
}

# ---------------------------------------------------------------- HTML
def md_code(s):
    return re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", esc(s).replace("&#x27;", "'"))


nav_tab = "\n".join(f'<a href="#t-{slug(t["nome"])}">{esc(t["nome"])} <span class="badge-mini {BADGE[INFO_TAB[t["nome"]][0]]}">{BADGE[INFO_TAB[t["nome"]][0]]}</span></a>' for t in tabelas)
nav_med = "\n".join(f'<a href="#g-{slug(p)}">{esc(p)} <span class="badge-mini med">{len(grupos[p])}</span></a>' for p in pastas)
inv_rows = "\n".join(f'<tr><td class="tab-name">{esc(t["nome"])}</td><td><span class="badge-inline {BADGE[INFO_TAB[t["nome"]][0]]}">{INFO_TAB[t["nome"]][0]}</span></td>'
                     f'<td class="right">{len(t["colunas"])}</td><td class="right">{len(t["medidas"])}</td><td>{esc(origem(t))}</td></tr>' for t in tabelas)
fontes_html = (f"modelo semântico <code>{esc(WS_DB)}</code> no workspace <code>{esc(WS_NOME)}</code>, lido em DirectQuery para Analysis Services "
               "(fato e dimensões remotas). Botões, parâmetros e textos das dicas são tabelas digitadas em M; o calendário é gerado em M.")
avisos_html = f'<div class="callout warn">A fonte aponta para o workspace <code>{esc(WS_NOME)}</code> (<code>{esc(WS_URL)}</code>). Ao publicar em outro workspace, troque o endereço em <code>expressions.tmdl</code>.</div>'
config_html = "\n".join(f'<li><span class="key">{esc(k)}</span><span class="val{" on" if k == "Auto Date/Time" and auto_dt == "ligado" else ""}">{esc(v)}</span></li>' for k, v in config)

cards = []
for t in tabelas:
    tipo, tag, gran, desc = INFO_TAB[t["nome"]]
    c = [f'<article class="table-card" id="t-{slug(t["nome"])}">',
         f'<div class="table-card-head"><span class="table-card-name">{esc(t["nome"])}</span><span class="badge-inline {BADGE[tipo]}">{tipo}</span>'
         f'<span class="table-card-meta">{len(t["colunas"])} colunas · {len(t["medidas"])} medidas · {esc(origem(t))}</span></div>',
         '<div class="table-card-body">', f"<p>{md_code(tag)}</p>", f"<p>{md_code(desc + (' ' + t['desc'] if t['desc'] else ''))}</p>",
         '<div class="label">Granularidade</div>', f"<p>{md_code(gran)}</p>"]
    if t["colunas"]:
        c.append('<div class="label">Colunas</div><table class="col-table"><thead><tr><th>Coluna</th><th>Tipo</th><th>Papel</th><th>Notas</th></tr></thead><tbody>')
        c += [f'<tr><td class="col-name">{esc(col["nome"])}</td><td class="col-type">{esc(col["props"].get("dataType", "—"))}</td>'
              f'<td class="col-papel">{esc(papel_col(t, col))}</td><td class="col-notas">{md_code(notas_col(col))}</td></tr>' for col in t["colunas"]]
        c.append("</tbody></table>")
    if t["medidas"]:
        c.append(f'<div class="label">Medidas hospedadas</div><p>{len(t["medidas"])} medidas em {len(pastas)} pastas — ver <a href="#medidas">02 · Medidas</a>.</p>')
    if t["particao"] and t["nome"] != "_medidas":
        c.append(f'<details class="source-m"><summary>Source M (resumo)</summary><pre class="code">{esc(resumo_m(t))}</pre></details>')
    c.append("</div></article>")
    cards.append("\n".join(c))

grupos_html = []
for p in pastas:
    g = [f'<div class="measure-group" id="g-{slug(p)}"><div class="measure-group-title">{esc(p)}</div><div class="measure-group-meta">{len(grupos[p])} medidas</div>']
    for m in grupos[p]:
        txt, inf = o_que_faz(m)
        anc = m["nome"] in ANCORAS
        linha1 = next((l.strip() for l in m["dax"].split("\n") if l.strip()), "")
        deps = sorted(usada_por[m["nome"]])
        usa = sorted(m["usa_med"]) + sorted(m["usa_col"])
        pags = sorted(uso_visual.get(m["nome"], []))
        g.append(
            f'<details class="measure-mini{" anchor" if anc else ""}"{" open" if anc else ""}>'
            f'<summary><span class="name">{esc(m["nome"])}</span><span class="dax">{esc(linha1[:110])}</span><span class="toggle">+</span></summary>'
            f'<div class="mini-body"><p class="meta">Tabela: <code>{esc(m["host"])}</code> · Format: <code>{esc(fmt(m))}</code> · Pasta: <code>{esc(p)}</code></p>'
            f'<p class="desc"><strong>O que faz:</strong> {md_code(txt)}{" <em>(inferido do nome)</em>" if inf else ""}</p>'
            f'<pre class="code">{realce(m["dax"])}</pre>'
            f'<div class="label">Como funciona</div><p class="desc">{md_code(como_funciona(m))}</p>'
            f'<div class="label">Usa</div><p class="measure-deps">{" · ".join(f"<code>{esc(u)}</code>" for u in usa) or "—"}</p>'
            f'<div class="label">É usada por</div><p class="measure-deps">{" · ".join(f"<code>{esc(u)}</code>" for u in deps) or "nenhuma medida (medida-raiz)"}</p>'
            + (f'<div class="label">Páginas</div><p class="measure-deps">{esc(", ".join(pags))}</p>' if pags else "")
            + "</div></details>")
    g.append("</div>")
    grupos_html.append("\n".join(g))

# SVG estrela
POS = {"F_rais": (480, 300), "D_Calendario": (130, 90), "D_Ano": (130, 200), "D_regiao": (830, 70), "D_Sexo": (830, 150),
       "D_Escolaridade": (830, 230), "D_FaixaIdade": (830, 310), "D_Raca": (830, 390), "D_Cnae": (480, 470),
       "D_GrupoSetor": (830, 480), "D_Comparavel": (300, 580), "D_AflAtividade": (660, 580)}
svg = ['<svg class="rel-svg" viewBox="0 0 960 640" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagrama de relacionamentos">']
for r in relacoes:
    if r["fromTab"] in POS and r["toTab"] in POS:
        (x1, y1), (x2, y2) = POS[r["fromTab"]], POS[r["toTab"]]
        cor = "var(--neon-magenta)" if card(r) == "N:N" else "var(--accent-glow)"
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:{cor};stroke-width:1.5;opacity:.7"/>')
        svg.append(f'<text x="{(x1 + x2) / 2}" y="{(y1 + y2) / 2 - 6}" text-anchor="middle" style="fill:var(--text-muted);font-family:var(--font-mono);font-size:11px">{card(r)}</text>')
for n, (x, y) in POS.items():
    w = 150 if n != "F_rais" else 170
    fato = n == "F_rais"
    svg.append(f'<rect x="{x - w / 2}" y="{y - 20}" width="{w}" height="40" rx="8" style="fill:var(--bg-elevated);stroke:{"var(--accent-gold-bright)" if fato else "var(--border-mid)"};stroke-width:{2 if fato else 1}"/>')
    svg.append(f'<text x="{x}" y="{y + 5}" text-anchor="middle" style="fill:{"var(--accent-gold-bright)" if fato else "var(--text-primary)"};font-family:var(--font-mono);font-size:13px">{esc(n)}</text>')
svg.append(f'<text x="20" y="630" style="fill:var(--text-muted);font-family:var(--font-body);font-size:12px">Sem relação: {esc(", ".join(sem_rel))}</text>')
svg.append("</svg>")

rel_rows = "\n".join(f'<tr><td>{i}</td><td class="from">{esc(r["fromColumn"])}</td><td class="to">{esc(r["toColumn"])}</td><td class="card">{card(r)}</td>'
                     f'<td class="{"dir-bi" if r["crossFilteringBehavior"] == "bothDirections" else "dir-single"}">{"Ambas" if r["crossFilteringBehavior"] == "bothDirections" else "Única"}</td>'
                     f'<td>{"✓" if r["isActive"] != "false" else "✗"}</td><td>{esc(notas_rel(r))}</td></tr>' for i, r in enumerate(relacoes, 1))

dep_html = []
for n in raizes_html:
    dep_html.append(f'<span class="root">{esc(n)}</span>')
    for pref, f, cls, suf in arvore(n, 1, set()):
        dep_html.append(f'{esc(pref)}<span class="{cls}">{esc(f)}{esc(suf)}</span>')
    dep_html.append("")
rev_html = []
for k, n in base_rank[:20]:
    lst = sorted(usada_por[n])
    rev_html.append(f'<div class="dep-reverse-card"><div class="head"><span class="name">{esc(n)}</span><span class="tag">base · {k} dependentes</span></div>'
                    f'<p class="by">{" · ".join(f"<code>{esc(u)}</code>" for u in lst[:24])}{f" · … e mais {len(lst) - 24}" if len(lst) > 24 else ""}</p>'
                    f'<p class="impl">Mudar <code>{esc(n)}</code> afeta {k} medidas diretamente.</p></div>')
top_html = "\n".join(f"<li><code>{esc(t)}</code> — referenciada por {k} medidas</li>" for t, k in top_tab)

tpl = (SKILL / "relatorio.html").read_text(encoding="utf-8")
# textos de exemplo do template (não são placeholders) trocados pelos reais deste modelo
tpl = tpl.replace("19 medidas agrupadas pelos 3 displayFolders do modelo. Detalhe das 4 medidas-âncora (Faturamento, Margem Bruta, % YoY, Medida Selecionada). Resto listado de forma compacta.",
                  f"{len(medidas)} medidas agrupadas em {len(pastas)} displayFolders. As {len(ANCORAS)} medidas-base mais reusadas abrem expandidas; clique nas demais para ver DAX e explicação.")
tpl = tpl.replace("Star schema clássico — todas as dimensões relacionam diretamente com a fato fVendas. 4 relacionamentos ativos, 1 deles bi-direcional.",
                  f"Estrela com F_rais no centro e D_Cnae como floco. {len(relacoes)} relacionamentos ativos, nenhum bi-direcional, 1 muitos-para-muitos (calendário).")
tpl = tpl.replace("Quem depende de quem entre as medidas. Útil pra entender o impacto de mudanças — alterar Faturamento mexe em 6 medidas a jusante.",
                  f"Quem depende de quem entre as medidas. Alterar {base_rank[0][1]} mexe em {base_rank[0][0]} medidas diretamente.")
tpl = tpl.replace("Árvore de % Faturamento YoY (medida-raiz):", f"Árvores das {len(raizes_html)} maiores medidas-raiz (de {len(raizes)}):")
tpl = tpl.replace("Doc gerada em 4 minutos por", "Doc gerada por")
overview_desc = (f"{len(tabelas)} tabelas: 1 fato (F_rais), {sum(1 for t in tabelas if INFO_TAB[t['nome']][0] == 'Dimensão')} dimensões, "
                 f"{sum(1 for t in tabelas if INFO_TAB[t['nome']][0] == 'Auxiliar')} auxiliares (botões, parâmetros e textos) e 1 tabela de medidas.")
mapa = dict(GLOBAIS, PROJECT_HERO_SUB=f"Observatório Abrasel · Painel RAIS · gerado em {TS}", OVERVIEW_DESC=overview_desc,
            NAV_TABLES_HTML=nav_tab, NAV_MEASURES_HTML=nav_med, INVENTORY_TABLE_ROWS=inv_rows, DATA_SOURCES_TEXT=fontes_html,
            WARNINGS_HTML=avisos_html, CONFIG_LIST_HTML=config_html, TABLES_CARDS_HTML="\n".join(cards), MEASURE_GROUPS_HTML="\n".join(grupos_html),
            REL_SVG_HTML="\n".join(svg), REL_TABLE_ROWS=rel_rows, DEP_TREE_HTML="\n".join(dep_html), DEP_REVERSE_HTML="\n".join(rev_html),
            TOP_TABLES_LIST_HTML=top_html)
saidas["index.html"] = preencher(tpl, {k: (esc(v) if k in GLOBAIS or k in ("PROJECT_HERO_SUB", "OVERVIEW_DESC") else v) for k, v in mapa.items()})

for nome, txt in saidas.items():
    (OUT / nome).write_text(txt, encoding="utf-8", newline="\n")
sobra = re.findall(r"\{\{[A-Z_]+\}\}", re.sub(r"<!--.*?-->", "", saidas["index.html"], flags=re.S))
print(f"tabelas={len(tabelas)} medidas={len(medidas)} relacoes={len(relacoes)} colunas={n_col} tamanho={TAM} pastas={len(pastas)} raizes={len(raizes)}")
print("sem descrição:", sum(1 for m in medidas if not m["desc"]), "| placeholders sobrando:", sobra)
print("base:", base_rank[:6])
