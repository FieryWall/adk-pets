from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
import os
from logger import log

# Load reviewer instruction from external file if available
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../reviewer_prompt.md")
    with open(prompt_path, "r") as file:
        REVIEWER_INSTRUCTION = file.read()
except FileNotFoundError:
    print(f"Reviewer prompt file not found at {prompt_path}. Using default instruction.")

guidance_reviewer_agent = Agent(
    name="guidance_reviewer",
    model= Gemini(
        model_name="gemini-2.5-flash-lite",
    ),
    instruction=REVIEWER_INSTRUCTION,
    output_key="review_feedback",
)