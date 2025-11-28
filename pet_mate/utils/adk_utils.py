from google.genai import types
from settings import is_debug, is_verbose
from google.adk.runners import Runner
from state import USER_ID

retry_options = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


async def run(user_message: str, runner: Runner, session_id: str):
    if is_debug():
        events = await runner.run_debug(user_message, session_id=session_id, verbose=is_verbose())
    else:
        events = runner.run_async(
            new_message=types.Content(parts=[types.Part(text=user_message)], role="user"),
            session_id=session_id,
            user_id=USER_ID
        )

    async for event in process_events(events):
        if event and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    agent_name = getattr(event, 'author', None) or 'Unknown'
                    if is_verbose():
                        print(f"[{agent_name}]: {part.text}")
                    elif agent_name == "refiner_agent":
                        print(f"[Agent]: {part.text}")


async def process_events(events):
    """generic function to extract text from events"""
    if isinstance(events, list):
        for event in events:
            yield event
    else:
        async for event in events:
            yield event