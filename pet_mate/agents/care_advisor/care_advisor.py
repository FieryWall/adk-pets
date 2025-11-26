from google.adk.agents import Agent, SequentialAgent, LoopAgent
# No FunctionTool wrappers used; use raw callables for AFC.

from .reviewer import guidance_reviewer_agent
from .writer import guidance_writer_agent


# [TODO] This is a placeholder agents definition. Update as needed!
# reference: https://www.kaggle.com/code/kaggle5daysofai/day-1b-agent-architectures
def exit_loop():
    """Call this function ONLY when the guidance is 'APPROVED', indicating the story is finished and no more changes are needed."""
    return {"status": "approved", "message": "guidance approved. Exiting refinement loop."}

refiner_agent = Agent(
    name="RefinerAgent",
    model="gemini-2.5-flash-lite",
    instruction="""You are a guidance refiner. You have a guidance draft and review on this guidance.

    Guidance Draft: {guidance}
    Guidance Review: {review_feedback}

    Your task is to analyze the guidance.
    - IF the guidance is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the guidance draft to fully incorporate the feedback from the guidance.""",

    output_key="current_guidance",
    tools=[exit_loop]
)


guidance_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[guidance_reviewer_agent, refiner_agent],
    max_iterations=2,
)


care_advisor_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[guidance_writer_agent, guidance_refinement_loop],
)