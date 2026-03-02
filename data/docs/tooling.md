# Tooling

## doc_search
- Inputs: user query string
- Output: top-k doc snippets with file path and lexical score
- Purpose: provide local context for questions about docs/specs/notes

## duckdb_sql
- Inputs: SQL query string
- Output: columns + rows
- Purpose: deterministic computation for sums, counts, groupings, etc.