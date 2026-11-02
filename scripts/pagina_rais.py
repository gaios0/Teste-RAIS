"""Gera o relatório e as páginas do painel RAIS (PBIR): recursos, tema, fundos e visuais.

Etapa 1: tema Empregos (Todos os setores e AFL). Recusa sobrescrever páginas existentes (use --refazer para recriar as geradas por aqui).
Tooltips nativos e (i) compartilhados vêm em etapa seguinte; a navegação entre as páginas também (navegacao_rais.py).
"""
import json
import random
import re
import shutil
import sys
from pathlib import Path

import config_paginas as cp
import fundo_rais as fb
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
BLANK_INICIAL = "533042cd0022947b421a"
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
        pb.salvar(destino / "visuals" / v["name"] / "visual.json", v)
        vis[papel] = v["name"]

    # filtros
    sync = {"Ano": "rais_ano", "Localização": "rais_uf", "Sexo": "rais_sexo", "Escolaridade": "rais_esc", "Raça/cor": "rais_raca", "Setores": "rais_setores", "CNAE AFL": "rais_cnae", "Divisão": "rais_divisao"}
    campos = {"Ano": ("D_Calendario", "Ano"), "Localização": ("D_UF", "estado"), "Sexo": ("D_Sexo", "sexo"), "Escolaridade": ("D_Escolaridade", "escolaridade_agrupada"),
              "Raça/cor": ("D_Raca", "raca_cor"), "CNAE AFL": ("D_AflAtividade", "nome"),
              "Setores": ("D_Comparavel", "comparavel_AFL_rotulo"), "Divisão": ("D_Cnae", "nm_divisao")}
    for rot, (x, w) in pos.items():
        if rot == "Limpar":
            gravar("limpar", pb.limpar(n("limpar"), (x, 136, w, 48, prox()), LIMPAR_ARQ))
        else:
            tab, col = campos[rot]
            gravar("f_" + rot, pb.slicer_dropdown(n("f_" + rot), (x - 4, 132, w + 8, 52, prox()), tab, col, sync[rot], rot,
                                                  inicial=ANO_PADRAO if rot == "Ano" else None, unico=rot == "Ano"))
    # manchete e KPIs
    gravar("manchete", pb.html(n("manchete"), (40, 196, 1840, 118, prox()), f"Manchete_Emp_{u}_HTML"))
    kx = [fb.cx(0), fb.cx(4), fb.cx(8)]
    for i, m in enumerate((f"KPI_Emp_{u}_HTML", f"KPI_Peso_{u}_HTML", f"KPI_Cresc_{u}_HTML")):
        gravar(f"kpi{i + 1}", pb.html(n(f"kpi{i + 1}"), (kx[i] + 20, fb.KPI_Y + 20, fb.cw(4) - 84, 156, prox()), m))
    # linha 2: série (índice) + contratos
    ax, aw, bx, bw_ = fb.cx(0), fb.cw(8), fb.cx(8), fb.cw(4)
    gravar("t_serie", pb.html(n("t_serie"), (ax + 24, fb.L2_Y + 16, aw - 96, 90, prox()), "Titulo_Emp_Serie_HTML" if afl else "Titulo_Emp_SerieTotal_HTML"))
    series = [("Emp_Indice_AFL_Pre", "AFL (2009–2021)", cp.LARANJA, "0.0"), ("Emp_Indice_AFL_Pos", "AFL (2022 em diante)", cp.LARANJA, "0.0"),
              ("Emp_Indice_Comp_Pre", "Comparáveis (2009–2021)", cp.CINZA, "0.0"), ("Emp_Indice_Comp_Pos", "Comparáveis (2022 em diante)", cp.CINZA, "0.0")]
    if not afl:
        series += [("Emp_Indice_Sel_Pre", "Seleção atual (2009–2021)", "#98A2B3", "0.0"), ("Emp_Indice_Sel_Pos", "Seleção atual (2022 em diante)", "#98A2B3", "0.0")]
    tips = [("Empregos_Ref_AFL", "Empregos do AFL", "#,0"), ("Empregos_Ref_Comparavel", "Empregos dos comparáveis", "#,0"),
            ("Empregos_Var_Pct_AFL", "AFL sobre o ano anterior", "+0.0%;-0.0%;0.0%"), ("Empregos_Var_Pct_Comparavel", "Comparáveis sobre o ano anterior", "+0.0%;-0.0%;0.0%")]
    gravar("serie", pb.linhas(n("serie"), (ax + 16, fb.L2_Y + 132, aw - 32, fb.L2_H - 148, prox()), pb.coluna("D_Calendario", "Ano"), series, tips))
    gravar("t_contrato", pb.html(n("t_contrato"), (bx + 24, fb.L2_Y + 16, bw_ - 48, 112, prox()), "Titulo_Emp_Contrato_HTML"))
    gravar("contrato", pb.html(n("contrato"), (bx + 24, fb.L2_Y + 140, bw_ - 48, fb.L2_H - 160, prox()), "Emp_Contratos_HTML"))
    # capítulo 2
    if afl:
        gravar("t_rank", pb.html(n("t_rank"), (ax + 24, fb.L3_Y + 16, aw - 48, 84, prox()), "Titulo_Emp_Atividades_HTML"))
        gravar("rank", pb.barras(n("rank"), (ax + 16, fb.L3_Y + 108, aw - 32, fb.L3_H - 124, prox()), pb.coluna("D_AflAtividade", "nome"), "Empregos_Ref", "Empregos", "#,0",
                                 tooltips=[("Emp_Atividade_Var", "Sobre o ano anterior", "+0.0%;-0.0%;0.0%")]))
        gravar("t_uf", pb.html(n("t_uf"), (bx + 24, fb.L3_Y + 16, bw_ - 48, 112, prox()), "Titulo_Emp_UF_AFL_HTML"))
        gravar("uf", pb.barras(n("uf"), (bx + 16, fb.L3_Y + 140, bw_ - 32, fb.L3_H - 156, prox()), pb.coluna("D_UF", "uf"), "Emp_UF_Top", "Empregos do AFL", "#,0",
                               tooltips=[("Emp_UF_Peso_AFL", "Peso nos empregos comparáveis", "0.0%")]))
    else:
        gravar("t_rank", pb.html(n("t_rank"), (ax + 24, fb.L3_Y + 16, aw - 48, 84, prox()), "Titulo_Emp_Ranking_HTML"))
        gravar("setores", pb.botoes_setor(n("setores"), (ax + 24, fb.L3_Y + 100, aw - 48, 48, prox()), "D_Rank_Divisao", "setor_principal"))
        gravar("rank", pb.barras(n("rank"), (ax + 16, fb.L3_Y + 158, aw - 32, fb.L3_H - 174, prox()), pb.coluna("D_Rank_Divisao", "nm_divisao"), "Emp_Divisao_Top", "Empregos", "#,0",
                                 cor_por_medida="Cor_Emp_Divisao"))
        gravar("t_uf", pb.html(n("t_uf"), (bx + 24, fb.L3_Y + 16, bw_ - 48, 112, prox()), "Titulo_Emp_UF_Total_HTML"))
        gravar("uf", pb.barras(n("uf"), (bx + 16, fb.L3_Y + 140, bw_ - 32, fb.L3_H - 156, prox()), pb.coluna("D_UF", "uf"), "Emp_UF_Peso_Top", "Peso do AFL nos empregos comparáveis", "0.0%",
                               tooltips=[("Empregos_Ref_AFL", "Empregos do AFL", "#,0")]))
    # interações: o gráfico de série ignora o segmentador de ano e não filtra os demais; os botões de setor só filtram o ranking
    todos = [v for p, v in vis.items() if p not in ("limpar",) and not p.startswith("f_") and p != "setores"]
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
    if afl:
        pagina["filterConfig"] = {"filters": [pb.filtro_in("D_Cnae", "setor_afl", ["Sim"])]}
    pb.salvar(destino / "page.json", pagina)
    print(tema, recorte, pid, len(vis), "visuais")
    return pid, fundo


def main():
    refazer = "--refazer" in sys.argv
    recursos_base()
    imagens, ordem = [], []
    for (tema, recorte) in cp.PAGINAS:
        pid, fundo = montar(tema, recorte, refazer)
        imagens.append(fundo)
        ordem.append(pid)
    atualizar_report(imagens)
    pj = pb.DEF / "pages" / "pages.json"
    d = json.loads(pj.read_text(encoding="utf-8"))
    antigas = [p for p in d["pageOrder"] if p not in ordem and p != BLANK_INICIAL and not p.startswith("a3d1f2c4e6b8097a1c")]
    d["pageOrder"] = [p for p in d["pageOrder"] if p.startswith("a3d1f2c4e6b8097a1c") and p not in ordem] + ordem + antigas + ([BLANK_INICIAL] if BLANK_INICIAL in d["pageOrder"] else [])
    d["activePageName"] = ordem[0]
    pj.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
