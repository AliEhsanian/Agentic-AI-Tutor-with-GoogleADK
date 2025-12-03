"""
Simple manual evaluation harness for the AI Tutor Agent using InMemoryRunner.

This does not depend on ADK evalset files; it just sends fixed prompts and
checks that the responses satisfy simple heuristic criteria.
"""


import asyncio
import logging
from dataclasses import dataclass
from typing import List, Sequence

from google.adk.runners import InMemoryRunner
from google.genai import types as genai_types

from src.app_factory import app


# Silence noisy SDK logs for evaluation
logging.getLogger("google_adk").setLevel(logging.ERROR)
logging.getLogger("google_genai.types").setLevel(logging.ERROR)


@dataclass
class SimpleTestCase:
    """Minimal test case representation for manual evaluation."""
    name: str
    user_query: str
    must_contain_any: Sequence[str] | None = None
    must_contain_all: Sequence[str] | None = None
    min_length: int = 0  # optional sanity check


def _passes_heuristics(tc: SimpleTestCase, text: str) -> bool:
    text_lower = text.lower()

    if tc.min_length and len(text.strip()) < tc.min_length:
        return False

    if tc.must_contain_any:
        if not any(k.lower() in text_lower for k in tc.must_contain_any):
            return False

    if tc.must_contain_all:
        if not all(k.lower() in text_lower for k in tc.must_contain_all):
            return False

    return True


async def run_manual_tests() -> None:
    """Run a few simple tests using InMemoryRunner directly."""
    runner = InMemoryRunner(app=app)

    user_id = "eval_user"
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=None,
    )
    session_id = session.id

    test_cases: List[SimpleTestCase] = [
        # 1) Tutor should profile a new learner (ask about background/experience/goals)
        SimpleTestCase(
            name="profiling_new_learner",
            user_query="Hi, I want to learn machine learning but I'm a beginner.",
            must_contain_any=[
                "background",
                "experience",
                "programming",
                "math",
                "goals",
            ],
            min_length=50,
        ),
        # 2) Tutor should be able to explain a specific RL topic
        SimpleTestCase(
            name="explains_rl_topic",
            user_query="Explain Q-learning to me in simple terms.",
            must_contain_any=["q-learning"],
            min_length=60,
        ),
    ]

    print("=== Manual Behavior Checks (InMemoryRunner) ===")

    for tc in test_cases:
        user_message = genai_types.Content(
            role="user",
            parts=[genai_types.Part(text=tc.user_query)],
        )

        final_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message,
        ):
            if event.author == "user":
                continue

            if event.content:
                parts = getattr(event.content, "parts", None) or []
                texts = [
                    getattr(p, "text", "")
                    for p in parts
                    if getattr(p, "text", "")
                ]
                if texts:
                    final_text = "\n".join(texts)

        passed = _passes_heuristics(tc, final_text)
        status = "PASS" if passed else "FAIL"

        if passed:
            details = "Response satisfied heuristic criteria."
        else:
            details = (
                "Response did not satisfy heuristic criteria. Got:\n"
                f"{final_text}"
            )

        print(f"[{status}] {tc.name}: {details}\n")


if __name__ == "__main__":
    asyncio.run(run_manual_tests())
