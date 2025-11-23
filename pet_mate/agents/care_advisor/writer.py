from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from common import ClarificationNeeded

# [TODO] This is a placeholder agent definition. Update as needed!
def ask_clarification(question: str) -> str:
    """
    A tool the agent uses to explicitly ask the user for more information 
    to resolve a task. This function raises an exception to pause the flow.

    Args:
        question: The specific question the agent needs answered.

    Returns:
        str: The user's response (in a full ADK flow).
    """
    raise ClarificationNeeded(question)

guidance_writer_agent = Agent(
    name="care_advisor",
    description="Agent that provides advice and information on pet care",
    instruction="""You are a helpful assistant providing pet care advice. 
    
    CRITICAL RULE: You are strictly forbidden from asking any clarifying questions in your direct text response.
    
    If the user's input is ambiguous or lacks critical details (like pet species or symptoms), 
    you MUST **stop** your current thought process and call the `ask_clarification` tool. 
    The argument to the tool must be the exact, specific question you need answered to continue the guidance.""",
    tools= [FunctionTool(func=ask_clarification)],
    output_key="guidance",
    model="gemini-2.5-flash-lite"
)