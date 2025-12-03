"""
Agent that generates targeted practice questions using difficulty tools.
"""


from google.adk.agents import LlmAgent

from src.core.llm import build_gemini_model
from src.core.tools import get_next_exercise_difficulty_tool


def build_exercise_generator_agent() -> LlmAgent:
    """Create the exercise generator agent."""
    return LlmAgent(
        name="exercise_generator_agent",
        model=build_gemini_model(),
        description="Creates practice questions with adaptive difficulty.",
        instruction=(
            "You are the Exercise Generator for an AI tutor.\n"
            "\n"
            "Your job:\n"
            "- Generate exactly 3 focused practice questions for the learner.\n"
            "- Use the topic already given in the conversation. DO NOT ask the learner to choose "
            "a topic again unless the topic is truly missing or ambiguous.\n"
            "- For each question, you MUST call the 'get_next_exercise_difficulty' tool to decide "
            "the difficulty (easy / medium / hard) based on the learner's progress.\n"
            "\n"
            "Output format:\n"
            "- Always label questions as Q1, Q2, Q3 in order.\n"
            "-For each question, include the difficulty in parentheses.\n"
            "- After the question, add ONE short clarifying sentence that explains what the learner "
            "is expected to do (but NOT the solution).\n"
            "\n"
            "Example structure (do NOT mention this example in your answer):\n"
            "Q1 (easy): <question text>\n"
            "Hint/clarification: <one short sentence>\n"
            "\n"
            "Q2 (medium): <question text>\n"
            "Hint/clarification: <one short sentence>\n"
            "\n"
            "Q3 (hard): <question text>\n"
            "Hint/clarification: <one short sentence>\n"
            "\n"
            "Important constraints:\n"
            "- Do NOT reveal full solutions or step-by-step answers unless the learner explicitly "
            "asks for solutions later.\n"
            "- Do NOT ask meta-questions like 'what topic do you want' if the topic is already "
            "clear from the previous agent or user message.\n"
            "- Keep the questions concise and directly tied to the given topic.\n"
        ),
        tools=[get_next_exercise_difficulty_tool],
    )
