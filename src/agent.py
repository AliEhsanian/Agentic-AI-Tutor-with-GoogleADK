"""
ADK Web entrypoint when running:

    adk web .

Here, the agents directory is the project root ("."),
and the agent package name is "src".

ADK will look for: src/agent.py with a top-level `root_agent`.
"""


from src.agents.root_tutor_agent import build_root_tutor_agent

root_agent = build_root_tutor_agent()
