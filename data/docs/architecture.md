# Architecture

OpsPilot is a small agentic assistant built around a clear workflow:

1. **Route**: decide whether the query needs tools (docs retrieval or SQL).
2. **Act**: run the selected tool deterministically.
3. **Respond**: synthesize the final answer using tool outputs.
4. **Trace**: store a lightweight audit trail (tool name, input, output summary).

## Why this design
- **Determinism for numbers**: Aggregations are executed by DuckDB, not guessed by the LLM.
- **Simple retrieval**: Local docs search provides relevant context without external databases.
- **Observable agent**: Traces are logged as JSONL to debug decisions and tool calls.

## Tools
- `doc_search(query)` → lexical retrieval over `data/docs`
- `duckdb_sql(sql)` → runs SQL over a local DuckDB file (auto-created)