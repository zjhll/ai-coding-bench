"""Core benchmark runner that orchestrates model evaluations across coding tasks."""

import asyncio
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

from .models import ModelAdapter, list_available_models
from .tasks.code_generation import CodeGenerationTask
from .tasks.code_review import CodeReviewTask
from .tasks.debugging import DebuggingTask

console = Console()

TASKS = [CodeGenerationTask, CodeReviewTask, DebuggingTask]


class BenchmarkRunner:
    """Orchestrates evaluation of AI models across coding task categories."""

    def __init__(self, models: list[str] | None = None):
        self.models = [ModelAdapter.for_name(m) for m in (models or list_available_models())]
        self.results: list[dict[str, Any]] = []

    def run(self) -> Table:
        console.print("[bold cyan]AI Coding Bench v1.0[/] — Evaluating coding models\n")

        for model in self.models:
            console.print(f"\n[bold yellow]▶[/] Running {model.name}…")
            for task_cls in TASKS:
                task = task_cls()
                start = time.perf_counter()
                score = asyncio.run(task.evaluate(model))
                elapsed = time.perf_counter() - start
                self.results.append({
                    "model": model.name,
                    "task": task.name,
                    "score": score,
                    "elapsed": round(elapsed, 2),
                    "timestamp": datetime.utcnow().isoformat(),
                })
                console.print(f"  {task.name}: {score:.1f}% ({elapsed:.1f}s)")

        return self._render_table()

    def _render_table(self) -> Table:
        table = Table(title="Benchmark Results", header_style="bold cyan")
        table.add_column("Model", style="bold")
        table.add_column("Code Gen", justify="right")
        table.add_column("Code Review", justify="right")
        table.add_column("Debugging", justify="right")
        table.add_column("Overall", justify="right", style="bold green")

        for model in self.models:
            scores = {r["task"]: r["score"] for r in self.results if r["model"] == model.name}
            avg = sum(scores.values()) / len(scores) if scores else 0
            table.add_row(
                model.name,
                f"{scores.get('Code Generation', 0):.1f}",
                f"{scores.get('Code Review', 0):.1f}",
                f"{scores.get('Debugging', 0):.1f}",
                f"{avg:.1f}",
            )

        console.print(table)
        return table

    def export_json(self, path: str = "benchmarks/results") -> Path:
        import json

        out = Path(path) / f"results_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(self.results, indent=2))
        console.print(f"\n[dim]Results saved to {out}[/]")
        return out


def main():
    runner = BenchmarkRunner()
    runner.run()
    runner.export_json()


if __name__ == "__main__":
    main()
