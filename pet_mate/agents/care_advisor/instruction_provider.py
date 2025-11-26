from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from pet_mate.utils.adk_utils import retry_options
import os
from ..pet_db_service import pet_db_search, pet_db_service
import asyncio
from typing import List

# session is just a class with an array - 
# Define DummySession locally for testing data insertion
class DummySession:
    def __init__(self, messages: List[str] = None):
        self.messages = messages or []
        # ADK Message objects typically have a 'text' attribute, but a simple list of strings works with SQLiteMemoryService
        # If using real ADK messages, they would have a 'text' property.

# Function to pre-populate the database with some example pet care instructions
async def add_initial_data_if_empty():
    """Adds initial sample data to the DB if no entries exist."""
    print("Checking for existing database entries...")
    # Use a generic query to check if any data exists
    check_results = await pet_db_service.search_memory("care", top_k=1)
    
    if check_results:
        print(f"Database contains {len(check_results)} existing entries. Skipping initial data addition.")
        return

    print("Adding sample pet care instructions to the database...")
    
    sample_instructions = [
        "Dog care: Ensure your Labrador gets at least 60 minutes of vigorous exercise daily to maintain joint health and prevent obesity. Check paws daily for cuts.",
        "Cat care: A 10-year-old Siamese cat must have a checkup every 6 months, not just yearly, to monitor kidney function. Feed low-phosphorus wet food.",
        "Hamster care: If a Syrian hamster has wet tail symptoms (diarrhea and lethargy), isolate immediately and seek vet care. Keep cage dry and clean.",
        "Parrot care: African Grey parrots require a consistent diet of pellets, fresh fruits, and vegetables (avoid avocado and chocolate, which are toxic). Provide at least 4 hours of social interaction daily.",
        "General advice: Always use pet-safe cleaners around your house, as common household chemicals can be fatal if ingested or inhaled by pets."
    ]

    # The SQLiteMemoryService expects a session-like object with a 'messages' attribute
    dummy_session = DummySession(messages=sample_instructions)
    
    try:
        session_id = await pet_db_service.add_session_to_memory(dummy_session)
        print(f"Successfully added initial data in session ID: {session_id}")
    except Exception as e:
        print(f"Error adding initial data: {e}")

# Call the function to ensure data exists when the agent runs
asyncio.run(add_initial_data_if_empty())
print("Initial data check and addition complete.")

# --- 1. Instruction Provider Agent (The Agent) ---

# Try to read prompt file
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "../instruction_provider_prompt.md")
    with open(prompt_path, "r") as file:
        INSTRUCTION_PROVIDER = file.read()
except FileNotFoundError:
    # Fallback in case pathing is wrong in the execution environment
    INSTRUCTION_PROVIDER = "You are a specialized search assistant for pet care instructions. Use the provided `pet_db_search_tool` to find information based on the user's query."
print(f"Instruction Provider prompt loaded. Length: {len(INSTRUCTION_PROVIDER)} characters.")


# Instruction Provider Agent Definition
instruction_provider_agent = Agent(
    name="instruction_provider_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
    description="Searches for pet care instructions from a specialized pet care database",
    instruction=INSTRUCTION_PROVIDER,
    output_key="care_instructions",
    # Register the raw pet_db_search callable so the model can call the DB directly via AFC.
    tools=[pet_db_search],
)
print(f"Instruction Provider Agent defined with name: {instruction_provider_agent.name}")
