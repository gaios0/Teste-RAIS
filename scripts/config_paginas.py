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
