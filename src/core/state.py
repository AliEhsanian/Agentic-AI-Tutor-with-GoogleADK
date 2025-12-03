"""
Helpers for reading/writing domain models to/from ADK state dictionaries.
"""


from __future__ import annotations

from typing import Any, Dict, Optional

from src.core.models import StudentProfile, StudentProgress, TopicStats


STATE_KEY_PROFILE = "user:student_profile"
STATE_KEY_PROGRESS = "user:student_progress"


def load_profile(state: Dict[str, Any]) -> Optional[StudentProfile]:
    """Load StudentProfile from state if present, otherwise None."""
    raw = state.get(STATE_KEY_PROFILE)
    if not isinstance(raw, dict):
        return None

    return StudentProfile(
        level=raw.get("level", "beginner"),
        goals=list(raw.get("goals", [])),
        preferred_style=raw.get("preferred_style", "intuitive examples"),
        focus_topics=list(raw.get("focus_topics", [])),
    )


def save_profile(profile: StudentProfile, state: Dict[str, Any]) -> None:
    """Persist StudentProfile into the state."""
    state[STATE_KEY_PROFILE] = {
        "level": profile.level,
        "goals": list(profile.goals),
        "preferred_style": profile.preferred_style,
        "focus_topics": list(profile.focus_topics),
    }


def load_progress(state: Dict[str, Any]) -> StudentProgress:
    """Load StudentProgress from state, or create an empty one."""
    raw = state.get(STATE_KEY_PROGRESS)
    if not isinstance(raw, dict):
        return StudentProgress()

    topics: Dict[str, TopicStats] = {}
    for topic_name, stats_raw in raw.get("topics", {}).items():
        topics[topic_name] = TopicStats(
            attempts=int(stats_raw.get("attempts", 0)),
            correct=int(stats_raw.get("correct", 0)),
        )

    return StudentProgress(
        total_attempts=int(raw.get("total_attempts", 0)),
        total_correct=int(raw.get("total_correct", 0)),
        topics=topics,
        difficulty_history=list(raw.get("difficulty_history", [])),
    )


def save_progress(progress: StudentProgress, state: Dict[str, Any]) -> None:
    """Persist StudentProgress into the state."""
    topics_dict = {
        name: {
            "attempts": stats.attempts,
            "correct": stats.correct,
        }
        for name, stats in progress.topics.items()
    }

    state[STATE_KEY_PROGRESS] = {
        "total_attempts": progress.total_attempts,
        "total_correct": progress.total_correct,
        "topics": topics_dict,
        "difficulty_history": list(progress.difficulty_history),
    }
