from google.adk.agents import SequentialAgent
from .profile_writer import profile_writer_agent

pet_profile_generator_agent = SequentialAgent(
    name="pet_profile_generator",
    sub_agents=[profile_writer_agent]
)