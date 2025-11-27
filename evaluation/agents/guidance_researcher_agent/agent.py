import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../pet_mate'))

from pet_mate.agents import guidance_researcher_agent as root_agent

# Re-export the agent for evaluation  
__all__ = ["guidance_researcher_agent", "root_agent"]