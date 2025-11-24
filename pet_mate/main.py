import asyncio
import os

from state import State
from flows import GuidanceFlow

async def start():
    # check GOOGLE_API_KEY
    if "GOOGLE_API_KEY" not in os.environ:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return
    
    # Initialize application state
    state = State()
    await state.reset() # reset state to initial values

    # --------------------- Identification Flow ---------------------
    # (Future implementation)

    # --------------------- Guidance Flow --------------------- 
    guidance_flow = GuidanceFlow(state)
    await guidance_flow.setup()
    await guidance_flow.run()
         

if __name__ == "__main__":
    asyncio.run(start())