from __future__ import annotations
from typing import TypedDict, Optional, Any, List

class AgentState(TypedDict):
    user_input: str
    chat_history: List[dict]
    tool_trace: List[dict]
    data: dict[str, Any]
    final_answer: Optional[str]