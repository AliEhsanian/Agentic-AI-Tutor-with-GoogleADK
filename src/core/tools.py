"""
Custom ADK tools that:
- update the StudentProfile
- record exercise results
- choose the next exercise difficulty

The tools rely on the domain models, state helpers, and difficulty strategy.
"""


from __future__ import annotations

import logging
from typing import Any, Dict

from google.adk.tools.tool_context import ToolContext
from google.adk.tools.function_tool import FunctionTool

from src.core.difficulty_strategy import AccuracyBasedDifficultyStrategy
from src.core.models import StudentProfile
from src.core.state import (
    load_profile,
    load_progress,
    save_profile,
    save_progress,
)


logger = logging.getLogger("agentic_ai_tutor_with_gooleadk.tools")
logger.setLevel(logging.INFO)

_difficulty_strategy = AccuracyBasedDifficultyStrategy()


def update_student_profile(
    profile_json: Dict[str, Any],
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Update the persistent learner profile for the current user.
    """
    state = tool_context.state

    current_profile = load_profile(state) or StudentProfile(
        level=profile_json.get("level", "beginner"),
        goals=list(profile_json.get("goals", [])),
        preferred_style=profile_json.get("preferred_style", "intuitive examples"),
        focus_topics=list(profile_json.get("focus_topics", [])),
    )

    if "level" in profile_json:
        current_profile.level = profile_json["level"]
    if "goals" in profile_json:
        current_profile.goals = list(profile_json["goals"])
    if "preferred_style" in profile_json:
        current_profile.preferred_style = profile_json["preferred_style"]
    if "focus_topics" in profile_json:
        current_profile.focus_topics = list(profile_json["focus_topics"])

    save_profile(current_profile, state)
    logger.info("Tool(update_student_profile): profile=%s", current_profile)

    return {"status": "success", "profile": vars(current_profile)}


def record_exercise_result(
    topic: str,
    difficulty: str,
    was_correct: bool,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Record the result of a single exercise attempt and update mastery stats.
    """
    state = tool_context.state
    progress = load_progress(state)

    progress.record_result(topic=topic, difficulty=difficulty, was_correct=was_correct)
    save_progress(progress, state)

    topic_accuracy = progress.topics[topic].accuracy
    logger.info(
        "Tool(record_exercise_result): topic=%s difficulty=%s correct=%s "
        "overall_acc=%.3f topic_acc=%.3f",
        topic,
        difficulty,
        was_correct,
        progress.overall_accuracy,
        topic_accuracy,
    )

    return {
        "status": "success",
        "overall_accuracy": progress.overall_accuracy,
        "topic_accuracy": topic_accuracy,
        "total_attempts": progress.total_attempts,
    }


def get_next_exercise_difficulty(
    topic: str,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Choose the next difficulty level for the given topic based on past performance.
    """
    state = tool_context.state
    progress = load_progress(state)

    difficulty = _difficulty_strategy.choose_difficulty(topic, progress)
    reason = "Difficulty chosen by accuracy-based strategy."

    logger.info(
        "Tool(get_next_exercise_difficulty): topic=%s -> difficulty=%s",
        topic,
        difficulty,
    )

    return {
        "status": "success",
        "topic": topic,
        "recommended_difficulty": difficulty,
        "reason": reason,
    }


# FunctionTool wrappers for ADK registration
update_student_profile_tool = FunctionTool(func=update_student_profile)
record_exercise_result_tool = FunctionTool(func=record_exercise_result)
get_next_exercise_difficulty_tool = FunctionTool(func=get_next_exercise_difficulty)
