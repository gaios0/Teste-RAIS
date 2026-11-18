"""Imprime a definição de medidas do _medidas.tmdl (linhas longas truncadas). Uso: python ver_medida.py Nome1 Nome2 ... [--largura 400]"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
TMDL = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
largura = int(sys.argv[sys.argv.index("--largura") + 1]) if "--largura" in sys.argv else 400
if "--largura" in sys.argv:
    args = [a for a in args if a != str(largura)]
linhas = TMDL.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n")
for nome in args:
    achou = False
    for i, l in enumerate(linhas):
        m = re.match(r"^\tmeasure (\w+)", l)
        if m and (m.group(1) == nome or (nome.endswith("*") and m.group(1).startswith(nome[:-1]))):
            achou = True
            j = i + 1
            while j < len(linhas) and (linhas[j].startswith("\t\t") or linhas[j] == ""):
                j += 1
            print("=====", m.group(1), f"(linha {i + 1})")
            for x in linhas[i:j]:
                if x.strip():
                    print(x if len(x) <= largura else x[:largura] + " …")
    if not achou:
        print("=====", nome, "NÃO ENCONTRADA")
