"""Prévias das páginas do painel RAIS (HTML 1920 px + PNG), com os números reais de docs/previa/indicadores.json.

Servem para alinhar análises e layout antes de montar no Power BI. Seguem o design system dos painéis AFL (RF):
abas no topo, filtros sem cabeçalho, manchete-afirmação + contexto, 3 KPIs com acento, 4 cards com título-afirmação e (i),
AFL em laranja só contra cinza, comparação de referência AFL × Comparáveis, nota fixa da quebra de 2022.
"""
import html
import json
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PREVIA = RAIZ / "docs" / "previa"
I = json.loads((PREVIA / "indicadores.json").read_text(encoding="utf-8"))
EDGE = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
ANO = I["ano"]
LARANJA, CINZA, TINTA, TINTA2, LINHA = "#F58220", "#C4C5C8", "#1D1E21", "#434446", "#E8E8E9"
MULHER, HOMEM = "#7F56D9", "#0E9384"           # papéis novos da RAIS (não usados no RF)
SEQ = ["#E0E7FF", "#A5B4FC", "#6366F1", "#312E81"]  # escolaridade (do menor ao maior nível)


# ------------------------------------------------------------------ formatos
def n(x):
    return f"{round(x):,}".replace(",", ".")


def p(x, d=1, sinal=False):
    if abs(x * 100) < 0.5 * 10 ** -d:
        return "0," + "0" * d + "%" if d else "0%"
    s = f"{x * 100:+.{d}f}" if sinal else f"{x * 100:.{d}f}"
    return s.replace(".", ",").replace("-", "−") + "%"


def r(x, d=0):
    s = f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + s


def e(t):
    return html.escape(str(t))


# ------------------------------------------------------------------ peças
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1920px;background:#fff;font-family:'Segoe UI',Arial,sans-serif;color:#1D1E21;font-variant-numeric:tabular-nums;position:relative}
.abs{position:absolute}
.aba{position:absolute;top:24px;height:56px;width:224px;display:flex;align-items:center;justify-content:center;font-size:24px;color:#1D1E21;border-bottom:1px solid #E8E8E9}
.aba.on{color:#B86218;font-weight:600;border-bottom:3px solid #F58220}
.logo{position:absolute;top:30px;right:40px;font-size:46px;font-weight:800;color:#00652E;letter-spacing:-1px}
.rot{position:absolute;top:104px;font-size:24px;font-weight:600;color:#434446}
.cx{position:absolute;top:136px;height:48px;border:1px solid #DDDDDE;border-radius:4px;font-size:22px;padding:9px 12px;color:#1D1E21;display:flex;justify-content:space-between;align-items:center}
.card{position:absolute;background:#fff;border:1px solid #DDDDDE;border-radius:8px;box-shadow:0 4px 6px -1px rgba(0,0,0,.1),0 2px 4px -2px rgba(0,0,0,.1)}
.acento{position:absolute;top:-1px;left:-1px;right:-1px;height:4px;border-radius:8px 8px 0 0}
.info{position:absolute;width:28px;height:28px;border:2px solid #434446;border-radius:50%;font-size:18px;font-weight:700;color:#434446;display:flex;align-items:center;justify-content:center;font-style:italic}
.tit{position:absolute;left:24px;top:18px;right:72px}
.tit b{display:block;font-size:26px;line-height:32px;font-weight:600}
.tit span{display:block;font-size:21px;line-height:27px;color:#434446}
.kpi-r{font-size:24px;font-weight:600;color:#434446}
.kpi-v{font-size:56px;line-height:64px;font-weight:600;margin-top:4px}
.kpi-l{font-size:22px;color:#434446;margin-top:4px;display:flex;gap:8px;align-items:center;flex-wrap:nowrap;white-space:nowrap}
.chip{display:inline-block;padding:1px 9px;border-radius:6px;font-size:20px;font-weight:600}
.chip.afl{border:1px solid #F58220;background:#FDF7F1;color:#B86218}
.chip.ref{border:1px solid #434446;background:#F2F4F7;color:#1D1E21}
.chip.ref small{font-weight:400;color:#434446;font-size:17px}
.nota{position:absolute;left:40px;right:40px;height:56px;border-radius:8px;background:#FEF0C7;color:#B54708;font-size:21px;display:flex;align-items:center;padding:0 22px;gap:14px}
.leg{font-size:20px;color:#434446;display:flex;gap:22px;align-items:center}
.leg i{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:7px;vertical-align:-1px}
"""


def topo(tema, recorte, filtros):
    s = []
    temas = ["Empregos", "Quem trabalha", "Quanto ganha"]
    for i, t in enumerate(temas):
        s.append(f'<div class="aba{" on" if t == tema else ""}" style="left:{40 + i * 224}px">{t}</div>')
    for i, t in enumerate(["Todos os setores", "AFL"]):
        s.append(f'<div class="aba{" on" if t == recorte else ""}" style="left:{40 + 3 * 224 + 32 + i * 224}px">{t}</div>')
    s.append('<div class="logo">abrasel</div>')
    x = 40
    for rot, val, w in filtros:
        s.append(f'<div class="rot" style="left:{x}px">{e(rot)}</div>')
        seta = "" if val.startswith("☐") else '<span style="font-size:18px">⌄</span>'
        s.append(f'<div class="cx" style="left:{x}px;width:{w}px"><span>{e(val)}</span>{seta}</div>')
        x += w + 16
    s.append('<div class="cx" style="left:1660px;width:220px;justify-content:center;font-weight:600">⛉ Limpar filtros</div>')
    return "".join(s)


def manchete(titulo, contexto, dica=""):
    return (f'<div class="abs" style="left:40px;top:208px;right:96px;font-size:38px;line-height:46px;font-weight:600">{e(titulo)}</div>'
            f'<div class="abs" style="left:40px;top:258px;font-size:24px;color:#434446">{e(contexto)}</div>'
            + (f'<div class="abs" style="left:40px;top:290px;font-size:21px;color:#6B6C70">{e(dica)}</div>' if dica else "")
            + '<div class="info" style="left:1848px;top:226px">i</div>')


def kpi(x, cor, rotulo, valor, linhas):
    corpo = "".join(f'<div class="kpi-l">{l}</div>' for l in linhas)
    return (f'<div class="card" style="left:{x}px;top:324px;width:601.7px;height:192px"><div class="acento" style="background:{cor}"></div>'
            f'<div class="abs" style="left:20px;top:20px;right:60px"><div class="kpi-r">{e(rotulo)}</div><div class="kpi-v">{valor}</div>{corpo}</div>'
            f'<div class="info" style="right:20px;top:24px;width:24px;height:24px;font-size:15px">i</div></div>')


def chip_afl(t):
    return f'<span class="chip afl">AFL {t}</span>'


def chip_ref(t):
    return f'<span class="chip ref">Comparáveis {t} <small>· ref.</small></span>'


def card(x, y, w, h, titulo, sub, corpo, leg=""):
    return (f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;display:flex;flex-direction:column;padding:18px 24px 14px 24px">'
            f'<div style="padding-right:48px"><div style="font-size:26px;line-height:32px;font-weight:600">{e(titulo)}</div>'
            + (f'<div style="font-size:21px;line-height:27px;color:#434446">{e(sub)}</div>' if sub else "") + "</div>"
            + (f'<div class="leg" style="margin-top:8px;flex-wrap:wrap;gap:4px 22px">{leg}</div>' if leg else "")
            + f'<div style="flex:1;margin-top:12px;position:relative;overflow:hidden">{corpo}</div>'
            f'<div class="info" style="right:24px;top:24px">i</div></div>')


def tabela_contratos(C):
    cats = ["CLT por prazo indeterminado", "Prazo determinado ou temporário", "Intermitente", "Parcial", "Aprendiz"]
    linhas_t = "".join(f'<tr><td style="padding:9px 0;border-top:1px solid #E8E8E9">{c}</td>'
                       f'<td style="text-align:right;font-weight:600;border-top:1px solid #E8E8E9">{p(C["AFL"].get(c, 0))}</td>'
                       f'<td style="text-align:right;border-top:1px solid #E8E8E9;color:#434446">{p(C["Comparável"].get(c, 0))}</td></tr>' for c in cats)
    return ('<table style="width:100%;border-collapse:collapse;font-size:21px"><tr style="color:#434446"><th style="text-align:left;font-weight:600;padding-bottom:6px">Contrato</th>'
            '<th style="text-align:right;font-weight:600">AFL</th><th style="text-align:right;font-weight:600">Comparáveis</th></tr>' + linhas_t + "</table>")


def nota(y, texto):
    return f'<div class="nota" style="top:{y}px"><span style="font-size:24px">⚠</span><span>{e(texto)}</span></div>'


def pagina(nome, corpo, altura=1652):
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head><body style="height:{altura}px">{corpo}</body></html>'
    arq = PREVIA / f"{nome}.html"
    arq.write_text(doc, encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", f"--screenshot={PREVIA / (nome + '.png')}",
                    f"--window-size=1920,{altura}", arq.as_uri()], capture_output=True)
    return arq


# ------------------------------------------------------------------ gráficos (SVG)
def colunas_ano(serie, w, h, cor=TINTA, destaque=None):
    """Colunas por ano com rótulo = % sobre o ano anterior; espaço e marca na quebra de 2022."""
    anos = [s["ano"] for s in serie]
    gap = 40
    bw = (w - 60 - gap) / len(anos)
    vmax = max(s["v"] for s in serie) * 1.12
    base = h - 40
    out = [f'<svg width="{w}" height="{h}" font-family="Segoe UI" font-size="17">']
    xq = None
    for i, s in enumerate(serie):
        x = 30 + i * bw + (gap if s["ano"] >= 2022 else 0)
        if s["ano"] == 2022:
            xq = x - gap / 2 - 2
        bh = s["v"] / vmax * (base - 20)
        c = destaque.get(s["ano"], cor) if destaque else cor
        out.append(f'<rect x="{x + 5:.1f}" y="{base - bh:.1f}" width="{bw - 10:.1f}" height="{bh:.1f}" rx="2" fill="{c}"/>')
        rot = "" if s["var"] is None else p(s["var"], 1, True)
        cor_r = "#137547" if (s["var"] or 0) > 0 else "#B42318"
        if rot:
            out.append(f'<text x="{x + bw / 2:.1f}" y="{base - bh - 8:.1f}" text-anchor="middle" fill="{cor_r}" font-weight="600">{rot}</text>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="{base + 24}" text-anchor="middle" fill="#434446">{s["ano"]}</text>')
    if xq:
        out.append(f'<line x1="{xq}" y1="10" x2="{xq}" y2="{base}" stroke="#B54708" stroke-dasharray="5 4" stroke-width="2"/>')
        out.append(f'<text x="{xq + 8}" y="22" fill="#B54708" font-size="17">eSocial: não comparável com 2021</text>')
    out.append(f'<line x1="20" y1="{base}" x2="{w - 10}" y2="{base}" stroke="#C4C5C8"/></svg>')
    return "".join(out)


def barras_h(itens, w, h, fmt=n, rot_extra=None, largura_rot=330, cor_padrao=CINZA):
    """Barras horizontais com rótulo completo; item com 'afl' em laranja."""
    nb = len(itens)
    lh = h / nb
    vmax = max(i["v"] for i in itens)
    area = w - largura_rot - (330 if rot_extra else 150)
    out = [f'<svg width="{w}" height="{h}" font-family="Segoe UI" font-size="18">']
    for k, it in enumerate(itens):
        y = k * lh
        bw = it["v"] / vmax * area
        cor = LARANJA if it.get("afl") else it.get("cor", cor_padrao)
        lim = int(largura_rot / 9.6)
        nome = it["nome"] if len(it["nome"]) <= lim else it["nome"][:lim - 1] + "…"
        out.append(f'<text x="{largura_rot - 10}" y="{y + lh / 2 + 6:.1f}" text-anchor="end" fill="#1D1E21" font-weight="{600 if it.get("afl") else 400}">{e(nome)}</text>')
        out.append(f'<rect x="{largura_rot}" y="{y + lh * 0.2:.1f}" width="{bw:.1f}" height="{lh * 0.6:.1f}" rx="2" fill="{cor}"/>')
        txt = fmt(it["v"]) + (f'<tspan fill="#434446" font-weight="400"> · {rot_extra(it)}</tspan>' if rot_extra else "")
        out.append(f'<text x="{largura_rot + bw + 8:.1f}" y="{y + lh / 2 + 6:.1f}" fill="#1D1E21" font-weight="600">{txt}</text>')
    out.append("</svg>")
    return "".join(out)


def empilhadas(linhas, cats, cores, w, h, rot_min=0.04):
    """Barras 100% (uma por grupo) com % dentro dos segmentos grandes."""
    nb = len(linhas)
    lh = min(70, h / nb)
    out = [f'<svg width="{w}" height="{h}" font-family="Segoe UI" font-size="18">']
    for k, (nome, vals) in enumerate(linhas):
        y = k * (lh + 18)
        out.append(f'<text x="0" y="{y + lh / 2 + 6:.1f}" fill="#1D1E21" font-weight="600">{e(nome)}</text>')
        x = 150
        for c, cor in zip(cats, cores):
            v = vals.get(c, 0)
            bw = v * (w - 160)
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{lh:.1f}" fill="{cor}"/>')
            if v >= rot_min:
                claro = cor in ("#E0E7FF", "#A5B4FC", "#D0D5DD", "#C4C5C8", "#98A2B3")
                out.append(f'<text x="{x + bw / 2:.1f}" y="{y + lh / 2 + 6:.1f}" text-anchor="middle" fill="{TINTA if claro else "#FFFFFF"}" font-weight="600">{p(v, 0)}</text>')
            x += bw
    out.append("</svg>")
    return "".join(out)


def linhas(series, anos, w, h, fmt, vmin=None, vmax=None, quebra=True, rot_fim=True):
    """series: [(nome, cor, tracejado, [valores])]."""
    vals = [v for _, _, _, s in series for v in s if v is not None]
    lo = vmin if vmin is not None else min(vals) * 0.9
    hi = vmax if vmax is not None else max(vals) * 1.08
    x0, x1, y0, y1 = 70, w - 260, 20, h - 40
    X = lambda i: x0 + i * (x1 - x0) / (len(anos) - 1)
    Y = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)
    out = [f'<svg width="{w}" height="{h}" font-family="Segoe UI" font-size="17">']
    for i, a in enumerate(anos):
        if a % 2 == 1 or a == anos[-1]:
            out.append(f'<text x="{X(i):.1f}" y="{h - 12}" text-anchor="middle" fill="#434446">{a}</text>')
    if quebra and 2022 in anos:
        xq = (X(anos.index(2021)) + X(anos.index(2022))) / 2
        out.append(f'<line x1="{xq:.1f}" y1="{y0}" x2="{xq:.1f}" y2="{y1}" stroke="#B54708" stroke-dasharray="5 4" stroke-width="2"/>')
        out.append(f'<text x="{xq - 8:.1f}" y="{y0 + 14}" text-anchor="end" fill="#B54708">eSocial →</text>')
    out.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#C4C5C8"/>')
    fins = []
    for nome, cor, trac, s in series:
        pts = [(X(i), Y(v)) for i, v in enumerate(s) if v is not None]
        # a linha não atravessa a quebra
        seg1 = [pt for pt, a in zip(pts, anos) if a <= 2021]
        seg2 = [pt for pt, a in zip(pts, anos) if a >= 2022]
        for seg in (seg1, seg2):
            if len(seg) > 1:
                out.append(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in seg)}" fill="none" stroke="{cor}" stroke-width="3.5"'
                           + (' stroke-dasharray="9 6"' if trac else "") + "/>")
        if rot_fim:
            a, b = pts[-1]
            out.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="5" fill="{cor}"/>')
            fins.append([b, cor, f'{fmt(s[-1])} <tspan font-weight="400" fill="#434446">{e(nome)}</tspan>', a])
    fins.sort()
    for k in range(1, len(fins)):
        fins[k][0] = max(fins[k][0], fins[k - 1][0] + 22)
    for b, cor, txt, a in fins:
        out.append(f'<text x="{a + 12:.1f}" y="{b + 6:.1f}" fill="{TINTA}" font-weight="600">{txt}</text>')
    out.append("</svg>")
    return "".join(out)


def piramide(pir, ref, w, h):
    """Pirâmide etária por sexo (% do total do grupo) com o contorno do grupo de referência."""
    faixas = list(pir.keys())[::-1]
    lh = (h - 30) / len(faixas)
    meio = w / 2
    vmax = max(max(v.values()) for v in list(pir.values()) + list(ref.values())) * 1.1
    esc = (meio - 120) / vmax
    out = [f'<svg width="{w}" height="{h}" font-family="Segoe UI" font-size="18">']
    for k, fx in enumerate(faixas):
        y = k * lh
        m, hm = pir[fx]["Mulher"], pir[fx]["Homem"]
        out.append(f'<rect x="{meio - 45 - m * esc:.1f}" y="{y + 6:.1f}" width="{m * esc:.1f}" height="{lh - 12:.1f}" fill="{MULHER}"/>')
        out.append(f'<rect x="{meio + 45:.1f}" y="{y + 6:.1f}" width="{hm * esc:.1f}" height="{lh - 12:.1f}" fill="{HOMEM}"/>')
        rm, rh = ref[fx]["Mulher"], ref[fx]["Homem"]
        out.append(f'<rect x="{meio - 45 - rm * esc:.1f}" y="{y + 4:.1f}" width="{rm * esc:.1f}" height="{lh - 8:.1f}" fill="none" stroke="#1D1E21" stroke-dasharray="4 3"/>')
        out.append(f'<rect x="{meio + 45:.1f}" y="{y + 4:.1f}" width="{rh * esc:.1f}" height="{lh - 8:.1f}" fill="none" stroke="#1D1E21" stroke-dasharray="4 3"/>')
        out.append(f'<text x="{meio}" y="{y + lh / 2 + 6:.1f}" text-anchor="middle" fill="#1D1E21" font-weight="600">{fx}</text>')
        out.append(f'<text x="{meio - 52 - m * esc:.1f}" y="{y + lh / 2 + 6:.1f}" text-anchor="end" fill="#434446">{p(m)}</text>')
        out.append(f'<text x="{meio + 52 + hm * esc:.1f}" y="{y + lh / 2 + 6:.1f}" fill="#434446">{p(hm)}</text>')
    out.append("</svg>")
    return "".join(out)


def halteres(itens, w, h, fmt, rot_w=260, lo=None, hi=None, ref_linha=None):
    """Dois pontos por linha (AFL laranja × referência cinza escuro)."""
    nb = len(itens)
    lh = h / nb
    vals = [v for it in itens for v in (it["a"], it["b"]) if v is not None]
    lo = lo if lo is not None else min(vals) * 0.9
    hi = hi if hi is not None else max(vals) * 1.05
    x0, x1 = rot_w + 16, w - 205
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    out = [f'<svg width="{w}" height="{h}" font-family="Segoe UI" font-size="18">']
    if ref_linha is not None:
        out.append(f'<line x1="{X(ref_linha):.1f}" y1="0" x2="{X(ref_linha):.1f}" y2="{h}" stroke="#98A2B3" stroke-dasharray="4 4"/>')
    for k, it in enumerate(itens):
        y = k * lh + lh / 2
        out.append(f'<text x="{rot_w}" y="{y + 6:.1f}" text-anchor="end" fill="#1D1E21">{e(it["nome"])}</text>')
        if it["a"] is not None and it["b"] is not None:
            out.append(f'<line x1="{X(it["a"]):.1f}" y1="{y:.1f}" x2="{X(it["b"]):.1f}" y2="{y:.1f}" stroke="#DDDDDE" stroke-width="6"/>')
        if it["b"] is not None:
            out.append(f'<circle cx="{X(it["b"]):.1f}" cy="{y:.1f}" r="9" fill="#434446"/>')
        if it["a"] is not None:
            out.append(f'<circle cx="{X(it["a"]):.1f}" cy="{y:.1f}" r="9" fill="{LARANJA}"/>')
            out.append(f'<text x="{w - 4}" y="{y + 6:.1f}" text-anchor="end" fill="#1D1E21" font-weight="600">{fmt(it["a"])} '
                       f'<tspan fill="#434446" font-weight="400">× {fmt(it["b"])}</tspan></text>')
    out.append("</svg>")
    return "".join(out)


LEG_AFL_REF = f'<span><i style="background:{LARANJA}"></i>AFL</span><span><i style="background:#434446"></i>Comparáveis (referência)</span>'
NOTA_QUEBRA = "A partir de 2022 a RAIS vem do eSocial e passou a incluir empregos de empresas pequenas que antes ficavam de fora: 2022 em diante não se compara com os anos anteriores."
CTX = f"31/12/{ANO} · Brasil · RAIS ({'eSocial'})"
X1, X2, X3 = 40, 658.7, 1277.3
NOME_CURTO = {"5611201": "Restaurantes e similares", "5611203": "Lanchonetes, casas de chá, de sucos e similares",
              "4721102": "Padaria e confeitaria (revenda)", "5620104": "Alimentos preparados p/ consumo domiciliar",
              "5611204": "Bares sem entretenimento", "5611205": "Bares com entretenimento"}


# ------------------------------------------------------------------ páginas
def empregos_afl():
    E = I["emp"]
    serie = I["serie"]["AFL"]
    filtros = [("Ano", f"{ANO}", 140), ("CNAE AFL", "Todas", 276.8), ("Localização", "Todos", 250), ("Sexo", "Todos", 220),
               ("Escolaridade", "Todas", 250), ("Raça/cor", "Todas", 220)]
    s = [topo("Empregos", "AFL", filtros)]
    s.append(manchete(f"O AFL fechou {ANO} com {n(E['afl'])} empregos formais: a {E['seq_altas_afl']}ª alta seguida",
                      f"{CTX} · AFL (6 CNAEs)"))
    s.append(kpi(X1, "#17B26A", f"Empregos em 31/12/{ANO}", n(E["afl"]),
                 [f'<span style="color:#137547">▲ +{n(E["abs_afl"])} ({p(E["var_afl"], 1, True)}) sobre {ANO - 1}</span>',
                  chip_ref(p(E["var_comp"], 1, True))]))
    s.append(kpi(X2, LARANJA, "Peso nos empregos comparáveis", p(E["part_comp"]),
                 [f"dos empregos do AFL + comparáveis", f'{p(E["part_todos"])} de todo o emprego formal']))
    s.append(kpi(X3, TINTA, "Crescimento médio ao ano desde 2022", p(E["cagr_afl"], 1, True),
                 [f"{E['seq_altas_afl']} altas seguidas", chip_ref(p(E["cagr_comp"], 1, True))]))
    destaque = {2020: "#B42318"}
    s.append(card(X1, 540, 1220.3, 456, f"Em 2020 o AFL perdeu {p(-E['queda_2020'])} dos empregos; os comparáveis, {p(-E['comp_queda_2020'])}",
                  f"Recuperou o nível de 2019 só em 2022, já com a fonte nova. Rótulo = variação sobre o ano anterior.",
                  colunas_ano(serie, 1172, 300, destaque=destaque)))
    C = I["contratos"]
    cats = ["CLT por prazo indeterminado", "Prazo determinado ou temporário", "Intermitente", "Parcial", "Aprendiz"]
    cores = [TINTA, "#667085", LARANJA, "#98A2B3", "#D0D5DD"]
    leg = "".join(f'<span><i style="background:{c}"></i>{k.split(" por")[0]}</span>' for k, c in zip(cats, cores))
    s.append(card(X3, 540, 602.7, 456, f"{p(C['AFL']['CLT por prazo indeterminado'], 0)} são CLT por prazo indeterminado",
                  f"Prazo determinado: {p(C['AFL']['Prazo determinado ou temporário'])} (comparáveis {p(C['Comparável']['Prazo determinado ou temporário'])})",
                  tabela_contratos(C)))
    at = I["atividades"]
    tot = sum(a["v"] for a in at)
    itens = [{"nome": NOME_CURTO.get(a["cnae"], a["nome"]), "v": a["v"], "var": a["var"], "cor": TINTA} for a in at]
    s.append(card(X1, 1020, 1220.3, 520, f"Restaurantes e similares concentram {p(at[0]['v'] / tot, 0)} dos empregos do AFL",
                  f"Quem mais cresceu em {ANO}: {NOME_CURTO[at[max(range(len(at)), key=lambda k: at[k]['var'])]['cnae']]} ({p(max(a['var'] for a in at), 1, True)})",
                  barras_h(itens, 1172, 350, rot_extra=lambda it: p(it["var"], 1, True) + f" sobre {ANO - 1}", largura_rot=560)))
    uf = I["ufs"][:10]
    top_part = max(I["ufs"], key=lambda u: u["part_comp"])
    s.append(card(X3, 1020, 602.7, 520, f"SP tem {p(uf[0]['afl'] / E['afl'], 0)} dos empregos do AFL",
                  f"Onde o AFL pesa mais: {top_part['uf']} ({p(top_part['part_comp'])} dos empregos comparáveis)",
                  barras_h([{"nome": u["uf"], "v": u["afl"], "cor": TINTA} for u in uf], 554, 340, largura_rot=60,
                           rot_extra=lambda it: p(next(x["part_comp"] for x in I["ufs"] if x["uf"] == it["nome"]))[:-1] + "% comp.")))
    s.append(nota(1572, NOTA_QUEBRA))
    return pagina("empregos-afl", "".join(s))


def empregos_todos():
    E = I["emp"]
    serie = I["serie"]["Todos"]
    filtros = [("Ano", f"{ANO}", 140), ("Setores ⓘ", "☐ Só os comparáveis ao AFL", 360), ("Localização", "Todos", 250), ("Sexo", "Todos", 220),
               ("Escolaridade", "Todas", 250), ("Raça/cor", "Todas", 200)]
    s = [topo("Empregos", "Todos os setores", filtros)]
    s.append(manchete(f"O Brasil fechou {ANO} com {n(E['todos'])} empregos formais; o AFL é a {I['pos_afl']}ª maior divisão",
                      f"{CTX} · todos os setores"))
    s.append(kpi(X1, "#17B26A", f"Empregos em 31/12/{ANO}", n(E["todos"]),
                 [f'<span style="color:#137547">▲ +{n(E["abs_todos"])} ({p(E["var_todos"], 1, True)}) sobre {ANO - 1}</span>',
                  chip_afl(p(E["var_afl"], 1, True)) + " " + chip_ref(p(E["var_comp"], 1, True))]))
    s.append(kpi(X2, LARANJA, "Peso do AFL", p(E["part_todos"]),
                 [f"de todo o emprego formal", f'<span class="chip ref">{p(E["part_comp"])} do AFL + comparáveis <small>· ref.</small></span>']))
    s.append(kpi(X3, TINTA, "Crescimento médio ao ano desde 2022", p(E["cagr_todos"], 1, True),
                 [chip_afl(p(E["cagr_afl"], 1, True)), chip_ref(p(E["cagr_comp"], 1, True))]))
    s.append(card(X1, 540, 1220.3, 456, f"De 2022 a {ANO}, o emprego formal cresceu em todos os anos",
                  f"Em 2022 a RAIS passou a vir do eSocial: o salto de {p(E['salto_2022_todos'], 1, True)} mistura emprego novo e cobertura nova",
                  colunas_ano(serie, 1172, 300)))
    C = I["contratos"]
    cats = ["CLT por prazo indeterminado", "Prazo determinado ou temporário", "Intermitente", "Parcial", "Aprendiz"]
    leg = "".join(f'<span><i style="background:{c}"></i>{k.split(" por")[0]}</span>' for k, c in zip(cats, [TINTA, "#667085", "#B86218", "#98A2B3", "#D0D5DD"]))
    s.append(card(X3, 540, 602.7, 456, f"Intermitente: {p(C['AFL']['Intermitente'])} no AFL e {p(C['Comparável']['Intermitente'])} nos comparáveis",
                  "Comparação de referência: AFL × setores comparáveis",
                  tabela_contratos(C)))
    rk = I["ranking"][:10]
    if not any(x.get("afl") for x in rk):
        rk = rk[:9] + [next(x for x in I["ranking"] if x.get("afl"))]
    botoes = "".join(f'<div style="flex:1;border-right:1px solid #DDDDDE;text-align:center;font-size:20px;padding:8px 0">{b}</div>'
                     for b in ["Agropecuária", "Comércio", "Construção", "Indústria", "Serviços"])
    s.append(card(X1, 1020, 1220.3, 520, f"O AFL é a {I['pos_afl']}ª maior divisão do emprego formal entre {I['n_div']}",
                  f"Em crescimento médio desde 2022 é a {I['pos_afl_cresc']}ª de {I['n_div_cresc']} (divisões com 100 mil empregos ou mais)",
                  f'<div style="display:flex;border:1px solid #DDDDDE;border-radius:4px;margin-bottom:10px">{botoes}</div>'
                  + barras_h([{"nome": x["nome"], "v": x["v"], "afl": x.get("afl")} for x in rk], 1172, 300, largura_rot=480)))
    uf = I["ufs"][:10]
    s.append(card(X3, 1020, 602.7, 520, f"No RJ, o AFL é {p(next(u['part_comp'] for u in I['ufs'] if u['uf'] == 'RJ'))} do emprego comparável",
                  "Peso do AFL nos empregos comparáveis, nas 10 UFs com mais empregos do AFL",
                  barras_h([{"nome": u["uf"], "v": u["part_comp"], "cor": LARANJA if False else "#667085"} for u in uf], 554, 340, fmt=lambda v: p(v), largura_rot=60)))
    s.append(nota(1572, NOTA_QUEBRA))
    return pagina("empregos-todos", "".join(s))


def perfil_afl():
    P, Pc = I["perfil"]["AFL"], I["perfil"]["Comparável"]
    filtros = [("Ano", f"{ANO}", 140), ("CNAE AFL", "Todas", 276.8), ("Localização", "Todos", 250), ("Sexo", "Todos", 220),
               ("Escolaridade", "Todas", 250), ("Raça/cor", "Todas", 220)]
    s = [topo("Quem trabalha", "AFL", filtros)]
    s.append(manchete(f"No AFL, {p(P['mulheres'])} dos empregados são mulheres e quase 1 em cada 4 tem até 24 anos",
                      f"{CTX} · AFL (6 CNAEs)", "Passe o mouse na manchete para ver o perfil completo e a comparação com os setores comparáveis"))
    s.append(kpi(X1, MULHER, "Mulheres", p(P["mulheres"]), [chip_ref(p(Pc["mulheres"]))]))
    s.append(kpi(X2, HOMEM, "Até 24 anos", p(P["ate24"]),
                 [chip_ref(p(Pc["ate24"])), f"idade média {P['idade']:.1f} anos (era {P['idade_2009']:.1f} em 2009)".replace(".", ",")]))
    s.append(kpi(X3, TINTA, "Ensino médio completo ou mais", p(P["medio_mais"]),
                 [chip_ref(p(Pc["medio_mais"])), f"superior: {p(P['escolaridade']['Superior (completo ou não)'])} (comp. {p(Pc['escolaridade']['Superior (completo ou não)'])})"]))
    pir, ref = P["piramide"], Pc["piramide"]
    mais_fem = [fx for fx in pir if pir[fx]["Mulher"] > pir[fx]["Homem"]]
    leg = (f'<span><i style="background:{MULHER}"></i>Mulheres</span><span><i style="background:{HOMEM}"></i>Homens</span>'
           f'<span><i style="background:#fff;border:1px dashed #1D1E21"></i>Comparáveis (referência)</span>')
    s.append(card(X1, 540, 1220.3, 456, f"Mulheres são maioria em {len(mais_fem)} das 7 faixas de idade",
                  "Distribuição por idade e sexo (% do total de empregos do AFL); contorno = setores comparáveis", piramide(pir, ref, 1172, 270), leg))
    cats = list(P["escolaridade"].keys())
    leg = "".join(f'<span><i style="background:{c}"></i>{k}</span>' for k, c in zip(cats, SEQ))
    s.append(card(X3, 540, 602.7, 456, f"{p(P['escolaridade']['Médio completo'], 0)} têm o ensino médio completo",
                  f"Superior: {p(P['escolaridade']['Superior (completo ou não)'], 0)} no AFL × {p(Pc['escolaridade']['Superior (completo ou não)'], 0)} nos comparáveis",
                  empilhadas([("AFL", P["escolaridade"]), ("Comparáveis", Pc["escolaridade"])], cats, SEQ, 554, 200)
                  + f'<div class="leg" style="flex-wrap:wrap;gap:6px 18px;margin-top:20px">{leg}</div>'))
    cb = I["cbo"][:8]
    s.append(card(X1, 1020, 1220.3, 520, f"{cb[0]['nome']} é a ocupação mais comum: {n(cb[0]['v'])} empregos, {p(cb[0]['mulheres'], 0)} mulheres",
                  "Ocupações (CBO) com mais empregos no AFL · % de mulheres e remuneração média de dezembro",
                  barras_h([{"nome": c["nome"].replace(" (Desativado em 2010)", ""), "v": c["v"], "cor": TINTA, "m": c["mulheres"], "r": c["media"]} for c in cb], 1172, 350,
                           rot_extra=lambda it: f"{p(it['m'], 0)} mulheres · {r(it['r'])}", largura_rot=430)))
    rc, rcc = P["raca"], Pc["raca"]
    prim = I["primeiro"]["AFL"][-1]["pct"]
    prim_c = I["primeiro"]["Comparável"][-1]["pct"]
    it = I["interm"]["AFL"][-1]
    it_c = I["interm"]["Comparável"][-1]
    cats = ["Branca", "Negra", "Amarela", "Indígena"]
    cores = ["#D0D5DD", "#475467", "#98A2B3", "#1D1E21"]
    corpo = (empilhadas([("AFL", rc), ("Comparáveis", rcc)], cats, cores, 554, 160)
             + '<div class="leg" style="margin-top:10px">' + "".join(f'<span><i style="background:{c}"></i>{k}{" (preta + parda)" if k == "Negra" else ""}</span>' for k, c in zip(cats[:2], cores[:2])) + "</div>"
             + f'<div style="margin-top:22px;border-top:1px solid #E8E8E9;padding-top:14px;font-size:21px;line-height:30px">'
               f'<b>Primeiro emprego</b> (só até 2021): {p(prim)} dos empregos do AFL × {p(prim_c)}<br>'
               f'<b>Intermitente</b> ({ANO}): {n(it["v"])} empregos, {p(it["pct"])} × {p(it_c["pct"])}</div>')
    s.append(card(X3, 1020, 602.7, 520, f"{p(rc['Negra'], 0)} dos empregados do AFL são negros",
                  f"Sobre quem declarou cor ({p(P['raca_cobertura'], 0)} dos vínculos) · comparáveis: {p(rcc['Negra'], 0)}", corpo))
    s.append(nota(1572, NOTA_QUEBRA + " Primeiro emprego só existe até 2021."))
    return pagina("perfil-afl", "".join(s))


def salario_afl():
    R, Rc = I["remun"]["AFL"], I["remun"]["Comparável"]
    filtros = [("Ano", f"{ANO}", 140), ("CNAE AFL", "Todas", 276.8), ("Localização", "Todos", 250), ("Sexo", "Todos", 220),
               ("Escolaridade", "Todas", 250), ("Raça/cor", "Todas", 220)]
    s = [topo("Quanto ganha", "AFL", filtros)]
    s.append(manchete(f"Metade do AFL ganhava até {r(R['mediana'])} em dez/{ANO}: {p(R['mediana'] / Rc['mediana'], 0)} da mediana dos comparáveis",
                      f"dez/{ANO} · Brasil · AFL (6 CNAEs) · RAIS (eSocial) · valores nominais"))
    s.append(kpi(X1, "#17B26A", "Remuneração mediana de dezembro", r(R["mediana"]),
                 [chip_ref(r(Rc["mediana"])), f"média {r(R['media'])} · " + f"{I['sal_serie']['AFL'][-1]['sm']:.2f}".replace(".", ",") + " salário mínimo"]))
    s.append(kpi(X2, MULHER, "Mulheres ganham, em média,", p(R["razao_sexo"], 0) + '<span style="font-size:26px;font-weight:400"> do que ganham os homens</span>',
                 [chip_ref(p(Rc["razao_sexo"], 0))]))
    s.append(kpi(X3, TINTA, "Negros ganham, em média,", p(R["razao_raca"], 0) + '<span style="font-size:26px;font-weight:400"> do que ganham os brancos</span>',
                 [chip_ref(p(Rc["razao_raca"], 0))]))
    ss = I["sal_serie"]
    anos = I["anos"]
    rz = I["remun"]["razao_afl_comp_media"]
    s.append(card(X1, 540, 1220.3, 456, f"A média do AFL subiu de {p(rz[0]['r'], 0)} para {p(rz[-1]['r'], 0)} da média dos comparáveis desde {anos[0]}",
                  "Remuneração de dezembro, média e mediana, em R$ nominais (a linha não atravessa a quebra de 2022)",
                  linhas([("AFL média", LARANJA, False, [x["media"] for x in ss["AFL"]]), ("AFL mediana", LARANJA, True, [x["mediana"] for x in ss["AFL"]]),
                          ("comp. média", "#434446", False, [x["media"] for x in ss["Comparável"]]), ("comp. mediana", "#434446", True, [x["mediana"] for x in ss["Comparável"]])],
                         anos, 1172, 270, lambda v: r(v), vmin=0), LEG_AFL_REF + '<span>— média · - - mediana</span>'))
    ESC = ["Fundamental Incompleto", "Fundamental Completo", "Médio Incompleto", "Médio Completo", "Superior Incompleto", "Superior Completo"]
    sup = R["por_esc"]["Superior Completo"] / Rc["por_esc"]["Superior Completo"]
    s.append(card(X3, 540, 602.7, 456, f"Com superior completo, o AFL paga {p(sup, 0)} da média comparável",
                  "Remuneração média por escolaridade (R$ nominais)",
                  halteres([{"nome": x.replace("Fundamental", "Fund.").replace("Incompleto", "incompl.").replace("Completo", "compl."),
                             "a": R["por_esc"][x], "b": Rc["por_esc"][x]} for x in ESC], 554, 250, lambda v: r(v), rot_w=150, lo=1500, hi=8500), LEG_AFL_REF))
    gaps = [{"nome": x.replace("Fundamental", "Fund.").replace("Incompleto", "incompl.").replace("Completo", "compl."),
             "a": R["razao_sexo_esc"][x], "b": Rc["razao_sexo_esc"][x]} for x in ESC]
    gaps_r = [{"nome": g["nome"], "a": R["razao_raca_esc"][x], "b": Rc["razao_raca_esc"][x]} for g, x in zip(gaps, ESC)]
    lo_g = min(min(g["a"], g["b"]) for g in gaps)
    hi_g = max(max(g["a"], g["b"]) for g in gaps)
    corpo = ('<div style="display:flex;gap:30px">'
             f'<div><div style="font-size:21px;font-weight:600;margin-bottom:6px">Mulheres ÷ homens</div>{halteres(gaps, 560, 300, lambda v: p(v, 0), rot_w=150, lo=0.6, hi=1.0, ref_linha=1.0)}</div>'
             f'<div><div style="font-size:21px;font-weight:600;margin-bottom:6px">Negros ÷ brancos</div>{halteres(gaps_r, 560, 300, lambda v: p(v, 0), rot_w=150, lo=0.6, hi=1.0, ref_linha=1.0)}</div></div>')
    s.append(card(X1, 1020, 1220.3, 520, f"Na mesma escolaridade, a diferença por sexo e cor é menor no AFL que nos comparáveis",
                  f"Mulheres ganham {p(min(g['a'] for g in gaps), 0)} a {p(max(g['a'] for g in gaps), 0)} do salário dos homens no AFL e {p(min(g['b'] for g in gaps), 0)} a {p(max(g['b'] for g in gaps), 0)} nos comparáveis (100% = mesmo salário)", corpo, LEG_AFL_REF))
    ufs = sorted([u for u in I["ufs"] if u["media_afl"]], key=lambda u: -u["media_afl"])[:10]
    pior = min(I["ufs"], key=lambda u: u["razao"] or 9)
    s.append(card(X3, 1020, 602.7, 520, f"{ufs[0]['uf']} paga a maior média do AFL: {r(ufs[0]['media_afl'])}",
                  f"Maior distância para os comparáveis: {pior['uf']} ({p(pior['razao'], 0)} da média comparável)",
                  barras_h([{"nome": u["uf"], "v": u["media_afl"], "cor": TINTA, "rz": u["razao"]} for u in ufs], 554, 340, fmt=lambda v: r(v), largura_rot=60,
                           rot_extra=lambda it: p(it["rz"], 0) + " do comp.")))
    s.append(nota(1572, "Valores nominais, remuneração de dezembro. " + NOTA_QUEBRA))
    return pagina("salario-afl", "".join(s))


def main():
    for f in (empregos_afl, empregos_todos, perfil_afl, salario_afl):
        print(f())


if __name__ == "__main__":
    main()
