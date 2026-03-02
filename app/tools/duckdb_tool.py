from __future__ import annotations
from pathlib import Path
import duckdb

DB_PATH = Path("data/sample.duckdb")

def init_db_if_missing() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        return

    con = duckdb.connect(str(DB_PATH))
    con.execute("""
        CREATE TABLE sales(
          date DATE,
          item VARCHAR,
          quantity INTEGER,
          revenue DOUBLE
        );
    """)
    con.execute("""
        INSERT INTO sales VALUES
        ('2025-01-01','A',10,100.0),
        ('2025-01-02','A',5,55.0),
        ('2025-01-01','B',7,84.0),
        ('2025-02-01','B',2,25.0);
    """)
    con.close()

def duckdb_sql(sql: str) -> dict:
    init_db_if_missing()
    con = duckdb.connect(str(DB_PATH), read_only=False)
    try:
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        return {"columns": cols, "rows": rows}
    finally:
        con.close()