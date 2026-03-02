# Design Decisions

## 1) Tool routing: heuristic first, LLM second
A fast heuristic handles obvious cases (docs vs SQL). If unclear, the LLM router is used.

Reason: heuristics are stable, cheap, and reduce failure modes.

## 2) SQL generation + deterministic execution
The LLM proposes SQL, but DuckDB executes it. Results are shown back to the LLM for explanation.

Reason: avoids hallucinated totals and keeps the system auditable.

## 3) Trace logging as JSONL
Each user turn appends a JSON record to `logs/trace.jsonl`.

Reason: easy to diff, easy to parse, production-like observability.

## 4) Minimal dependencies
No paid subscriptions, no local model install. Uses HuggingFace Router + open source libraries.