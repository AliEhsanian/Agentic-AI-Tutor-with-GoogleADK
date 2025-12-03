"""
Callbacks and logging helpers for keeping track of agent behavior.
"""


from __future__ import annotations

import logging
from typing import Any, Optional

from google.genai import types as genai_types
from google.adk.agents.callback_context import CallbackContext

from src.core.state import STATE_KEY_PROGRESS


logger = logging.getLogger("agentic_ai_tutor_with_googleadk")
logger.setLevel(logging.INFO)


def extract_overall_accuracy(state: Any) -> float:
    """
    Calculate an approximate overall accuracy from raw progress state.

    Works with both a plain dict and google.adk.sessions.State.
    """
    if state is None:
        return 0.0

    try:
        raw_progress = state.get(STATE_KEY_PROGRESS, {})
    except AttributeError:
        # Fallback if we ever get a plain dict or something else
        raw_progress = {}
        if isinstance(state, dict):
            raw_progress = state.get(STATE_KEY_PROGRESS, {})

    total_attempts = raw_progress.get("total_attempts", 0)
    total_correct = raw_progress.get("total_correct", 0)

    if total_attempts == 0:
        return 0.0
    return total_correct / total_attempts


def tutor_after_agent_callback(
    callback_context: CallbackContext,
) -> Optional[genai_types.Content]:
    """
    Simple after-agent callback for logging and basic observability.

    Logs:
      - agent name
      - invocation id
      - overall accuracy (if available in state)
    """
    state = callback_context.state
    overall_accuracy = extract_overall_accuracy(state)

    # Try to log whether we have progress or not, without relying on .keys()
    try:
        has_progress = STATE_KEY_PROGRESS in state  # works for State and dict
    except TypeError:
        has_progress = False

    logger.info(
        "[AFTER_AGENT] name=%s invocation_id=%s overall_acc=%.3f has_progress=%s",
        callback_context.agent_name,
        callback_context.invocation_id,
        overall_accuracy,
        has_progress,
    )

    # Do not modify content; this callback is for side-effect logging only.
    return None
