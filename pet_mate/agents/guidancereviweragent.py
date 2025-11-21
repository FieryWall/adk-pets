from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.prompts import Prompt
import json
from typing import Dict, Any
import yaml
import os

def _load_agent_config(filepath: str) -> Dict[str, Any]:
    """
    Helper function to securely load the agent configuration from a structured YAML file.
    """
    try:
        # Assumes the YAML file is in the current working directory
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Agent YAML file not found at {filepath}. Cannot create agent.")
        return {}
    except Exception as e:
        print(f"Error loading YAML file: {e}")
        return {}


def create_guidance_reviewer_agent(yaml_filepath: str = 'reviewer_agent.yaml') -> LlmAgent | None:
    """
    Creates and configures the Guidance Reviewer LlmAgent by reading its system 
    instructions and configuration from the external YAML file.
    
    Args:
        yaml_filepath: The path to the YAML file containing the agent definition.
        
    Returns:
        An LlmAgent instance configured for review, or None if configuration fails.
    """
    
    config = _load_agent_config(yaml_filepath)
    if not config:
        return None

    # Retrieve the system instruction text from the loaded configuration
    system_instruction_text = config.get('system_instructions', '')
    
    # Define the strict JSON schema required for the LLM output
    json_schema = {
        "type": "OBJECT",
        "properties": {
            # Based on your YAML output requirements:
            "reviewer_agent": {"type": "STRING", "description": "Name of the agent (Guidance Reviewer)."},
            "review_status": {"type": "STRING", "enum": ["PASS", "FAIL"], "description": "Overall status of the advice."},
            "failed_criteria": {"type": "ARRAY", "items": {"type": "STRING"}, "description": "List of failed criteria IDs (C1, C2, etc.)."},
            "reasoning_summary": {"type": "STRING", "description": "A brief explanation of the decision."},
            "revision_instructions": {"type": "STRING", "description": "Explicit steps to fix the advice if status is FAIL."}
        }
    }
    
    # Instantiate the LlmAgent using the loaded prompt and the ADK functions
    try:
        reviewer_agent = LlmAgent(
            model=Gemini.GEMINI_FLASH, # Use the ADK reference for Gemini Flash
            system_instruction=Prompt(system_instruction_text),
            config={
                # Force the model to output a parsable JSON object
                "response_mime_type": "application/json",
                "response_schema": json_schema
            }
        )
        return reviewer_agent
    except Exception as e:
        print(f"Failed to instantiate LlmAgent: {e}")
        return None