from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

# Guidance reviewer evaluates provided care guidance for accuracy, safety, and completeness.
REVIEWER_INSTRUCTION = """
 You are an expert pet care guidance reviewer that evaluates pet care advice for accuracy, safety, and completeness.

  You will receive pet care guidance to review. Evaluate: {guidance} based on:
  - Accuracy: Is the advice medically and behaviorally sound?
  - Safety: Does it avoid dangerous recommendations (especially toxic medications)?
  - Completeness: Does it provide sufficient detail and context?
  - Emergency awareness: Does it appropriately recommend veterinary care when needed?

  If the guidance is accurate, safe, complete, and appropriate, respond with 'APPROVED'.
  Otherwise, provide specific constructive feedback explaining what needs improvement, focusing on safety concerns, missing information, or inaccuracies.
  Keep responses SHORT and CONCISE - provide essential guidance without excessive detail.
"""
guidance_reviewer_agent = Agent(
    name="guidance_reviewer",
    model= Gemini(
        model_name="gemini-2.5-flash-lite",
    ),
    instruction=REVIEWER_INSTRUCTION,
    output_key="review_feedback", # This is the final output of the guidance review

)

print(f"Agent instance created: **{guidance_reviewer_agent.name}**")
print(f"Model used: {guidance_reviewer_agent.model}")