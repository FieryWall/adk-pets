import os
from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.adk.models.google_llm import Gemini
from utils.adk_utils import retry_options
from .trait_researcher import trait_researcher_agent
from .image_finder import image_finder_agent
from common import ClarificationNeeded, GuessConfirmationNeeded
from google.adk.tools import FunctionTool
from pydantic import BaseModel, Field
from settings import current_model
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../guesser_prompt.md")
    with open(prompt_path, "r") as file:
        INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Guesser prompt file not found at {prompt_path}.")

def ask_clarification(question: str):
    """
    MANDATORY TOOL: Use this tool when you need more information from the user to identify the pet.
    Call this tool when the description is insufficient (e.g., user only says "cat" or "dog" without details).
    Call this tool when multiple variants are equally likely and you need to distinguish between them.
    DO NOT output to schema - use this tool instead.
    
    Args:
        question: The specific question the agent needs answered to proceed with identification.
    """
    raise ClarificationNeeded(question)


def confirm_guess(question: str, pet_name: str, image_url: str = ""):
    """
    MANDATORY TOOL: Use this tool to ask the user to confirm your pet identification guess.
    You MUST call this tool after getting an image from image_finder_agent and before outputting to schema.
    DO NOT output to schema until after the user confirms via this tool.
    
    Args:
        question: The confirmation question to ask the user (e.g., "Is this correct?")
        pet_name: The pet name that is being confirmed (official full name with breed if applicable)
        image_url: The image URL from image_finder_agent for visual confirmation
    """
    guess_details = {
        "pet_name": pet_name,
        "image_url": image_url
    }
    raise GuessConfirmationNeeded(question, guess_details)


class GuessDetails(BaseModel):
    pet_full_name: str = Field(description="The official full name of the pet (species and breed if applicable). Examples: 'Golden Retriever', 'Persian cat', 'European Hedgehog', 'Ball Python'")
    pet_image_url: str = Field(description="The URL of the image of the pet")


pet_guesser_agent = Agent(
    name="PetGuesser",
    description="Agent that identifies pets based on descriptions by researching traits and finding visual confirmation",
    model=Gemini(model=current_model(), retry_options=retry_options),
    instruction=INSTRUCTION,
    output_schema=GuessDetails,
    tools=[
        AgentTool(agent=trait_researcher_agent),
        AgentTool(agent=image_finder_agent),
        FunctionTool(func=ask_clarification),
        FunctionTool(func=confirm_guess)]
)