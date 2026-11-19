# -*- coding: utf-8 -*-
"""Rankings de escolaridade e de deficiência: sem botão de nível/tipo escolhido, os números somam tudo
(todos os níveis de escolaridade; todos os empregados com deficiência), em vez de cair em Médio completo / Física."""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MED = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl"
GER = RAIZ / "scripts" / "ranking_deficiencia.py"
ANO = "REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A"


def trocar(t, a, b, minimo=1):
    n = t.count(a)
    if n < minimo:
        raise SystemExit(f"não achei ({n}x): {a[:90]}")
    return t.replace(a, b), n


t = MED.read_text(encoding="utf-8")
cont = {}

# ---- escolaridade: nível vazio = todos os níveis
t, cont["nivel"] = trocar(t, 'VAR Niv = COALESCE(SELECTEDVALUE(D_Ct_Nivel[nivel]), "Médio completo")', "VAR Niv = SELECTEDVALUE(D_Ct_Nivel[nivel])", 6)
padrao = re.compile(r', (CALCULATE\(\[(Empregos|Remuneracao_Media)\], ' + re.escape(ANO) +
                    r', KEEPFILTERS\(D_Escolaridade\[escolaridade_agrupada\] IN \{"Médio Completo"\}\)\))(\))')
t, cont["switch"] = padrao.subn(lambda m: f', "Médio completo", {m.group(1)}, CALCULATE([{m.group(2)}], {ANO}){m.group(3)}', t)
nome_niv = 'SWITCH(Niv, "Até fundamental", "até o fundamental completo", "Médio incompleto", "médio incompleto", "Superior", "superior (completo ou não)", "médio completo")'
t, cont["nome_nivel"] = trocar(t, nome_niv, nome_niv[:-len('"médio completo")')] + '"Médio completo", "médio completo", "todos os níveis")', 3)

# ---- deficiência: tipo vazio = todos os empregados com deficiência
t, cont["tipo"] = trocar(t, 'VAR T = COALESCE(SELECTEDVALUE(D_Ct_Def[tipo]), "Física")', "VAR T = SELECTEDVALUE(D_Ct_Def[tipo])")
filtro = ('KEEPFILTERS(FILTER(ALL(F_rais[tipo_deficiencia], F_rais[indicador_portador_deficiencia]), '
          'IF(ISBLANK(T), F_rais[indicador_portador_deficiencia] = "Sim", F_rais[tipo_deficiencia] = T)))')
t, cont["filtro_def"] = trocar(t, "KEEPFILTERS(F_rais[tipo_deficiencia] = T)", filtro, 2)
t, cont["nome_tipo"] = trocar(t, 'SWITCH(COALESCE(SELECTEDVALUE(D_Ct_Def[tipo]), "Física"), ', "SWITCH(SELECTEDVALUE(D_Ct_Def[tipo]), ", 3)
t, cont["nome_tipo_fim"] = trocar(t, '"Reabilitado", "reabilitado", "física")', '"Reabilitado", "reabilitado", "todos os tipos")', 3)
t = t.replace("(Física quando nada está escolhido)", "(vazio quando nada está escolhido: soma todos os tipos)")
MED.write_text(t, encoding="utf-8", newline="")
print(cont)

# ---- gerador do ranking de deficiência, para não voltar ao jeito antigo
g = GER.read_text(encoding="utf-8")
g = g.replace("VAR T = COALESCE(SELECTEDVALUE(D_Ct_Def[tipo]), \"Física\")", "VAR T = SELECTEDVALUE(D_Ct_Def[tipo])")
g = g.replace("KEEPFILTERS(F_rais[tipo_deficiencia] = T)", filtro)
g = g.replace("SWITCH(COALESCE(SELECTEDVALUE(D_Ct_Def[tipo]), \"Física\"), ", "SWITCH(SELECTEDVALUE(D_Ct_Def[tipo]), ")
g = g.replace('"Reabilitado", "reabilitado", "física")', '"Reabilitado", "reabilitado", "todos os tipos")')
g = g.replace("(Física quando nada está escolhido)", "(vazio quando nada está escolhido: soma todos os tipos)")
GER.write_text(g, encoding="utf-8", newline="")
