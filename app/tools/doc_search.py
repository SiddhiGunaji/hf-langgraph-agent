from __future__ import annotations
from pathlib import Path
from typing import List, Tuple

DOCS_DIR = Path("data/docs")

def _read_docs() -> List[Tuple[str, str]]:
    docs = []
    if not DOCS_DIR.exists():
        return docs
    for p in DOCS_DIR.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".txt"}:
            docs.append((str(p), p.read_text(encoding="utf-8", errors="ignore")))
    return docs

def doc_search(query: str, k: int = 5) -> List[dict]:
    terms = {t.lower() for t in query.split() if len(t) > 2}
    scored = []
    for path, text in _read_docs():
        low = text.lower()
        score = sum(1 for t in terms if t in low)
        if score > 0:
            scored.append((score, path, text))

    scored.sort(reverse=True, key=lambda x: x[0])

    results = []
    for score, path, text in scored[:k]:
        snippet = text[:700].replace("\n", " ")
        results.append({"path": path, "score": score, "snippet": snippet})
    return results