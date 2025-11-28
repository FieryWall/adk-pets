import asyncio
from common import ClarificationNeeded
from flows import Flow
from state import State, APP_NAME
from agents import build_care_advisor_agent
from google.adk.runners import Runner
import google.genai.types as types
from utils.adk_utils import run

class GuidanceFlow(Flow):

    # Constructor
    def __init__(self, state: State):
        self.state = state


    async def setup(self):
        care_advisor_agent = build_care_advisor_agent(self.state.db_service)
        self.runner = Runner(
            app_name=APP_NAME,
            agent=care_advisor_agent,
            session_service=self.state.session_service)
        

    async def run(self):
        print("[Agent]: Hello, I'm a Pet Mate AI! I can help you with your pet's care. How can I assist you today?")

        while True:
            user_input = await asyncio.to_thread(input, "[User]: ")

            while True:
                if user_input.strip() in ["exit", "quit"]:
                    print("Exiting application...")
                    return

                try:
                    await run(user_input, runner=self.runner, session_id=self.state.session.id)
                    break

                except ClarificationNeeded as e:
                    user_input = await asyncio.to_thread(input, f"[Agent]: {e.question}\n[User]: ")