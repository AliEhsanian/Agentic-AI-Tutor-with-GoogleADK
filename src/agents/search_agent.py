"""
Creates an agent tool for google search. This agent is created because ADK does not accepts google search tool
with other functions tools!!!
"""


from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

from src.core.llm import build_gemini_model


def build_search_agent() -> LlmAgent:
    """Agent that ONLY uses the Google Search built-in tool."""
    return LlmAgent(
        name="google_search_agent",
        model=build_gemini_model(),
        description="Searches the web using Google Search.",
        instruction=(
            "You are a specialist in using Google Search. "
            "Use the google_search tool to fetch up-to-date information. "
            "Then summarize results clearly, and cite important sources."
        ),
        tools=[google_search],
    )

search_agent = build_search_agent()
google_search_tool = AgentTool(search_agent)
