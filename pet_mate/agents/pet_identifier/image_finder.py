import os
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.models.google_llm import Gemini
from utils.adk_utils import retry_options


try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../image_finder_prompt.md")
    with open(prompt_path, "r") as file:
        INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Image finder prompt file not found at {prompt_path}. Using default instruction.")


image_finder_agent = Agent(
    name="image_finder_agent",
    description="A specialist agent that searches the web for a photo of a specified pet.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
    instruction=INSTRUCTION,
    tools=[google_search],
    output_key="pet_image_url"
)