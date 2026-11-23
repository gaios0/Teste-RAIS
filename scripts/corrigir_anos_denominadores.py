# -*- coding: utf-8 -*-
"""Correções no painel RAIS OFICIAL.

1. D_Ano vai de 2009 até o ano corrente (antes parava em 2025).
2. Ano_Ref = ano escolhido no filtro de ano (ou o último ano da base), sem depender dos demais filtros.
   Antes era MAX(F_rais[ano]) depois de todos os filtros: um filtro que zerasse o ano mais recente trocava o ano sem aviso.
3. Participações por escolaridade e por idade: o total deixa de fora "Ignorado/Faltante" e "Não categorizado",
   para as faixas somarem 100% (mesma regra de raça, que já divide só por quem declarou).
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent / "RAIS OFICIAL"
DEF = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables"
MED = DEF / "_medidas.tmdl"

SEM_ESC = 'D_Escolaridade[escolaridade_agrupada] <> "Ignorado/Faltante"'
SEM_IDADE = 'D_FaixaIdade[faixa_idade] <> "Não categorizado"'
ANO = "REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = A"
cont = {}


def troca(t, a, b, chave, minimo=1):
    n = t.count(a)
    if n < minimo:
        sys.exit(f"{chave}: achei {n}x, esperava {minimo}+ :: {a[:100]}")
    cont[chave] = cont.get(chave, 0) + n
    return t.replace(a, b)


def em_medida(t, nome, f):
    m = re.search(r"(?ms)^\tmeasure " + re.escape(nome) + r" =\n.*?(?=^\t(?:///|measure |partition ))", t)
    if not m:
        sys.exit(f"medida não achada: {nome}")
    novo = f(m.group(0))
    if novo == m.group(0):
        sys.exit(f"nada mudou em {nome}")
    cont[nome] = 1
    return t[:m.start()] + novo + t[m.end():]


# ---- 1. D_Ano
da = DEF / "D_Ano.tmdl"
s = da.read_text(encoding="utf-8")
s = troca(s, "// Tabela local: a D_Ano não existe mais no Painel_RAIS. Anos da F_rais remota: 2009 a 2025 (incluir o ano novo aqui quando a base crescer).",
          "// Tabela local: a D_Ano não existe mais no Painel_RAIS. Vai de 2009 ao ano corrente, igual à D_Calendario, e cresce sozinha.", "D_Ano comentário")
s = troca(s, "Anos = List.Numbers(2009, 2025 - 2009 + 1),", "Anos = List.Numbers(2009, Date.Year(DateTime.LocalNow()) - 2009 + 1),", "D_Ano lista")
da.write_text(s, encoding="utf-8", newline="")

t = MED.read_text(encoding="utf-8")

# ---- 2. Ano_Ref
t = troca(t, "\tmeasure Ano_Ref = CALCULATE(MAX(F_rais[ano]))\n",
          "\tmeasure Ano_Ref =\n"
          "\t\t\t// Ano escolhido no filtro de ano (ou no eixo do gráfico); sem filtro de ano, o último ano da base.\n"
          "\t\t\t// Os outros filtros (UF, CBO, intermitente...) não mudam o ano: sem dados, o número fica vazio.\n"
          "\t\t\tCALCULATE(MAX(F_rais[ano]), REMOVEFILTERS(), TREATAS(VALUES(D_Calendario[Ano]), F_rais[ano]))\n", "Ano_Ref")

# ---- 3a. totais com REMOVEFILTERS(D_Escolaridade) / REMOVEFILTERS(D_FaixaIdade) sem faixa = total sem ignorados
t = troca(t, "REMOVEFILTERS(D_Escolaridade))", f"REMOVEFILTERS(D_Escolaridade), {SEM_ESC})", "total escolaridade", 5)
t = troca(t, "REMOVEFILTERS(D_FaixaIdade))", f"REMOVEFILTERS(D_FaixaIdade), {SEM_IDADE})", "total idade (pirâmide)", 3)

# ---- 3b. KPIs de perfil
den_esc = f"VAR Den = CALCULATE([Empregos_Ref], KEEPFILTERS({SEM_ESC}))"
den_idade = f"VAR Den = CALCULATE([Empregos_Ref], KEEPFILTERS({SEM_IDADE}))"
for n, d in (("Perf_MedioMais", den_esc), ("Perf_Superior", den_esc), ("Perf_Ate24", den_idade)):
    t = em_medida(t, n, lambda b, d=d: b.replace("VAR Den = [Empregos_Ref]", d))


# ---- 3c. indicadores (Quem contrata): denominador sem ignorados nos de idade e de escolaridade
def ind(b):
    linhas = b.split("\n")
    for i, l in enumerate(linhas):
        f = SEM_IDADE if re.search(r'"(Até 24 anos|55 anos ou mais)", DIVIDE\(', l) else SEM_ESC if '"Superior", DIVIDE(' in l else None
        if f:
            k = l.rfind(f"{ANO})")
            if k < 0:
                sys.exit("indicador: denominador não achado: " + l[:80])
            linhas[i] = l[:k] + f"{ANO}, KEEPFILTERS({f}))" + l[k + len(ANO) + 1:]
    return "\n".join(linhas)


for n in ("Ind_Valor_Ctx", "Ind_Valor_Ano"):
    t = em_medida(t, n, ind)

# ---- 3d. ranking por escolaridade: total e "todos os níveis" sem ignorados
TOT = f"CALCULATE([Empregos], {ANO})"
TOT_OK = f"CALCULATE([Empregos], {ANO}, KEEPFILTERS({SEM_ESC}))"
for n in ("Ct_Esc_Qtd", "Ct_Esc_Rep", "Ct_Esc_Tot", "KPI_Ct_Esc_AFL_HTML"):
    t = em_medida(t, n, lambda b: b.replace(TOT + ")", TOT_OK + ")").replace(TOT + ",", TOT_OK + ",") if n != "KPI_Ct_Esc_AFL_HTML"
                  else b.replace(f"VAR T = {TOT}\n", f"VAR T = {TOT_OK}\n"))
t = em_medida(t, "KPI_Ct_Esc_Total_HTML", lambda b: b.replace(f"VAR T = CALCULATE([Empregos], {ANO}, KEEPFILTERS(SetFiltro))",
                                                              f"VAR T = CALCULATE([Empregos], {ANO}, KEEPFILTERS(SetFiltro), KEEPFILTERS({SEM_ESC}))"))

MED.write_text(t, encoding="utf-8", newline="")
for k, v in cont.items():
    print(f"{v:>3}x {k}")
