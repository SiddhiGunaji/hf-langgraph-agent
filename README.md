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
  agent.py         # LangGraph workflow (route → tool → respond)
  llm.py           # HuggingFace Router chat completion client
  trace.py         # JSONL trace logging
  main.py          # CLI entry point
  state.py         # Agent state definition
  prompts.py       # System prompt configuration
  tools/
    doc_search.py  # Local document retrieval
    duckdb_tool.py # Deterministic SQL tool
    utils.py       # Helper utilities

data/
  docs/            # Architecture & design documents (used for retrieval demo)

logs/
  .gitkeep         # Keeps logs folder tracked

tests/
  test_tools.py    # Basic validation tests

.github/
  workflows/ci.yml # GitHub Actions CI
```

## Setup (Windows PowerShell)

### 1. Create a HuggingFace Token

- Go to **HuggingFace → Settings → Access Tokens**
- Create a **Fine-grained token**
- Enable:

  Inference → Make calls to Inference Providers


### 2. Create `.env`

Edit:

```bash
HF_TOKEN=hf_your_token_here
HF_MODEL=meta-llama/Llama-3.1-8B-Instruct
```

### 3. Install and Run

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install the project in editable mode:

```powershell
pip install -e .
```

```powershell
hfagent
```

## Example Prompts
```text
From my docs, what is this repo about?
Total revenue by item
Count rows in sales table
```
### Example output:
```text
Agent: Total revenue per item is:
- Item A: $155.00
- Item B: $109.00

Trace: duckdb_sql
```
