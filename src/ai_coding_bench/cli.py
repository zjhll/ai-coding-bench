"""Command-line interface for AI Coding Bench."""

import argparse

from .runner import BenchmarkRunner
from .models import list_available_models


def main():
    parser = argparse.ArgumentParser(
        description="AI Coding Bench — Evaluate AI models on real coding tasks"
    )
    parser.add_argument(
        "--models", nargs="*",
        help=f"Models to benchmark. Available: {', '.join(list_available_models())}"
    )
    parser.add_argument(
        "--output", default="benchmarks/results",
        help="Output directory for results JSON"
    )
    parser.add_argument("--version", action="version", version="1.0.0")
    args = parser.parse_args()

    runner = BenchmarkRunner(models=args.models)
    runner.run()
    if args.output:
        runner.export_json(args.output)


if __name__ == "__main__":
    main()
