# -*- coding: utf-8 -*-
"""Lista (e com --aplicar, apaga) as medidas de _medidas que nenhum visual, página ou tooltip usa,
nem direta nem indiretamente (por outra medida usada).

Uso: python scripts/limpar_medidas.py            -> só lista
     python scripts/limpar_medidas.py --aplicar  -> apaga do _medidas.tmdl
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SM = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition"
REP = RAIZ / "RAIS Emprego Formal.Report" / "definition"
ARQ = SM / "tables" / "_medidas.tmdl"

texto = ARQ.read_text(encoding="utf-8")
linhas = texto.split("\n")


def nome_de(s):
    s = s.strip()
    return s[1:-1].replace("''", "'") if s.startswith("'") else s


# blocos de medida: linhas /// + "\tmeasure" + tudo até a próxima linha com 1 tab
blocos = []   # (nome, ini, fim)  fim exclusivo
i = 0
while i < len(linhas):
    m = re.match(r"^\tmeasure ('(?:[^']|'')+'|[^=]+?)\s*=", linhas[i])
    if m:
        ini = i
        while ini > 0 and linhas[ini - 1].startswith("\t///"):
            ini -= 1
        fim = i + 1
        while fim < len(linhas) and not (linhas[fim].startswith("\t") and not linhas[fim].startswith("\t\t")):
            fim += 1
        # devolve as linhas /// da próxima medida
        while fim > i + 1 and linhas[fim - 1].startswith("\t///"):
            fim -= 1
        blocos.append((nome_de(m.group(1)), ini, fim))
        i = fim
    else:
        i += 1
NOMES = {b[0] for b in blocos}
CORPO = {n: "\n".join(linhas[a:b]) for n, a, b in blocos}

RE_STR = re.compile(r'"(?:[^"]|"")*"|//[^\n]*|/\*.*?\*/', re.S)


def refs(dax):
    d = RE_STR.sub('""', dax)
    return {x for x in re.findall(r"\[([^\]]+)\]", d) if x in NOMES}


# 1) usadas no relatório (visuais, páginas, tooltips, filtros, formatação condicional)
usadas = set()
for f in REP.rglob("*.json"):
    t = f.read_text(encoding="utf-8")
    for n in re.findall(r'"Property":\s*"([^"]+)"', t):
        if n in NOMES:
            usadas.add(n)
    for n in re.findall(r'_medidas\.([^"\s,\)]+)', t):
        if n in NOMES:
            usadas.add(n)
diretas = set(usadas)

# 2) usadas por outras tabelas do modelo (colunas/tabelas calculadas)
for f in (SM / "tables").glob("*.tmdl"):
    if f.name != "_medidas.tmdl":
        usadas |= refs(f.read_text(encoding="utf-8"))

# 3) fecho: o que as medidas usadas usam
fila = list(usadas)
while fila:
    n = fila.pop()
    for r in refs(CORPO[n]):
        if r not in usadas:
            usadas.add(r)
            fila.append(r)

sobra = [b for b in blocos if b[0] not in usadas]
print(f"medidas={len(NOMES)} usadas_no_relatorio={len(diretas)} usadas_total={len(usadas)} sem_uso={len(sobra)}")
for n, _, _ in sorted(sobra, key=lambda b: b[0].lower()):
    print(" -", n)

if "--aplicar" in sys.argv and sobra:
    apagar = set()
    for _, a, b in sobra:
        apagar.update(range(a, b))
    novo = "\n".join(l for k, l in enumerate(linhas) if k not in apagar)
    novo = re.sub(r"\n{3,}", "\n\n", novo)
    ARQ.write_text(novo, encoding="utf-8", newline="")
    print(f"apagadas {len(sobra)} medidas de {ARQ.name}")
