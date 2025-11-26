from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from utils.adk_utils import retry_options
import os


try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../trait_researcher_prompt.md")
    with open(prompt_path, "r") as file:
        INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Trait researcher prompt file not found at {prompt_path}.")


trait_researcher_agent = Agent(
    name="trait_researcher_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
    description="Searches for information using Google search",
    instruction=INSTRUCTION,
    tools=[google_search]
)