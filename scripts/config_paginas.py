"""Configuração de cada página: acentos dos KPIs, legendas fixas, trilho de setores e nota de rodapé (usada pelo fundo e pelo gerador de páginas)."""
LARANJA, CINZA = "#F58220", "#434446"
NOTA_QUEBRA = ("A RAIS passou a vir do eSocial em 2022 e incluiu empregos de empresas pequenas que ficavam de fora: "
               "2022 em diante não se compara com os anos anteriores.")
LEG_SERIE = [("AFL", LARANJA, "linha"), ("Comparáveis (referência)", CINZA, "linha")]

LEG_SERIE_TOTAL = LEG_SERIE + [("Seleção atual (mercado ou setores filtrados)", "#98A2B3", "linha")]

PAGINAS = {
    ("Empregos", "Todos os setores"): dict(nome="empregos-todos", acentos=["#17B26A", LARANJA, "#1D1E21"], legendas={"L2A": LEG_SERIE_TOTAL}, trilho=True, nota=NOTA_QUEBRA),
    ("Empregos", "AFL"): dict(nome="empregos-afl", acentos=["#17B26A", LARANJA, "#1D1E21"], legendas={"L2A": LEG_SERIE}, trilho=False, nota=NOTA_QUEBRA),
}

# ---- Quem trabalha, Quanto ganha, Quem contrata
VIOLETA, CINZA_H = "#7F56D9", "#98A2B3"
LEG_PIR = [("Mulheres", VIOLETA, "quadro"), ("Homens", CINZA_H, "quadro")]
LEG_AFL_COMP = [("AFL", LARANJA, "quadro"), ("Comparáveis (referência)", CINZA, "quadro")]
LEG_REM = [("AFL · média", LARANJA, "linha"), ("AFL · mediana", LARANJA, "tracejado"), ("Comparáveis · média", CINZA, "linha"), ("Comparáveis · mediana", CINZA, "tracejado")]
NOTA_PERFIL = (NOTA_QUEBRA + " Cor/raça: até 2022, de 24% a 33% dos empregados não declaravam; os percentuais são sobre quem declarou.")
NOTA_REM = ("Valores nominais (sem correção pela inflação), remuneração de dezembro. " + NOTA_QUEBRA)
NOTA_CONTRATA = ("Primeiro emprego só existe até 2021 e trabalho intermitente desde 2018. Divisões com menos de 50 mil empregos ficam fora do ranking. " + NOTA_QUEBRA)
ACENTOS_PERFIL = ["#7F56D9", LARANJA, "#1D1E21"]
ACENTOS_REM = ["#17B26A", "#7F56D9", "#1D1E21"]
ACENTOS_CONTRATA = [LARANJA, "#17B26A", "#1D1E21"]

for _rec, _trilho, _l2a in (("Todos os setores", True, None), ("AFL", False, None)):
    sfx = "todos" if _rec == "Todos os setores" else "afl"
    PAGINAS[("Quem trabalha", _rec)] = dict(nome=f"trabalha-{sfx}", acentos=ACENTOS_PERFIL, legendas={"L2A": LEG_PIR}, trilho=False, nota=NOTA_PERFIL)
    PAGINAS[("Quanto ganha", _rec)] = dict(nome=f"ganha-{sfx}", acentos=ACENTOS_REM, legendas={"L2A": LEG_REM, "L2B": LEG_AFL_COMP, "L3A": LEG_AFL_COMP}, trilho=False, nota=NOTA_REM)
    PAGINAS[("Quem contrata", _rec)] = dict(nome=f"contrata-{sfx}", acentos=ACENTOS_CONTRATA, legendas={"L2B": LEG_SERIE}, trilho=False, trilho_ind=True, nota=NOTA_CONTRATA)
