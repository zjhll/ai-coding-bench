# AI Coding Bench

<p align="center">
  <strong>Benchmark framework for evaluating AI coding models across real-world software engineering tasks</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/models-Claude%20|%20DeepSeek%20|%20MiMo-blueviolet" alt="Models">
</p>

## Overview

AI Coding Bench is a multi-model benchmark framework that evaluates AI models on three core software engineering capabilities:

| Task | What it measures |
|------|-----------------|
| **Code Generation** | Producing correct, production-ready code from specifications |
| **Code Review** | Identifying bugs, security issues, and design flaws |
| **Debugging** | Locating root causes and proposing correct fixes |

## Supported Models

- **Claude (Opus 4.7)** — Anthropic's flagship reasoning model
- **DeepSeek (V3)** — Cost-efficient open-weight model
- **MiMo (V2.5)** — Xiaomi's multi-modal large model with strong coding performance

## Quick Start

```bash
pip install ai-coding-bench

# Set API keys
export ANTHROPIC_API_KEY="sk-..."
export DEEPSEEK_API_KEY="sk-..."
export MIMO_API_KEY="sk-..."

# Run full benchmark
ai-bench --models claude deepseek mimo
```

## Example Output

```
AI Coding Bench v1.0 — Evaluating coding models

▶ Running Claude (Opus 4.7)…
  Code Generation: 100.0% (2.3s)
  Code Review: 100.0% (1.8s)
  Debugging: 100.0% (2.1s)

▶ Running DeepSeek (V3)…
  Code Generation: 66.7% (3.1s)
  Code Review: 100.0% (2.5s)
  Debugging: 66.7% (2.9s)

▶ Running MiMo (V2.5)…
  Code Generation: 100.0% (1.9s)
  Code Review: 100.0% (1.6s)
  Debugging: 100.0% (1.8s)

┌──────────────────┬──────────┬─────────────┬───────────┬─────────┐
│ Model            │ Code Gen │ Code Review │ Debugging │ Overall │
├──────────────────┼──────────┼─────────────┼───────────┼─────────┤
│ Claude (Opus 4.7)│   100.0  │     100.0   │   100.0   │  100.0  │
│ DeepSeek (V3)    │    66.7  │     100.0   │    66.7   │   77.8  │
│ MiMo (V2.5)      │   100.0  │     100.0   │   100.0   │  100.0  │
└──────────────────┴──────────┴─────────────┴───────────┴─────────┘
```

## API Usage

```python
from ai_coding_bench.runner import BenchmarkRunner

runner = BenchmarkRunner(models=["claude", "deepseek", "mimo"])
runner.run()
runner.export_json("results/")
```

## Architecture

```
src/ai_coding_bench/
├── cli.py          # CLI entry point
├── models.py       # Model adapters (Claude, DeepSeek, MiMo)
├── runner.py       # Benchmark orchestrator
├── report.py       # Report generator
└── tasks/
    ├── base.py             # Abstract task interface
    ├── code_generation.py  # Code-from-specs evaluation
    ├── code_review.py      # Bug/security review evaluation
    └── debugging.py        # Root-cause analysis evaluation
```

## Adding a New Model

```python
from ai_coding_bench.models import ModelAdapter

@dataclass
class MyModelAdapter:
    name = "MyModel (v1)"
    provider = "Custom"

    async def generate(self, prompt: str, max_tokens: int = 4096) -> str:
        # Your inference logic here
        ...

# Register
MODEL_REGISTRY["mymodel"] = MyModelAdapter
```

## Roadmap

- [x] Claude / DeepSeek / MiMo adapters
- [x] Code generation, review, debugging tasks
- [ ] Streaming output evaluation
- [ ] Multi-language support (TypeScript, Go, Rust)
- [ ] Multi-agent collaboration benchmark
- [ ] Prompt caching efficiency comparison
- [ ] Web dashboard for results visualization

## License

MIT © 2026
