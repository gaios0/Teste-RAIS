"""Trava contra regravação de edições manuais: o usuário ajusta o PBIP no Desktop e salva; os geradores regravam páginas e TMDL.

Antes de regravar, exige que as pastas afetadas estejam sem alterações não commitadas (use --forcar só depois de commitar ou copiar o estado atual).
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
IGNORAR = ("editorSettings.json", "__pycache__")


def exigir_limpo(*caminhos):
    if "--forcar" in sys.argv:
        return
    saida = subprocess.run(["git", "status", "--porcelain", "--", *map(str, caminhos)], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8").stdout
    sujos = [l for l in saida.splitlines() if l.strip() and not any(i in l for i in IGNORAR)]
    if sujos:
        print("Há alterações não commitadas (possíveis edições manuais no Desktop) em:")
        for l in sujos[:15]:
            print("  ", l)
        raise SystemExit("Interrompido para não sobrescrevê-las. Commite ou copie o estado atual e rode de novo (ou use --forcar).")
