"""Testa as medidas-base contra o modelo aberto no Desktop (DEFINE MEASURE; somente leitura).

Antes de reabrir o PBIP o calendário ainda não existe no modelo carregado: use --sem-calendario para tirar as referências a ele.
Uso: python scripts/testar_base.py [--sem-calendario]
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import modelo_base as mb

PS1 = Path(tempfile.gettempdir()) / "dax_decada.ps1"     # cliente ADOMD do projeto RF (conecta no msmdsrv local)


def definicoes(sem_calendario):
    blocos = []
    for nome, _, dax, _, _, _ in mb.medidas():
        if sem_calendario:
            dax = dax.replace("REMOVEFILTERS(D_Calendario), ", "")
        tabela = "F_rais" if sem_calendario else "_medidas"      # antes de reabrir, a _medidas também não existe
        blocos.append(f"MEASURE {tabela}[{nome}] =\n{dax}")
    return "DEFINE\n" + "\n".join(blocos) + "\n"


def rodar(consultas):
    arq = Path(tempfile.gettempdir()) / "consultas_rais.dax"
    arq.write_text("\n###\n".join(consultas), encoding="utf-8", newline="\n")
    r = subprocess.run(["powershell", "-NoProfile", "-File", str(PS1), "-File", str(arq)], capture_output=True, text=True, encoding="utf-8")
    return r.stdout.replace("\r", "")


def main():
    d = definicoes("--sem-calendario" in sys.argv)
    nomes = ["Ano_Ref", "Ano_Inicio_Trecho", "Fonte_RAIS_Ref", "Empregos_Ref", "Empregos_Ano_Anterior", "Empregos_Var", "Empregos_Var_Pct",
             "Empregos_Cresc_Medio_Ano", "Remuneracao_Media_Ref", "Remuneracao_Media_SM_Ref", "Remuneracao_Mediana_Ref",
             "Empregos_Ref_AFL", "Empregos_Ref_Comparavel", "Empregos_Var_Pct_AFL", "Empregos_Cresc_Medio_Ano_AFL",
             "Remuneracao_Media_Ref_AFL", "Remuneracao_Mediana_Ref_AFL", "Remuneracao_Media_Ref_Comparavel", "Remuneracao_Mediana_Ref_Comparavel"]
    q = []
    for ano in (2025, 2022, 2021, 2009):
        q.append(f"-- ano {ano}\n{d}EVALUATE ROW(" + ", ".join(f'"{n}", CALCULATE([{n}], D_Ano[ano] = {ano})' for n in nomes) + ")")
    q.append(f"-- sem filtro (último ano)\n{d}EVALUATE ROW(" + ", ".join(f'"{n}", [{n}]' for n in nomes[:4]) + ")")
    q.append(f"-- mediana AFL mulheres SP 2025\n{d}EVALUATE ROW(\"m\", CALCULATE([Remuneracao_Mediana_Ref_AFL], D_Ano[ano] = 2025, D_Sexo[sexo] = \"Mulher\", D_UF[uf] = \"SP\"))")
    q.append(f"-- mediana bloqueada por raça\n{d}EVALUATE ROW(\"m\", CALCULATE([Remuneracao_Mediana_Ref_AFL], D_Ano[ano] = 2025, D_Raca[raca_cor] = \"Parda\"), \"media\", CALCULATE([Remuneracao_Media_Ref_AFL], D_Ano[ano] = 2025, D_Raca[raca_cor] = \"Parda\"))")
    print(rodar(q))


if __name__ == "__main__":
    main()
