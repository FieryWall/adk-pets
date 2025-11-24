from google.adk.agents import Agent
from google.adk.tools import FunctionTool, AgentTool
from google.adk.tools.google_search_tool import google_search
from google.adk.models import Gemini
from common import ClarificationNeeded
from utils.adk_utils import retry_options
import os

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


WRITER_INSTRUCTION = None
# Load writer instruction from external file if available
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../writer_prompt.md")
    with open(prompt_path, "r") as file:
        WRITER_INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Writer prompt file not found at {prompt_path}. Using default instruction.")

# Helper agent for Google Search to avoid tool conflict with Function Calling
search_agent = Agent(
    name="search_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
    description="Searches for information using Google search",
    instruction="Use the google_search tool to find information on the given topic.",
    tools=[google_search]
)

guidance_writer_agent = Agent(
    name="guidance_writer_agent",
    description="Agent that provides advice and information on pet care",
    instruction=WRITER_INSTRUCTION,
    tools= [FunctionTool(func=ask_clarification), AgentTool(agent=search_agent)],
    output_key="guidance",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options)
)