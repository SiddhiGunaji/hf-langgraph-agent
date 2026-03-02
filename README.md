# OpsPilot - Tool-Using Agent (HF Router + LangGraph)

OpsPilot is a small **agentic AI** project that demonstrates how to build a **tool-using assistant** with:
- **HuggingFace Router** (no local model install)
- **LangGraph** for agent routing + execution
- **DuckDB** for deterministic analytics (no hallucinated totals)
- Local document retrieval over `data/docs`
- JSONL trace logging for observability

## Why this is agentic
This project implements a simple agent loop:

**Route → Tool → Respond → Trace**
- Routes queries to tools (docs retrieval vs SQL)
- Executes tools deterministically
- Uses the LLM to synthesize a final answer using tool outputs
- Logs a trace of tool usage

## Project structure
```text
app/
  agent.py        # LangGraph workflow (route → tool → respond)
  llm.py          # HF Router chat completion client
  trace.py        # JSONL trace logging
  tools/
    doc_search.py # local retrieval
    duckdb_tool.py# deterministic SQL tool
data/
  docs/           # architecture + design docs (used for retrieval demos)
logs/
  .gitkeep
tests/
  test_tools.py


## Setup (Windows PowerShell)

### 1) Create a HuggingFace token
HuggingFace → Settings → Access Tokens → Fine-grained token  
Enable: **Inference → Make calls to Inference Providers**

### 2) Create `.env`
Copy:
```powershell
copy .env.example .env