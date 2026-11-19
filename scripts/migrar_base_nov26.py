"""Adapta o painel à base Painel_RAIS reestruturada (18/11/2026).

Mudanças da base: saíram D_Ano, D_UF, F_Mediana, F_rais[estado], F_rais[municipio], D_Cnae[nm_divisao] e D_Cnae[nm_secao];
entraram D_regiao (cod_municipio, municipio, uf = nome do estado, sigla_uf), F_rais[id_municipio] e D_Cnae[divisao_afl].

Troca no _medidas.tmdl e nos visual.json:
- REMOVEFILTERS(D_Ano) -> REMOVEFILTERS(F_rais[ano]); D_Ano[ano] -> F_rais[ano]
- D_UF[uf] -> D_regiao[sigla_uf]; D_UF[estado] -> D_regiao[uf]; tabela D_UF -> D_regiao
- F_rais[municipio] -> D_regiao[municipio]
- D_Cnae[nm_divisao] -> D_Cnae[divisao_afl]; D_Cnae[nm_secao] sai do teste da mediana
- Remuneracao_Mediana_Ref -> BLANK() (a base não tem mais a F_Mediana)
- VAR Min -> VAR MinEmp (Min é nome de função no DAX)

Uso: python scripts/migrar_base_nov26.py [--testar]   (--testar só mostra quantas trocas faria)
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MEDIDAS = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl"
PAGINAS = RAIZ / "RAIS Emprego Formal.Report" / "definition" / "pages"

TROCAS_DAX = [
    (r"REMOVEFILTERS\(\s*'?D_Ano'?\s*\)", "REMOVEFILTERS(F_rais[ano])"),
    (r"'?D_Ano'?\[ano\]", "F_rais[ano]"),
    (r"'?D_UF'?\[uf\]", "D_regiao[sigla_uf]"),
    (r"'?D_UF'?\[estado\]", "D_regiao[uf]"),
    (r"\(\s*'?D_UF'?\s*\)", "(D_regiao)"),
    (r"'?F_rais'?\[municipio\]", "D_regiao[municipio]"),
    (r"\n[ \t]*\|\| ISFILTERED\(D_Cnae\[nm_secao\]\)", ""),
    (r"'?D_Cnae'?\[nm_divisao\]", "D_Cnae[divisao_afl]"),
    (r"\bVAR Min = ", "VAR MinEmp = "),
    (r"Den >= Min,", "Den >= MinEmp,"),
]

# (entidade, coluna) antiga -> nova
TROCAS_CAMPO = {
    ("D_UF", "uf"): ("D_regiao", "sigla_uf"),
    ("D_UF", "estado"): ("D_regiao", "uf"),
    ("F_rais", "municipio"): ("D_regiao", "municipio"),
    ("D_Cnae", "nm_divisao"): ("D_Cnae", "divisao_afl"),
}

MEDIANA = re.compile(r"(\tmeasure Remuneracao_Mediana_Ref =\n)(.*?)(\n\t\tformatString:)", re.S)


def medidas(testar):
    t = MEDIDAS.read_text(encoding="utf-8")
    novo, n_med = MEDIANA.subn(lambda m: m.group(1) + "\t\t\tBLANK()" + m.group(3), t)
    total = {"mediana": n_med}
    for pad, rep in TROCAS_DAX:
        novo, n = re.subn(pad, rep, novo)
        total[pad] = n
    # REMOVEFILTERS(F_rais[ano]) repetido em seguida não faz mal, mas limpa a leitura
    sobra = [p for p in ("D_Ano", "D_UF", "F_Mediana", "nm_divisao", "nm_secao") if re.search(rf"\b{p}\b", novo)]
    if sobra:
        print("AINDA SOBROU no _medidas:", sobra)
    for k, v in total.items():
        print(f"  {v:4}  {k}")
    if not testar:
        MEDIDAS.write_text(novo, encoding="utf-8", newline="")


def trocar_visual(obj, alias):
    """Troca Column {Expression.SourceRef, Property} conforme TROCAS_CAMPO. Devolve quantas trocas."""
    n = 0
    if isinstance(obj, dict):
        if "Property" in obj and isinstance(obj.get("Expression"), dict) and "SourceRef" in obj["Expression"]:
            ref = obj["Expression"]["SourceRef"]
            ent = ref.get("Entity") or alias.get(ref.get("Source"))
            chave = (ent, obj["Property"])
            if chave in TROCAS_CAMPO:
                nova_ent, nova_col = TROCAS_CAMPO[chave]
                obj["Property"] = nova_col
                if "Entity" in ref:
                    ref["Entity"] = nova_ent
                elif nova_ent != ent:
                    novo_alias = "rg_" + ref["Source"]
                    alias[novo_alias] = nova_ent
                    alias.setdefault("__novos__", {})[novo_alias] = nova_ent
                    ref["Source"] = novo_alias
                n += 1
        for k, v in obj.items():
            if k == "queryRef" and isinstance(v, str):
                for (e, c), (ne, nc) in TROCAS_CAMPO.items():
                    if v == f"{e}.{c}":
                        obj[k] = f"{ne}.{nc}"
            else:
                n += trocar_visual(v, alias)
    elif isinstance(obj, list):
        for v in obj:
            n += trocar_visual(v, alias)
    return n


def apelidos(obj, out):
    if isinstance(obj, dict):
        if "From" in obj and isinstance(obj["From"], list):
            for f in obj["From"]:
                if isinstance(f, dict) and "Name" in f and "Entity" in f:
                    out[f["Name"]] = f["Entity"]
        for v in obj.values():
            apelidos(v, out)
    elif isinstance(obj, list):
        for v in obj:
            apelidos(v, out)


def incluir_from(obj, novos):
    if isinstance(obj, dict):
        if "From" in obj and isinstance(obj["From"], list):
            tem = {f.get("Name") for f in obj["From"] if isinstance(f, dict)}
            for nome, ent in novos.items():
                if nome not in tem:
                    obj["From"].append({"Name": nome, "Entity": ent, "Type": 0})
        for v in obj.values():
            incluir_from(v, novos)
    elif isinstance(obj, list):
        for v in obj:
            incluir_from(v, novos)


def visuais(testar):
    total = 0
    arquivos = 0
    for f in sorted(PAGINAS.rglob("*.json")):
        texto = f.read_text(encoding="utf-8")
        if not re.search(r'"(D_UF|F_rais|D_Cnae)"', texto):
            continue
        dados = json.loads(texto)
        alias = {}
        apelidos(dados, alias)
        n = trocar_visual(dados, alias)
        if alias.get("__novos__"):
            incluir_from(dados, alias["__novos__"])
        if n:
            total += n
            arquivos += 1
            if not testar:
                f.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"  visuais: {total} campos trocados em {arquivos} arquivos")
    sobra = [str(f.relative_to(PAGINAS)) for f in PAGINAS.rglob("*.json")
             if re.search(r'"Entity": "(D_UF|D_Ano|F_Mediana)"|"Property": "(nm_divisao|estado)"', f.read_text(encoding="utf-8"))
             and "D_Rank_Divisao" not in f.read_text(encoding="utf-8")]
    if sobra and not testar:
        print("  conferir à mão:", sobra)


if __name__ == "__main__":
    testar = "--testar" in sys.argv
    print("_medidas.tmdl:")
    medidas(testar)
    visuais(testar)
