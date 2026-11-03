"""Fundação do modelo local do painel RAIS: calendário padrão do time, tabela de medidas e medidas-base.

- D_Calendario (importada): o M padrão do time, de 01/01/2009 ao fim do ano corrente (a fato é DirectQuery e só tem `ano`,
  então o M não lê a menor e a maior data dela), mais `Fonte RAIS` e `Trecho da Série` (quebra do eSocial em 2022).
- Relações muitos-para-muitos D_Calendario[Ano] → F_rais[ano] e F_Mediana[ano] (o calendário filtra a fato).
- _medidas: estoque de 31/12 de um único ano (nunca soma anos), variação que não atravessa a quebra de 2022,
  crescimento médio dentro do trecho, remuneração de dezembro (média = soma/quantidade de salários válidos; mediana da
  F_Mediana) e as versões AFL e Comparável.
Idempotente: reescreve D_Calendario.tmdl e _medidas.tmdl, e só acrescenta relações e refs que faltam.
"""
import re
import uuid
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DEF = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition"
TAB = DEF / "tables"
QUEBRA = 2022          # primeiro ano do eSocial (grupo 3): não comparável com 2021
INICIO = 2009          # primeiro ano da base

# ------------------------------------------------------------------ calendário
M_CALENDARIO = r'''let
    // Calendário padrão do time. A fato da RAIS é DirectQuery e só tem o ano, então o intervalo é fixo:
    // de 01/01/2009 (início da base) ao fim do ano corrente.
    DataInicial = #date(2009, 1, 1),
    DataFinal = Date.EndOfYear(Date.From(DateTime.LocalNow())),
    Duracao = Duration.Days(DataFinal - DataInicial) + 1,
    Fonte = List.Dates(DataInicial, Duracao, #duration(1, 0, 0, 0)),
    #"Convertido para Tabela" = Table.FromList(Fonte, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Convertido para Tabela",{{"Column1", type date}}),
    #"Colunas Renomeadas" = Table.RenameColumns(#"Tipo Alterado",{{"Column1", "Data"}}),
    #"Ano Inserido" = Table.AddColumn(#"Colunas Renomeadas", "Ano", each Date.Year([Data]), Int64.Type),
    #"Mês Inserido" = Table.AddColumn(#"Ano Inserido", "Mês", each Date.Month([Data]), Int64.Type),
    #"Nome do Mês Inserido" = Table.AddColumn(#"Mês Inserido", "Nome do Mês", each Date.MonthName([Data]), type text),
    #"Dia Inserido" = Table.AddColumn(#"Nome do Mês Inserido", "Dia", each Date.Day([Data]), Int64.Type),
    #"Dia da Semana Inserido" = Table.AddColumn(#"Dia Inserido", "Dia da Semana", each Date.DayOfWeek([Data]), Int64.Type),
    #"Nome do Dia Inserido" = Table.AddColumn(#"Dia da Semana Inserido", "Nome do Dia", each Date.DayOfWeekName([Data]), type text),
    #"Coluna Condicional Adicionada" = Table.AddColumn(#"Nome do Dia Inserido", "Semestre", each if [Mês] <= 6 then "S1" else "S2"),
    #"Tipo Alterado1" = Table.TransformColumnTypes(#"Coluna Condicional Adicionada",{{"Semestre", type text}}),
    #"Coluna Condicional Adicionada1" = Table.AddColumn(#"Tipo Alterado1", "Trimestre", each if [Mês] <= 3 then "T1" else if [Mês] <= 6 then "T2" else if [Mês] <= 9 then "T3" else "T4"),
    #"Tipo Alterado2" = Table.TransformColumnTypes(#"Coluna Condicional Adicionada1",{{"Trimestre", type text}}),
    #"Coluna Personalizada Adicionada" = Table.AddColumn(#"Tipo Alterado2", "Mês/Ano", each Text.Combine({Text.Start([Nome do Mês], 3), "/", Text.From([Ano], "pt-BR")}), type text),
    #"Colunas Renomeadas1" = Table.RenameColumns(#"Coluna Personalizada Adicionada",{{"Data", "ID Data"}}),
    #"Semana do Ano Inserida" = Table.AddColumn(#"Colunas Renomeadas1", "Semana do Ano", each Date.WeekOfYear([ID Data]), Int64.Type),
    #"Semana do Mês Inserida" = Table.AddColumn(#"Semana do Ano Inserida", "Semana do Mês", each Date.WeekOfMonth([ID Data]), Int64.Type),
    #"Início da Semana Inserido" = Table.AddColumn(#"Semana do Mês Inserida", "Início da Semana", each Date.StartOfWeek([ID Data]), type date),
    #"Fim da Semana Inserido" = Table.AddColumn(#"Início da Semana Inserido", "Fim da Semana", each Date.EndOfWeek([ID Data]), type date),
    #"Colocar Cada Palavra Em Maiúscula" = Table.TransformColumns(#"Fim da Semana Inserido",{{"Nome do Mês", Text.Proper, type text}, {"Nome do Dia", Text.Proper, type text}}),
    #"Colunas Renomeadas2" = Table.RenameColumns(#"Colocar Cada Palavra Em Maiúscula",{{"ID Data", "Data"}}),
    #"Primeiros Caracteres Inseridos" = Table.AddColumn(#"Colunas Renomeadas2", "Primeiros caracteres", each Text.Start([Nome do Mês], 3), type text),
    #"Colunas Renomeadas3" = Table.RenameColumns(#"Primeiros Caracteres Inseridos",{{"Primeiros caracteres", "Mês Abrev"}, {"Mês", "Mês Num"}}),
    #"Coluna Condicional Adicionada2" = Table.AddColumn(#"Colunas Renomeadas3", "Dias Uteis", each if [Dia da Semana] = 0 then "Não" else if [Dia da Semana] = 6 then "Não" else "Sim"),
    #"Primeiros Caracteres Inseridos1" = Table.AddColumn(#"Coluna Condicional Adicionada2", "Dia da Semana Letra", each Text.Start([Nome do Dia], 3), type text),
    #"Coluna Condicional Adicionada3" = Table.AddColumn(#"Primeiros Caracteres Inseridos1", "Semana do Mes Letra", each if [Dia] <= 7 then "S1" else if [Dia] <= 15 then "S2" else if [Dia] <= 22 then "S3" else "S4"),
    #"Personalização adicionada" = Table.AddColumn(#"Coluna Condicional Adicionada3", "ano_mes_num", each Number.ToText([Ano]) & "-" & Number.ToText([Mês Num])),
    #"Coluna condicional inserida" = Table.AddColumn(#"Personalização adicionada", "Data ate Hoje", each if [Data] <= Date.From(DateTime.LocalNow()) then "Sim" else "Não"),
    #"Coluna condicional inserida 1" = Table.AddColumn(#"Coluna condicional inserida", "Dia Atual", each if [Data] = Date.From(DateTime.LocalNow()) then "Dia Atual" else if [Data] = Date.AddDays(Date.From(DateTime.LocalNow()),-1) then "Dia Anterior" else "Não"),
    #"Tipo Alterado3" = Table.TransformColumnTypes(#"Coluna condicional inserida 1", {{"Semana do Mes Letra", type text}, {"Dias Uteis", type text}, {"ano_mes_num", type text}, {"Data ate Hoje", type text}, {"Dia Atual", type text}}),
    #"Ano Trimestre Adicionado" = Table.AddColumn(#"Tipo Alterado3", "Ano Trimestre",
        each Text.From([Ano]) & " " & (if [Trimestre] = "T1" then "1º" else if [Trimestre] = "T2" then "2º" else if [Trimestre] = "T3" then "3º" else "4º"), type text),
    // RAIS: quebra de série em 2022 (eSocial). Anos de trechos diferentes não se comparam.
    #"Fonte RAIS Adicionada" = Table.AddColumn(#"Ano Trimestre Adicionado", "Fonte RAIS", each if [Ano] >= 2022 then "eSocial" else "RAIS declaratória", type text),
    #"Trecho Adicionado" = Table.AddColumn(#"Fonte RAIS Adicionada", "Trecho da Série", each if [Ano] >= 2022 then "2022 em diante" else "2009–2021", type text)
in
    #"Trecho Adicionado"'''

COLUNAS = [  # (nome, tipo, formato, ordenar_por)
    ("Data", "dateTime", "Long Date", None), ("Ano", "int64", "0", None), ("Mês Num", "int64", "0", None),
    ("Nome do Mês", "string", None, "Mês Num"), ("Dia", "int64", "0", None), ("Dia da Semana", "int64", "0", None),
    ("Nome do Dia", "string", None, None), ("Semestre", "string", None, None), ("Trimestre", "string", None, None),
    ("Mês/Ano", "string", None, None), ("Semana do Ano", "int64", "0", None), ("Semana do Mês", "int64", "0", None),
    ("Início da Semana", "dateTime", "Long Date", None), ("Fim da Semana", "dateTime", "Long Date", None),
    ("Mês Abrev", "string", None, "Mês Num"), ("Dias Uteis", "string", None, None), ("Dia da Semana Letra", "string", None, None),
    ("Semana do Mes Letra", "string", None, None), ("ano_mes_num", "string", None, None), ("Data ate Hoje", "string", None, None),
    ("Dia Atual", "string", None, None), ("Ano Trimestre", "string", None, None), ("Fonte RAIS", "string", None, None),
    ("Trecho da Série", "string", None, None),
]


def nome_tmdl(n):
    return f"'{n}'" if re.search(r"[^A-Za-z0-9_]", n) else n


def tags_existentes(arq):
    """Preserva lineageTags já gravados (o Desktop usa para rastrear objetos)."""
    if not arq.exists():
        return {}
    t = arq.read_text(encoding="utf-8")
    return {m.group(2): m.group(3) for m in re.finditer(r"\t(column|measure) (.+?)(?: =.*)?\n(?:.*\n)*?\t\tlineageTag: ([0-9a-f-]+)", t)}


def calendario():
    arq = TAB / "D_Calendario.tmdl"
    tags = tags_existentes(arq)
    tag_tab = re.search(r"^\tlineageTag: ([0-9a-f-]+)", arq.read_text(encoding="utf-8"), re.M).group(1) if arq.exists() else str(uuid.uuid4())
    L = ["table D_Calendario", f"\tlineageTag: {tag_tab}", ""]
    for nome, tipo, fmt, ordem in COLUNAS:
        n = nome_tmdl(nome)
        L.append(f"\tcolumn {n}")
        L.append(f"\t\tdataType: {tipo}")
        if fmt:
            L.append(f"\t\tformatString: {fmt}")
        L.append(f"\t\tlineageTag: {tags.get(n, str(uuid.uuid4()))}")
        L.append("\t\tsummarizeBy: none")
        L.append(f"\t\tsourceColumn: {nome}")
        if ordem:
            L.append(f"\t\tsortByColumn: {nome_tmdl(ordem)}")
        L.append("")
        L.append("\t\tannotation SummarizationSetBy = Automatic")
        if tipo == "dateTime":
            L.append("")
            L.append("\t\tannotation UnderlyingDateTimeDataType = Date")
        L.append("")
    L.append("\tpartition D_Calendario = m")
    L.append("\t\tmode: import")
    L.append("\t\tsource =")
    L += ["\t\t\t\t" + l for l in M_CALENDARIO.split("\n")]
    L += ["", "\tannotation PBI_ResultType = Table", ""]
    arq.write_text("\n".join(L), encoding="utf-8")


# ------------------------------------------------------------------ medidas
ANO_FIXO = "REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), D_Ano[ano] = {a}"
GRUPO = "REMOVEFILTERS(D_GrupoSetor), REMOVEFILTERS(D_Cnae), D_GrupoSetor[grupo_setor] = \"{g}\""

# filtros que a F_Mediana não tem (a mediana pré-calculada não existe para esses recortes)
SEM_MEDIANA = ["D_Raca[raca_cor]", "D_Raca[grupo_raca]", "D_Raca[declarada]", "D_FaixaIdade[faixa_idade]",
               "D_Cnae[cnae_fiscal]", "D_Cnae[nm_subclasse]", "D_Cnae[nm_classe]", "D_Cnae[nm_divisao]", "D_Cnae[nm_secao]",
               "D_Cnae[setor_afl]", "D_Cnae[setor_comparavel_afl]", "D_Cnae[setor_principal]",
               "F_rais[municipio]", "F_rais[ambito]", "F_rais[cbo_2002]", "F_rais[categoria_vinculo]", "F_rais[natureza_empresa]",
               "F_rais[modalidade_contrato]", "F_rais[tipo_admissao]", "F_rais[trabalho_intermitente]", "F_rais[trabalho_parcial]",
               "F_rais[faixa_horas_contratuais]", "F_rais[indicador_portador_deficiencia]", "F_rais[tipo_deficiencia]"]


def medidas():
    """(nome, descrição, DAX, pasta, formato, oculta)."""
    m = []

    def add(nome, doc, dax, pasta, fmt=None, oculta=False):
        m.append((nome, doc, dax, pasta, fmt, oculta))

    add("Ano_Ref", "Ano de referência: o último ano com dados no contexto (com o segmentador de ano, o ano escolhido).",
        "CALCULATE(MAX(F_rais[ano]))", "Base\\Ano", "0")
    add("Ano_Inicio_Trecho", f"Primeiro ano do trecho comparável do ano de referência: {INICIO} (RAIS declaratória) ou {QUEBRA} (eSocial).",
        f"VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A), IF(A >= {QUEBRA}, {QUEBRA}, {INICIO}))", "Base\\Ano", "0")
    add("Fonte_RAIS_Ref", "Fonte do ano de referência: RAIS declaratória (até 2021) ou eSocial (desde 2022).",
        f"VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A), IF(A >= {QUEBRA}, \"eSocial\", \"RAIS declaratória\"))", "Base\\Ano")
    add("Comparavel_Ano_Anterior", f"1 quando o ano de referência pode ser comparado com o anterior (não é {INICIO} nem {QUEBRA}, a quebra do eSocial).",
        f"VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A) && A <> {INICIO} && A <> {QUEBRA}, 1, 0)", "Base\\Ano", "0", True)

    # --- empregos (estoque em 31/12)
    add("Empregos", "Vínculos ativos em 31/12 no contexto. Em visuais por ano é o estoque do ano; não some anos.",
        "SUM(F_rais[vinculos])", "Base\\Empregos", "#,0")
    add("Empregos_Ref", "Empregos formais em 31/12 do ano de referência (um único ano).",
        "VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A), CALCULATE([Empregos], " + ANO_FIXO.format(a="A") + "))", "Base\\Empregos", "#,0")
    add("Empregos_Ano_Anterior", "Empregos em 31/12 do ano anterior; BLANK em 2009 e em 2022 (quebra do eSocial: 2022 não se compara com 2021).",
        "VAR A = [Ano_Ref]\nRETURN IF([Comparavel_Ano_Anterior] = 1, CALCULATE([Empregos], " + ANO_FIXO.format(a="A - 1") + "))", "Base\\Empregos", "#,0")
    add("Empregos_Var", "Variação absoluta dos empregos sobre o ano anterior (BLANK quando não há ano comparável).",
        "VAR Ant = [Empregos_Ano_Anterior]\nRETURN IF(NOT ISBLANK(Ant), [Empregos_Ref] - Ant)", "Base\\Empregos", "+#,0;-#,0;0")
    add("Empregos_Var_Pct", "Variação % dos empregos sobre o ano anterior (BLANK quando não há ano comparável).",
        "DIVIDE([Empregos_Var], [Empregos_Ano_Anterior])", "Base\\Empregos", "+0.0%;-0.0%;0.0%")
    add("Empregos_Inicio_Trecho", "Empregos em 31/12 do primeiro ano do trecho comparável (2009 ou 2022).",
        "VAR I = [Ano_Inicio_Trecho]\nRETURN IF(NOT ISBLANK(I), CALCULATE([Empregos], " + ANO_FIXO.format(a="I") + "))", "Base\\Empregos", "#,0")
    add("Empregos_Cresc_Medio_Ano", "Crescimento médio ao ano dentro do trecho: (fim ÷ início)^(1 ÷ anos) − 1; BLANK no primeiro ano do trecho.",
        "VAR A = [Ano_Ref]\nVAR I = [Ano_Inicio_Trecho]\nVAR Fim = [Empregos_Ref]\nVAR Ini = [Empregos_Inicio_Trecho]\n"
        "RETURN IF(A > I && Ini > 0, (Fim / Ini) ^ (1 / (A - I)) - 1)", "Base\\Empregos", "+0.0%;-0.0%;0.0%")

    # --- remuneração de dezembro (nominal)
    add("Remuneracao_Media", "Remuneração média de dezembro (R$ nominais) no contexto = soma ÷ quantidade de salários válidos (0,3 a 150 SM).",
        "DIVIDE(SUM(F_rais[soma_salario_valido]), SUM(F_rais[qtd_salario_valido]))", "Base\\Remuneração", "#,0.00")
    add("Remuneracao_Media_Ref", "Remuneração média de dezembro do ano de referência (R$ nominais).",
        "VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A), CALCULATE([Remuneracao_Media], " + ANO_FIXO.format(a="A") + "))", "Base\\Remuneração", "#,0.00")
    add("Remuneracao_Media_SM_Ref", "Remuneração média de dezembro do ano de referência em salários mínimos.",
        "VAR A = [Ano_Ref]\nRETURN IF(NOT ISBLANK(A), CALCULATE(DIVIDE(SUM(F_rais[soma_sm_valido]), SUM(F_rais[qtd_salario_valido])), " + ANO_FIXO.format(a="A") + "))",
        "Base\\Remuneração", "0.00")
    filtros = "\n    || ".join(f"ISFILTERED({c})" for c in SEM_MEDIANA)
    add("Mediana_Disponivel", "1 quando a mediana pré-calculada (F_Mediana: setor, UF, sexo e escolaridade) existe para os filtros do contexto; 0 com raça, idade, CNAE, município ou atributos do vínculo.",
        f"VAR Bloqueado =\n    {filtros}\n"
        "VAR Varios = (ISFILTERED(D_UF[uf]) && NOT HASONEVALUE(D_UF[uf])) || (ISFILTERED(D_Sexo[sexo]) && NOT HASONEVALUE(D_Sexo[sexo]))\n"
        "    || (ISFILTERED(D_Escolaridade[escolaridade_agrupada]) && NOT HASONEVALUE(D_Escolaridade[escolaridade_agrupada]))\n"
        "    || (COUNTROWS(VALUES(D_GrupoSetor[grupo_setor])) > 1 && COUNTROWS(VALUES(D_GrupoSetor[grupo_setor])) < COUNTROWS(ALL(D_GrupoSetor[grupo_setor])))\n"
        "RETURN IF(Bloqueado || Varios, 0, 1)", "Base\\Remuneração", "0", True)
    add("Remuneracao_Mediana_Ref", "Mediana da remuneração de dezembro do ano de referência (R$ nominais), da F_Mediana; recorte \"Todos\" quando a dimensão não está filtrada. BLANK quando a mediana não existe para os filtros.",
        "VAR A = [Ano_Ref]\n"
        "VAR G = IF(COUNTROWS(VALUES(D_GrupoSetor[grupo_setor])) = COUNTROWS(ALL(D_GrupoSetor[grupo_setor])), \"Todos\", SELECTEDVALUE(D_GrupoSetor[grupo_setor]))\n"
        "VAR U = IF(ISFILTERED(D_UF[uf]), SELECTEDVALUE(D_UF[uf]), \"Todos\")\n"
        "VAR S = IF(ISFILTERED(D_Sexo[sexo]), SELECTEDVALUE(D_Sexo[sexo]), \"Todos\")\n"
        "VAR E = IF(ISFILTERED(D_Escolaridade[escolaridade_agrupada]), SELECTEDVALUE(D_Escolaridade[escolaridade_agrupada]), \"Todos\")\n"
        "RETURN\n    IF([Mediana_Disponivel] = 1 && NOT ISBLANK(A) && NOT ISBLANK(G),\n"
        "        CALCULATE(MAX(F_Mediana[mediana_salario]),\n"
        "            REMOVEFILTERS(D_Calendario), REMOVEFILTERS(D_Ano), REMOVEFILTERS(D_UF), REMOVEFILTERS(D_Sexo),\n"
        "            REMOVEFILTERS(D_Escolaridade), REMOVEFILTERS(D_GrupoSetor),\n"
        "            F_Mediana[ano] = A, F_Mediana[grupo_setor] = G, F_Mediana[uf] = U, F_Mediana[sexo] = S, F_Mediana[escolaridade_agrupada] = E))",
        "Base\\Remuneração", "#,0.00")

    # --- AFL e Comparável (a comparação correta é sempre AFL × Comparável; Comparável já exclui o AFL)
    for base, fmt in (("Empregos_Ref", "#,0"), ("Empregos_Var_Pct", "+0.0%;-0.0%;0.0%"), ("Empregos_Cresc_Medio_Ano", "+0.0%;-0.0%;0.0%"),
                      ("Remuneracao_Media_Ref", "#,0.00"), ("Remuneracao_Mediana_Ref", "#,0.00")):
        for g, suf in (("AFL", "AFL"), ("Comparável", "Comparavel")):
            add(f"{base}_{suf}", f"{base} só do grupo {g}, independente do filtro de setores da página.",
                f"CALCULATE([{base}], " + GRUPO.format(g=g) + ")", f"Base\\{suf}", fmt)
    import dax_rais
    import dax_rais2
    import dax_rais3
    import dax_dicas
    m += dax_rais.medidas() + dax_rais2.medidas() + dax_rais3.medidas() + dax_dicas.medidas()
    # medida sem VAR própria não pode começar com RETURN: acrescenta uma VAR inócua
    m = [(t[0], t[1], "VAR _A = 0\n" + t[2] if t[2].lstrip().startswith("RETURN") else t[2]) + tuple(t[3:]) for t in m]
    return m


def gravar_medidas():
    arq = TAB / "_medidas.tmdl"
    tags = tags_existentes(arq)
    tag_tab = re.search(r"^\tlineageTag: ([0-9a-f-]+)", arq.read_text(encoding="utf-8"), re.M).group(1) if arq.exists() else str(uuid.uuid4())
    L = ["table _medidas", f"\tlineageTag: {tag_tab}", ""]
    for nome, doc, dax, pasta, fmt, oculta in medidas():
        L.append(f"\t/// {doc}")
        if "\n" in dax:
            L.append(f"\tmeasure {nome} =")
            L += ["\t\t\t" + l for l in dax.split("\n")]
        else:
            L.append(f"\tmeasure {nome} = {dax}")
        if fmt:
            L.append(f"\t\tformatString: {fmt}")
        if oculta:
            L.append("\t\tisHidden")
        L.append(f"\t\tdisplayFolder: {pasta}")
        L.append(f"\t\tlineageTag: {tags.get(nome, str(uuid.uuid4()))}")
        L.append("")
    L += ["\tcolumn Coluna", "\t\tdataType: string", "\t\tisHidden", f"\t\tlineageTag: {tags.get('Coluna', str(uuid.uuid4()))}",
          "\t\tsummarizeBy: none", "\t\tsourceColumn: Coluna", "", "\t\tannotation SummarizationSetBy = Automatic", "",
          "\tpartition _medidas = m", "\t\tmode: import", "\t\tsource =",
          "\t\t\t\tlet", "\t\t\t\t    Fonte = #table(type table [Coluna = text], {})", "\t\t\t\tin", "\t\t\t\t    Fonte", "",
          "\tannotation PBI_ResultType = Table", ""]
    arq.write_text("\n".join(L), encoding="utf-8")
    return len(medidas())


# ------------------------------------------------------------------ tabelas locais (importadas) de apoio aos visuais
def _tabela_m(nome, colunas, linhas):
    """Tabela importada por M (#table), com lineageTags preservados."""
    arq = TAB / f"{nome}.tmdl"
    tags = tags_existentes(arq)
    tag_tab = re.search(r"^\tlineageTag: ([0-9a-f-]+)", arq.read_text(encoding="utf-8"), re.M).group(1) if arq.exists() else str(uuid.uuid4())
    L = [f"table {nome}", f"\tlineageTag: {tag_tab}", ""]
    for c in colunas:
        L += [f"\tcolumn {c}", "\t\tdataType: string", f"\t\tlineageTag: {tags.get(c, str(uuid.uuid4()))}", "\t\tsummarizeBy: none", f"\t\tsourceColumn: {c}"]
        if c in ("nome", "indicador") and "ordem" in colunas:
            L.append("\t\tsortByColumn: ordem")
        L += ["", "\t\tannotation SummarizationSetBy = Automatic", ""]
    tipos = ", ".join(f"{c} = text" for c in colunas)
    corpo = ", ".join("{" + ", ".join('"' + str(v).replace('"', '""') + '"' for v in l) + "}" for l in linhas)
    L += [f"\tpartition {nome} = m", "\t\tmode: import", "\t\tsource =", "\t\t\t\tlet", f"\t\t\t\t    Fonte = #table(type table [{tipos}], {{{corpo}}})",
          "\t\t\t\tin", "\t\t\t\t    Fonte", "", "\tannotation PBI_ResultType = Table", ""]
    arq.write_text("\n".join(L), encoding="utf-8")


AFL_ATIVIDADES = [("5611201", "Restaurantes e similares", "1"), ("5611203", "Lanchonetes, casas de chá, de sucos e similares", "2"),
                  ("4721102", "Padaria e confeitaria (revenda)", "3"), ("5620104", "Alimentos preparados p/ consumo domiciliar", "4"),
                  ("5611204", "Bares sem entretenimento", "5"), ("5611205", "Bares com entretenimento", "6")]
LOCAIS = ["D_Comparavel", "D_AflAtividade", "D_Rank_Divisao", "D_Indicador"]
INDICADORES = ["Primeiro emprego", "Mulheres", "Até 24 anos", "55 anos ou mais", "Superior", "Negros", "Intermitente"]


def tabelas_locais():
    import json
    divs = json.loads((RAIZ / "docs" / "previa" / "divisoes.json").read_text(encoding="utf-8"))
    _tabela_m("D_Comparavel", ["comparavel_AFL", "comparavel_AFL_rotulo"], [("Sim", "Setores comparáveis ao AFL"), ("Não", "Demais setores")])
    _tabela_m("D_Indicador", ["indicador", "ordem"], [(n, str(i + 1)) for i, n in enumerate(INDICADORES)])
    _tabela_m("D_AflAtividade", ["cnae_fiscal", "nome", "ordem"], AFL_ATIVIDADES)
    _tabela_m("D_Rank_Divisao", ["nm_divisao", "setor_principal"], [(n, s) for n, s in divs] + [("AFL · conjunto de 6 CNAEs", "Serviços")])


# ------------------------------------------------------------------ relações e refs
def relacoes():
    arq = DEF / "relationships.tmdl"
    t = arq.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in t else "\n"
    for de, para in (("D_Cnae.setor_comparavel_afl", "D_Comparavel.comparavel_AFL"), ("D_Cnae.cnae_fiscal", "D_AflAtividade.cnae_fiscal")):
        if f"fromColumn: {de}{nl}\ttoColumn: {para}" not in t:
            t = t.rstrip("\r\n") + nl + nl + nl.join([f"relationship {uuid.uuid4()}", f"\tfromColumn: {de}", f"\ttoColumn: {para}"]) + nl
    for fato in ("F_rais", "F_Mediana"):
        if f"fromColumn: {fato}.ano{nl}\ttoColumn: D_Calendario.Ano" in t:
            continue
        t = t.rstrip("\r\n") + nl + nl + nl.join([
            f"relationship {uuid.uuid4()}", "\ttoCardinality: many", f"\tfromColumn: {fato}.ano", "\ttoColumn: D_Calendario.Ano"]) + nl
    arq.write_text(t, encoding="utf-8", newline="")


def refs():
    arq = DEF / "model.tmdl"
    t = arq.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in t else "\n"
    for tab in ("_medidas", "D_Calendario", *LOCAIS):
        if f"ref table {tab}{nl}" not in t:
            t = t.replace(f"ref table F_rais{nl}", f"ref table F_rais{nl}ref table {tab}{nl}", 1) if tab == "_medidas" else \
                t.replace(f"ref table D_Ano{nl}", f"ref table D_Ano{nl}ref table {tab}{nl}", 1)
    t = re.sub(r'annotation PBI_QueryOrder = \[.*?\]', 'annotation PBI_QueryOrder = ["DirectQuery para AS – Painel_RAIS","_medidas","D_Calendario","D_Comparavel","D_AflAtividade","D_Rank_Divisao","D_Indicador"]', t)
    arq.write_text(t, encoding="utf-8", newline="")


def main():
    tabelas_locais()
    calendario()
    n = gravar_medidas()
    relacoes()
    refs()
    print("D_Calendario, _medidas (", n, "medidas), relações e refs gravados")


if __name__ == "__main__":
    main()
