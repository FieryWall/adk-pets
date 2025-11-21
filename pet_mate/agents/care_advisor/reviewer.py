from google.adk.agents import Agent

# [TODO] This is a placeholder agent definition. Update as needed!
guidance_reviewer_agent = Agent(
    name="guidance_reviewer",
    description="Agent that reviews and provides feedback on pet care guidance",
    instruction="""You are a helpful assistant that reviews and provides feedback on pet care guidance.
    Review the guidance provided below.
    Guidance: {guidance}

    Evaluate the accuracy and relevance of the guidance.
    - If the guidance is accurate and relevant, respond with 'APPROVED'.
    - Otherwise, provide constructive feedback on how to improve it.
    """,
    output_key="review_feedback",
    model="gemini-2.5-flash-lite"
)