"""Extrai do modelo aberto no Desktop os números das prévias das 6 páginas (grava docs/previa/dados.json).

Usa só colunas e as medidas-base (DEFINE), então roda com ou sem o calendário carregado.
"""
import json
import subprocess
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "docs" / "previa" / "dados.json"
PS1 = Path(tempfile.gettempdir()) / "dax_decada.ps1"
ANO = 2025
G = 'D_GrupoSetor[grupo_setor]'

CONSULTAS = {
    # estoque por ano e grupo (AFL, Comparável, Demais)
    "serie_emp": "EVALUATE SUMMARIZECOLUMNS(D_Ano[ano], D_GrupoSetor[grupo_setor], \"v\", SUM(F_rais[vinculos]))",
    # remuneração média por ano e grupo
    "serie_media": "EVALUATE SUMMARIZECOLUMNS(D_Ano[ano], D_GrupoSetor[grupo_setor], \"s\", SUM(F_rais[soma_salario_valido]), \"q\", SUM(F_rais[qtd_salario_valido]), \"sm\", SUM(F_rais[soma_sm_valido]))",
    # mediana por ano e grupo (UF, sexo e escolaridade = Todos)
    "serie_mediana": "EVALUATE FILTER(SUMMARIZECOLUMNS(F_Mediana[ano], F_Mediana[grupo_setor], F_Mediana[uf], F_Mediana[sexo], F_Mediana[escolaridade_agrupada], \"m\", MAX(F_Mediana[mediana_salario])), "
                     "F_Mediana[uf] = \"Todos\" && F_Mediana[sexo] = \"Todos\" && F_Mediana[escolaridade_agrupada] = \"Todos\")",
    # contratos e jornada
    "contrato": f"EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_GrupoSetor[grupo_setor], F_rais[modalidade_contrato], F_rais[trabalho_intermitente], F_rais[trabalho_parcial], \"v\", SUM(F_rais[vinculos])), D_Ano[ano] = {ANO})",
    # divisões (sem os CNAEs do AFL) em 2025 e 2022
    "divisoes": "EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_Cnae[nm_divisao], D_Cnae[setor_principal], D_Cnae[setor_comparavel_afl], D_Ano[ano], \"v\", SUM(F_rais[vinculos])), D_Cnae[setor_afl] = \"Não\", D_Ano[ano] IN {2022, 2024, 2025})",
    # atividades do AFL
    "atividades": "EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_Cnae[cnae_fiscal], D_Cnae[nm_subclasse], D_Ano[ano], \"v\", SUM(F_rais[vinculos]), \"s\", SUM(F_rais[soma_salario_valido]), \"q\", SUM(F_rais[qtd_salario_valido]), "
                  "\"mul\", CALCULATE(SUM(F_rais[vinculos]), D_Sexo[sexo] = \"Mulher\")), D_Cnae[setor_afl] = \"Sim\", D_Ano[ano] IN {2022, 2024, 2025})",
    # UF
    "uf": f"EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_UF[uf], D_GrupoSetor[grupo_setor], D_Ano[ano], \"v\", SUM(F_rais[vinculos]), \"s\", SUM(F_rais[soma_salario_valido]), \"q\", SUM(F_rais[qtd_salario_valido])), D_Ano[ano] IN {{2024, {ANO}}})",
    # perfil 2025
    "sexo_idade": f"EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_GrupoSetor[grupo_setor], D_Sexo[sexo], D_FaixaIdade[faixa_idade], D_FaixaIdade[ordem], \"v\", SUM(F_rais[vinculos])), D_Ano[ano] = {ANO})",
    "idade_media": "EVALUATE SUMMARIZECOLUMNS(D_Ano[ano], D_GrupoSetor[grupo_setor], \"si\", SUM(F_rais[soma_idade]), \"qi\", SUM(F_rais[qtd_idade]), \"mul\", CALCULATE(SUM(F_rais[vinculos]), D_Sexo[sexo] = \"Mulher\"), \"v\", SUM(F_rais[vinculos]))",
    "escolaridade": f"EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_GrupoSetor[grupo_setor], D_Escolaridade[escolaridade_agrupada], D_Escolaridade[ordem], \"v\", SUM(F_rais[vinculos]), \"s\", SUM(F_rais[soma_salario_valido]), \"q\", SUM(F_rais[qtd_salario_valido])), D_Ano[ano] = {ANO})",
    "raca": f"EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_GrupoSetor[grupo_setor], D_Raca[raca_cor], D_Raca[grupo_raca], D_Raca[declarada], D_Raca[ordem], \"v\", SUM(F_rais[vinculos]), \"s\", SUM(F_rais[soma_salario_valido]), \"q\", SUM(F_rais[qtd_salario_valido])), D_Ano[ano] = {ANO})",
    "cbo": f"EVALUATE TOPN(12, CALCULATETABLE(SUMMARIZECOLUMNS(D_Cbo[ocupacao], \"v\", SUM(F_rais[vinculos]), \"mul\", CALCULATE(SUM(F_rais[vinculos]), D_Sexo[sexo] = \"Mulher\"), \"s\", SUM(F_rais[soma_salario_valido]), \"q\", SUM(F_rais[qtd_salario_valido])), {G} = \"AFL\", D_Ano[ano] = {ANO}), [v], DESC)",
    "primeiro_interm": "EVALUATE SUMMARIZECOLUMNS(D_Ano[ano], D_GrupoSetor[grupo_setor], \"v\", SUM(F_rais[vinculos]), \"prim\", CALCULATE(SUM(F_rais[vinculos]), F_rais[tipo_admissao] = \"Primeiro Emprego\"), "
                       "\"interm\", CALCULATE(SUM(F_rais[vinculos]), F_rais[trabalho_intermitente] = \"Sim\"), \"jovem\", CALCULATE(SUM(F_rais[vinculos]), D_FaixaIdade[faixa_idade] IN {\"14-17\", \"18-24\"}))",
    # remuneração por sexo e por escolaridade × sexo (média) em 2025
    "sal_sexo_esc": f"EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_GrupoSetor[grupo_setor], D_Sexo[sexo], D_Escolaridade[escolaridade_agrupada], D_Escolaridade[ordem], \"s\", SUM(F_rais[soma_salario_valido]), \"q\", SUM(F_rais[qtd_salario_valido])), D_Ano[ano] = {ANO})",
    "sal_sexo_serie": "EVALUATE SUMMARIZECOLUMNS(D_Ano[ano], D_GrupoSetor[grupo_setor], D_Sexo[sexo], \"s\", SUM(F_rais[soma_salario_valido]), \"q\", SUM(F_rais[qtd_salario_valido]))",
    "sal_raca_esc": f"EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(D_GrupoSetor[grupo_setor], D_Raca[grupo_raca], D_Escolaridade[escolaridade_agrupada], D_Escolaridade[ordem], \"s\", SUM(F_rais[soma_salario_valido]), \"q\", SUM(F_rais[qtd_salario_valido])), D_Ano[ano] = {ANO})",
    # mediana por sexo e por escolaridade (UF = Todos)
    "mediana_cortes": f"EVALUATE FILTER(SUMMARIZECOLUMNS(F_Mediana[grupo_setor], F_Mediana[uf], F_Mediana[sexo], F_Mediana[escolaridade_agrupada], F_Mediana[ano], \"m\", MAX(F_Mediana[mediana_salario])), F_Mediana[uf] = \"Todos\" && F_Mediana[ano] = {ANO})",
}


def rodar(consultas):
    arq = Path(tempfile.gettempdir()) / "consultas_previa.dax"
    arq.write_text("\n###\n".join(f"-- {k}\n{v}" for k, v in consultas.items()), encoding="utf-8", newline="\n")
    r = subprocess.run(["powershell", "-NoProfile", "-File", str(PS1), "-File", str(arq)], capture_output=True, text=True, encoding="utf-8")
    saida, atual = {}, None
    for linha in r.stdout.replace("\r", "").split("\n"):
        if linha.startswith("--- -- "):
            atual = linha[7:].strip()
            saida[atual] = []
        elif atual and linha.startswith("   "):
            if linha.strip().startswith("ERRO"):
                raise SystemExit(f"{atual}: {linha.strip()}")
            saida[atual].append([c.strip() for c in linha[3:].split(" | ")])
    return saida


def main():
    dados = rodar(CONSULTAS)
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in dados.items()})


if __name__ == "__main__":
    main()
