"""Model adapter layer — unified interface for Claude, DeepSeek, GPT, and MiMo."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol


class ModelAdapter(Protocol):
    """Protocol for AI model backends."""

    name: str
    provider: str

    async def generate(self, prompt: str, max_tokens: int = 4096) -> str: ...
    async def count_tokens(self, text: str) -> int: ...


@dataclass
class ClaudeAdapter:
    name = "Claude (Opus 4.7)"
    provider = "Anthropic"

    async def generate(self, prompt: str, max_tokens: int = 4096) -> str:
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        msg = await client.messages.create(
            model="claude-opus-4-7",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text

    async def count_tokens(self, text: str) -> int:
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        return (await client.messages.count_tokens(
            model="claude-opus-4-7",
            messages=[{"role": "user", "content": text}],
        )).input_tokens


@dataclass
class DeepSeekAdapter:
    name = "DeepSeek (V3)"
    provider = "DeepSeek"

    async def generate(self, prompt: str, max_tokens: int = 4096) -> str:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com/v1",
        )
        resp = await client.chat.completions.create(
            model="deepseek-chat",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content or ""


@dataclass
class MiMoAdapter:
    name = "MiMo (V2.5)"
    provider = "Xiaomi"

    async def generate(self, prompt: str, max_tokens: int = 4096) -> str:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(
            api_key=os.environ["MIMO_API_KEY"],
            base_url="https://api.xiaomimimo.com/v1",
        )
        resp = await client.chat.completions.create(
            model="mimo-v2.5",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content or ""


MODEL_REGISTRY: dict[str, type[ModelAdapter]] = {
    "claude": ClaudeAdapter,
    "deepseek": DeepSeekAdapter,
    "mimo": MiMoAdapter,
}


def list_available_models() -> list[str]:
    return list(MODEL_REGISTRY.keys())


class ModelAdapter:
    """Factory for model backends."""

    @staticmethod
    def for_name(name: str) -> ModelAdapter:
        cls = MODEL_REGISTRY.get(name.lower())
        if cls is None:
            raise ValueError(f"Unknown model: {name}. Available: {list(MODEL_REGISTRY)}")
        return cls()
