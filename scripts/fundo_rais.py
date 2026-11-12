"""Fundos das páginas do painel RAIS (SVG + PNG 2×, 1920 × 1652), no padrão visual do RF (design system Painéis AFL v3).

Tudo que é estático vai no fundo: abas com texto, logo, rótulos e caixas dos filtros, molduras dos cards com sombra, acento dos KPIs,
trilho dos botões de setor, legendas fixas e a nota de rodapé. No Power BI ficam só botões, segmentadores e visuais.
Temas (abas): Empregos · Quem trabalha · Quanto ganha · Quem contrata; recortes: Todos os setores · AFL.
"""
import re
import subprocess
from pathlib import Path

from texto_path import largura, texto

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "docs" / "fundos"
ICONES = RAIZ / "assets" / "icones"
LOGO = RAIZ / "assets" / "logo-abrasel-verde.svg"
EDGE = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

W, H = 1920, 1652
M, G, NCOL = 40, 16, 12
COL = (W - 2 * M - (NCOL - 1) * G) / NCOL
cx = lambda i: M + i * (COL + G)
cw = lambda n: n * COL + (n - 1) * G
R = lambda v: round(v, 1)
PT = lambda pt: pt * 4 / 3
K = {"card": "#FFFFFF", "borda": "#DDDDDE", "linha": "#E8E8E9", "tinta": "#1D1E21", "tinta2": "#434446", "acao": "#F58220", "acao_txt": "#B86218",
     "acao_suave": "#FDF7F1", "aviso_fundo": "#FEF0C7", "aviso_txt": "#B54708", "verde": "#17B26A"}
TEMAS = ["Empregos", "Quem trabalha", "Quanto ganha", "Quem contrata"]
RECORTES = ["Todos os setores", "AFL"]
ABA_Y, ABA_H, ABA_W, ABA_GAP = 24, 56, 224, 32
FL_ROT, FL_Y, FL_H, LIMPAR_W = 124, 136, 48, 220
KPI_Y, KPI_H, L2_Y, L2_H, L3_Y, L3_H, NOTA_Y, NOTA_H = 324, 192, 540, 456, 1020, 520, 1572, 56

DEFS = """<defs><filter id="md" x="-5%" y="-5%" width="110%" height="115%" color-interpolation-filters="sRGB">
<feMorphology in="SourceAlpha" operator="erode" radius="1" result="e1"/><feGaussianBlur in="e1" stdDeviation="3" result="b1"/><feOffset in="b1" dy="4" result="o1"/>
<feComponentTransfer in="o1" result="s1"><feFuncA type="linear" slope="0.10"/></feComponentTransfer>
<feMorphology in="SourceAlpha" operator="erode" radius="2" result="e2"/><feGaussianBlur in="e2" stdDeviation="2" result="b2"/><feOffset in="b2" dy="2" result="o2"/>
<feComponentTransfer in="o2" result="s2"><feFuncA type="linear" slope="0.10"/></feComponentTransfer>
<feMerge><feMergeNode in="s1"/><feMergeNode in="s2"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>"""

# filtros por recorte: (rótulo, largura fixa ou None = divide o resto)
FILTROS = {
    "Todos os setores": [("Ano", 140), ("Setores", 360), ("Localização", None), ("Sexo", None), ("Escolaridade", None), ("Raça/cor", None)],
    "AFL": [("Ano", 140), ("CNAE AFL", 300), ("Localização", None), ("Sexo", None), ("Escolaridade", None), ("Raça/cor", None)],
}


def icone(nome, x, y, tam=24, cor="#434446"):
    corpo = re.search(r"<svg[^>]*>(.*)</svg>", (ICONES / f"{nome}.svg").read_text(encoding="utf-8"), re.S).group(1)
    corpo = re.sub(r"<!--.*?-->", "", corpo, flags=re.S).strip()
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({tam / 24:g})" fill="none" stroke="{cor}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{corpo}</g>')


def logo(x, y, h):
    corpo = re.search(r"<svg[^>]*>(.*)</svg>", LOGO.read_text(encoding="utf-8"), re.S).group(1).strip()
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({h / 120:.5f})">{corpo}</g>'


def card(x, y, w, h, acento=None):
    s = [f'<rect x="{R(x) + .5}" y="{R(y) + .5}" width="{R(w) - 1}" height="{R(h) - 1}" rx="8" fill="{K["card"]}" stroke="{K["borda"]}" filter="url(#md)"/>']
    if acento:
        s.append(f'<path d="M{R(x) + 8},{R(y)} H{R(x + w) - 8} A8,8 0 0 1 {R(x + w)},{R(y) + 8} V{R(y) + 4} H{R(x)} V{R(y) + 8} A8,8 0 0 1 {R(x) + 8},{R(y)} Z" fill="{acento}"/>')
    return s


def navegacao(tema, recorte):
    s, x = [], M
    for grupo, abas, ativo in (("Tema", TEMAS, tema), ("Recorte", RECORTES, recorte)):
        gw = ABA_W * len(abas)
        s.append(f'<rect x="{x}" y="{ABA_Y + ABA_H}" width="{gw}" height="1" fill="{K["linha"]}"/>')
        for i, nome in enumerate(abas):
            ax, atual = x + i * ABA_W, nome == ativo
            if atual:
                s.append(f'<rect x="{ax}" y="{ABA_Y + ABA_H - 2}" width="{ABA_W}" height="3" fill="{K["acao"]}"/>')
            s.append(texto(nome, ax + ABA_W / 2, ABA_Y + 36.5, PT(18), K["acao_txt"] if atual else K["tinta"], 600 if atual else 400, "middle"))
        x += gw + ABA_GAP
    s.append(logo(W - M - 630 / 120 * 32, ABA_Y + 12, 32))
    return s


def filtros(recorte):
    """Rótulos e caixas dos segmentadores; devolve (svg, posições x/larg por rótulo) para posicionar os visuais."""
    itens = FILTROS[recorte]
    lx = W - M - LIMPAR_W
    livre = lx - G - M - (len(itens) - 1) * G - sum(w for _, w in itens if w)
    resto = livre / sum(1 for _, w in itens if not w)
    s, pos, sx = [], {}, M
    for nome, w in itens:
        sw = w or resto
        s.append(texto(nome, sx, FL_ROT, PT(18), K["tinta2"], 600))
        # A moldura do campo fica no fundo; o segmentador sobreposto não tem borda.
        # A moldura pertence ao fundo; o segmentador sobreposto permanece sem borda.
        s.append(f'<rect x="{R(sx) + .5}" y="{FL_Y + .5}" width="{R(sw) - 1}" height="{FL_H - 1}" rx="4" fill="{K["card"]}" stroke="{K["borda"]}"/>')
        pos[nome] = (R(sx), R(sw))
        sx += sw + G
    pos["Limpar"] = (lx, LIMPAR_W)
    return s, pos


def trilho_setores(x, y, w, n=5):
    """Trilho dos botões de setor (5 segmentos) dentro de um card."""
    s = [f'<rect x="{R(x) + .5}" y="{y + .5}" width="{R(w) - 1}" height="47" rx="4" fill="{K["card"]}" stroke="{K["borda"]}"/>']
    s += [f'<rect x="{R(x + j * w / n)}" y="{y + 10}" width="1" height="28" fill="{K["borda"]}"/>' for j in range(1, n)]
    return s


def legenda(x, y, itens):
    """Legenda fixa: itens = [(rótulo, cor, 'quadro' | 'linha' | 'tracejado')]."""
    s, cursor = [], x
    for rot, cor, forma in itens:
        if forma == "quadro":
            s.append(f'<rect x="{R(cursor)}" y="{y}" width="14" height="14" rx="3" fill="{cor}"/>')
            cursor += 22
        elif forma == "tracejado":
            s.append(f'<rect x="{R(cursor)}" y="{y + 5}" width="8" height="4" rx="1" fill="{cor}"/><rect x="{R(cursor) + 14}" y="{y + 5}" width="8" height="4" rx="1" fill="{cor}"/>')
            cursor += 34
        else:
            s.append(f'<rect x="{R(cursor)}" y="{y + 5}" width="26" height="4" rx="2" fill="{cor}"/>')
            cursor += 34
        s.append(texto(rot, cursor, y + 13, PT(16), K["tinta2"]))
        cursor += largura(rot, PT(16)) + 28
    return s


def nota(texto_nota):
    s = [f'<rect x="{M}" y="{NOTA_Y}" width="{W - 2 * M}" height="{NOTA_H}" rx="8" fill="{K["aviso_fundo"]}"/>',
         icone("triangle-alert", 60, NOTA_Y + 16, 24, K["aviso_txt"])]
    linhas = [texto_nota] if largura(texto_nota, PT(16)) < W - 2 * M - 110 else None
    if linhas is None:                       # quebra em duas linhas
        palavras, a, b = texto_nota.split(" "), "", ""
        for p in palavras:
            if largura(a + " " + p, PT(16)) < W - 2 * M - 130 and not b:
                a = (a + " " + p).strip()
            else:
                b = (b + " " + p).strip()
        linhas = [a, b]
    if len(linhas) == 1:
        s.append(texto(linhas[0], 104, NOTA_Y + 35, PT(16), K["aviso_txt"]))
    else:
        s.append(texto(linhas[0], 104, NOTA_Y + 24, PT(16), K["aviso_txt"]))
        s.append(texto(linhas[1], 104, NOTA_Y + 47, PT(16), K["aviso_txt"]))
    return s


def posicoes_cartoes():
    """(x, y, largura) de cada cartão; o (i) fica no canto superior direito."""
    return {"K1": (cx(0), KPI_Y, cw(4)), "K2": (cx(4), KPI_Y, cw(4)), "K3": (cx(8), KPI_Y, cw(4)), "L2A": (cx(0), L2_Y, cw(8)), "L2B": (cx(8), L2_Y, cw(4)),
            "L3A": (cx(0), L3_Y, cw(8)), "L3B": (cx(8), L3_Y, cw(4))}


def centro_info(cartao):
    x, y, w = posicoes_cartoes()[cartao]
    return x + w - 38, y + 40


def icones_info():
    s = []
    for c in posicoes_cartoes():
        ix, iy = centro_info(c)
        s.append(icone("info", ix - 12, iy - 12, 24, K["tinta2"]))
    return s


def montar(tema, recorte, cfg):
    """cfg: acentos (3 cores dos KPIs), legendas {'L2A': [...]}, trilho (bool), nota (texto). Devolve (svg, geometria dos filtros)."""
    s = [navegacao(tema, recorte)]
    f, pos = filtros(recorte)
    s.append(f)
    kx = [cx(0), cx(4), cx(8)]
    for x, cor in zip(kx, cfg["acentos"]):
        s.append(card(x, KPI_Y, cw(4), KPI_H, cor))
    s.append(card(cx(0), L2_Y, cw(8), L2_H))
    s.append(card(cx(8), L2_Y, cw(4), L2_H))
    s.append(card(cx(0), L3_Y, cw(8), L3_H))
    s.append(card(cx(8), L3_Y, cw(4), L3_H))
    for chave, (x, y) in {"L2A": (cx(0) + 24, L2_Y + 106), "L2B": (cx(8) + 24, L2_Y + 122), "L3A": (cx(0) + 24, L3_Y + 124), "L3B": (cx(8) + 24, L3_Y + 108)}.items():
        if cfg.get("legendas", {}).get(chave):
            s.append(legenda(x, y, cfg["legendas"][chave]))
    if cfg.get("trilho_ind"):
        s.append(trilho_setores(cx(0) + 24, L2_Y + 100, cw(8) - 48, 7))
    if cfg.get("trilho"):
        s.append(trilho_setores(cx(0) + 24, L3_Y + 100, cw(8) - 48))
    s.append(icones_info())
    s.append(nota(cfg["nota"]))
    plano = [e for grupo in s for e in grupo]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n{DEFS}\n<rect width="{W}" height="{H}" fill="#FFFFFF"/>\n'
           + "\n".join(plano) + "\n</svg>\n")
    return svg, pos


def gravar(nome, tema, recorte, cfg):
    SAIDA.mkdir(parents=True, exist_ok=True)
    svg, pos = montar(tema, recorte, cfg)
    arq = SAIDA / f"{nome}-bg.svg"
    arq.write_text(svg, encoding="utf-8")
    png = SAIDA / f"{nome}-bg.png"
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2", f"--screenshot={png}",
                    f"--window-size={W},{H}", arq.as_uri()], capture_output=True, check=True)
    return png, pos
