"""
Simple domain models for the AI Tutor:
- StudentProfile: stable learner info
- TopicStats: per-topic statistics
- StudentProgress: overall progression and mastery tracking
"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class StudentProfile:
    """Represents stable information about the learner."""

    level: str  # e.g. "beginner", "intermediate", "advanced"
    goals: List[str] = field(default_factory=list)
    preferred_style: str = "intuitive examples"
    focus_topics: List[str] = field(default_factory=list)


@dataclass
class TopicStats:
    """Running statistics for a single topic."""

    attempts: int = 0
    correct: int = 0

    @property
    def accuracy(self) -> float:
        if self.attempts == 0:
            return 0.0
        return self.correct / self.attempts


@dataclass
class StudentProgress:
    """
    Tracks performance across topics and difficulty history,
    providing a basis for adaptive exercise difficulty.
    """

    total_attempts: int = 0
    total_correct: int = 0
    topics: Dict[str, TopicStats] = field(default_factory=dict)
    difficulty_history: List[str] = field(default_factory=list)

    @property
    def overall_accuracy(self) -> float:
        if self.total_attempts == 0:
            return 0.0
        return self.total_correct / self.total_attempts

    def record_result(self, topic: str, difficulty: str, was_correct: bool) -> None:
        """Update global and per-topic stats with a new exercise result."""
        self.total_attempts += 1
        if was_correct:
            self.total_correct += 1

        if topic not in self.topics:
            self.topics[topic] = TopicStats()

        stats = self.topics[topic]
        stats.attempts += 1
        if was_correct:
            stats.correct += 1

        self.difficulty_history.append(difficulty)
