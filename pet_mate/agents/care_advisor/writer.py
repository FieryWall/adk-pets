from google.adk.agents import Agent
from google.adk.tools import FunctionTool, AgentTool
from google.adk.tools.google_search_tool import google_search
from google.adk.models import Gemini
from common import ClarificationNeeded
from utils.adk_utils import retry_options
import os
from .researcher import guidance_researcher_agent

# [TODO] This is a placeholder agent definition. Update as needed!
def ask_clarification(question: str) -> str:
    """
    A tool the agent uses to explicitly ask the user for more information 
    to resolve a task. This function raises an exception to pause the flow.

    Args:
        question: The specific question the agent needs answered.

    Returns:
        str: The user's response (in a full ADK flow).
    """
    raise ClarificationNeeded(question)


# Load writer instruction from external file if available
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../writer_prompt.md")
    with open(prompt_path, "r") as file:
        WRITER_INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Writer prompt file not found at {prompt_path}. Using default instruction.")


guidance_writer_agent = Agent(
    name="guidance_writer_agent",
    description="Agent that provides advice and information on pet care",
    instruction=WRITER_INSTRUCTION,
    tools = [FunctionTool(func=ask_clarification), AgentTool(agent=guidance_researcher_agent)],
    output_key="guidance",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options)
)