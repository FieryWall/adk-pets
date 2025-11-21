import os
import json
from google.adk.agents import Agent, SequentialAgent, LoopAgent
from google.adk.tools import FunctionTool
from google import genai
from google.genai import types

from .instruction_provider import get_core_care_instructions
from .reviewer import guidance_reviewer_agent
from .writer import guidance_writer_agent


# [TODO] This is a placeholder agents definition. Update as needed!
# reference: https://www.kaggle.com/code/kaggle5daysofai/day-1b-agent-architectures
#    """Call this function ONLY when the guidance is 'APPROVED', indicating the story is finished and no more changes are needed."""
#    return {"status": "approved", "message": "guidance approved. Exiting refinement loop."}

#refiner_agent = Agent(
#    name="RefinerAgent",
#    model="gemini-2.5-flash-lite",
#    instruction="""You are a guidance refiner. You have a guidance draft and review on this guidance.
#
#    Guidance Draft: {guidance}
#    Guidance Review: {review_feedback}
#
#    Your task is to analyze the guidance.
#    - IF the guidance is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
#    - OTHERWISE, rewrite the guidance draft to fully incorporate the feedback from the guidance.""",
#
#    output_key="current_guidance",
#    tools=[FunctionTool(exit_loop)]
#)



#guidance_refinement_loop = LoopAgent(
#    name="StoryRefinementLoop",
#    sub_agents=[guidance_reviewer_agent, refiner_agent],
#    max_iterations=2,
#)


#care_advisor_agent = SequentialAgent(
#    name="StoryPipeline",
#    sub_agents=[guidance_writer_agent, guidance_refinement_loop],
#)

# --- 2. Parent Agent Simulation: Care Advisor ---

def care_advisor_agent(user_prompt: str):
    """
    The Care Advisor agent (Parent Agent). 
    
    It uses the Gemini model and is guided by a system instruction to provide 
    accurate, high-level guidance. It decides whether to use the 
    'Instruction Provider' subagent (Tool) to gather specific core knowledge.
    """
    print(f"--- Care Advisor Agent Activated ---")
    print(f"User Query: {user_prompt}\n")

    # Initialize the client
    # The API key is typically loaded from the environment variable GEMINI_API_KEY
    try:
        client = genai.Client()
    except Exception as e:
        print("Error initializing Gemini Client. Ensure the GEMINI_API_KEY environment variable is set.")
        print(f"Details: {e}")
        return

    # System instruction for the Care Advisor agent
    system_instruction = (
        "You are the Care Advisor, a compassionate and highly accurate parent agent "
        "for pet care. Your primary goal is to provide specific, accurate, and "
        "actionable guidance based on the user's described situation. "
        "ALWAYS use the provided tools (the Instruction Provider subagent) "
        "if the user's query relates to core care or standard emergency protocols "
        "for dogs or cats to integrate that foundational knowledge into your response."
    )

    # 1. Initial request to the Gemini model
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[get_core_care_instructions] # Register the subagent function as a tool
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', # Or a similar model
        contents=[user_prompt],
        config=config,
    )

    # --- Tool/Subagent Execution Loop (Handles the delegation) ---
    
    while response.function_calls:
        function_call = response.function_calls[0]
        func_name = function_call.name
        func_args = dict(function_call.args)
        
        print(f"🤖 Care Advisor detected need for Subagent...")
        print(f"    -> Calling Instruction Provider (Tool): {func_name}")
        print(f"    -> Arguments: {func_args}\n")

        # Execute the function that simulates the subagent
        if func_name == "get_core_care_instructions":
            tool_output = get_core_care_instructions(**func_args)
        else:
            tool_output = f"Error: Unknown function requested: {func_name}"

        print(f"✅ Instruction Provider (Subagent) returned:\n{tool_output}\n")
        
        # 2. Send the tool's output back to the model for final answer generation
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                user_prompt,
                types.Content(
                    role="model", 
                    parts=[types.Part.from_function_call(function_call)]
                ),
                types.Content(
                    role="tool", 
                    parts=[types.Part.from_function_response(
                        name=func_name, 
                        response={"result": tool_output}
                    )]
                )
            ],
            config=config,
        )

    # --- Final Output ---
    print("--- Final Care Advisor Guidance ---")
    print(response.text)
    print("-----------------------------------")

    if __name__ == "__main__":
    # Ensure you have the API key set in your environment:
    # export GEMINI_API_KEY="YOUR_API_KEY"

    # Example 1: Query that requires core instruction retrieval (Dog Diet)
        care_advisor_agent("My puppy is 10 weeks old. What are the general feeding guidelines and are there any human foods I must never give my dog?")
    
    print("\n" + "="*80 + "\n")

    # Example 2: Query that requires core instruction retrieval (Cat Emergency)
    care_advisor_agent("I think my male cat hasn't peed all day and seems very lethargic. What should I do right now?")

    print("\n" + "="*80 + "\n")
    
    # Example 3: Query that does not necessarily require the tool (General behavior advice)
    care_advisor_agent("How do I help my dog stop barking at the mailman? Should I use punishment?")

    print("\nNote: This is a simulation. To run this, you need the google-genai library installed ('pip install google-genai') and your GEMINI_API_KEY environment variable set.")