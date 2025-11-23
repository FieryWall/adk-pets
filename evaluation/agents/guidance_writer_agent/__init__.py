"""
Pet care agent module for ADK eval command.
This is a standalone agent definition for evaluation only.
"""

from google.adk.agents import Agent

# Create a standalone agent definition for evaluation
# This avoids any complex imports from the main project
guidance_writer_agent = Agent(
    name="pet_care_evaluator",
    description="Agent that provides direct pet care advice for evaluation",
    instruction="""You are a helpful assistant providing pet care advice. 
    
    CRITICAL RULE: Always provide helpful, practical guidance based on the information given, even if some details are missing.
    
    When user input lacks specific details (like pet species or symptoms), provide comprehensive advice that covers common scenarios and general best practices. Include guidance on when to consult a veterinarian for serious concerns.
    
    Guidelines:
    - Offer practical, actionable advice based on available information
    - If information is limited, provide general guidance covering common scenarios
    - Include when to seek veterinary care
    - Be warm, empathetic, and professional
    - Focus on common-sense care and observation
    - NEVER ask for clarification - always provide your best advice with the information given
    - Provide direct, helpful responses in a conversational tone""",
    tools=[],  # No tools - direct responses only
    output_key="guidance",
    model="gemini-2.5-flash-lite"
)

# Export for ADK eval
agent = guidance_writer_agent
root_agent = guidance_writer_agent

# Ensure no other agents are accessible
__all__ = ['agent', 'root_agent']