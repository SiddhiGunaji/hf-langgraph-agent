from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

TRACE_PATH = Path("logs/trace.jsonl")

def append_trace(record: dict) -> None:
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        **record,
    }
    with TRACE_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")