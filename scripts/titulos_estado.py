"""Manchetes dos cards de estado (Empregos e Quanto ganha, Todos os setores e AFL): nome completo do estado em vez da sigla.

Mexe só em três medidas: Titulo_Emp_UF_AFL_HTML, Titulo_Emp_UF_Total_HTML e Titulo_Rem_UF_HTML (esta atende Todos e AFL).
O nome vem de D_UF[estado] por LOOKUPVALUE a partir da sigla já calculada; sem correspondência, a sigla é mantida. Idempotente.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
TMDL = RAIZ / "RAIS Emprego Formal.SemanticModel" / "definition" / "tables" / "_medidas.tmdl"
NOME = 'COALESCE(LOOKUPVALUE(D_UF[estado], D_UF[uf], {v}), {v})'

# medida -> lista de (trecho antigo, trecho novo); \n vira a quebra de linha do arquivo, \t\t\t o recuo das linhas da medida
EDICOES = {
    "Titulo_Emp_UF_AFL_HTML": [
        ('VAR UF = CONCATENATEX(Lider, D_UF[uf], "")', 'VAR UF = CONCATENATEX(Lider, D_UF[uf], "")\n\t\t\tVAR UFN = ' + NOME.format(v="UF")),
        ('VAR UFMais = CONCATENATEX(Mais, D_UF[uf], "")', 'VAR UFMais = CONCATENATEX(Mais, D_UF[uf], "")\n\t\t\tVAR UFMaisN = ' + NOME.format(v="UFMais")),
        ('UF & " reúne os empregos do filtro"', 'UFN & " reúne os empregos do filtro"'),
        ('UF & " tem " &', 'UFN & " tem " &'),
        ('"Onde o AFL pesa mais: " & UFMais &', '"Onde o AFL pesa mais: " & UFMaisN &'),
    ],
    "Titulo_Emp_UF_Total_HTML": [
        ('VAR UFMais = CONCATENATEX(Mais, D_UF[uf], "")', 'VAR UFMais = CONCATENATEX(Mais, D_UF[uf], "")\n\t\t\tVAR UFMaisN = ' + NOME.format(v="UFMais")),
        ('"Em " & UFMais & ", o AFL é "', '"Em " & UFMaisN & ", o AFL é "'),
    ],
    "Titulo_Rem_UF_HTML": [
        ('VAR UF = CONCATENATEX(Lider1, D_UF[uf], "")', 'VAR UF = CONCATENATEX(Lider1, D_UF[uf], "")\n\t\t\tVAR UFN = ' + NOME.format(v="UF")),
        ('VAR UFP = CONCATENATEX(Pior, D_UF[uf], "")', 'VAR UFP = CONCATENATEX(Pior, D_UF[uf], "")\n\t\t\tVAR UFPN = ' + NOME.format(v="UFP")),
        ('UF & ": R$ "', 'UFN & ": R$ "'),
        ('UF & " paga a maior média: R$ "', 'UFN & " paga a maior média: R$ "'),
        ('"Maior distância para os Comparáveis: " & UFP &', '"Maior distância para os Comparáveis: " & UFPN &'),
    ],
}


def bloco(t, nome):
    ini = t.index(f"\tmeasure {nome} =")
    fim = t.index("\n\t///", ini) if "\n\t///" in t[ini:] else len(t)
    return ini, min(fim, t.index("\n\tmeasure ", ini + 10) if "\n\tmeasure " in t[ini + 10:] else len(t))


def main():
    bruto = TMDL.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in bruto else "\n"
    t = bruto.replace("\r\n", "\n")
    for nome, edicoes in EDICOES.items():
        ini, fim = bloco(t, nome)
        corpo = t[ini:fim]
        if "UFN" in corpo or "UFMaisN" in corpo:
            print(nome, "já ajustada")
            continue
        for antes, depois in edicoes:
            assert corpo.count(antes) == 1, f"{nome}: trecho não encontrado exatamente uma vez: {antes}"
            corpo = corpo.replace(antes, depois)
        t = t[:ini] + corpo + t[fim:]
        print(nome, "ajustada")
    TMDL.write_bytes(t.replace("\n", eol).encode("utf-8"))


if __name__ == "__main__":
    main()
