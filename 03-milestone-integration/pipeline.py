#!/usr/bin/env python3
"""Skeleton RAG pipeline gluing N19 retrieval + N20 llama-server.
Tối ưu cho model có khả năng Thinking (Reasoning).
"""
from __future__ import annotations
import time
import httpx
from dataclasses import dataclass
from typing import Iterable

LLAMA_SERVER_BASE = "http://localhost:8080/v1"
SYSTEM_PROMPT = (
    "You are a serving-engineering tutor. Answer using only the documents provided. "
    "If the documents don't contain the answer, say so."
)

TOY_DOCS = [
    {"id": "n20-paged", "text": "PagedAttention treats KV cache like virtual memory pages, eliminating 60-80% fragmentation."},
    {"id": "n20-radix", "text": "RadixAttention stores KV in a prefix trie; cache hit on shared prefix lets the engine skip prefill."},
    {"id": "n20-disagg", "text": "Disaggregated serving (Mooncake, llm-d, Dynamo) splits prefill and decode onto separate GPU pools."},
    {"id": "n20-goodput", "text": "Goodput@SLO = req/s satisfying TTFT and TPOT SLOs. Throughput at saturation ignores SLO."},
    {"id": "n20-quant", "text": "GGUF Q4_K_M is the production-quality default for laptop/edge serving via llama.cpp."},
]

@dataclass
class Doc:
    id: str
    text: str
    score: float

def retrieve(query: str, k: int = 3) -> list[Doc]:
    """Cải tiến tìm kiếm từ khóa đơn giản."""
    q_terms = {w.lower().strip("?!.,@") for w in query.split() if len(w) > 3}
    scored = []
    for d in TOY_DOCS:
        d_text_lower = d["text"].lower()
        score = sum(1 for term in q_terms if term in d_text_lower)
        scored.append(Doc(d["id"], d["text"], float(score)))
    return sorted(scored, key=lambda d: d.score, reverse=True)[:k]

def build_prompt(query: str, contexts: Iterable[Doc]) -> list[dict]:
    ctx_block = "\n".join(f"[{c.id}] {c.text}" for c in contexts)
    user = f"Context:\n{ctx_block}\n\nQuestion: {query}"
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]

def call_llm(messages: list[dict]) -> tuple[str, str, float]:
    """Trả về (thinking, content, elapsed_ms)."""
    t0 = time.perf_counter()
    r = httpx.post(
        f"{LLAMA_SERVER_BASE}/chat/completions",
        json={"model": "local", "messages": messages, "max_tokens": 500, "temperature": 0.3},
        timeout=120.0,
    )
    r.raise_for_status()
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    
    data = r.json()["choices"][0]["message"]
    thinking = data.get("reasoning_content", "")
    content = data.get("content", "")
    
    return thinking, content, elapsed_ms

def answer(query: str) -> dict:
    t_total = time.perf_counter()
    docs = retrieve(query, k=3)
    messages = build_prompt(query, docs)
    thinking, text, t_llm_ms = call_llm(messages)

    return {
        "query": query,
        "thinking": thinking,
        "answer": text,
        "contexts": [{"id": d.id, "score": d.score} for d in docs],
        "timings_ms": {
            "retrieve": round(0.1, 1), # Toy logic
            "llm": round(t_llm_ms, 1),
            "total": round((time.perf_counter() - t_total) * 1000.0, 1),
        },
    }

def main() -> None:
    queries = [
        "Why is goodput more useful than throughput?",
        "What problem does PagedAttention actually solve?",
    ]
    for q in queries:
        print(f"\n{'='*20} {q} {'='*20}")
        result = answer(q)
        if result['thinking']:
            print(f"\n[THINKING]:\n{result['thinking']}")
        print(f"\n[ANSWER]:\n{result['answer'].strip()}")
        print(f"\n(Time: {result['timings_ms']['total']}ms | Contexts: {[c['id'] for c in result['contexts']]})")

if __name__ == "__main__":
    main()
