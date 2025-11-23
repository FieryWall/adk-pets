import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../pet_mate'))

from pet_mate.agents import guidance_reviewer_agent

# Define root_agent for ADK Web Server
root_agent = guidance_reviewer_agent

# Re-export the agent for evaluation  
__all__ = ["guidance_reviewer_agent", "root_agent"]