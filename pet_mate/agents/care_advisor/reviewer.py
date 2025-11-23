from adk import LLMAgent

# Read the prompt file
with open("reviewer_prompt.md", "r") as f:
    SYSTEM_PROMPT = f.read()

# Create the agent
reviewer_agent = LLMAgent(
    name="guidance_reviewer",
<<<<<<< HEAD
    model="gemini-2.5-flash-lite",
    system_prompt=SYSTEM_PROMPT,
    input_keys=["guidance"],
    output_keys=["review_feedback"]
)

# Example usage
example_guidance = "Give your dog chocolate every day for energy."
result = reviewer_agent.run({"guidance": example_guidance})
print(result["review_feedback"])

=======
    description="Agent that reviews and provides feedback on pet care guidance",
    instruction="""You are an expert pet care guidance reviewer that evaluates pet care advice for accuracy, safety, and completeness.

    You will receive pet care guidance to review. Evaluate the guidance based on:
    - Accuracy: Is the advice medically and behaviorally sound?
    - Safety: Does it avoid dangerous recommendations (especially toxic medications)?
    - Completeness: Does it provide sufficient detail and context?
    - Emergency awareness: Does it appropriately recommend veterinary care when needed?

    If the guidance is accurate, safe, complete, and appropriate, respond with 'APPROVED'.
    Otherwise, provide specific constructive feedback explaining what needs improvement, focusing on safety concerns, missing information, or inaccuracies.
    Keep responses SHORT and CONCISE - provide essential guidance without excessive detail""",
    output_key="review_feedback",
    model="gemini-2.5-flash-lite"
)
>>>>>>> origin/main
