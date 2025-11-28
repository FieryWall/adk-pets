from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, FunctionTool
from utils.adk_utils import retry_options
import os
from .profile_researcher import profile_researcher_agent
from settings import current_model
from pet_db_service import PetDBService
from .common import ProfileGeneratorInput, ProfileGeneratorOutput

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../profile_writer_prompt.md")
    with open(prompt_path, "r") as file:
        INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Profile writer prompt file not found at {prompt_path}.")


def build_profile_writer_agent(db_service: PetDBService) -> Agent:
    async def save_pet_profile(pet_profile: str):
        """
        MANDATORY TOOL: Saves the pet profile to the database.
        You MUST call this tool after compiling the profile to persist it for future use.
        
        Args:
            pet_profile: The complete pet profile string to save
        """
        await db_service.save(pet_profile)
        return {"status": "success", "message": "Pet profile saved successfully"}

    return Agent(
        name="profile_writer",
        description="Agent that writes a profile for a pet",
        model=Gemini(model=current_model(), retry_options=retry_options),
        instruction=INSTRUCTION,
        tools=[AgentTool(agent=profile_researcher_agent), FunctionTool(func=save_pet_profile)],
        input_schema=ProfileGeneratorInput,
        output_schema=ProfileGeneratorOutput
    )