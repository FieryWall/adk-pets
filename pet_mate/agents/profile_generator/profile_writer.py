from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from utils.adk_utils import retry_options
import os
from .profile_researcher import profile_researcher_agent


try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../profile_writer_prompt.md")
    with open(prompt_path, "r") as file:
        INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Profile writer prompt file not found at {prompt_path}.")

profile_writer_agent = Agent(
    name="profile_writer",
    description="Agent that writes a profile for a pet",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
    instruction=INSTRUCTION,
    tools=[AgentTool(agent=profile_researcher_agent)],
    input_schema=[
        {
            "name": "pet_full_name",
            "type": "string",
            "description": "The official full name of the pet (species and breed if applicable)"
        }
    ],
    output_schema=[
        {
            "name": "pet_profile",
            "type": "string",
            "description": "Comprehensive pet profile including most important characteristics, care guidelines, and interesting facts. Structured for use in future guidance scenarios."
        }
    ]
)