# HF + LangGraph Agent 

A no-subscription agentic AI using:
- HuggingFace Inference API (free tier)
- LangGraph for tool routing
- DuckDB for deterministic analytics
- Local doc search over `data/docs`

## Setup

### 1) HuggingFace token
Create a token in HuggingFace → Settings → Access Tokens

### 2) Create `.env`
`.env`contains the HF token.

### 3) Install + run
```bash
python -m venv .venv
source .\.venv\Scripts\activate
pip install -e .
hfagent
