"""Base task definition for benchmark evaluations."""

from abc import ABC, abstractmethod

from ..models import ModelAdapter


class BaseTask(ABC):
    name: str

    @abstractmethod
    async def evaluate(self, model: ModelAdapter) -> float:
        """Run evaluation and return score 0-100."""
