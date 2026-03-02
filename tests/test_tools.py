from app.tools.doc_search import doc_search
from app.tools.duckdb_tool import duckdb_sql, init_db_if_missing

def test_doc_search_finds_architecture_doc():
    results = doc_search("Architecture route tool respond", k=5)
    assert any("architecture.md" in r["path"].lower() for r in results)

def test_duckdb_sql_total_revenue():
    init_db_if_missing()
    out = duckdb_sql("SELECT SUM(revenue) AS total_revenue FROM sales;")
    assert out["columns"] == ["total_revenue"]
    assert len(out["rows"]) == 1
    total = out["rows"][0][0]
    assert abs(total - (100.0 + 55.0 + 84.0 + 25.0)) < 1e-9