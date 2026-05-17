"""Benchmark results reporter — generates comparative analysis."""

from pathlib import Path
from typing import Any


class ReportGenerator:
    """Generates markdown comparison reports from benchmark results."""

    def __init__(self, results: list[dict[str, Any]]):
        self.results = results

    def markdown(self) -> str:
        lines = [
            "# AI Coding Benchmark Results",
            "",
            "## Models Compared",
            "",
        ]
        models = sorted({r["model"] for r in self.results})
        for m in models:
            lines.append(f"- {m}")

        lines += ["", "## Scores", "", "| Model | Code Gen | Code Review | Debugging | Overall |", "|-------|----------|-------------|-----------|---------|"]

        for model in models:
            scores = {r["task"]: r["score"] for r in self.results if r["model"] == model}
            avg = sum(scores.values()) / len(scores) if scores else 0
            lines.append(
                f"| {model} "
                f"| {scores.get('Code Generation', 0):.1f}% "
                f"| {scores.get('Code Review', 0):.1f}% "
                f"| {scores.get('Debugging', 0):.1f}% "
                f"| **{avg:.1f}%** |"
            )

        lines += ["", "> Run `ai-bench --models claude deepseek mimo` to reproduce."]
        return "\n".join(lines)

    def save(self, path: str = "benchmarks") -> Path:
        out = Path(path) / "REPORT.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.markdown())
        return out
