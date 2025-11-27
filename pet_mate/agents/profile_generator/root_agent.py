from google.adk.agents import SequentialAgent
from .profile_writer import build_profile_writer_agent
from pet_db_service import PetDBService


def build_pet_profile_generator_agent(db_service: PetDBService) -> SequentialAgent:
    return SequentialAgent(
        name="pet_profile_generator",
        sub_agents=[build_profile_writer_agent(db_service)]
    )