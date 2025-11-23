from google.adk.agents import Agent

# --- 1. Define the System Prompt/Instructions ---
# This is the 'instructions' block from YAML configuration
INSTRUCTION = """
You are the Guidance Reviewer.
Your task is to review the provided guidance and evaluate its accuracy and relevance.

Evaluation rules:
- If the guidance is accurate AND relevant, respond only with:
  APPROVED
- Otherwise, provide constructive feedback explaining:
  * what is inaccurate or irrelevant
  * how the guidance can be improved

Your output must always be a plain string.
Do not output JSON, headings, lists, or any formatting.
Keep the feedback concise and focused.
"""

# --- 2. Create the Agent Instance ---
reviewer_agent = Agent(
    name="guidance_reviewer",
    model="gemini-2.5-flash-lite",  # Matching the model specified in the YAML
    sinstruction=INSTRUCTION,
    input_keys=["guidance"],       # Matching the 'inputs' name
    output_keys=["review_feedback"] # Matching the 'outputs' name
)

# --- 3. Example Usage (Reviewing guidance to boil water faster) ---
if __name__ == "__main__":
    example_guidance = "To boil water faster, cover the pot with a lid."

    print(f"--- Reviewing Guidance: '{example_guidance}' ---")
    
    # Run the agent with the example guidance
    result = reviewer_agent.run({"guidance": example_guidance})

    print("\nReview Result:")
    # The output key 'review_feedback' contains the agent's response
    print(result["review_feedback"])