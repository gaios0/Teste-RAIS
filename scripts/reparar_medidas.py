"""Diagnóstico/reparo do _medidas.tmdl: compara o arquivo atual (sem as medidas Ct_*) com a versão do Git e, se só houver sobras
(linhas em branco e formatStringDefinition soltos), refaz o arquivo a partir da versão do Git + as medidas novas."""
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ARQ = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl"
REL = "RAIS Emprego Formal.SemanticModel/definition/tables/_medidas.tmdl"
MEU = re.compile(r"(Ct_|KPI_Ct_|Titulo_Ct_|Manchete_Ct_|Tip_Ct_)")


def sem_meus_blocos(t):
    """Remove (por linhas) os blocos das medidas minhas, as linhas formatStringDefinition soltas e as linhas em branco."""
    L = t.split("\n")
    saida, i = [], 0
    while i < len(L):
        l = L[i]
        m = re.match(r"^\tmeasure (\w+)", l)
        if m and MEU.match(m.group(1)):
            while saida and saida[-1].startswith("\t///"):
                saida.pop()                                  # doc da medida
            i += 1
            while i < len(L) and (L[i].startswith("\t\t") or L[i] == ""):
                i += 1                                       # corpo, propriedades e filhos
            continue
        saida.append(l)
        i += 1
    return [x for x in saida if x.strip() and not x.startswith("\t\tformatStringDefinition")]


def main():
    atual = ARQ.read_bytes().decode("utf-8").replace("\r\n", "\n")
    head = subprocess.run(["git", "show", f"HEAD:{REL}"], cwd=RAIZ, capture_output=True).stdout.decode("utf-8").replace("\r\n", "\n")
    a, h = sem_meus_blocos(atual), sem_meus_blocos(head)
    print("linhas úteis (sem medidas Ct_, sem brancos): atual", len(a), "· git", len(h), "· iguais:", a == h)
    if a != h:
        for n, (x, y) in enumerate(zip(a, h)):
            if x != y:
                print("primeira diferença na linha útil", n, "\n  atual:", x[:120], "\n  git  :", y[:120])
                break
    if "--reparar" in sys.argv and a == h:
        ARQ.write_bytes(head.replace("\n", "\r\n").encode("utf-8"))
        print("arquivo restaurado da versão do Git (rode contrata_v2.py --so-medidas em seguida)")


if __name__ == "__main__":
    main()
