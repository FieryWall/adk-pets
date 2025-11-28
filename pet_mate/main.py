import asyncio
import os
from settings import parse_args
from logger import setup_logger

from flows import FlowAction
from state import State
from flows import GuidanceFlow, IdentificationFlow

async def start():
    # check GOOGLE_API_KEY
    if "GOOGLE_API_KEY" not in os.environ:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return

    parse_args()
    setup_logger()
    
    # Initialize application state
    state = State()
    await state.reset() # reset state to initial values

    # --------------------- Identification Flow ---------------------
    identification_flow = IdentificationFlow(state)
    await identification_flow.setup()
    action = await identification_flow.run()
    if action == FlowAction.BREAK:
        print("Exiting app")
        return

    # --------------------- Guidance Flow --------------------- 
    guidance_flow = GuidanceFlow(state)
    await guidance_flow.setup()
    action = await guidance_flow.run()
    if action == FlowAction.BREAK:
        print("Exiting app")


if __name__ == "__main__":
    asyncio.run(start())