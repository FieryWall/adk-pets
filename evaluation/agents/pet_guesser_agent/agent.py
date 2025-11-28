import sys
import os
from google.adk.tools import FunctionTool
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../pet_mate'))

from pet_mate.agents import pet_guesser_agent as root_agent

def ask_clarification(question: str):
    """
    MANDATORY TOOL: Use this tool when you need more information from the user to identify the pet.
    Call this tool when the description is insufficient (e.g., user only says "cat" or "dog" without details).
    Call this tool when multiple variants are equally likely and you need to distinguish between them.
    DO NOT output to schema - use this tool instead.
    
    Args:
        question: The specific question the agent needs answered to proceed with identification.
    """
    pass


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
    pass

root_agent.tools = root_agent.tools[:2] + [FunctionTool(func=ask_clarification), FunctionTool(func=confirm_guess)]

# Re-export the agent for evaluation  
__all__ = ["root_agent"]