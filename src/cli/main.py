"""
Clean CLI entrypoint to interact with the AI Tutor Agent using ADK.
"""


import asyncio
import logging
from typing import List, Optional

from google.adk.runners import InMemoryRunner
from google.genai import types as genai_types

from src.app_factory import app


# Color codes for terminal output (ANSI)
BLUE = "\033[94m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Disable all logging for the CLI session
logging.disable(logging.CRITICAL)


def print_banner() -> None:
    """Print a nice boxed banner for the CLI."""
    BANNER_WIDTH = 70  # total characters for the top/bottom border
    border = "=" * BANNER_WIDTH

    line_1 = "              ***** AI Tutor Agent with Google ADK *****"
    line_2 = "                         Type 'exit' to quit."
    line_3 = "Example: you > Hi, I'm a beginner in reinforcement learning."
    line_4 = "         Can you help me learn?"

    def box_line(text: str) -> str:
        # 2 chars for "|" and "|" → BANNER_WIDTH - 2 space for content
        return f"| {text.ljust(BANNER_WIDTH - 3)}|"

    print(border)
    print(box_line(line_1))
    print(box_line(line_2))
    print(box_line(line_3))
    print(box_line(line_4))
    print(border)
    print()


def content_to_text(content: Optional[genai_types.Content]) -> str:
    """
    Convert a Gemini Content object into a readable text string.
    """
    if not content:
        return ""

    parts = getattr(content, "parts", None) or []
    texts: List[str] = []

    for part in parts:
        text = getattr(part, "text", None)
        if text:
            texts.append(text)

    return "\n".join(texts)


async def run_cli() -> None:
    """Start an interactive CLI session with the tutor."""
    runner = InMemoryRunner(app=app)

    user_id = "cli_user"
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=None,
    )
    session_id = session.id

    print_banner()

    while True:
        user_input = input(f"{BLUE}you > {RESET}")
        if user_input.strip().lower() in {"exit", "quit"}:
            break

        user_message = genai_types.Content(
            role="user",
            parts=[genai_types.Part(text=user_input)],
        )

        final_text: str = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message,
        ):
            if event.author == "user":
                continue
            text = content_to_text(event.content)
            if text:
                final_text = text


        if final_text:
            print(f"\n{GREEN}tutor > {RESET}{final_text}\n")
        else:
            print(f"\n{GREEN}tutor > {RESET}[No text response]\n")


if __name__ == "__main__":
    asyncio.run(run_cli())
