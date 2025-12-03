"""
Creates the ADK App, wiring together the root agent, memory, and
context compaction (summarization).
"""


import warnings

from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer

from src.config import config
from src.core.llm import build_gemini_model
from src.agents.root_tutor_agent import build_root_tutor_agent


def build_app() -> App:
    """Build the ADK App for the AI Tutor."""
    root_agent = build_root_tutor_agent()

    summarizer_llm = build_gemini_model()
    summarizer = LlmEventSummarizer(llm=summarizer_llm)

    # Hide the experimental warning for EventsCompactionConfig
    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message=r"\[EXPERIMENTAL\] EventsCompactionConfig:.*",
    )

    compaction_config = EventsCompactionConfig(
        summarizer=summarizer,
        compaction_interval=8,
        overlap_size=2,
    )

    return App(
        name=config.app_name,
        root_agent=root_agent,
        events_compaction_config=compaction_config,
    )

# Global instances that other modules (CLI, evaluation, etc.) can reuse
app: App = build_app()
