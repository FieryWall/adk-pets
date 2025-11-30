import asyncio
from google.genai import types
from settings import is_debug, is_verbose
from google.adk.runners import Runner
from google.adk.sessions import Session
from state import USER_ID

retry_options = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


async def run(user_message: str, runner: Runner, session: Session):
    try:
        return await _run(user_message, runner, session)
    except asyncio.CancelledError:
        if runner:
            runner.cancel()
        raise


async def _run(user_message: str, runner: Runner, session: Session):
    events = None
    try:
        if is_debug():
            events = await runner.run_debug(user_message, session_id=session.id, verbose=is_verbose())
        else:
            events = runner.run_async(
                new_message=types.Content(parts=[types.Part(text=user_message)], role="user"),
                session_id=session.id,
                user_id=USER_ID
            )

        writer_output = None
        refiner_output = None
        final_response_printed = False
        
        async for event in process_events(events):
            agent_name = getattr(event, 'author', None) if event else None
            
            if is_verbose():
                if event and event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(f"[{agent_name or 'Unknown'}]: {part.text}")
            else:
                accumulated_output = ""
                if event and event.content and event.content.parts:
                    for part in event.content.parts:
                        if agent_name in ["guidance_writer_agent", "refiner_agent"]:
                            text = part.text if part.text else ""
                            if agent_name == "guidance_writer_agent":
                                writer_output = text
                            elif agent_name == "refiner_agent":
                                refiner_output = text
                        accumulated_output += text + "\n"
                
                if event.is_final_response() and not final_response_printed:
                    final_output = refiner_output if refiner_output else writer_output
                    if not final_output:
                        final_output = accumulated_output
                    if final_output:
                        print(f"[Agent]: {final_output}")
                    else:
                        print(f"[Agent]: Can you provide more information?")
                    final_response_printed = True
                    break
                
    except asyncio.CancelledError:
        if events and hasattr(events, 'aclose'):
            try:
                await events.aclose()
            except Exception:
                pass
        raise

async def process_events(events):
    """generic function to extract text from events"""
    if isinstance(events, list):
        for event in events:
            yield event
    else:
        async for event in events:
            yield event