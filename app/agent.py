from __future__ import annotations
from typing import Literal

from langgraph.graph import StateGraph, END

from app.state import AgentState
from app.prompts import SYSTEM_PROMPT
from app.llm import call_llm
from app.tools.doc_search import doc_search
from app.tools.duckdb_tool import duckdb_sql
from app.tools.utils import format_table

def _router_heuristic(text: str) -> Literal["DOCS", "SQL", "FINAL"]:
    t = text.lower()
    if any(x in t for x in ["docs", "notes", "readme", "documentation", "from my docs", "data/docs"]):
        return "DOCS"
    if any(x in t for x in ["sql", "query", "sum", "total", "average", "avg", "count", "group by", "revenue", "quantity"]):
        return "SQL"
    return "FINAL"

def decide(state: AgentState) -> Literal["use_docs", "use_sql", "final"]:
    h = _router_heuristic(state["user_input"])
    if h == "DOCS":
        return "use_docs"
    if h == "SQL":
        return "use_sql"

    prompt = f"""{SYSTEM_PROMPT}

Decide the next step.
Return exactly one token: DOCS, SQL, or FINAL.

User: {state["user_input"]}
"""
    out = call_llm(prompt, temperature=0.0, max_new_tokens=10).strip().upper()
    if "DOC" in out:
        return "use_docs"
    if "SQL" in out:
        return "use_sql"
    return "final"

def use_docs(state: AgentState) -> AgentState:
    results = doc_search(state["user_input"], k=5)
    state["tool_trace"].append({"tool": "doc_search", "input": state["user_input"], "output": results})
    state["data"]["doc_results"] = results
    return state

def use_sql(state: AgentState) -> AgentState:
    sql_prompt = """You are a data assistant.
Write a DuckDB SQL query ONLY (no explanation).
Table: sales(date, item, quantity, revenue).

User question:
""" + state["user_input"]

    sql = call_llm(sql_prompt, temperature=0.0, max_new_tokens=120).strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    result = duckdb_sql(sql)
    pretty = format_table(result)

    state["tool_trace"].append({"tool": "duckdb_sql", "input": sql, "output": result})
    state["data"]["sql"] = sql
    state["data"]["sql_result_pretty"] = pretty
    return state

def final(state: AgentState) -> AgentState:
    docs_ctx = ""
    if state["data"].get("doc_results"):
        docs_ctx = "\n".join([f"- {r['path']} (score={r['score']}): {r['snippet']}" for r in state["data"]["doc_results"]])

    sql_ctx = ""
    if state["data"].get("sql_result_pretty"):
        sql_ctx = f"SQL:\n{state['data'].get('sql','')}\n\nResult:\n{state['data']['sql_result_pretty']}"

    prompt = f"""{SYSTEM_PROMPT}

Chat history:
{state["chat_history"]}

User:
{state["user_input"]}

Doc context (if any):
{docs_ctx}

SQL context (if any):
{sql_ctx}

Now answer the user.
Also include a short "Trace" section listing tools used (names only). Tools used so far: {tools_used}
"""
    answer = call_llm(prompt, temperature=0.2, max_new_tokens=350).strip()
    state["final_answer"] = answer
    return state

def build_graph():
    g = StateGraph(AgentState)
    g.add_node("decide", lambda s: s)
    g.add_node("use_docs", use_docs)
    g.add_node("use_sql", use_sql)
    g.add_node("final", final)

    g.set_entry_point("decide")
    g.add_conditional_edges(
        "decide",
        lambda s: decide(s),
        {"use_docs": "use_docs", "use_sql": "use_sql", "final": "final"},
    )
    g.add_edge("use_docs", "final")
    g.add_edge("use_sql", "final")
    g.add_edge("final", END)
    return g.compile()