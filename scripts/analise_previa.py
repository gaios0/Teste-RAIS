"""Indicadores das prévias, calculados a partir de docs/previa/dados.json (grava docs/previa/indicadores.json).

AFL × Comparável é a comparação de referência; "Todos" = AFL + Comparável + Demais (mercado formal inteiro).
"""
import json
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
D = json.loads((RAIZ / "docs" / "previa" / "dados.json").read_text(encoding="utf-8"))
ANO, ANT, QUEBRA = 2025, 2024, 2022
GR = ("AFL", "Comparável", "Demais")


def f(x):
    return float(x) if x not in ("", None) else 0.0


def por(chave, *idx, val):
    out = defaultdict(float)
    for l in D[chave]:
        out[tuple(l[i] for i in idx)] += f(l[val])
    return out


# ---------------- empregos
emp = por("serie_emp", 0, 1, val=2)              # (ano, grupo) -> vínculos
anos = sorted({int(a) for a, _ in emp})


def e(ano, grupo):
    return emp[(str(ano), grupo)] if grupo != "Todos" else sum(emp[(str(ano), g)] for g in GR)


def var(ano, grupo):
    if ano in (anos[0], QUEBRA):
        return None
    return e(ano, grupo) / e(ano - 1, grupo) - 1


def cagr(ano, grupo):
    ini = QUEBRA if ano >= QUEBRA else anos[0]
    return (e(ano, grupo) / e(ini, grupo)) ** (1 / (ano - ini)) - 1 if ano > ini else None


serie = {g: [{"ano": a, "v": e(a, g), "var": var(a, g)} for a in anos] for g in ("AFL", "Comparável", "Todos")}
# sequência de altas do AFL dentro do trecho
seq = 0
for a in range(ANO, QUEBRA, -1):
    if var(a, "AFL") and var(a, "AFL") > 0:
        seq += 1
    else:
        break
pico_trecho1 = max(range(anos[0], QUEBRA), key=lambda a: e(a, "AFL"))
emp_ind = {
    "afl": e(ANO, "AFL"), "comp": e(ANO, "Comparável"), "todos": e(ANO, "Todos"),
    "var_afl": var(ANO, "AFL"), "var_comp": var(ANO, "Comparável"), "var_todos": var(ANO, "Todos"),
    "abs_afl": e(ANO, "AFL") - e(ANT, "AFL"), "abs_todos": e(ANO, "Todos") - e(ANT, "Todos"),
    "cagr_afl": cagr(ANO, "AFL"), "cagr_comp": cagr(ANO, "Comparável"), "cagr_todos": cagr(ANO, "Todos"),
    "part_todos": e(ANO, "AFL") / e(ANO, "Todos"), "part_comp": e(ANO, "AFL") / (e(ANO, "AFL") + e(ANO, "Comparável")),
    "part_todos_2022": e(QUEBRA, "AFL") / e(QUEBRA, "Todos"),
    "seq_altas_afl": seq, "afl_2019": e(2019, "AFL"), "afl_2020": e(2020, "AFL"), "queda_2020": e(2020, "AFL") / e(2019, "AFL") - 1,
    "comp_queda_2020": e(2020, "Comparável") / e(2019, "Comparável") - 1, "pico_trecho1": pico_trecho1, "afl_2021": e(2021, "AFL"),
    "afl_2022": e(QUEBRA, "AFL"), "salto_2022_afl": e(QUEBRA, "AFL") / e(2021, "AFL") - 1, "salto_2022_todos": e(QUEBRA, "Todos") / e(2021, "Todos") - 1,
}

# contratos 2025: categorias
cont = defaultdict(float)
for g, mod, inter, parc, v in D["contrato"]:
    if g not in ("AFL", "Comparável"):
        continue
    if inter == "Sim":
        cat = "Intermitente"
    elif mod == "Aprendiz":
        cat = "Aprendiz"
    elif parc == "Sim":
        cat = "Parcial"
    elif mod == "CLT Prazo Indeterminado":
        cat = "CLT por prazo indeterminado"
    elif mod in ("CLT Prazo Determinado", "Contrato por Prazo Determinado", "Temporário", "Contrato Temporário"):
        cat = "Prazo determinado ou temporário"
    else:
        cat = "Outros"
    cont[(g, cat)] += f(v)
contratos = {g: {c: cont[(g, c)] / sum(v for (gg, _), v in cont.items() if gg == g) for (gg, c) in cont if gg == g} for g in ("AFL", "Comparável")}

# divisões 2025 (sem os CNAEs do AFL) + AFL sintético
div = defaultdict(dict)
for nome, setor, comp, ano, v in D["divisoes"]:
    d = div[nome]
    d["setor"], d["comp"] = setor, comp
    d[int(ano)] = d.get(int(ano), 0) + f(v)
ranking = [{"nome": n, "setor": d["setor"], "comp": d["comp"], "v": d.get(ANO, 0), "cresc": (d.get(ANO, 0) / d[QUEBRA]) ** (1 / 3) - 1 if d.get(QUEBRA) else None}
           for n, d in div.items() if d.get(ANO)]
ranking.append({"nome": "AFL · conjunto de 6 CNAEs", "setor": "Serviços", "comp": "Sim", "v": e(ANO, "AFL"), "cresc": cagr(ANO, "AFL"), "afl": True})
ranking.sort(key=lambda r: -r["v"])
pos_afl = [i for i, r in enumerate(ranking) if r.get("afl")][0] + 1
ranking_cresc = sorted([r for r in ranking if r["cresc"] is not None and r["v"] >= 100000], key=lambda r: -r["cresc"])
pos_afl_cresc = [i for i, r in enumerate(ranking_cresc) if r.get("afl")][0] + 1

# atividades do AFL
at = defaultdict(dict)
for cnae, nome, ano, v, s, q, mul in D["atividades"]:
    at[(cnae, nome)][int(ano)] = (f(v), f(s), f(q), f(mul))
atividades = sorted([{"cnae": c, "nome": n, "v": d[ANO][0], "var": d[ANO][0] / d[ANT][0] - 1, "cagr": (d[ANO][0] / d[QUEBRA][0]) ** (1 / 3) - 1,
                      "media": d[ANO][1] / d[ANO][2], "mulheres": d[ANO][3] / d[ANO][0]} for (c, n), d in at.items()], key=lambda r: -r["v"])

# UF
uf = defaultdict(lambda: defaultdict(float))
for u, g, ano, v, s, q in D["uf"]:
    uf[u][(g, int(ano), "v")] += f(v)
    uf[u][(g, int(ano), "s")] += f(s)
    uf[u][(g, int(ano), "q")] += f(q)
ufs = sorted([{"uf": u, "afl": d[("AFL", ANO, "v")], "var": d[("AFL", ANO, "v")] / d[("AFL", ANT, "v")] - 1 if d[("AFL", ANT, "v")] else None,
               "part_comp": d[("AFL", ANO, "v")] / (d[("AFL", ANO, "v")] + d[("Comparável", ANO, "v")]),
               "media_afl": d[("AFL", ANO, "s")] / d[("AFL", ANO, "q")] if d[("AFL", ANO, "q")] else None,
               "media_comp": d[("Comparável", ANO, "s")] / d[("Comparável", ANO, "q")] if d[("Comparável", ANO, "q")] else None} for u, d in uf.items()],
             key=lambda r: -r["afl"])
for r in ufs:
    r["razao"] = r["media_afl"] / r["media_comp"] if r["media_afl"] and r["media_comp"] else None

# ---------------- perfil
si = por("sexo_idade", 0, 1, 2, val=4)


def soma_g(g, cond):
    return sum(v for k, v in si.items() if (k[0] == g or (g == "Todos" and k[0] in GR)) and cond(k))


perfil = {}
for g in ("AFL", "Comparável", "Todos"):
    tot = soma_g(g, lambda k: True)
    perfil[g] = {"mulheres": soma_g(g, lambda k: k[1] == "Mulher") / tot,
                 "ate24": soma_g(g, lambda k: k[2] in ("14-17", "18-24")) / tot,
                 "piramide": {fx: {s: soma_g(g, lambda k, fx=fx, s=s: k[2] == fx and k[1] == s) / tot for s in ("Mulher", "Homem")}
                              for fx in ("14-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+")}}
im = defaultdict(float)
for ano, g, s_, q_, mul, v in D["idade_media"]:
    im[(int(ano), g, "si")] += f(s_)
    im[(int(ano), g, "qi")] += f(q_)
for g in ("AFL", "Comparável"):
    perfil[g]["idade"] = im[(ANO, g, "si")] / im[(ANO, g, "qi")]
    perfil[g]["idade_2009"] = im[(2009, g, "si")] / im[(2009, g, "qi")]
esc = por("escolaridade", 0, 1, val=4)
GRUPOS_ESC = {"Até fundamental completo": ("< 1 ano de estudo", "Fundamental Incompleto", "Fundamental Completo"),
              "Médio incompleto": ("Médio Incompleto",), "Médio completo": ("Médio Completo",), "Superior (completo ou não)": ("Superior Incompleto", "Superior Completo")}
for g in ("AFL", "Comparável"):
    tot = sum(v for (gg, _), v in esc.items() if gg == g)
    perfil[g]["escolaridade"] = {k: sum(esc[(g, x)] for x in xs) / tot for k, xs in GRUPOS_ESC.items()}
    perfil[g]["medio_mais"] = perfil[g]["escolaridade"]["Médio completo"] + perfil[g]["escolaridade"]["Superior (completo ou não)"]
rc = defaultdict(float)
for g, cor, grupo, decl, ordem, v, s, q in D["raca"]:
    rc[(g, grupo, decl)] += f(v)
for g in ("AFL", "Comparável"):
    decl = sum(v for (gg, _, d), v in rc.items() if gg == g and d == "Sim")
    tot = sum(v for (gg, _, _), v in rc.items() if gg == g)
    perfil[g]["raca"] = {k: rc[(g, k, "Sim")] / decl for k in ("Branca", "Negra", "Amarela", "Indígena")}
    perfil[g]["raca_cobertura"] = decl / tot
cbo = [{"nome": l[0], "v": f(l[1]), "mulheres": f(l[2]) / f(l[1]), "media": f(l[3]) / f(l[4]) if f(l[4]) else None} for l in D["cbo"]]
cbo.sort(key=lambda r: -r["v"])
pi = defaultdict(float)
for ano, g, v, prim, interm, jovem in D["primeiro_interm"]:
    for k, x in (("v", v), ("prim", prim), ("interm", interm), ("jovem", jovem)):
        pi[(int(ano), g, k)] += f(x)
primeiro = {g: [{"ano": a, "pct": pi[(a, g, "prim")] / pi[(a, g, "v")]} for a in range(anos[0], QUEBRA)] for g in ("AFL", "Comparável")}
interm = {g: [{"ano": a, "pct": pi[(a, g, "interm")] / pi[(a, g, "v")], "v": pi[(a, g, "interm")]} for a in range(2018, ANO + 1)] for g in ("AFL", "Comparável")}

# ---------------- remuneração
sm = defaultdict(float)
for ano, g, s_, q_, smv in D["serie_media"]:
    sm[(int(ano), g, "s")] += f(s_)
    sm[(int(ano), g, "q")] += f(q_)
    sm[(int(ano), g, "sm")] += f(smv)
med = {(int(a), g): f(m) for a, g, _, _, _, m in D["serie_mediana"]}
sal_serie = {g: [{"ano": a, "media": sm[(a, g, "s")] / sm[(a, g, "q")], "mediana": med.get((a, g)), "sm": sm[(a, g, "sm")] / sm[(a, g, "q")]} for a in anos]
             for g in ("AFL", "Comparável")}
ss = defaultdict(float)
for g, sexo, escn, ordem, s_, q_ in D["sal_sexo_esc"]:
    ss[(g, sexo, escn, "s")] += f(s_)
    ss[(g, sexo, escn, "q")] += f(q_)


def media_ss(g, sexo=None, escn=None):
    s_ = sum(v for k, v in ss.items() if k[0] == g and (sexo is None or k[1] == sexo) and (escn is None or k[2] == escn) and k[3] == "s")
    q_ = sum(v for k, v in ss.items() if k[0] == g and (sexo is None or k[1] == sexo) and (escn is None or k[2] == escn) and k[3] == "q")
    return s_ / q_ if q_ else None


ESC = ["Fundamental Incompleto", "Fundamental Completo", "Médio Incompleto", "Médio Completo", "Superior Incompleto", "Superior Completo"]
remun = {}
for g in ("AFL", "Comparável"):
    remun[g] = {"media": media_ss(g), "razao_sexo": media_ss(g, "Mulher") / media_ss(g, "Homem"),
                "por_esc": {x: media_ss(g, escn=x) for x in ESC},
                "razao_sexo_esc": {x: (media_ss(g, "Mulher", x) / media_ss(g, "Homem", x)) if media_ss(g, "Homem", x) else None for x in ESC}}
rr = defaultdict(float)
for g, grupo, escn, ordem, s_, q_ in D["sal_raca_esc"]:
    rr[(g, grupo, escn, "s")] += f(s_)
    rr[(g, grupo, escn, "q")] += f(q_)


def media_rr(g, grupo, escn=None):
    s_ = sum(v for k, v in rr.items() if k[0] == g and k[1] == grupo and (escn is None or k[2] == escn) and k[3] == "s")
    q_ = sum(v for k, v in rr.items() if k[0] == g and k[1] == grupo and (escn is None or k[2] == escn) and k[3] == "q")
    return s_ / q_ if q_ else None


for g in ("AFL", "Comparável"):
    remun[g]["razao_raca"] = media_rr(g, "Negra") / media_rr(g, "Branca")
    remun[g]["razao_raca_esc"] = {x: (media_rr(g, "Negra", x) / media_rr(g, "Branca", x)) if media_rr(g, "Branca", x) else None for x in ESC}
mc = {(g, s, e_): f(m) for g, u, s, e_, a, m in D["mediana_cortes"]}
for g in ("AFL", "Comparável"):
    remun[g]["mediana"] = mc[(g, "Todos", "Todos")]
    remun[g]["mediana_sexo"] = {s: mc[(g, s, "Todos")] for s in ("Mulher", "Homem")}
afl_serie = sal_serie["AFL"]
remun["razao_afl_comp_media"] = [{"ano": a["ano"], "r": a["media"] / c["media"], "rm": (a["mediana"] / c["mediana"]) if a["mediana"] and c["mediana"] else None}
                                 for a, c in zip(afl_serie, sal_serie["Comparável"])]

out = {"ano": ANO, "anos": anos, "emp": emp_ind, "serie": serie, "contratos": contratos, "ranking": ranking[:40], "pos_afl": pos_afl,
       "n_div": len(ranking), "ranking_cresc": ranking_cresc[:12], "pos_afl_cresc": pos_afl_cresc, "n_div_cresc": len(ranking_cresc),
       "atividades": atividades, "ufs": ufs, "perfil": perfil, "cbo": cbo, "primeiro": primeiro, "interm": interm,
       "sal_serie": sal_serie, "remun": remun}
(RAIZ / "docs" / "previa" / "indicadores.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: out[k] for k in ("emp", "contratos", "pos_afl", "n_div", "pos_afl_cresc", "n_div_cresc")}, ensure_ascii=False, indent=1))
print(json.dumps({g: {k: v for k, v in out["perfil"][g].items() if k != "piramide"} for g in ("AFL", "Comparável")}, ensure_ascii=False, indent=1))
print(json.dumps({g: {k: v for k, v in out["remun"][g].items()} for g in ("AFL", "Comparável")}, ensure_ascii=False, indent=1))
print(json.dumps(out["remun"]["razao_afl_comp_media"][-5:], ensure_ascii=False))
print([(a["nome"][:30], round(a["v"]), round(a["var"], 3), round(a["media"])) for a in atividades])
print([(c["nome"], round(c["v"]), round(c["mulheres"], 2)) for c in cbo[:8]])
print([(u["uf"], round(u["afl"]), round(u["part_comp"], 3), round(u["razao"], 2)) for u in ufs[:6]])
print([(r["nome"][:30], round(r["cresc"], 3)) for r in ranking_cresc[:6]])
print(out["interm"]["AFL"][-3:], out["primeiro"]["AFL"][-3:])
