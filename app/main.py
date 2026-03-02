from __future__ import annotations
from rich.console import Console

from app.agent import build_graph
from app.state import AgentState

console = Console()

def run():
    graph = build_graph()
    state: AgentState = {
        "user_input": "",
        "chat_history": [],
        "tool_trace": [],
        "data": {},
        "final_answer": None,
    }

    console.print("[bold green]HF + LangGraph Agent[/bold green] (type 'exit' to quit)\n")

    while True:
        user = console.input("[bold cyan]You[/bold cyan]: ").strip()
        if user.lower() in {"exit", "quit"}:
            break

        state["user_input"] = user
        state["chat_history"].append({"role": "user", "content": user})

        out = graph.invoke(state)
        answer = out.get("final_answer") or ""

        console.print(f"\n[bold magenta]Agent[/bold magenta]: {answer}\n")

        state["chat_history"].append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    run()