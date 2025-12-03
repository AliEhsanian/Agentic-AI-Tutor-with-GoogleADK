"""
ADK-based evaluation using AgentEvaluator and an evalset file.

For this to run, you need an evalset JSON file created via ADK Web, e.g.:

    src/ai_tutor_basic.evalset.json

You can create it by:
  1) Run: `uv run adk web .`
  2) Use the web UI to chat with your tutor
  3) Add the session to an eval set from the Eval tab
  4) Save the evalset as ai_tutor_basic.evalset.json (it will be written to src/)
"""


import asyncio
from pathlib import Path
import json
import warnings

from google.adk.evaluation.agent_evaluator import AgentEvaluator


# Global: ignore all UserWarnings (including [EXPERIMENTAL])
warnings.filterwarnings("ignore", category=UserWarning)


async def run_adk_eval() -> None:
    """
    Run ADK's AgentEvaluator on an evalset file, if present.

    This uses the official ADK evaluation pipeline and will:
      - load your agent from the 'src.agent' module (root_agent in src/agent.py)
      - load the evalset at src/ai_tutor_basic.evalset.json
      - run evaluation using Vertex Eval service (depending on your ADK setup)
    """

    src_dir = Path(__file__).resolve().parents[1]
    eval_path = src_dir / "ai_tutor_basic.evalset.json"

    print("=== AgentEvaluator (ADK evalset) ===")

    if not eval_path.exists():
        print(f"Evalset file not found at: {eval_path}")
        print(
            "Create an evalset via `uv run adk web .` (Eval tab → save as "
            "ai_tutor_basic) and re-run this script.\n"
        )
        return

    print(f"Running evalset: {eval_path}\n")

    eval_config = {
    "criteria": {
        "tool_trajectory_avg_score": 0.6,  # Perfect tool usage required
        "response_match_score": 0.5,  # 50% text similarity threshold
        }
    }

    # eval_config = {
    #     "criteria": {
    #     "final_response_match_v2": {
    #      "threshold": 0.5,
    #     "judge_model_options": {
    #             "judge_model": "gemini-2.5-flash-lite",
    #             "num_samples": 1
    #             }
    #         }
    #     }
    # }

    with open("src/test_config.json", "w") as f:
        json.dump(eval_config, f, indent=2)

    await AgentEvaluator.evaluate(
        agent_module="src.agent",
        eval_dataset_file_path_or_dir=str(eval_path),
        num_runs=1,
    )

    print("\nAgentEvaluator evaluation finished successfully.\n")


if __name__ == "__main__":
    asyncio.run(run_adk_eval())
