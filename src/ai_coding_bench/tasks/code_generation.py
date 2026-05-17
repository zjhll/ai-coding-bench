"""Code generation task — measures ability to produce correct code from specs."""

from .base import BaseTask

CODING_PROMPTS = [
    {
        "prompt": "Write a Python function that implements a thread-safe LRU cache with TTL support. "
                  "Include type hints, docstring, and handle edge cases.",
        "check": lambda out: "lru" in out.lower()
        and "cache" in out.lower()
        and "ttl" in out.lower()
        and "thread" in out.lower(),
    },
    {
        "prompt": "Write a REST API endpoint in FastAPI that accepts a CSV file upload, "
                  "validates it against a Pydantic schema, transforms each row, and streams "
                  "the result back as JSON Lines. Handle errors gracefully.",
        "check": lambda out: "fastapi" in out.lower()
        and "csv" in out.lower()
        and "pydantic" in out.lower(),
    },
    {
        "prompt": "Implement an async connection pool for WebSocket clients in Python "
                  "with automatic reconnection, backpressure handling, and graceful shutdown.",
        "check": lambda out: "websocket" in out.lower()
        and "async" in out.lower()
        and "pool" in out.lower(),
    },
]


class CodeGenerationTask(BaseTask):
    name = "Code Generation"

    async def evaluate(self, model) -> float:
        passed = 0
        for case in CODING_PROMPTS:
            output = await model.generate(case["prompt"], max_tokens=2048)
            if case["check"](output):
                passed += 1
        return (passed / len(CODING_PROMPTS)) * 100
