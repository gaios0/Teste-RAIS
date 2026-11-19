"""Gera o relatório e as páginas do painel RAIS (PBIR): recursos, tema, fundos e visuais.

Etapa 1: tema Empregos (Todos os setores e AFL). Recusa sobrescrever páginas existentes (use --refazer para recriar as geradas por aqui).
Tooltips nativos e (i) compartilhados vêm em etapa seguinte; a navegação entre as páginas também (navegacao_rais.py).
"""
import json
import random
import re
import shutil
import sys
import types
from pathlib import Path

import config_paginas as cp
import fundo_rais as fb
import dax_tooltips
import info_rais
import seguranca
import navegacao_rais
import pbir_rais as pb

RF_RECURSOS = Path("C:/dados/datalab/rf/painel/Receita Federal Empresas e Mercado.Report/StaticResources/RegisteredResources")
RECURSOS = pb.REPORT / "StaticResources" / "RegisteredResources"
TEMA = "Pain_is_AFL___Est_dio_Abrasel_43178999335479706.json"
LIMPAR_ARQ = {"normal": "limpar-filtros-normal04164138347692414.svg", "hover": "limpar-filtros-hover190261450118843.svg",
              "press": "limpar-filtros-pressionado6370449083639115.svg"}
IDS = {("Empregos", "Todos os setores"): "a3d1f2c4e6b8097a1c11", ("Empregos", "AFL"): "a3d1f2c4e6b8097a1c12",
       ("Quem trabalha", "Todos os setores"): "a3d1f2c4e6b8097a1c21", ("Quem trabalha", "AFL"): "a3d1f2c4e6b8097a1c22",
       ("Quanto ganha", "Todos os setores"): "a3d1f2c4e6b8097a1c31", ("Quanto ganha", "AFL"): "a3d1f2c4e6b8097a1c32",
       ("Quem contrata", "Todos os setores"): "a3d1f2c4e6b8097a1c41", ("Quem contrata", "AFL"): "a3d1f2c4e6b8097a1c42"}
BLANK_INICIAL = None
ANO_PADRAO = 2025


# ------------------------------------------------------------------ relatório
def recursos_base():
    RECURSOS.mkdir(parents=True, exist_ok=True)
    for arq in (TEMA, *LIMPAR_ARQ.values()):
        if not (RECURSOS / arq).exists():
            shutil.copyfile(RF_RECURSOS / arq, RECURSOS / arq)


def registrar_fundo(nome):
    """Copia o PNG do fundo com sufixo aleatório (o Desktop cacheia pelo nome) e o registra no report.json."""
    existentes = sorted(p.name for p in RECURSOS.glob(f"{nome}-bg[0-9]*.png"))
    origem = fb.SAIDA / f"{nome}-bg.png"
    if existentes:                                  # regravação: sobrescreve o arquivo registrado
        shutil.copyfile(origem, RECURSOS / existentes[-1])
        return existentes[-1]
    arq = f"{nome}-bg{random.randint(10 ** 15, 10 ** 16 - 1)}.png"
    shutil.copyfile(origem, RECURSOS / arq)
    return arq


def atualizar_report(imagens):
    rj = pb.DEF / "report.json"
    d = json.loads(rj.read_text(encoding="utf-8"))
    ver = {"visual": "2.14.0", "report": "3.4.0", "page": "2.3.1"}
    d["themeCollection"]["customTheme"] = {"name": TEMA, "reportVersionAtImport": ver, "type": "RegisteredResources"}
    d["publicCustomVisuals"] = [pb.HTML]
    d.setdefault("objects", {})["outspacePane"] = [{"properties": {"expanded": pb.lit("false")}}]
    pacote = next((p for p in d["resourcePackages"] if p["name"] == "RegisteredResources"), None)
    if not pacote:
        pacote = {"name": "RegisteredResources", "type": "RegisteredResources", "items": []}
        d["resourcePackages"].append(pacote)
    itens = {i["name"]: i for i in pacote["items"]}
    itens[TEMA] = {"name": TEMA, "path": TEMA, "type": "CustomTheme"}
    for a in LIMPAR_ARQ.values():
        itens[a] = {"name": a, "path": a, "type": "Image"}
    for a in imagens:
        itens[a] = {"name": a, "path": a, "type": "Image"}
    pacote["items"] = sorted(itens.values(), key=lambda i: i["name"].lower())
    rj.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


# ------------------------------------------------------------------ corpos por tema
def corpo_empregos(c):
    pid, afl, u, n, gravar, prox, vis = c.pid, c.afl, c.u, c.n, c.gravar, c.prox, c.vis
    gravar("manchete", pb.html(n("manchete"), (40, 196, 1840, 118, prox()), f"Manchete_Emp_{u}_HTML"))
    kx = [fb.cx(0), fb.cx(4), fb.cx(8)]
    for i, m in enumerate((f"KPI_Emp_{u}_HTML", f"KPI_Peso_{u}_HTML", f"KPI_Cresc_{u}_HTML")):
        gravar(f"kpi{i + 1}", pb.html(n(f"kpi{i + 1}"), (kx[i] + 20, fb.KPI_Y + 12, fb.cw(4) - 84, 172, prox()), m))
    # linha 2: série (índice) + contratos
    ax, aw, bx, bw_ = fb.cx(0), fb.cw(8), fb.cx(8), fb.cw(4)
    gravar("t_serie", pb.html(n("t_serie"), (ax + 24, fb.L2_Y + 16, aw - 96, 92, prox()), "Titulo_Emp_Var_AFL_HTML" if afl else "Titulo_Emp_Var_Total_HTML"))
    series = [("Empregos_Var_Pct_AFL", "AFL", cp.LARANJA)]
    if not afl:
        series.append(("Empregos_Var_Pct", "Seleção atual", "#98A2B3"))
    gravar("serie", pb.linhas(n("serie"), (ax + 16, fb.L2_Y + 132, aw - 32, fb.L2_H - 148, prox()), pb.coluna("D_Calendario", "Ano"),
                                [(m, r, cor, "+0%;-0%;0%") for m, r, cor in series], rotulos=not afl))
    gravar("t_contrato", pb.html(n("t_contrato"), (bx + 24, fb.L2_Y + 16, bw_ - 48, 114, prox()), "Titulo_Emp_Contrato_HTML"))
    gravar("contrato", pb.html(n("contrato"), (bx + 24, fb.L2_Y + 140, bw_ - 48, fb.L2_H - 160, prox()), "Emp_Contratos_HTML"))
    # capítulo 2
    if afl:
        gravar("t_rank", pb.html(n("t_rank"), (ax + 24, fb.L3_Y + 16, aw - 48, 86, prox()), "Titulo_Emp_Atividades_HTML"))
        gravar("rank", pb.barras(n("rank"), (ax + 16, fb.L3_Y + 108, aw - 32, fb.L3_H - 124, prox()), pb.coluna("D_AflAtividade", "nome"), "Empregos_Ref", "Empregos", "#,0",
                                 tooltips=[("Emp_Atividade_Var", "Sobre o ano anterior", "+0.0%;-0.0%;0.0%")]))
        gravar("t_uf", pb.html(n("t_uf"), (bx + 24, fb.L3_Y + 16, bw_ - 48, 114, prox()), "Titulo_Emp_UF_AFL_HTML"))
        gravar("uf", pb.barras(n("uf"), (bx + 16, fb.L3_Y + 140, bw_ - 32, fb.L3_H - 156, prox()), pb.coluna("D_UF", "uf"), "Empregos_Ref", "Empregos do AFL", "#,0", categoria2=pb.coluna("F_rais", "municipio", False, True), foco=True, espaco=10,
                               tooltips=[("Emp_UF_Peso_AFL", "Peso nos empregos comparáveis", "0.0%")]))
    else:
        gravar("t_rank", pb.html(n("t_rank"), (ax + 24, fb.L3_Y + 16, aw - 48, 86, prox()), "Titulo_Emp_Ranking_HTML"))
        gravar("setores", pb.botoes_setor(n("setores"), (ax + 24, fb.L3_Y + 102, aw - 48, 48, prox()), "D_Rank_Divisao", "setor_principal"))
        gravar("rank", pb.barras(n("rank"), (ax + 16, fb.L3_Y + 160, aw - 32, fb.L3_H - 176, prox()), pb.coluna("D_Rank_Divisao", "nm_divisao"), "Emp_Divisao_Top", "Empregos", "#,0",
                                 cor_por_medida="Cor_Emp_Divisao"))
        gravar("t_uf", pb.html(n("t_uf"), (bx + 24, fb.L3_Y + 16, bw_ - 48, 114, prox()), "Titulo_Emp_UF_Total_HTML"))
        gravar("uf", pb.barras(n("uf"), (bx + 16, fb.L3_Y + 140, bw_ - 32, fb.L3_H - 156, prox()), pb.coluna("D_UF", "uf"), "Emp_UF_Peso_Geo", "Peso do AFL nos empregos comparáveis", "0.0%", categoria2=pb.coluna("F_rais", "municipio", False, True), foco=True, espaco=10,
                               tooltips=[("Empregos_Ref_AFL", "Empregos do AFL", "#,0")]))


TIPS = {"Tip_RazaoSexo_HTML": "a3d1f2c4e6b8097a1c51", "Tip_RazaoRaca_HTML": "a3d1f2c4e6b8097a1c52", "Tip_Mediana_HTML": "a3d1f2c4e6b8097a1c53",
        "Tip_Contrata_Pos_HTML": "a3d1f2c4e6b8097a1c54", "Tip_Contrata_Dif_HTML": "a3d1f2c4e6b8097a1c55", "Tip_Contrata_Max_Total_HTML": "a3d1f2c4e6b8097a1c56",
        "Tip_Contrata_Max_AFL_HTML": "a3d1f2c4e6b8097a1c57"}
CINZA_SEL = "#98A2B3"
# gráficos nativos → medida da página de tooltip (a página vem de dax_tooltips.TOOLTIPS)
TT_GRAFICO = {("Empregos", "serie", None): "Tip_Emp_Ano_HTML", ("Empregos", "rank", False): "Tip_Emp_Divisao_HTML", ("Empregos", "rank", True): "Tip_Emp_Atividade_HTML",
              ("Empregos", "uf", None): "Tip_Emp_UF_HTML", ("Quem trabalha", "pir", None): "Tip_Pir_HTML", ("Quem trabalha", "cbo", None): "Tip_CBO_HTML",
              ("Quanto ganha", "serie", None): "Tip_Rem_Ano_HTML", ("Quanto ganha", "esc", None): "Tip_Rem_Esc_HTML", ("Quanto ganha", "g_Sexo", None): "Tip_Rem_Gap_Sexo_HTML",
              ("Quanto ganha", "g_Raca", None): "Tip_Rem_Gap_Raca_HTML", ("Quanto ganha", "uf", None): "Tip_Rem_UF_HTML",
              ("Quem contrata", "rank", False): "Tip_Ind_Divisao_HTML", ("Quem contrata", "rank", True): "Tip_Ind_Atividade_HTML", ("Quem contrata", "serie", None): "Tip_Ind_Ano_HTML",
              ("Quem contrata", "uf", None): "Tip_Ind_UF_HTML"}
INFO_PAGINAS = {"P": "a3d1f2c4e6b8097a1c61", "M": "a3d1f2c4e6b8097a1c62", "G": "a3d1f2c4e6b8097a1c63"}
INFO_TAMANHOS = {"P": (720, 370), "M": (760, 440), "G": (800, 580)}
GUIA_LEITURA_PAGINA = "a3d1f2c4e6b8097a1c60"


def gatilhos_info(c, tema, recorte):
    """Um gatilho transparente por cartão sobre o (i) do fundo: página de dica dedicada (números calculados) ou tooltip compartilhado da D_Info."""
    classes = {l[0]: l[1] for l in info_rais.linhas()}
    for cartao in info_rais.CARTOES:
        dedic = info_rais.DEDICADOS.get((tema, recorte, cartao))
        pagina = TIPS[dedic] if dedic else INFO_PAGINAS[classes[info_rais.chave(tema, recorte, cartao)]]
        cxm, cym = fb.centro_info(cartao)
        c.gravar("info_" + cartao, pb.gatilho_info(c.n("info_" + cartao), (cxm - 42, cym - 31, 84, 62, 40000 + info_rais.CARTOES.index(cartao)),
                                                   info_rais.chave(tema, recorte, cartao), pagina))


def cabecalho(c, manchete, kpis, tips=None):
    c.gravar("manchete", pb.html(c.n("manchete"), (40, 196, 1840, 118, c.prox()), manchete))
    kx = [fb.cx(0), fb.cx(4), fb.cx(8)]
    for i, m in enumerate(kpis):
        tip = None
        c.gravar(f"kpi{i + 1}", pb.html(c.n(f"kpi{i + 1}"), (kx[i] + 20, fb.KPI_Y + 12, fb.cw(4) - 84, 172, c.prox()), m, tooltip=tip))


def geo():
    return fb.cx(0), fb.cw(8), fb.cx(8), fb.cw(4)


def titulo(c, papel, x, y, w, h, medida):
    # Geometria aprovada em Empregos · Todos os setores: os títulos HTML recebem
    # respiro extra para que o visual não exponha sua barra de rolagem interna.
    if medida.startswith("Titulo_"):
        if x < 100 and y == fb.L2_Y + 16:
            x, y, h = 64.3376597538455, 548.923437474299, 98.5598191973803
        elif x > 1000 and y == fb.L2_Y + 16:
            x, y, h = 1301.81094523206, 555.767869363006, 116.355342108018
        elif x < 100 and y == fb.L3_Y + 16:
            x, y, h = 64.3376597538455, 1029.40255606153, 93.0842736864147
        elif x > 1000 and y == fb.L3_Y + 16:
            x, y, h = 1301.81094523206, 1036.24698795023, 123.199773996725
    c.gravar(papel, pb.html(c.n(papel), (x, y, w, h, c.prox()), medida))


def corpo_perfil(c):
    u = c.u
    ax, aw, bx, bw_ = geo()
    cabecalho(c, f"Manchete_Perfil_{u}_HTML", [f"KPI_Mulheres_{u}_HTML", f"KPI_Jovens_{u}_HTML", f"KPI_Escol_{u}_HTML"])
    # pirâmide etária (mulheres à esquerda, homens à direita)
    titulo(c, "t_pir", ax + 24, fb.L2_Y + 16, aw - 48, 84, "Titulo_Pir_HTML")
    c.gravar("pir", pb.barras_grupo(c.n("pir"), (57.175792507204605, 634.46685878962535, 1189.6253602305474, 359.65417867435156, c.prox()), pb.coluna("D_FaixaIdade", "faixa_idade"),
                                    [("Pir_Mulheres", "Mulheres", cp.VIOLETA), ("Pir_Homens", "Homens", cp.CINZA_H)], "0.0%;0.0%;0.0%", empilhado=True,
                                    sort_cat=("D_FaixaIdade", "faixa_idade", "Descending"),
                                    tooltips=[("Pir_Mulheres_Comp", "Mulheres nos Comparáveis", "0.0%;0.0%;0.0%"), ("Pir_Homens_Comp", "Homens nos Comparáveis", "0.0%;0.0%;0.0%")]))
    titulo(c, "t_esc", bx + 24, fb.L2_Y + 16, bw_ - 48, 112, "Titulo_Esc_HTML")
    titulo(c, "esc", bx + 24, fb.L2_Y + 140, bw_ - 48, fb.L2_H - 160, "Esc_Barras_HTML")
    titulo(c, "t_cbo", ax + 24, fb.L3_Y + 16, aw - 48, 84, "Titulo_CBO_HTML")
    c.gravar("cbo", pb.barras(c.n("cbo"), (ax + 16, fb.L3_Y + 108, aw - 32, fb.L3_H - 124, c.prox()), pb.coluna("D_Cbo", "ocupacao"), "Emp_CBO_Top", "Empregos", "#,0",
                              tooltips=[("Perf_Mulheres", "Mulheres", "0.0%"), ("Remuneracao_Media_Ref", "Remuneração média de dezembro (R$)", "#,0.00")], foco=True, espaco=14))
    titulo(c, "t_raca", bx + 24, fb.L3_Y + 16, bw_ - 48, 112, "Titulo_Raca_HTML")
    titulo(c, "raca", bx + 24, fb.L3_Y + 140, bw_ - 48, fb.L3_H - 160, "Raca_HTML")


def corpo_salario(c):
    u = c.u
    todos = not c.afl
    ax, aw, bx, bw_ = geo()
    cabecalho(c, f"Manchete_Salario_{u}_HTML", [f"KPI_Mediana_{u}_HTML", f"KPI_RazaoSexo_{u}_HTML", f"KPI_RazaoRaca_{u}_HTML"],
              ["Tip_Mediana_HTML", "Tip_RazaoSexo_HTML", "Tip_RazaoRaca_HTML"])
    titulo(c, "t_serie", ax + 24, fb.L2_Y + 16, aw - 96, 90, "Titulo_Rem_Serie_HTML")
    s = [("Rem_Media_AFL_Pre", "AFL · média (2009–2021)", cp.LARANJA, "#,0"), ("Rem_Media_AFL_Pos", "AFL · média (2022 em diante)", cp.LARANJA, "#,0"),
         ("Rem_Mediana_AFL_Pre", "AFL · mediana (2009–2021)", cp.LARANJA, "#,0"), ("Rem_Mediana_AFL_Pos", "AFL · mediana (2022 em diante)", cp.LARANJA, "#,0"),
         ("Rem_Media_Comp_Pre", "Comparáveis · média (2009–2021)", cp.CINZA, "#,0"), ("Rem_Media_Comp_Pos", "Comparáveis · média (2022 em diante)", cp.CINZA, "#,0"),
         ("Rem_Mediana_Comp_Pre", "Comparáveis · mediana (2009–2021)", cp.CINZA, "#,0"), ("Rem_Mediana_Comp_Pos", "Comparáveis · mediana (2022 em diante)", cp.CINZA, "#,0")]
    if todos:
        s += [("Rem_Media_Sel_Pre", "Seleção atual · média (2009–2021)", CINZA_SEL, "#,0"), ("Rem_Media_Sel_Pos", "Seleção atual · média (2022 em diante)", CINZA_SEL, "#,0")]
    c.gravar("serie", pb.linhas(c.n("serie"), (ax + 16, fb.L2_Y + 132, aw - 32, fb.L2_H - 148, c.prox()), pb.coluna("D_Calendario", "Ano"), s, None,
                                tracejadas=[m for m, *_ in s if "Mediana" in m]))
    # escolaridade (card estreito): título 100, legenda em +120 (fundo), gráfico em +146
    titulo(c, "t_esc", bx + 24, fb.L2_Y + 16, bw_ - 48, 100, "Titulo_Rem_Esc_HTML")
    esc = [("Rem_Esc_AFL", "AFL", cp.LARANJA), ("Rem_Esc_Comp", "Comparáveis", cp.CINZA)] + ([("Rem_Esc_Sel", "Seleção atual", CINZA_SEL)] if todos else [])
    c.gravar("esc", pb.barras_grupo(c.n("esc"), (bx + 16, fb.L2_Y + 146, bw_ - 32, fb.L2_H - 158, c.prox()), pb.coluna("D_Escolaridade", "escolaridade_agrupada"),
                                    esc, "#,0", sort_cat=("D_Escolaridade", "escolaridade_agrupada", "Ascending"), espaco=8, fonte=14))
    # razões por sexo e cor
    titulo(c, "t_gap", ax + 24, fb.L3_Y + 16, aw - 48, 100, "Titulo_Rem_Gap_HTML")
    meia = (aw - 48 - 24) / 2
    for i, (nome, rot) in enumerate((("Sexo", "Rotulo_Gap_Sexo_HTML"), ("Raca", "Rotulo_Gap_Raca_HTML"))):
        x = ax + 24 + i * (meia + 24)
        titulo(c, "r_" + nome, x, fb.L3_Y + 150, meia, 30, rot)
        ser = [(f"Rem_Razao_{nome}_AFL", "AFL", cp.LARANJA), (f"Rem_Razao_{nome}_Comp", "Comparáveis", cp.CINZA)] + ([(f"Rem_Razao_{nome}", "Seleção atual", CINZA_SEL)] if todos else [])
        c.gravar("g_" + nome, pb.barras_grupo(c.n("g_" + nome), (x - 8, fb.L3_Y + 184, meia + 16, fb.L3_H - 196, c.prox()), pb.coluna("D_Escolaridade", "escolaridade_agrupada"),
                                              ser, "0%", sort_cat=("D_Escolaridade", "escolaridade_agrupada", "Ascending"), espaco=8, fonte=14))
    titulo(c, "t_uf", bx + 24, fb.L3_Y + 16, bw_ - 48, 112, "Titulo_Rem_UF_HTML")
    c.gravar("uf", pb.barras(c.n("uf"), (bx + 16, fb.L3_Y + 140, bw_ - 32, fb.L3_H - 156, c.prox()), pb.coluna("D_UF", "uf"), "Rem_UF_Geo", "Remuneração média (R$)", "#,0", categoria2=pb.coluna("F_rais", "municipio", False, True),
                             cor_fixa=cp.LARANJA if c.afl else "#1D1E21", tooltips=[("Rem_UF_Razao_Comp", "AFL ÷ média dos Comparáveis", "0%")], foco=True, espaco=10))


def corpo_contrata(c):
    u = c.u
    ax, aw, bx, bw_ = geo()
    afl = c.afl
    cabecalho(c, f"Manchete_Contrata_{u}_HTML", [f"KPI_Contrata1_{u}_HTML", f"KPI_Contrata2_{u}_HTML", f"KPI_Contrata3_{u}_HTML"],
              [None if afl else "Tip_Contrata_Pos_HTML", "Tip_Contrata_Dif_HTML", "Tip_Contrata_Max_AFL_HTML" if afl else "Tip_Contrata_Max_Total_HTML"])
    titulo(c, "t_rank", ax + 24, fb.L2_Y + 16, aw - 48, 84, "Titulo_Contrata_Rank_AFL_HTML" if afl else "Titulo_Contrata_Rank_Total_HTML")
    c.gravar("indicador", pb.botoes_setor(c.n("indicador"), (ax + 24, fb.L2_Y + 100, aw - 48, 48, c.prox()), "D_Indicador", "indicador", n=7, inicial="Mulheres", fonte=14))
    if afl:
        c.gravar("rank", pb.barras(c.n("rank"), (ax + 16, fb.L2_Y + 158, aw - 32, fb.L2_H - 170, c.prox()), pb.coluna("D_AflAtividade", "nome"), "Ind_Valor_Ctx", "Participação", "0.0%",
                                   cor_fixa=cp.LARANJA, espaco=14, foco=True))
    else:
        c.gravar("rank", pb.barras(c.n("rank"), (ax + 16, fb.L2_Y + 158, aw - 32, fb.L2_H - 170, c.prox()), pb.coluna("D_Rank_Divisao", "nm_divisao"), "Ind_Divisao_Top", "Participação", "0.0%",
                                   cor_por_medida="Cor_Ind_Divisao", espaco=6, fonte=14, foco=True))
    titulo(c, "t_serie", bx + 24, fb.L2_Y + 16, bw_ - 48, 100, "Titulo_Contrata_Serie_HTML")
    s = [("Ind_Serie_AFL_Pre", "AFL (2009–2021)", cp.LARANJA, "0.0%"), ("Ind_Serie_AFL_Pos", "AFL (2022 em diante)", cp.LARANJA, "0.0%"),
         ("Ind_Serie_Comp_Pre", "Comparáveis (2009–2021)", cp.CINZA, "0.0%"), ("Ind_Serie_Comp_Pos", "Comparáveis (2022 em diante)", cp.CINZA, "0.0%")]
    if not afl:
        s += [("Ind_Serie_Sel_Pre", "Seleção atual (2009–2021)", CINZA_SEL, "0.0%"), ("Ind_Serie_Sel_Pos", "Seleção atual (2022 em diante)", CINZA_SEL, "0.0%")]
    c.gravar("serie", pb.linhas(c.n("serie"), (bx + 16, fb.L2_Y + 146, bw_ - 32, fb.L2_H - 158, c.prox()), pb.coluna("D_Calendario", "Ano"), s, continuo=True))
    titulo(c, "t_tab", ax + 24, fb.L3_Y + 16, aw - 48, 84, "Titulo_Contrata_Tabela_HTML")
    titulo(c, "tabela", ax + 24, fb.L3_Y + 108, aw - 48, fb.L3_H - 128, "Contrata_Tabela_HTML" if afl else "Contrata_Tabela_Total_HTML")
    if afl:
        titulo(c, "t_uf", bx + 24, fb.L3_Y + 16, bw_ - 48, 112, "Titulo_Contrata_UF_HTML")
        c.gravar("uf", pb.barras(c.n("uf"), (bx + 16, fb.L3_Y + 140, bw_ - 32, fb.L3_H - 156, c.prox()), pb.coluna("D_UF", "uf"), "Ind_UF_Geo", "Participação no AFL", "0.0%", cor_fixa=cp.LARANJA, categoria2=pb.coluna("F_rais", "municipio", False, True),
                                 foco=True, espaco=10))
    else:
        titulo(c, "t_uf", bx + 24, fb.L3_Y + 16, bw_ - 48, 112, "Titulo_Contrata_UF_Total_HTML")
        c.gravar("uf", pb.barras(c.n("uf"), (bx + 16, fb.L3_Y + 140, bw_ - 32, fb.L3_H - 156, c.prox()), pb.coluna("D_UF", "uf"), "Ind_UF_Todos_Geo", "Participação", "0.0%", cor_fixa="#1D1E21", categoria2=pb.coluna("F_rais", "municipio", False, True),
                                 tooltips=[("Ind_UF_AFL_Dica", "No AFL desta UF", "0.0%")], foco=True, espaco=10))


# ------------------------------------------------------------------ páginas
def montar(tema, recorte, refazer=False):
    cfg = cp.PAGINAS[(tema, recorte)]
    pid = IDS[(tema, recorte)]
    destino = pb.DEF / "pages" / pid
    if destino.exists():
        if not refazer:
            raise SystemExit(f"{pid} já existe; use --refazer para recriar")
        shutil.rmtree(destino)
    png, pos = fb.gravar(cfg["nome"], tema, recorte, cfg)
    fundo = registrar_fundo(cfg["nome"])
    afl = recorte == "AFL"
    u = "AFL" if afl else "Total"
    z = [100]

    def prox():
        z[0] += 100
        return z[0]

    def n(papel):
        return pb.nome_visual(pid, papel)
    vis = {}

    def gravar(papel, v):
        medida_tt = TT_GRAFICO.get((tema, papel, afl)) or TT_GRAFICO.get((tema, papel, None))
        if medida_tt:
            v["visual"]["visualContainerObjects"]["visualTooltip"] = [{"properties": {"section": pb.lit(f"'{dax_tooltips.TOOLTIPS[medida_tt][0]}'"), "type": pb.lit("'Canvas'"), "show": pb.lit("true")}}]
        pb.salvar(destino / "visuals" / v["name"] / "visual.json", v)
        vis[papel] = v["name"]

    # filtros
    sync = {"Ano": "rais_ano", "Localização": "rais_uf", "Sexo": "rais_sexo", "Escolaridade": "rais_esc", "Raça/cor": "rais_raca", "Setores": "rais_setores", "CNAE AFL": "rais_cnae"}
    campos = {"Ano": ("D_Calendario", "Ano"), "Localização": ("D_UF", "estado"), "Sexo": ("D_Sexo", "sexo"), "Escolaridade": ("D_Escolaridade", "escolaridade_agrupada"),
              "Raça/cor": ("D_Raca", "raca_cor"), "CNAE AFL": ("D_AflAtividade", "nome"),
              "Setores": ("D_Comparavel", "comparavel_AFL_rotulo")}
    for rot, (x, w) in pos.items():
        if rot == "Limpar":
            gravar("limpar", pb.limpar(n("limpar"), (x, 136, w, 48, prox()), LIMPAR_ARQ))
        else:
            tab, col = campos[rot]
            if rot == "Setores":      # uma caixa: marcada = somente comparáveis; desmarcada = todos os setores não AFL
                gravar("f_Setores", pb.slicer_comparavel(n("f_Setores"), (x, 136, w, 48, prox()), sync[rot]))
                continue
            gravar("f_" + rot, pb.slicer_dropdown(n("f_" + rot), (x - 4, 132, w + 8, 52, prox()), tab, col, sync[rot], rot,
                                                  inicial=ANO_PADRAO if rot == "Ano" else None, unico=rot == "Ano"))
    gravar("info_leitura_botao", pb.botao_info_leitura(n("info_leitura_botao"), (0, 0, fb.W, 30, 33000)))
    gravar("info_leitura_gatilho", pb.gatilho_info_leitura(n("info_leitura_gatilho"), (0, 0, fb.W, 30, 34000), GUIA_LEITURA_PAGINA))
    c = types.SimpleNamespace(pid=pid, afl=afl, u=u, n=n, gravar=gravar, prox=prox, vis=vis)
    {"Empregos": corpo_empregos, "Quem trabalha": corpo_perfil, "Quanto ganha": corpo_salario, "Quem contrata": corpo_contrata}[tema](c)
    gatilhos_info(c, tema, recorte)
    # interações: o gráfico de série ignora o segmentador de ano e não filtra os demais; os botões de setor só filtram o ranking
    todos = [v for p, v in vis.items() if p not in ("limpar", "info_leitura_botao", "info_leitura_gatilho") and not p.startswith("f_") and p != "setores"]
    inter = []
    if "serie" in vis:
        inter = [{"source": vis["f_Ano"], "target": vis["serie"], "type": "NoFilter"}]
        inter += [{"source": vis["serie"], "target": t, "type": "NoFilter"} for t in todos if t != vis["serie"]]
    if "setores" in vis:
        inter += [{"source": vis["setores"], "target": t, "type": "NoFilter"} for t in todos if t != vis["rank"]]
        inter.append({"source": vis["setores"], "target": vis["rank"], "type": "DataFilter"})
    objetos = {"background": [{"properties": {"image": {"image": {"name": pb.lit(f"'{fundo}'"),
                                                                  "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageType": 1, "ItemName": fundo}}},
                                                                  "scaling": pb.lit("'Fit'")}}}}]}
    pagina = {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json", "name": pid,
              "displayName": f"{tema} · {recorte}", "displayOption": "FitToWidth", "height": fb.H, "width": fb.W, "objects": objetos, "visualInteractions": inter}
    pagina["filterConfig"] = {"filters": [pb.filtro_in("D_Cnae", "setor_afl", ["Sim" if afl else "Não"])]}
    pb.salvar(destino / "page.json", pagina)
    print(tema, recorte, pid, len(vis), "visuais")
    return pid, fundo


def main():
    refazer = "--refazer" in sys.argv
    seguranca.exigir_limpo(pb.DEF / "pages", pb.REPORT / "StaticResources")
    recursos_base()
    imagens, ordem = [], []
    for (tema, recorte) in sorted(cp.PAGINAS, key=lambda k: (fb.TEMAS.index(k[0]), fb.RECORTES.index(k[1]))):
        pid, fundo = montar(tema, recorte, refazer)
        imagens.append(fundo)
        ordem.append(pid)
    atualizar_report(imagens)
    for medida_tt, (pid, larg, alt) in dax_tooltips.TOOLTIPS.items():
        destino = pb.DEF / "pages" / pid
        if destino.exists():
            shutil.rmtree(destino)
        pagina, vis, v = pb.pagina_tooltip(pid, "Tooltip · " + medida_tt.replace("Tip_", "").replace("_HTML", "").replace("_", " "), medida_tt, larg, alt)
        pb.salvar(destino / "page.json", pagina)
        pb.salvar(destino / "visuals" / v / "visual.json", vis)
    for classe, pid in INFO_PAGINAS.items():
        destino = pb.DEF / "pages" / pid
        if destino.exists():
            shutil.rmtree(destino)
        larg, alt = INFO_TAMANHOS[classe]
        pagina, vis, v = pb.pagina_tooltip(pid, f"Tooltip (i) compartilhado · {classe}", "Info_Texto_HTML", larg, alt)
        pb.salvar(destino / "page.json", pagina)
        pb.salvar(destino / "visuals" / v / "visual.json", vis)
    destino = pb.DEF / "pages" / GUIA_LEITURA_PAGINA
    if destino.exists():
        shutil.rmtree(destino)
    pagina, vis, v = pb.pagina_tooltip(GUIA_LEITURA_PAGINA, "Tooltip · Informações para leitura", "Guia_Leitura_RAIS_HTML", 1040, 900)
    vis["visual"]["visualContainerObjects"]["general"] = [{"properties": {"altText": pb.lit("'Guia de leitura e glossário do painel RAIS.'")}}]
    pb.salvar(destino / "page.json", pagina)
    pb.salvar(destino / "visuals" / v / "visual.json", vis)
    for medida_nome, pid in TIPS.items():
        destino = pb.DEF / "pages" / pid
        if destino.exists():
            shutil.rmtree(destino)
        pagina, vis, v = pb.pagina_tooltip(pid, "Dica · " + medida_nome.replace("Tip_", "").replace("_HTML", "").replace("_", " "), medida_nome)
        pb.salvar(destino / "page.json", pagina)
        pb.salvar(destino / "visuals" / v / "visual.json", vis)
    navegacao_rais.gerar({k: IDS[k] for k in cp.PAGINAS})
    pj = pb.DEF / "pages" / "pages.json"
    d = json.loads(pj.read_text(encoding="utf-8"))
    antigas = [p for p in d["pageOrder"] if p not in ordem and p != BLANK_INICIAL and not p.startswith("a3d1f2c4e6b8097a1c")]
    d["pageOrder"] = ordem + [GUIA_LEITURA_PAGINA] + list(TIPS.values()) + list(INFO_PAGINAS.values()) + [x[0] for x in dax_tooltips.TOOLTIPS.values()] + [p for p in antigas if p not in TIPS.values() and p not in INFO_PAGINAS.values() and p != GUIA_LEITURA_PAGINA and p not in [x[0] for x in dax_tooltips.TOOLTIPS.values()]] + ([BLANK_INICIAL] if BLANK_INICIAL in d["pageOrder"] else [])
    d["activePageName"] = ordem[0]
    pj.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
