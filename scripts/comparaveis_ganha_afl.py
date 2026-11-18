"""Quanto ganha · AFL: onde se lia "Referência" passa a ler "Comparáveis" (tooltips e nomes das séries do gráfico).

Os tooltips Tip_Rem_*_Total_HTML são compartilhados com a página Todos os setores, que continua dizendo "Referência": a troca só acontece
quando a página de origem é do recorte AFL (filtro de página D_Cnae[setor_afl] = "Sim", o mesmo critério dos demais tooltips).
A legenda desenhada no fundo é tratada por ajuste_legendas.py. Idempotente.
"""
import re
from pathlib import Path

import pbir_rais as pb

RAIZ = Path(__file__).resolve().parents[1]
TMDL = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl"
SERIE_AFL = pb.DEF / "pages" / "a3d1f2c4e6b8097a1c32" / "visuals" / "cde6fd3756841ddf81fc" / "visual.json"


def tooltips():
    t = TMDL.read_bytes().decode("utf-8")
    padrao = re.compile(r'(measure Tip_Rem_\w+_Total_HTML = )SUBSTITUTE\(\[(Tip_Rem_\w+_HTML)\], "Comparáveis", "Referência"\)')
    t, n = padrao.subn(lambda m: f'{m.group(1)}IF(SELECTEDVALUE(D_Cnae[setor_afl]) = "Sim", [{m.group(2)}], '
                                 f'SUBSTITUTE([{m.group(2)}], "Comparáveis", "Referência"))', t)
    TMDL.write_bytes(t.encode("utf-8"))
    print("tooltips ajustados:", n)


def series():
    t = SERIE_AFL.read_text(encoding="utf-8")
    n = t.count("Referência · média")
    SERIE_AFL.write_text(t.replace("Referência · média", "Comparáveis · média"), encoding="utf-8")
    print("nomes de série trocados:", n)


if __name__ == "__main__":
    tooltips()
    series()
