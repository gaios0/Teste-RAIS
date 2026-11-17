"""Verificação estrutural da aba Quem contrata v2 (NÃO substitui o teste no Power BI Desktop).

Confere: JSONs válidos, toda medida/coluna/tabela usada pelos visuais existe no modelo, fundos registrados, e que cada medida
nova está no TMDL com os blocos esperados.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
R = RAIZ / "RAIS Emprego Formal.Report" / "definition"
M = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables"
texto_medidas = (M / "_medidas.tmdl").read_text(encoding="utf-8")
medidas = set(re.findall(r"^\tmeasure (\w+)", texto_medidas, re.M))
tabelas = {p.stem for p in M.glob("*.tmdl")}
colunas = {}
for p in M.glob("*.tmdl"):
    colunas[p.stem] = set(re.findall(r"^\tcolumn '?([^'\r\n]+?)'?\s*$", p.read_text(encoding="utf-8"), re.M))
PAGINAS = ["a3d1f2c4e6b8097a1c41", "a3d1f2c4e6b8097a1c42", "a3d1f2c4e6b8097a1c81", "a3d1f2c4e6b8097a1c82", "a3d1f2c4e6b8097a1c83"]
ref = re.compile(r'"Expression":\s*\{\s*"SourceRef":\s*\{\s*"Entity":\s*"([^"]+)"\s*\}\s*\},\s*"Property":\s*"([^"]+)"')
problemas, n = [], 0
for pg in PAGINAS:
    json.loads((R / "pages" / pg / "page.json").read_text(encoding="utf-8"))
    for f in (R / "pages" / pg / "visuals").glob("*/visual.json"):
        n += 1
        t = f.read_text(encoding="utf-8")
        json.loads(t)
        for e, pr in ref.findall(t):
            if e == "_medidas":
                if pr not in medidas:
                    problemas.append(f"medida ausente: {pr} ({pg}/{f.parent.name})")
            elif e not in tabelas:
                problemas.append(f"tabela ausente: {e}")
            elif pr not in colunas[e] and pr not in medidas:
                problemas.append(f"coluna ausente: {e}[{pr}]")
json.loads((R / "report.json").read_text(encoding="utf-8"))
json.loads((R / "pages" / "pages.json").read_text(encoding="utf-8"))
print("visuais lidos:", n, "· problemas:", len(problemas))
for p in sorted(set(problemas)):
    print("  ", p)
rep = (R / "report.json").read_text(encoding="utf-8")
for pg in PAGINAS[:2]:
    t = (R / "pages" / pg / "page.json").read_text(encoding="utf-8")
    a = re.search(r"(contrata-[a-z]+-bg\d+\.png)", t).group(1)
    existe = (RAIZ / "RAIS Emprego Formal.Report" / "StaticResources" / "RegisteredResources" / a).exists()
    print(pg, a, "arquivo:", existe, "registrado:", a in rep)
# medidas novas: todas referenciadas por outra medida ou visual existem
import dax_contrata2
novas = {m[0] for m in dax_contrata2.medidas()}
usadas = set(re.findall(r"\[(Ct_\w+|KPI_Ct_\w+|Titulo_Ct_\w+)\]", " ".join(m[2] for m in dax_contrata2.medidas())))
print("medidas novas:", len(novas), "· no TMDL:", len(novas & medidas), "· referências internas sem definição:", sorted(usadas - novas))
refs_modelo = re.findall(r"\[([A-Za-z_][A-Za-z0-9_]*)\]", " ".join(m[2] for m in dax_contrata2.medidas()))
col_conhecidas = {c for cs in colunas.values() for c in cs}
desconhecidas = sorted({r for r in refs_modelo if r not in medidas and r not in col_conhecidas})
print("nomes entre colchetes que não são medida nem coluna:", desconhecidas)
