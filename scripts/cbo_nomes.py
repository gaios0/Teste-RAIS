"""Troca o código CBO (F_rais[cbo_2002]) pelo nome da ocupação (D_Cbo[ocupacao]).

A base nova só traz o código em F_rais. O nome vem de D_Cbo, ligada por
F_rais[cbo_2002] -> D_Cbo[cbo_2002]. Edita no lugar: medidas, visuais e geradores.
"""
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MODELO = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl"
PAGINAS = RAIZ / "RAIS Emprego Formal.Report" / "definition" / "pages"
SCRIPTS = RAIZ / "scripts"

# Medidas e geradores: rank, líder e tooltip passam a usar o nome da ocupação.
TROCAS_DAX = [
    ("RANKX(ALLSELECTED(F_rais[cbo_2002])", "RANKX(ALLSELECTED(D_Cbo[ocupacao])"),
    ("VALUES(F_rais[cbo_2002])", "VALUES(D_Cbo[ocupacao])"),
    ("DESC, F_rais[cbo_2002], ASC", "DESC, D_Cbo[ocupacao], ASC"),
    ("CONCATENATEX(Lider1, F_rais[cbo_2002]", "CONCATENATEX(Lider1, D_Cbo[ocupacao]"),
    ("TREATAS({Nome}, F_rais[cbo_2002])", "TREATAS({Nome}, D_Cbo[ocupacao])"),
    ("SELECTEDVALUE(F_rais[cbo_2002])", "SELECTEDVALUE(D_Cbo[ocupacao])"),
    ("REMOVEFILTERS(F_rais[cbo_2002])", "REMOVEFILTERS(D_Cbo)"),
]
TROCAS_PY = TROCAS_DAX + [
    ('pb.coluna("F_rais", "cbo_2002")', 'pb.coluna("D_Cbo", "ocupacao")'),
    ("SUMMARIZECOLUMNS(F_rais[cbo_2002]", "SUMMARIZECOLUMNS(D_Cbo[ocupacao]"),
]


def trocar_texto(caminho, trocas):
    txt = caminho.read_text(encoding="utf-8")
    novo = txt
    for a, b in trocas:
        novo = novo.replace(a, b)
    if novo != txt:
        caminho.write_text(novo, encoding="utf-8", newline="")
        print("ok", caminho.relative_to(RAIZ))


def trocar_json(no):
    n = 0
    if isinstance(no, dict):
        col = no.get("Column")
        if isinstance(col, dict) and col.get("Property") == "cbo_2002":
            ref = col.get("Expression", {}).get("SourceRef", {})
            if ref.get("Entity") == "F_rais":
                ref["Entity"] = "D_Cbo"
                col["Property"] = "ocupacao"
                n += 1
        for k, v in list(no.items()):
            if k == "queryRef" and v == "F_rais.cbo_2002":
                no[k] = "D_Cbo.ocupacao"
            elif k == "nativeQueryRef" and v == "cbo_2002":
                no[k] = "ocupacao"
            else:
                n += trocar_json(v)
    elif isinstance(no, list):
        for v in no:
            n += trocar_json(v)
    return n


def main():
    trocar_texto(MODELO, TROCAS_DAX)
    for nome in ("dax_rais2.py", "dax_tooltips.py", "pagina_rais.py", "testar_paginas.py", "dados_previa.py"):
        trocar_texto(SCRIPTS / nome, TROCAS_PY)
    for arq in PAGINAS.glob("*/visuals/*/visual.json"):
        txt = arq.read_text(encoding="utf-8")
        if "cbo_2002" not in txt:
            continue
        dado = json.loads(txt)
        n = trocar_json(dado)
        arq.write_text(json.dumps(dado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="")
        print("ok", arq.relative_to(RAIZ), n, "campos")
    sobra = [str(p.relative_to(RAIZ)) for p in list(PAGINAS.rglob("*.json")) + [MODELO]
             if "F_rais[cbo_2002]" in p.read_text(encoding="utf-8") or "F_rais.cbo_2002" in p.read_text(encoding="utf-8")]
    if sobra:
        print("SOBROU:", sobra)
        sys.exit(1)


if __name__ == "__main__":
    main()
