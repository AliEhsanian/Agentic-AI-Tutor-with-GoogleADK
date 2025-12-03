"""
Root tutor agent that orchestrates profiling, lesson pipelines, and feedback.
"""


from google.adk.agents import LlmAgent
from google.adk.tools import load_memory
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from src.core.llm import build_gemini_model
from src.core.observability import tutor_after_agent_callback
from src.agents.explanation_agent import build_explanation_agent
from src.agents.exercise_agent import build_exercise_generator_agent
from src.agents.feedback_agent import build_feedback_agent
from src.agents.lesson_pipeline_agent import build_lesson_pipeline_agent
from src.agents.profiling_agent import build_profiling_agent
from src.agents.search_agent import google_search_tool


def build_root_tutor_agent() -> LlmAgent:
    """
    Build the main user-facing AI Tutor agent.

    This agent:
      - decides when to profile, teach, or grade
      - delegates to sub-agents
      - can use tools itself (search + memory)
    """
    profiling_agent = build_profiling_agent()
    explanation_agent = build_explanation_agent()
    exercise_agent = build_exercise_generator_agent()
    feedback_agent = build_feedback_agent()
    lesson_pipeline_agent = build_lesson_pipeline_agent(
        explanation_agent=explanation_agent,
        exercise_agent=exercise_agent,
    )

    return LlmAgent(
        name="root_tutor_agent",
        model=build_gemini_model(),
        description=(
            "Orchestrates a team of tutoring agents that profile the learner, explain concepts, "
            "Adaptive AI tutor that profiles the learner, explains concepts, "
            "generates practice questions, and gives feedback with intelligent "
            "difficulty progression."
        ),
        instruction=(
            "You are the Orchestrator for an AI tutoring system.\n"
            "\n"
            "Important: You do NOT answer the user directly and you do NOT generate explanations or exercises "
            "yourself. Your ONLY job is to decide which sub-agent should handle the user's message.\n"
            "Your job is to route each user message to the right sub-agent and keep the "
            "overall experience smooth and natural.\n"
            "\n"
            "High-level behavior:\n"
            "- If the learner is new OR there is no stored profile in the context, delegate to "
            "  'profiling_agent' ONCE to collect their background, goals, and learning style.\n"
            "- If the learner asks to learn or understand a NEW topic, delegate to "
            "  'profiling_agent' ONCE to collect their background, goals, and learning style.\n"
            "- After profiling_agent has summarized and updated the profile, DO NOT send them back "
            "  into profiling again unless they explicitly say their background/goals have changed.\n"
            "- When the learner asks to learn a topic (e.g., 'Teach me Q-learning' or 'Help me with gradients'), "
            "  delegate to 'lesson_pipeline_agent' and let it run the explain, practice flow.\n"
            "- When the learner submits an answer to a question (e.g., mentions 'Q1', 'Q2', or phrases like "
            "  'For Q1 my answer is...', 'I think the answer is ...'), delegate to 'feedback_agent' to grade "
            "  and update progress.\n"
            "- Use 'google_search_tool' when the concept clearly benefits from external information or examples.\n"
            "- Use 'load_memory' or 'PreloadMemoryTool' to bring in relevant past context when available.\n"
            "\n"
            "Transition rules:\n"
            "- Do NOT ask the user to say 'yes', 'okay', or 'let's go' just to proceed. After profiling is done, "
            "  you should proactively guide them: either ask which topic they want to start with, or if their "
            "  original request already contained a topic, move directly into teaching via 'lesson_pipeline_agent'.\n"
            "- Avoid repeating profiling questions that profiling_agent already asked.\n"
            "- If the user seems to answer a question or asks 'Is this correct?', treat it as an answer and "
            "  route to 'feedback_agent'.\n"
            "\n"
            "Response style:\n"
            "- Keep messages concise and structured (use short sections or bullet points when helpful).\n"
            "- Be encouraging, but do not over-apologize or repeat the same instructions.\n"
            "- Always make the next step obvious: either ask a clear follow-up question or move into a lesson "
            "  or feedback without extra friction.\n"
        ),
        tools=[google_search_tool, load_memory, PreloadMemoryTool()],
        sub_agents=[profiling_agent, lesson_pipeline_agent, feedback_agent],
        after_agent_callback=tutor_after_agent_callback,
    )
