from __future__ import annotations

def format_table(result: dict, max_rows: int = 20) -> str:
    cols = result.get("columns", [])
    rows = result.get("rows", [])[:max_rows]
    if not cols:
        return str(rows)

    lines = [" | ".join(cols), " | ".join(["---"] * len(cols))]
    for r in rows:
        lines.append(" | ".join(str(x) for x in r))
    return "\n".join(lines)