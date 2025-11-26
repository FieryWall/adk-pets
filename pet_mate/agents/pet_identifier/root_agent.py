from google.adk.agents import SequentialAgent
from .relevance_checker import relevance_checker_agent
from .guesser import pet_guesser_agent


pet_identifier_agent = SequentialAgent(
    name="PetIdentificationPipline",
    sub_agents=[relevance_checker_agent, pet_guesser_agent]
)