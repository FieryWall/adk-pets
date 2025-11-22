"""
Proxy agent module for guidance reviewer agent evaluation.
This module exposes the guidance reviewer agent for ADK evaluation.
"""

from google.adk.agents import Agent

# Direct agent definition for evaluation - avoids complex import paths
guidance_reviewer_agent = Agent(
    name="guidance_reviewer",
    description="Agent that reviews and provides feedback on pet care guidance",
    instruction="""You are an expert pet care guidance reviewer that evaluates pet care advice for accuracy, safety, and completeness.

    You will receive pet care guidance to review. Evaluate the guidance based on:
    - Accuracy: Is the advice medically and behaviorally sound?
    - Safety: Does it avoid dangerous recommendations (especially toxic medications)?
    - Completeness: Does it provide sufficient detail and context?
    - Emergency awareness: Does it appropriately recommend veterinary care when needed?

    If the guidance is accurate, safe, complete, and appropriate, respond with 'APPROVED'.
    Otherwise, provide specific constructive feedback explaining what needs improvement, focusing on safety concerns, missing information, or inaccuracies.""",
    output_key="review_feedback",
    model="gemini-2.5-flash-lite",
    tools=[]  # No tools needed for direct evaluation responses
)

# Export for ADK eval
agent = guidance_reviewer_agent
root_agent = guidance_reviewer_agent

# Ensure no other agents are accessible
__all__ = ['agent', 'root_agent']