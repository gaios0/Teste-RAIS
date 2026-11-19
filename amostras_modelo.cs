using System.IO;
using System.Text;

var sb = new StringBuilder();
string NL = Environment.NewLine;

Func<string, string, string> q = (titulo, dax) =>
{
    try { return "-- " + titulo + NL + Convert.ToString(EvaluateDax(dax)) + NL; }
    catch (Exception ex) { return "-- " + titulo + NL + "(falhou: " + ex.Message + ")" + NL; }
};

sb.AppendLine(q("D_regiao: pares uf | sigla_uf",
  @"CONCATENATEX(SUMMARIZE(D_regiao, D_regiao[uf], D_regiao[sigla_uf]), D_regiao[uf] & "" | "" & D_regiao[sigla_uf], "" ;; "", D_regiao[sigla_uf], ASC)"));
sb.AppendLine(q("D_regiao: 8 linhas (cod_municipio | municipio | uf | sigla_uf)",
  @"CONCATENATEX(TOPN(8, D_regiao, D_regiao[cod_municipio], ASC), D_regiao[cod_municipio] & "" | "" & D_regiao[municipio] & "" | "" & D_regiao[uf] & "" | "" & D_regiao[sigla_uf], "" ;; "", D_regiao[cod_municipio], ASC)"));
sb.AppendLine(q("F_rais[uf] distintos",
  @"CONCATENATEX(DISTINCT(F_rais[uf]), F_rais[uf], "", "", F_rais[uf], ASC)"));
sb.AppendLine(q("F_rais[id_municipio]: 5 exemplos",
  @"CONCATENATEX(TOPN(5, DISTINCT(F_rais[id_municipio]), F_rais[id_municipio], ASC), F_rais[id_municipio], "", "", F_rais[id_municipio], ASC)"));
sb.AppendLine(q("D_Cnae[divisao_afl] distintos",
  @"CONCATENATEX(DISTINCT(D_Cnae[divisao_afl]), D_Cnae[divisao_afl], "" ;; "", D_Cnae[divisao_afl], ASC)"));
sb.AppendLine(q("D_Cnae: 6 linhas (cnae_fiscal | nm_classe | grupo_setor | setor_afl | divisao_afl)",
  @"CONCATENATEX(TOPN(6, D_Cnae, D_Cnae[cnae_fiscal], ASC), D_Cnae[cnae_fiscal] & "" | "" & D_Cnae[nm_classe] & "" | "" & D_Cnae[grupo_setor] & "" | "" & D_Cnae[setor_afl] & "" | "" & D_Cnae[divisao_afl], "" ;; "", D_Cnae[cnae_fiscal], ASC)"));
sb.AppendLine(q("D_Cnae[setor_principal] distintos",
  @"CONCATENATEX(DISTINCT(D_Cnae[setor_principal]), D_Cnae[setor_principal], "", "", D_Cnae[setor_principal], ASC)"));
sb.AppendLine(q("D_Calendario: Ano | Base",
  @"CONCATENATEX(SUMMARIZE(D_Calendario, D_Calendario[Ano], D_Calendario[Base]), D_Calendario[Ano] & "" | "" & D_Calendario[Base], "" ;; "", D_Calendario[Ano], ASC)"));
sb.AppendLine(q("F_rais[ano] distintos",
  @"CONCATENATEX(DISTINCT(F_rais[ano]), F_rais[ano], "", "", F_rais[ano], ASC)"));

Directory.CreateDirectory(@"C:\temp");
File.WriteAllText(@"C:\temp\painel_rais_amostras.txt", sb.ToString(), Encoding.UTF8);
Info(@"Gerado: C:\temp\painel_rais_amostras.txt");
