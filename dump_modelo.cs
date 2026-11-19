// Tabular Editor 2/3 (C# Script) - gera o arquivo C:\temp\painel_rais_modelo.txt
// Inclui colunas/medidas OCULTAS, tipos, sortByColumn, relações e partições.
// Ao final, tenta pegar amostras de valores (só funciona no TE3 conectado ao modelo; se falhar, só pula).

using System.IO;
using System.Text;

var sb = new StringBuilder();
sb.AppendLine("MODELO: " + Model.Database.Name);
sb.AppendLine("Compat level: " + Model.Database.CompatibilityLevel);
sb.AppendLine();

foreach (var t in Model.Tables)
{
    sb.AppendLine("==== TABELA: " + t.Name + (t.IsHidden ? "  [OCULTA]" : ""));
    foreach (var p in t.Partitions)
        sb.AppendLine("  partition: " + p.Name + " | modo: " + p.Mode + " | tipo: " + p.SourceType);

    foreach (var c in t.Columns)
    {
        sb.AppendLine("  COL " + c.Name
            + " | " + c.DataType
            + " | " + c.Type
            + (c.IsHidden ? " | OCULTA" : "")
            + (c.IsKey ? " | KEY" : "")
            + (c.SortByColumn != null ? " | sortBy=" + c.SortByColumn.Name : ""));
    }
    foreach (var m in t.Measures)
        sb.AppendLine("  MEASURE " + m.Name + (m.IsHidden ? " | OCULTA" : ""));
    sb.AppendLine();
}

sb.AppendLine("==== RELACIONAMENTOS");
foreach (var r in Model.Relationships)
{
    sb.AppendLine(r.FromTable.Name + "[" + r.FromColumn.Name + "]  ->  "
        + r.ToTable.Name + "[" + r.ToColumn.Name + "]"
        + " | " + r.FromCardinality + ":" + r.ToCardinality
        + " | filtro: " + r.CrossFilteringBehavior
        + " | ativa: " + r.IsActive);
}
sb.AppendLine();

sb.AppendLine("==== AMOSTRAS (opcional)");
string[] consultas = new string[] {
    "EVALUATE TOPN(15, D_regiao)",
    "EVALUATE TOPN(10, D_Calendario)",
    "EVALUATE TOPN(10, F_rais)"
};
foreach (var q in consultas)
{
    sb.AppendLine("-- " + q);
    try
    {
        var dt = EvaluateDax(q) as System.Data.DataTable;
        if (dt != null)
        {
            sb.AppendLine(string.Join(" | ", dt.Columns.Cast<System.Data.DataColumn>().Select(x => x.ColumnName)));
            foreach (System.Data.DataRow row in dt.Rows)
                sb.AppendLine(string.Join(" | ", row.ItemArray.Select(x => x == null ? "" : x.ToString())));
        }
    }
    catch (Exception ex) { sb.AppendLine("(falhou: " + ex.Message + ")"); }
    sb.AppendLine();
}

Directory.CreateDirectory(@"C:\temp");
File.WriteAllText(@"C:\temp\painel_rais_modelo.txt", sb.ToString(), Encoding.UTF8);
Info("Gerado: C:\\temp\\painel_rais_modelo.txt");
