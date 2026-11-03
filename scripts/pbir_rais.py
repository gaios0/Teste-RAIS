"""Construtores de visuais PBIR do painel RAIS (mesmos padrões dos visuais salvos pelo Desktop nas páginas do RF)."""
import hashlib
import json
import shutil
import uuid
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
REPORT = RAIZ / "RAIS Emprego Formal.Report"
DEF = REPORT / "definition"
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json"
HTML = "htmlContent443BE3AD55E043BF878BED274D3A6865"
SLICER_PRESET = ""


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def cor(h):
    return {"solid": {"color": {"expr": {"Literal": {"Value": f"'{h}'"}}}}}


def cor_medida(nome):
    return {"solid": {"color": {"expr": {"Measure": {"Expression": {"SourceRef": {"Entity": "_medidas"}}, "Property": nome}}}}}


def coluna(tabela, nome, ativa=True):
    p = {"field": {"Column": {"Expression": {"SourceRef": {"Entity": tabela}}, "Property": nome}}, "queryRef": f"{tabela}.{nome}", "nativeQueryRef": nome}
    if ativa:
        p["active"] = True
    return p


def medida(nome, exibir=None, fmt=None):
    p = {"field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_medidas"}}, "Property": nome}}, "queryRef": f"_medidas.{nome}", "nativeQueryRef": exibir or nome}
    if exibir:
        p["displayName"] = exibir
    if fmt:
        p["format"] = fmt
    return p


def nome_visual(pagina, papel):
    return hashlib.md5(f"{pagina}:{papel}".encode()).hexdigest()[:20]


def salvar(caminho, obj):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def container(tooltip=None, titulo=False, extra=None, cabecalho=False):
    c = {"title": [{"properties": {"show": lit("false")}}], "background": [{"properties": {"show": lit("false")}}],
         "border": [{"properties": {"show": lit("false")}}], "subTitle": [{"properties": {"show": lit("false")}}],
         "visualHeader": [{"properties": {"show": lit("false")}}]}
    if cabecalho:       # mantém o cabeçalho do visual (aparece ao passar o mouse): modo foco, filtros e opções
        c["visualHeader"] = [{"properties": {"show": lit("true")}}]
    if tooltip:
        c["visualTooltip"] = [{"properties": {"section": lit(f"'{tooltip}'"), "type": lit("'Canvas'"), "show": lit("true")}}]
    if extra:
        c.update(extra)
    return c


def visual(nome, tipo, pos, query, objetos, cont=None, drill=True, sync=None, filtros=None, sort=None):
    v = {"$schema": SCHEMA, "name": nome,
         "position": {"x": round(pos[0], 1), "y": round(pos[1], 1), "z": pos[4], "height": round(pos[3], 1), "width": round(pos[2], 1), "tabOrder": pos[4]},
         "visual": {"visualType": tipo, "objects": objetos, "visualContainerObjects": cont or container(), "drillFilterOtherVisuals": drill}}
    if query:
        v["visual"] = {"visualType": tipo, "query": {"queryState": query}, **{k: x for k, x in v["visual"].items() if k != "visualType"}}
    if sort:
        v["visual"]["query"]["sortDefinition"] = sort
    if sync:
        v["visual"]["syncGroup"] = {"groupName": sync, "fieldChanges": False, "filterChanges": True}
    if filtros:
        v["filterConfig"] = {"filters": filtros}
    return v


def filtro_in(tabela, coluna_, valores, numerico=False):
    """Filtro categórico 'em' (visual ou página)."""
    vals = [[{"Literal": {"Value": f"{x}L" if numerico else f"'{x}'"}}] for x in valores]
    return {"name": uuid.uuid4().hex[:20], "field": {"Column": {"Expression": {"SourceRef": {"Entity": tabela}}, "Property": coluna_}}, "type": "Categorical",
            "filter": {"Version": 2, "From": [{"Name": "d", "Entity": tabela, "Type": 0}],
                       "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": coluna_}}], "Values": vals}}}]},
            "howCreated": "User"}


# ------------------------------------------------------------------ visuais
def html(nome, pos, medida_nome, tooltip=None):
    c = container(tooltip=tooltip)
    c["padding"] = [{"properties": {k: lit("0D") for k in ("top", "bottom", "left", "right")}}]
    if not tooltip:
        c["visualTooltip"] = [{"properties": {"show": lit("false")}}]
    return visual(nome, HTML, pos, {"content": {"projections": [medida(medida_nome)]}}, {"compatibility": [{"properties": {"legacyRendering": lit("false")}}]}, c)


def slicer_dropdown(nome, pos, tabela, col, sync, titulo, inicial=None, unico=False, ordenar=None):
    obj = {"data": [{"properties": {"mode": lit("'Dropdown'")}}],
           "selection": [{"properties": {"selectAllCheckboxEnabled": lit("false" if unico else "true"), "strictSingleSelect": lit("true" if unico else "false")}}],
           "header": [{"properties": {"textSize": lit("16D"), "show": lit("false")}}],
           "pendingChangesIcon": [{"properties": {"show": lit("false")}}], "items": [{"properties": {"textSize": lit("18D")}}]}
    if inicial is not None:
        obj["general"] = [{"properties": {"filter": {"filter": {"Version": 2, "From": [{"Name": "d", "Entity": tabela, "Type": 0}], "Where": [{"Condition": {"In": {
            "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": col}}], "Values": [[{"Literal": {"Value": f"{inicial}L"}}]]}}}]}}}}]
    cont = container()
    cont["title"] = [{"properties": {"show": lit("false"), "text": lit(f"'{titulo}'")}}]
    cont["padding"] = [{"properties": {k: lit("0D") for k in ("top", "bottom", "left", "right")}}]
    sort = {"sort": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": tabela}}, "Property": ordenar or col}}, "direction": "Ascending"}], "isDefaultSort": True}
    return visual(nome, "slicer", pos, {"Values": {"projections": [coluna(tabela, col)]}}, obj, cont, sync=sync, sort=sort)


def slicer_comparavel(nome, pos, sync):
    obj = {"data": [{"properties": {"mode": lit("'Basic'")}}],
           "selection": [{"properties": {"selectAllCheckboxEnabled": lit("false"), "strictSingleSelect": lit("false")}}],
           "header": [{"properties": {"show": lit("false"), "textSize": lit("16D")}}],
           "pendingChangesIcon": [{"properties": {"show": lit("false")}}], "items": [{"properties": {"textSize": lit("18D")}}]}
    cont = container()
    cont["padding"] = [{"properties": {k: lit("0D") for k in ("top", "bottom", "left", "right")}}]
    return visual(nome, "slicer", pos, {"Values": {"projections": [coluna("D_Comparavel", "comparavel_AFL_rotulo")]}}, obj, cont, sync=sync,
                  filtros=[filtro_in("D_Comparavel", "comparavel_AFL", ["Sim"])])


def botoes_setor(nome, pos, tabela, col, n=5, inicial=None, fonte=16):
    """Botão de setor (5 mosaicos); o trilho está no fundo."""
    tema = lambda i: {"solid": {"color": {"expr": {"ThemeDataColor": {"ColorId": i, "Percent": 0}}}}}
    obj = {"layout": [{"properties": {"orientation": lit("2D"), "style": lit("'Cards'"), "autoGrid": lit("true"), "maxTiles": lit(f"{n}L")}}],
           "overFlow": [{"properties": {"overFlowDirection": lit("1D")}}],
           "value": [{"properties": {"show": lit("true")}}, {"properties": {"fontSize": lit(f"{fonte}D")}, "selector": {"id": "default"}},
                     {"properties": {"fontColor": tema(0)}, "selector": {"id": "selection:selected"}}],
           "fillCustom": [{"properties": {"show": lit("true")}, "selector": {"id": "default"}}] +
                         [{"properties": {"fillColor": tema(5)}, "selector": {"id": s}} for s in ("interaction:hover", "interaction:press", "selection:selected")],
           "outline": [{"properties": {"show": lit("false")}, "selector": {"id": "default"}}],
           "background": [{"properties": {"show": lit("false")}, "selector": {"id": "selection:selected"}}]}
    if inicial is not None:
        obj["general"] = [{"properties": {"filter": {"filter": {"Version": 2, "From": [{"Name": "d", "Entity": tabela, "Type": 0}], "Where": [{"Condition": {"In": {
            "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": col}}], "Values": [[{"Literal": {"Value": f"'{inicial}'"}}]]}}}]}}}}]
    cont = {"stylePreset": [{"properties": {"name": lit("''")}}], "title": [{"properties": {"show": lit("false")}}]}
    return visual(nome, "advancedSlicerVisual", pos, {"Values": {"projections": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": tabela}}, "Property": col}},
                                                                                "queryRef": f"{tabela}.{col}", "nativeQueryRef": col}]}}, obj, cont)


def limpar(nome, pos, recursos):
    """Botão Limpar filtros: imagem com 3 estados (SVGs registrados) e ação ClearAllSlicers."""
    def estado(arq, sel=None):
        base = arq.rsplit(".", 1)[0].rstrip("0123456789") + ".svg"
        p = {"properties": {"sourceFile": {"image": {"name": lit(f"'{base}'"),
                                                     "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageType": 1, "ItemName": arq}}},
                                                     "scaling": lit("'Normal'")}}}}
        if sel:
            p["selector"] = {"id": sel}
        return p
    obj = {"image": [estado(recursos["normal"]), estado(recursos["hover"], "hover"), estado(recursos["press"], "press")]}
    cont = {"visualLink": [{"properties": {"show": lit("true"), "type": lit("'ClearAllSlicers'")}}]}
    return visual(nome, "image", pos, {}, obj, cont)


def _eixos():
    return {"categoryAxis": [{"properties": {"fontSize": lit("16D"), "fontFamily": lit("'Segoe UI'"), "showAxisTitle": lit("false")}}],
            "legend": [{"properties": {"show": lit("false")}}], "general": [{"properties": {"responsive": lit("false")}}]}


def linhas(nome, pos, categoria, series, tooltips=None, tracejadas=(), continuo=False):
    """Gráfico de linhas; series = [(medida, rótulo, cor, formato)]; cada série com marcador e linha de 3 px; sem rótulos de dados."""
    q = {"Category": {"projections": [categoria]}, "Y": {"projections": [medida(m, r, f) for m, r, c, f in series]}}
    if tooltips:
        q["Tooltips"] = {"projections": [medida(m, r, f) for m, r, f in tooltips]}
    o = _eixos()
    o["dataPoint"] = [{"properties": {"fill": cor(c)}, "selector": {"metadata": f"_medidas.{m}"}} for m, r, c, f in series]
    o["lineStyles"] = [{"properties": {"strokeWidth": lit("3L"), "showMarker": lit("true"), "markerColor": cor(c), "lineChartType": lit("'straight'"), **({"lineStyle": lit("'dashed'")} if m in tracejadas else {})},
                        "selector": {"metadata": f"_medidas.{m}"}} for m, r, c, f in series]
    o["labels"] = [{"properties": {"show": lit("false")}}]
    o["categoryAxis"][0]["properties"]["axisType"] = lit("'Continuous'" if continuo else "'Categorical'")
    if continuo:
        o["categoryAxis"][0]["properties"].update({"labelAngle": lit("0L")})
    o["valueAxis"] = [{"properties": {"fontSize": lit("16D"), "fontFamily": lit("'Segoe UI'"), "gridlineColor": cor("#EEEEEF"), "showAxisTitle": lit("false")}}]
    return visual(nome, "lineChart", pos, q, o, container())


def barras(nome, pos, categoria, medida_valor, exibir, fmt, cor_fixa="#1D1E21", cor_por_medida=None, tooltips=None, rotulos=True, foco=False, espaco=18, fonte=16):
    """Barras horizontais ordenadas pelo valor (decrescente), rótulo completo fora da barra."""
    q = {"Category": {"projections": [categoria]}, "Y": {"projections": [medida(medida_valor, exibir, fmt)]}}
    if tooltips:
        q["Tooltips"] = {"projections": [medida(m, r, f) for m, r, f in tooltips]}
    o = _eixos()
    if cor_por_medida:
        o["dataPoint"] = [{"properties": {"fill": cor_medida(cor_por_medida)}, "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}}]
    else:
        o["dataPoint"] = [{"properties": {"fill": cor(cor_fixa)}, "selector": {"metadata": f"_medidas.{medida_valor}"}}]
    o["labels"] = [{"properties": {"show": lit("true" if rotulos else "false"), "fontSize": lit("16D"), "fontFamily": lit("'Segoe UI'"), "color": cor("#1D1E21"),
                                   "labelDisplayUnits": lit("1D"), "labelPosition": lit("'OutsideEnd'")}}]
    o["categoryAxis"][0]["properties"].update({"innerPadding": lit(f"{espaco}L"), "maxMarginFactor": lit("40L"), "preferredCategoryWidth": lit("40D"), "fontSize": lit(f"{fonte}D")})
    o["valueAxis"] = [{"properties": {"show": lit("false")}}]
    sort = {"sort": [{"field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_medidas"}}, "Property": medida_valor}}, "direction": "Descending"}]}
    return visual(nome, "clusteredBarChart", pos, q, o, container(cabecalho=foco), sort=sort)


def barras_grupo(nome, pos, categoria, series, fmt, ordem_por=None, tooltips=None, empilhado=False, sort_cat=None, foco=False, espaco=None, fonte=16):
    """Barras horizontais com mais de uma série (AFL × Comparáveis, ou mulheres × homens empilhados).
    series = [(medida, rótulo, cor)]; ordena pela medida `ordem_por` (decrescente) ou pela coluna `sort_cat` (tabela, coluna, direção)."""
    q = {"Category": {"projections": [categoria]}, "Y": {"projections": [medida(m, r, fmt) for m, r, c in series]}}
    if tooltips:
        q["Tooltips"] = {"projections": [medida(m, r, f) for m, r, f in tooltips]}
    o = _eixos()
    o["dataPoint"] = [{"properties": {"fill": cor(c)}, "selector": {"metadata": f"_medidas.{m}"}} for m, r, c in series]
    o["labels"] = [{"properties": {"show": lit("true"), "fontSize": lit("16D"), "fontFamily": lit("'Segoe UI'"), "color": cor("#1D1E21"),
                                   "labelDisplayUnits": lit("1D"), **({} if empilhado else {"labelPosition": lit("'OutsideEnd'")})}}]
    o["categoryAxis"][0]["properties"].update({"innerPadding": lit(f"{espaco}L" if espaco is not None else ("12L" if not empilhado else "6L")), "maxMarginFactor": lit("40L"), "preferredCategoryWidth": lit("40D"), "fontSize": lit(f"{fonte}D")})
    o["valueAxis"] = [{"properties": {"show": lit("false")}}]
    if sort_cat:
        tab, col, d = sort_cat
        sort = {"sort": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": tab}}, "Property": col}}, "direction": d}]}
    else:
        sort = {"sort": [{"field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_medidas"}}, "Property": ordem_por or series[0][0]}}, "direction": "Descending"}]}
    return visual(nome, "barChart" if empilhado else "clusteredBarChart", pos, q, o, container(cabecalho=foco), sort=sort)


def pagina_tooltip(pid, nome, medida_nome, largura=600, altura=450):
    """Página de tooltip (600 × 450) com um visual HTML; devolve (page.json, visual.json, nome do visual)."""
    pagina = {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json", "name": pid, "displayName": nome,
              "displayOption": "FitToPage", "height": altura, "width": largura, "visibility": "HiddenInViewMode", "type": "Tooltip"}
    v = nome_visual(pid, "dica")
    vis = visual(v, HTML, (0, 0, largura, altura, 0), {"content": {"projections": [medida(medida_nome)]}}, {"compatibility": [{"properties": {"legacyRendering": lit("false")}}]}, container())
    vis["visual"]["visualContainerObjects"]["padding"] = [{"properties": {k: lit("0D") for k in ("top", "bottom", "left", "right")}}]
    return pagina, vis, v


def gatilho_info(nome, pos, chave, pagina_tooltip):
    """Mini-coluna nativa 100% transparente sobre o (i) do fundo; a chave da D_Info chega ao tooltip como categoria."""
    obj = {"dataPoint": [{"properties": {"fill": cor("#FFFFFF"), "fillTransparency": lit("100D")}}],
           "labels": [{"properties": {"show": lit("false")}}],
           "categoryAxis": [{"properties": {"show": lit("false"), "innerPadding": lit("0D")}}],
           "valueAxis": [{"properties": {"show": lit("false"), "start": lit("0D"), "end": lit("1D"), "gridlineShow": lit("false")}}],
           "legend": [{"properties": {"show": lit("false")}}], "general": [{"properties": {"responsive": lit("false")}}]}
    q = {"Y": {"projections": [medida("Info_Gatilho_Valor")]}, "Category": {"projections": [coluna("D_Info", "Chave")]}}
    cont = container(tooltip=pagina_tooltip)
    return visual(nome, "clusteredColumnChart", pos, q, obj, cont, filtros=[filtro_in("D_Info", "Chave", [chave])])


def colunas_grupo(nome, pos, categoria, series, fmt, tooltips=None, tooltip_pagina=None):
    """Colunas agrupadas por ano (série = [(medida, rótulo, cor)]), sem rótulos de dados; o detalhe vem no tooltip."""
    q = {"Category": {"projections": [categoria]}, "Y": {"projections": [medida(m, r, fmt) for m, r, c in series]}}
    if tooltips:
        q["Tooltips"] = {"projections": [medida(m, r, f) for m, r, f in tooltips]}
    o = _eixos()
    o["dataPoint"] = [{"properties": {"fill": cor(c)}, "selector": {"metadata": f"_medidas.{m}"}} for m, r, c in series]
    o["labels"] = [{"properties": {"show": lit("false")}}]
    o["categoryAxis"][0]["properties"]["axisType"] = lit("'Categorical'")
    o["valueAxis"] = [{"properties": {"fontSize": lit("16D"), "fontFamily": lit("'Segoe UI'"), "gridlineColor": cor("#EEEEEF"), "showAxisTitle": lit("false"), "labelDisplayUnits": lit("1D")}}]
    return visual(nome, "clusteredColumnChart", pos, q, o, container(tooltip=tooltip_pagina))
