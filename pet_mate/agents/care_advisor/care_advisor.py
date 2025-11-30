from google.adk.agents import SequentialAgent, LoopAgent

from .reviewer import guidance_reviewer_agent
from .writer import build_guidance_writer_agent
from .refiner import refiner_agent
from pet_db_service import PetDBService


def build_care_advisor_agent(db_service: PetDBService) -> SequentialAgent:
    writer_agent = build_guidance_writer_agent(db_service)
    
    guidance_refinement_loop = LoopAgent(
        name="GuidanceRefinementLoop",
        sub_agents=[guidance_reviewer_agent, refiner_agent],
        max_iterations=3,
    )
    
    return SequentialAgent(
        name="GuidancePipeline",
        sub_agents=[writer_agent, guidance_refinement_loop],
    )