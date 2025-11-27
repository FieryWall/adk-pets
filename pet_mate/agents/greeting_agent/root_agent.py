from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from utils.adk_utils import retry_options
import os
from google.adk.runners import Runner
from state import APP_NAME, State


try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../greeting_prompt.md")
    with open(prompt_path, "r") as file:
        INSTRUCTION = file.read()
except FileNotFoundError:
    raise Exception(f"Greeting prompt file not found at {prompt_path}.")
    

def build_greeting_runner(state: State) -> Agent:
    agent = Agent(
        name="greeting_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
        description="A greeting agent that greets the user",
        instruction=INSTRUCTION,
        output_key="greeting",
        tools=[state.db_service.pet_db_search],
    )

    return Runner(
        app_name=APP_NAME,
        agent=agent,
        session_service=state.session_service)