from __future__ import annotations

from rich.console import Console

from app.agent import build_graph
from app.state import AgentState
from app.trace import append_trace

console = Console()


def run() -> None:
    graph = build_graph()

    # Persistent conversation state
    state: AgentState = {
        "user_input": "",
        "chat_history": [],
        "tool_trace": [],
        "data": {},
        "final_answer": None,
    }

    console.print("[bold green]OpsPilot — Tool-Using Agent[/bold green] (type 'exit' to quit)\n")

    while True:
        user = console.input("[bold cyan]You[/bold cyan]: ").strip()
        if user.lower() in {"exit", "quit"}:
            break

        # Reset per-turn artifacts so traces/results don't accumulate across turns
        state["user_input"] = user
        state["tool_trace"] = []
        state["data"] = {}
        state["final_answer"] = None

        # Keep conversational memory
        state["chat_history"].append({"role": "user", "content": user})

        out = graph.invoke(state)
        answer = (out.get("final_answer") or "").strip()

        # Build a stable trace line (Python-generated, not LLM-dependent)
        tools = [t.get("tool") for t in out.get("tool_trace", []) if t.get("tool")]
        tools_unique = []
        for x in tools:
            if x not in tools_unique:
                tools_unique.append(x)
        tools_str = ", ".join(tools_unique) if tools_unique else "none"

        # Append structured trace to logs/trace.jsonl
        append_trace(
            {
                "user_input": user,
                "tools_used": tools_unique,
                "final_answer_preview": (answer[:250] + "...") if len(answer) > 250 else answer,
            }
        )

        console.print(f"\n[bold magenta]Agent[/bold magenta]: {answer}\n")
        console.print(f"[dim]Trace: {tools_str}[/dim]\n")

        state["chat_history"].append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    run()