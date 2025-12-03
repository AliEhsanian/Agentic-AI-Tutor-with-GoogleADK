"""
Sequential agent that runs explanation followed by exercise generation
for a single topic.
"""


from google.adk.agents import SequentialAgent
from google.adk.agents import Agent


def build_lesson_pipeline_agent(
    explanation_agent: Agent,
    exercise_agent: Agent,
) -> SequentialAgent:
    """Create the lesson pipeline agent (explain then exercise)."""
    return SequentialAgent(
        name="lesson_pipeline_agent",
        sub_agents=[explanation_agent, exercise_agent],
        description="Runs explanation then exercise for a single topic.",
    )
