from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.models import Gemini
from utils.adk_utils import retry_options
import os
from common import ClarificationNeeded


def steer_to_topic(excuse: str):
    """
    A tool the agent uses to excuse the user for not describing a pet.
    """
    raise ClarificationNeeded(excuse)


# Load writer instruction from external file if available
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../relevance_checker.md")
    with open(prompt_path, "r") as file:
        INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Writer prompt file not found at {prompt_path}. Using default instruction.")


relevance_checker_agent = Agent(
    name="relevance_checker_agent",
    description="Agent that confirms user describes a pet",
    instruction=INSTRUCTION,
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
    tools=[FunctionTool(func=steer_to_topic)])