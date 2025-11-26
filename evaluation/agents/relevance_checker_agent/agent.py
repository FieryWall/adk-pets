from google.adk.tools import FunctionTool
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../pet_mate'))

from pet_mate.agents import relevance_checker_agent as root_agent

def steer_to_topic(excuse: str):
    """
    A tool the agent uses to excuse the user for not describing a pet.
    """
    pass

root_agent.tools = [FunctionTool(func=steer_to_topic)]

# Re-export the agent for evaluation  
__all__ = ["relevance_checker_agent", "root_agent"]