"""Navegação entre as 8 páginas do painel RAIS (Tema × Recorte), por botões transparentes sobre as abas desenhadas no fundo.

Mesmo padrão do RF: cada página recebe um botão por aba que não é a ativa; normal = transparente (revela o rótulo do fundo), hover = #F58220 com texto
branco, press = #B86218; ação PageNavigation direta. Alterar o tema preserva o recorte e vice-versa. Chamado ao final de pagina_rais.py.
"""
import copy

import fundo_rais as fb
import pbir_rais as pb

lit, cor = pb.lit, pb.cor


def botao(nome, rotulo, x, destino, z):
    def estado(fundo, i):
        return {"properties": {"fillColor": cor(fundo), "transparency": lit("100D" if i == "default" else "0D")}, "selector": {"id": i}}
    texto = {"properties": {"show": lit("true"), "text": lit(f"'{rotulo}'"), "fontSize": lit("18D"), "fontColor": cor("#FFFFFF"), "horizontalAlignment": lit("'center'")}}
    return {
        "$schema": pb.SCHEMA, "name": nome,
        "position": {"x": x, "y": fb.ABA_Y, "z": z, "height": fb.ABA_H, "width": fb.ABA_W, "tabOrder": z},
        "visual": {
            "visualType": "actionButton",
            "objects": {
                "icon": [{"properties": {"show": lit("false")}}],
                "fill": [{"properties": {"show": lit("true")}}, estado("#FFFFFF", "default"), estado("#F58220", "hover"), estado("#B86218", "press")],
                "text": [{"properties": {"show": lit("true")}}, {**copy.deepcopy(texto), "selector": {"id": "hover"}}, {**copy.deepcopy(texto), "selector": {"id": "press"}}],
                "outline": [{"properties": {"show": lit("false")}}],
                "shape": [{"properties": {"tileShape": lit("'rectangle'")}}],
            },
            "visualContainerObjects": {
                "visualLink": [{"properties": {"show": lit("true"), "type": lit("'PageNavigation'"), "navigationSection": lit(f"'{destino}'")}}],
                "background": [{"properties": {"show": lit("false")}}], "border": [{"properties": {"show": lit("false")}}],
                "visualHeader": [{"properties": {"show": lit("false")}}],
                "general": [{"properties": {"altText": lit(f"'Ir para {rotulo}'")}}],
            },
            "drillFilterOtherVisuals": True,
        },
        "howCreated": "InsertVisualButton",
    }


def gerar(ids):
    """ids: {(tema, recorte): id da página}. Cria os botões nas 8 páginas."""
    total = 0
    for (tema, recorte), pid in ids.items():
        z = 30000
        x = fb.M
        for grupo, abas, ativo in (("Tema", fb.TEMAS, tema), ("Recorte", fb.RECORTES, recorte)):
            for i, rotulo in enumerate(abas):
                if rotulo != ativo:
                    destino = ids[(rotulo, recorte)] if grupo == "Tema" else ids[(tema, rotulo)]
                    nome = pb.nome_visual(pid, f"nav_{rotulo}")
                    pb.salvar(pb.DEF / "pages" / pid / "visuals" / nome / "visual.json", botao(nome, rotulo, x + i * fb.ABA_W, destino, z))
                    total += 1
                z += 1
            x += fb.ABA_W * len(abas) + fb.ABA_GAP
    print(total, "botões de navegação")
