from adk import LLMAgent

# Read the prompt file
with open("reviewer_prompt.md", "r") as f:
    SYSTEM_PROMPT = f.read()

# Create the agent
reviewer_agent = LLMAgent(
    name="guidance_reviewer",
    model="gemini-2.5-flash-lite",
    system_prompt=SYSTEM_PROMPT,
    input_keys=["guidance"],
    output_keys=["review_feedback"]
)

# Example usage
example_guidance = "Give your dog chocolate every day for energy."
result = reviewer_agent.run({"guidance": example_guidance})
print(result["review_feedback"])

