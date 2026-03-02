from __future__ import annotations
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_MODEL = os.getenv("HF_MODEL", "HuggingFaceH4/zephyr-7b-beta").strip()

if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is missing. Create a .env file with HF_TOKEN=... (see .env.example).")

API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json",
}

class HFError(RuntimeError):
    pass

def call_llm(prompt: str, temperature: float = 0.2, max_new_tokens: int = 350) -> str:
    payload = {
        "model": HF_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        # some providers expect max_tokens (OpenAI-style)
        "max_tokens": max_new_tokens,
    }

    last_err = None
    for attempt in range(3):
        try:
            r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)

            # Retry for common transient errors
            if r.status_code in (429, 503, 504):
                time.sleep(2 * (attempt + 1))
                continue

            # If it's an error, raise with the body so we know the exact reason
            if r.status_code >= 400:
                raise HFError(f"HTTP {r.status_code} - {r.text}")

            data = r.json()
            return data["choices"][0]["message"]["content"].strip()

        except Exception as e:
            last_err = e
            time.sleep(1 * (attempt + 1))

    raise HFError(f"HuggingFace router call failed after retries: {last_err}")