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
    debug_result = await runner.run_debug(user_message, session_id=session_id, verbose=is_verbose())
    return debug_result