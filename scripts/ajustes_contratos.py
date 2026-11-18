"""Tipos de contrato (Empregos · AFL) com o filtro Intermitente.

Emp_Contratos_HTML e Titulo_Emp_Contrato_HTML filtravam F_rais[trabalho_intermitente] / [modalidade_contrato] / [trabalho_parcial] com filtros
booleanos soltos no CALCULATE. Um filtro booleano SUBSTITUI o filtro que o segmentador já aplica na mesma coluna: com "Intermitente = Sim",
o total (denominador) respeitava o segmentador e os numeradores não (CLT contado entre os NÃO intermitentes ÷ total dos intermitentes = 9060,6%).
Com KEEPFILTERS as categorias passam a ser subconjuntos do que o filtro deixou: Sim -> só "Intermitente" (100%); Não -> as demais categorias
somam 100%; sem filtro, os números são os mesmos de antes. Idempotente.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
TMDL = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl"
COND = re.compile(r'(?<!KEEPFILTERS\()(F_rais\[(?:trabalho_intermitente|modalidade_contrato|trabalho_parcial)\] (?:<>|=|IN) (?:"[^"]*"|\{[^}]*\}))')


def corpo(t, nome):
    ini = t.index(f"\tmeasure {nome} =")
    linhas = t[ini:].split("\n")
    n = 1
    while n < len(linhas) and (linhas[n].startswith("\t\t") or linhas[n] == ""):
        n += 1
    return ini, ini + len("\n".join(linhas[:n]))


def main():
    bruto = TMDL.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in bruto else "\n"
    t = bruto.replace("\r\n", "\n")
    for nome in ("Emp_Contratos_HTML", "Titulo_Emp_Contrato_HTML"):
        ini, fim = corpo(t, nome)
        novo, n = COND.subn(r"KEEPFILTERS(\1)", t[ini:fim])
        print(f"{nome}: {n} condições protegidas com KEEPFILTERS" if n else f"{nome}: já ajustada")
        t = t[:ini] + novo + t[fim:]
    TMDL.write_bytes(t.replace("\n", eol).encode("utf-8"))


if __name__ == "__main__":
    main()
