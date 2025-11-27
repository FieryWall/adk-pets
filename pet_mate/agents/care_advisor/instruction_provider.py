from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from utils.adk_utils import retry_options
import os
from pet_db_service import PetDBService
from logger import log  
from settings import current_model

# --- 1. Instruction Provider Agent (The Agent) ---

# Try to read prompt file
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../instruction_provider_prompt.md")
    with open(prompt_path, "r") as file:
        INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Instruction Provider prompt file not found at {prompt_path}.")

log(f"Instruction Provider prompt loaded. Length: {len(INSTRUCTION)} characters.")


def build_instruction_provider_agent(db_service: PetDBService) -> Agent:
    return Agent(
        name="instruction_provider_agent",
        model=Gemini(model=current_model(), retry_options=retry_options),
        description="Searches for pet care instructions from a specialized pet care database",
        instruction=INSTRUCTION,
        output_key="care_instructions",
        tools=[db_service.search],
    )

