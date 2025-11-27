from google.genai import types
from logger import is_verbose
from google.adk.runners import Runner
from state import USER_ID

retry_options = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


async def run(user_message: str, runner: Runner, session_id: str):
    if is_verbose():
        debug_result = await runner.run_debug(user_message, session_id=session_id)
        print(debug_result)
        
        should_stop = False
        if hasattr(debug_result, "events"):
             for event in debug_result.events:
                if hasattr(event, "metadata") and event.metadata.get("stop_conversation"):
                    should_stop = True
                    break
        return should_stop
    else:
        events_async = runner.run_async(
            new_message=types.Content(parts=[types.Part(text=user_message)], role="user"),
            session_id=session_id, 
            user_id=USER_ID
        )
        
        full_response = []
        should_stop = False
        async for event in events_async:
            if hasattr(event, "metadata") and event.metadata.get("stop_conversation"):
                should_stop = True

            if event and event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        full_response.append(part.text)
        
        print(f"[Agent]: {''.join(full_response)}")
        return should_stop