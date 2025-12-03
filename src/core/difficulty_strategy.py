"""
Strategy pattern for choosing exercise difficulty
based on learner performance.
"""


from __future__ import annotations

from abc import ABC, abstractmethod

from src.core.models import StudentProgress


class DifficultyStrategy(ABC):
    """Abstraction for different adaptive difficulty strategies."""

    @abstractmethod
    def choose_difficulty(self, topic: str, progress: StudentProgress) -> str:
        """Return a difficulty label such as 'easy', 'medium', or 'hard'."""
        raise NotImplementedError


class AccuracyBasedDifficultyStrategy(DifficultyStrategy):
    """
    Concrete strategy based on topic-specific accuracy.

    Heuristic:
      - No history or very low attempts: 'easy'
      - < 0.4 accuracy: 'easy'
      - 0.4-0.75 accuracy: 'medium'
      - > 0.75 accuracy: 'hard'
    """

    def choose_difficulty(self, topic: str, progress: StudentProgress) -> str:
        stats = progress.topics.get(topic)
        if stats is None or stats.attempts == 0:
            return "easy"

        accuracy = stats.accuracy
        if accuracy < 0.4:
            return "easy"
        if accuracy < 0.75:
            return "medium"
        return "hard"
