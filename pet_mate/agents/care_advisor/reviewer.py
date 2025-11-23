from google.adk.agents import Agent

# Define the system instruction separately for readability
REVIEWER_INSTRUCTION = """
You are an expert pet care guidance reviewer that evaluates pet care advice for accuracy, safety, and completeness.

You will receive pet care guidance to review. Evaluate the guidance based on:
- Accuracy: Is the advice medically and behaviorally sound?
- Safety: Does it avoid dangerous recommendations (especially toxic medications)?
- Completeness: Does it provide sufficient detail and context?
- Emergency awareness: Does it appropriately recommend veterinary care when needed?

If the guidance is accurate, safe, complete, and appropriate, respond with 'APPROVED'.
Otherwise, provide specific constructive feedback explaining what needs improvement, focusing on safety concerns, missing information, or inaccuracies.
Keep responses SHORT and CONCISE - provide essential guidance without excessive detail
"""

# Creating the functional agent instance
guidance_reviewer_agent = Agent(
    name="guidance_reviewer",
    description="Agent that reviews and provides feedback on pet care guidance",
    instruction=REVIEWER_INSTRUCTION, # Using 'instruction' as per your example
    
    # Adding 'input_key' to define the required input variable name for the .run() method
    #input_key="guidance", 
    
    output_key="review_feedback", # Using 'output_key' as per your example
    model="gemini-2.5-flash-lite"
)

# -----------------------------------------------------------
# Instance Verification
# -----------------------------------------------------------

print(f"Agent instance created: **{guidance_reviewer_agent.name}**")
print(f"Agent description: {guidance_reviewer_agent.description}")
print(f"Model used: {guidance_reviewer_agent.model}")

# --- Example Usage (Conceptual) ---
# --- Execution Block ---
if __name__ == "__main__":
    
    # 1. Define the guidance you want the agent to review
    example_guidance = "If your dog is having a severe allergic reaction, give it a human Benadryl tablet and wait 30 minutes for symptoms to subside."
    
    print("\n--- Reviewing Guidance ---")
    print(f"Input Guidance: \"{example_guidance}\"")
    
    # 2. Execute the agent's run method (This triggers the ADK and LLM call)
    result = guidance_reviewer_agent.run(prompt=example_guidance)
    
    print("\nReview Result:")
    
    # 3. Print the output
    print(result["review_feedback"])