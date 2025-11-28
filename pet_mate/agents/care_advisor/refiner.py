from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools.tool_context import ToolContext
import os
from logger import log


def exit_loop(tool_context: ToolContext) -> str:
    """Call this function ONLY when the review_feedback is 'APPROVED', indicating the guidance is finished and no more changes are needed."""
    log("exit_loop called - exiting refinement loop")
    tool_context.actions.escalate = True
    return "Guidance approved. Exiting refinement loop."


# Load refiner instruction from external file if available
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../refiner_prompt.md")
    with open(prompt_path, "r") as file:
        REFINER_INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Refiner prompt file not found at {prompt_path}. Using default instruction.")

log(f"Refiner prompt loaded. Length: {len(REFINER_INSTRUCTION)} characters.")


refiner_agent = Agent(
    name="refiner_agent",
    model=Gemini(
        model_name="gemini-2.5-flash-lite",
    ),
    instruction=REFINER_INSTRUCTION,
    output_key="guidance",
    tools=[exit_loop]
)

