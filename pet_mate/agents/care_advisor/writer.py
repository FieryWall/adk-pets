from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import FunctionTool, AgentTool
from common import ClarificationNeeded
from utils.adk_utils import retry_options
import os
from .researcher import guidance_researcher_agent
from .instruction_provider import build_instruction_provider_agent
from pet_db_service import PetDBService
from logger import log

def ask_clarification(question: str) -> str:
    """
    Asks the user for clarification.
    
    CRITICAL: You MUST use this tool whenever you need more information from the user (like pet species, symptoms, etc.).
    Do NOT ask questions in your final response text. Call this tool instead.

    Args:
        question: The question to ask the user.
    """
    log(f"[Tool 'ask_clarification']: {question}")
    raise ClarificationNeeded(question)


# Load writer instruction from external file if available
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../writer_prompt.md")
    with open(prompt_path, "r") as file:
        WRITER_INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Writer prompt file not found at {prompt_path}. Using default instruction.")


def build_guidance_writer_agent(db_service: PetDBService) -> Agent:
    async def save_guidance(guidance: str) -> str:
        """Save the complete guidance to the database for future reference.
        
        CRITICAL: This tool MUST be called after providing guidance to the user. 
        The saved guidance enables future personalized responses and maintains conversation continuity.
        
        The guidance should be your complete, final response that you provided to the user.
        This includes all actionable advice, recommendations, and context.

        Args:
            guidance: The complete guidance text to save. This should be your full response 
                     that addresses the user's question with actionable pet care advice.
        
        Returns:
            Confirmation message that guidance was saved successfully.
        """
        await db_service.save(guidance)
        return "Guidance saved successfully"

    return Agent(
        name="guidance_writer_agent",
        description="Agent that provides advice and information on pet care",
        instruction=WRITER_INSTRUCTION,
        tools = [
            AgentTool(agent=guidance_researcher_agent),
            AgentTool(agent=build_instruction_provider_agent(db_service)),
            FunctionTool(func=ask_clarification),
            FunctionTool(func=save_guidance)],
        output_key="guidance",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
    )