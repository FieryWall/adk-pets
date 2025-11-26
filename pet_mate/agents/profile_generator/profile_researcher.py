from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from utils.adk_utils import retry_options
import os

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
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
    instruction=INSTRUCTION,
    tools=[google_search],
    input_schema=[
        {
            "name": "pet_full_name",
            "type": "string",
            "description": "The official full name of the pet (species and breed if applicable) from the session, e.g., 'Golden Retriever', 'Persian cat', 'European Hedgehog'."
        }
    ]
)