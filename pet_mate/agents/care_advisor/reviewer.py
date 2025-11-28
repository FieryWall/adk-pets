from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
import os
from utils.adk_utils import retry_options
from settings import current_model
# Load reviewer instruction from external file if available
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../reviewer_prompt.md")
    with open(prompt_path, "r") as file:
        REVIEWER_INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Reviewer prompt file not found at {prompt_path}.")

guidance_reviewer_agent = Agent(
    name="guidance_reviewer",
    model= Gemini(
        model=current_model(),
        retry_options=retry_options,
    ),
    instruction=REVIEWER_INSTRUCTION,
    output_key="review_feedback", # This is the final output of the guidance review

)