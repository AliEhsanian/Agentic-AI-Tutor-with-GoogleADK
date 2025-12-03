"""
Factory functions for configuring LLM models used by agents.
"""


from __future__ import annotations

from google.genai import types as genai_types
from google.adk.models.google_llm import Gemini

from src.config import config


def build_gemini_model() -> Gemini:
    """Create a Gemini model with sensible retry options."""
    retry_config = genai_types.HttpRetryOptions(
        attempts=5,
        exp_base=2,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    )
    generation_config = genai_types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.9,
    )

    return Gemini(
        model=config.model_name,
        retry_options=retry_config,
        generation_config=generation_config,
    )
