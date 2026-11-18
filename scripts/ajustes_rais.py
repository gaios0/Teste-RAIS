"""Ajustes pedidos em 17/11/2026 (Empregos e Quanto ganha). Idempotente; mexe só no que está listado:

Empregos
  1. KPI de peso (AFL): título "Representatividade de empregos do setor AFL em setores comparáveis" (em 2 linhas).
  2. Manchete da variação (AFL): "a quantidade de empregos subiu/caiu x%".
  3. Gráfico de estados (AFL): valor passa de empregos brutos para % do total analisado (medida nova Emp_UF_Pct_AFL); o tooltip fica igual.
  4. Tooltip dos CNAEs (AFL): a variável "Var" é palavra reservada do DAX e derrubava o tooltip ("Something's wrong with one or more fields").
Quanto ganha
  5. Manchete AFL: "os trabalhadores do AFL ganhavam, em média, R$ X ... % da média dos Comparáveis" (sem mediana).
  6. Tooltip da série de média no AFL: mostra AFL × Comparáveis (antes mostrava a "Seleção atual", que no AFL é igual ao AFL).
  7. Gráfico de salário médio por escolaridade (AFL): 2ª série passa de "Seleção atual" para "Comparáveis".
  8. Legenda do fundo desse card: ganha o item "Comparáveis".
"""
import datetime
import json
import re
import sys
import uuid
from pathlib import Path

import numpy as np
from PIL import Image

import fundo_rais as fb
import nav_ranking as nav
import pbir_rais as pb

RAIZ = Path(__file__).resolve().parents[1]
TMDL = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl"
C12, C32 = "a3d1f2c4e6b8097a1c12", "a3d1f2c4e6b8097a1c32"
CINZA_COMP = "#434446"
AFL_ESCURO = "#D97706"


# ------------------------------------------------------------------ medidas
def bloco(t, nome):
    ini = t.index(f"\tmeasure {nome} =")
    fim = ini + 1
    linhas = t[ini:].split("\n")
    n = 1
    while n < len(linhas) and (linhas[n].startswith("\t\t") or linhas[n] == ""):
        n += 1
    return ini, ini + len("\n".join(linhas[:n]))


def trocar(t, nome, antes, depois, unico=True):
    ini, fim = bloco(t, nome)
    corpo = t[ini:fim]
    if depois in corpo and antes not in corpo:
        print(f"  {nome}: já ajustado")
        return t
    assert (corpo.count(antes) == 1) if unico else (antes in corpo), f"{nome}: trecho não encontrado: {antes[:80]}"
    print(f"  {nome}: ok")
    return t[:ini] + corpo.replace(antes, depois) + t[fim:]


def medidas():
    bruto = TMDL.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in bruto else "\n"
    t = bruto.replace("\r\n", "\n")
    # 1. título do KPI de peso (AFL): duas linhas, fonte um pouco menor para caber no card de 172 px
    t = trocar(t, "KPI_Peso_AFL_HTML",
               "<div style='font-size:24px;line-height:28px;font-weight:600;color:#434446;white-space:nowrap;'>\" & \"Presença nos empregos comparáveis\" & \"</div>\"",
               "<div style='font-size:20px;line-height:24px;font-weight:600;color:#434446;max-height:48px;overflow:hidden;'>\" & \"Representatividade de empregos do setor AFL em setores comparáveis\" & \"</div>\"")
    # 1b. remove a linha "dos empregos do AFL + comparáveis" (redundante com o título)
    t = trocar(t, "KPI_Peso_AFL_HTML",
               "& \"<div style='margin-top:3px;font-size:22px;line-height:26px;white-space:nowrap;text-overflow:ellipsis;color:\" & \"#434446\" & \";overflow:hidden;'>\" & \"dos empregos do AFL + comparáveis\" & \"</div>\" & ",
               "& ")
    # 2. manchete da variação de emprego (AFL)
    t = trocar(t, "Titulo_Emp_Var_AFL_HTML", '", o emprego do AFL "', '", a quantidade de empregos "')
    # 4. tooltip dos CNAEs: "Var" é palavra reservada
    ini, fim = bloco(t, "Tip_Emp_Atividade_HTML")
    corpo = t[ini:fim]
    novo = re.sub(r"(?<![A-Za-z0-9_\[])Var(?![A-Za-z0-9_\]])", "VarAno", corpo)
    print("  Tip_Emp_Atividade_HTML:", "ok" if novo != corpo else "já ajustado", f"({len(re.findall(r'(?<![A-Za-z0-9_\[])Var(?![A-Za-z0-9_\]])', corpo))} usos de 'Var')")
    t = t[:ini] + novo + t[fim:]
    # 4b. peso do CNAE no tooltip: o total dos 6 CNAEs precisa ignorar o CNAE sobrevoado (REMOVEFILTERS(D_Cnae) não limpa o filtro de D_AflAtividade)
    t = trocar(t, "Tip_Emp_Atividade_HTML", "VAR Tot = [Empregos_Ref_AFL]", "VAR Tot = CALCULATE([Empregos_Ref_AFL], REMOVEFILTERS(D_AflAtividade))")
    # 5. manchete de Quanto ganha (AFL)
    t = trocar(t, "Manchete_Salario_AFL_HTML",
               'VAR Texto = Prep & ", metade do AFL ganhava até R$ " & FORMAT(MedAFL, "#,0", "pt-BR") & " em dez/" & A & ": " & FORMAT(DIVIDE(MedAFL, MedComp), "0%", "pt-BR") & " da mediana dos Comparáveis"',
               'VAR MediaAFL = [Remuneracao_Media_Ref_AFL]\n\t\t\tVAR MediaComp = [Remuneracao_Media_Ref_Comparavel]\n'
               '\t\t\tVAR Texto = IF(ISBLANK(MediaAFL), Prep & ", sem dados de remuneração do AFL para os filtros escolhidos", '
               'Prep & ", os trabalhadores do AFL ganhavam, em média, R$ " & FORMAT(MediaAFL, "#,0", "pt-BR") & " em dez/" & A & '
               'IF(ISBLANK(MediaComp), "", ": " & FORMAT(DIVIDE(MediaAFL, MediaComp), "0%", "pt-BR") & " da média dos Comparáveis"))')
    # 6. tooltip da série de média: no AFL usa o tooltip completo (AFL × Comparáveis)
    ini, fim = bloco(t, "Tip_Rem_Ano_Total_HTML")
    corpo = t[ini:fim]
    if "[Tip_Rem_Ano_HTML]" in corpo:
        print("  Tip_Rem_Ano_Total_HTML: já ajustado")
    else:
        a = "RETURN\n\t\t\t\t\"<div role='group'"
        assert corpo.count(a) == 1
        corpo = corpo.replace(a, "RETURN\n\t\t\t\tIF(SELECTEDVALUE(D_Cnae[setor_afl]) = \"Sim\", [Tip_Rem_Ano_HTML],\n\t\t\t\t\"<div role='group'")
        b = "\t\t\t\t& \"</div>\"\n\t\tdisplayFolder"
        assert corpo.count(b) == 1
        corpo = corpo.replace(b, "\t\t\t\t& \"</div>\")\n\t\tdisplayFolder")
        t = t[:ini] + corpo + t[fim:]
        print("  Tip_Rem_Ano_Total_HTML: ok")
    # 3. medida nova: % do total analisado por estado (e por município, dentro do estado)
    if "\tmeasure Emp_UF_Pct_AFL =" in t:
        ini, fim = bloco(t, "Emp_UF_Pct_AFL")
        tag = re.search(r"lineageTag: ([0-9a-f-]+)", t[ini:fim]).group(1)
        # remove doc anterior + bloco para reescrever
        antes = t[:ini].rstrip("\n").split("\n")
        while antes and antes[-1].startswith("\t///"):
            antes.pop()
        t = "\n".join(antes) + "\n" + t[fim:].lstrip("\n")
    else:
        tag = str(uuid.uuid4())
    nova = ("\t/// Participação do estado (ou do município, dentro do estado) no total de empregos do AFL em 31/12 do ano de referência. "
            "Total = todos os estados do filtro atual (ALLSELECTED); no nível município, o total do estado.\n"
            "\tmeasure Emp_UF_Pct_AFL =\n"
            "\t\t\tVAR V = [Empregos_Ref]\n"
            "\t\t\tVAR D = IF(ISINSCOPE(F_rais[municipio]), CALCULATE([Empregos_Ref], REMOVEFILTERS(F_rais[municipio])), CALCULATE([Empregos_Ref], ALLSELECTED(D_UF)))\n"
            "\t\t\tRETURN IF(NOT ISBLANK(V), DIVIDE(V, D))\n"
            "\t\tformatString: 0.0%\n"
            "\t\tdisplayFolder: Empregos\\UF\n"
            f"\t\tlineageTag: {tag}\n\n")
    ponto = t.index("\tcolumn Coluna\n")
    t = t[:ponto] + nova + t[ponto:]
    print("  Emp_UF_Pct_AFL: gravada")
    TMDL.write_bytes(t.replace("\n", eol).encode("utf-8"))


# ------------------------------------------------------------------ visuais
def arq_visual(pagina, prefixo):
    pasta = next(d for d in (pb.DEF / "pages" / pagina / "visuals").iterdir() if d.name.startswith(prefixo))
    return pasta / "visual.json"


def achar_uf_c12():
    for f in (pb.DEF / "pages" / C12 / "visuals").glob("*/visual.json"):
        v = json.loads(f.read_text(encoding="utf-8"))
        q = v["visual"].get("query", {}).get("queryState", {})
        if any("D_UF" in p["queryRef"] for p in q.get("Category", {}).get("projections", [])) and v["visual"]["visualType"] == "clusteredBarChart":
            return f
    raise SystemExit("gráfico de UF da página AFL não encontrado")


def visuais():
    f = achar_uf_c12()
    t = f.read_text(encoding="utf-8")
    if "Emp_UF_Pct_AFL" not in t:
        v = json.loads(t)
        y = v["visual"]["query"]["queryState"]["Y"]["projections"][0]
        y["field"]["Measure"]["Property"] = "Emp_UF_Pct_AFL"
        y.update({"queryRef": "_medidas.Emp_UF_Pct_AFL", "nativeQueryRef": "Participação no total de empregos do AFL",
                  "displayName": "Participação no total de empregos do AFL", "format": "0.0%"})
        v["visual"]["query"]["sortDefinition"]["sort"][0]["field"]["Measure"]["Property"] = "Emp_UF_Pct_AFL"
        pb.salvar(f, v)
        print("  c12 gráfico de UF:", f.parent.name[:6], "-> % do total")
    else:
        print("  c12 gráfico de UF: já ajustado")
    f = arq_visual(C32, "012e26")
    t = f.read_text(encoding="utf-8")
    if "Rem_Esc_Sel" in t:
        t = t.replace("Rem_Esc_Sel", "Rem_Esc_Comp").replace('"Seleção atual"', '"Comparáveis"').replace("'#98A2B3'", f"'{CINZA_COMP}'").replace('"#98A2B3"', f'"{CINZA_COMP}"')
        f.write_text(t, encoding="utf-8")
        json.loads(t)
        print("  c32 salário por escolaridade: 2ª série = Comparáveis")
    else:
        print("  c32 salário por escolaridade: já ajustado")


# ------------------------------------------------------------------ legenda do fundo
def legenda():
    atual = nav.fundo_atual(C32)
    img = Image.open(nav.RECURSOS / atual).convert("RGB")
    a = np.asarray(img).astype(int)
    # item AFL existente: quadrado laranja do card de escolaridade (região do card à direita)
    reg = a[1300:1420, 2560:2800]
    cor = np.array([int(AFL_ESCURO[i:i + 2], 16) for i in (1, 3, 5)])
    ys, xs = np.where((np.abs(reg - cor).sum(axis=2) < 30))
    x0, y0 = (xs.min() + 2560) / 2, (ys.min() + 1300) / 2
    print(f"  quadrado AFL em x={x0}, y={y0} (página)")
    # teste de idempotência: já existe um quadrado cinza à direita do AFL?
    cinza = np.array([int(CINZA_COMP[i:i + 2], 16) for i in (1, 3, 5)])
    teste = a[int(y0 * 2):int(y0 * 2) + 28, 2760:3200]
    if (np.abs(teste - cinza).sum(axis=2) < 30).sum() > 200:
        print("  legenda: já tem Comparáveis")
        return
    altura = img.height // 2
    plano = fb.legenda(x0, y0, [("AFL", AFL_ESCURO, "quadro"), ("Comparáveis", CINZA_COMP, "quadro")])
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fb.W} {altura}" width="{fb.W}" height="{altura}">'
           f'<rect width="{fb.W}" height="{altura}" fill="#FFFFFF"/>' + "".join(plano) + "</svg>")
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        s, p = Path(d) / "l.svg", Path(d) / "l.png"
        s.write_text(svg, encoding="utf-8")
        subprocess.run([fb.EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2", f"--screenshot={p}",
                        f"--window-size={fb.W},{altura}", s.as_uri()], capture_output=True, check=True)
        leg = np.asarray(Image.open(p).convert("RGB")).astype(int)
    faixa = (slice(int(y0 * 2) - 6, int(y0 * 2) + 40), slice(int(x0 * 2) - 6, int(x0 * 2) + 700))
    saida = a.copy()
    saida[faixa] = np.minimum(a[faixa], leg[faixa])          # escuro sobre branco: o item novo entra por cima, o AFL existente fica igual
    novo = re.sub(r"\d+\.png$", datetime.datetime.now().strftime("%Y%m%d%H%M") + ".png", atual)
    Image.fromarray(saida.astype(np.uint8)).save(nav.RECURSOS / novo, optimize=True)
    pj = pb.DEF / "pages" / C32 / "page.json"
    pj.write_text(pj.read_text(encoding="utf-8").replace(atual, novo), encoding="utf-8")
    nav.registrar(novo)
    print("  legenda:", atual, "->", novo)


if __name__ == "__main__":
    print("medidas"); medidas()
    print("visuais"); visuais()
    print("legenda do fundo"); legenda()
