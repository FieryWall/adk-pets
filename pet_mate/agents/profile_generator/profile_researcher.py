from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import google_search
from utils.adk_utils import retry_options
import os
from settings import current_model
from .common import ProfileGeneratorInput
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../profile_researcher_prompt.md")
    with open(prompt_path, "r") as file:
        INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Profile researcher prompt file not found at {prompt_path}.")



profile_researcher_agent = Agent(
    name="profile_researcher",
    description="Agent that researches a profile for a pet",
    model=Gemini(model=current_model(), retry_options=retry_options),
    instruction=INSTRUCTION,
    tools=[google_search],
    input_schema=ProfileGeneratorInput
)