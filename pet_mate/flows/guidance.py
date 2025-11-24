import asyncio
from common import ClarificationNeeded
from flows import Flow
from state import State, APP_NAME
from agents import care_advisor_agent
from google.adk.runners import Runner

class GuidanceFlow(Flow):

    # Constructor
    def __init__(self, state: State):
        self.state = state


    async def setup(self):
        self.runner = Runner(
            app_name=APP_NAME,
            agent=care_advisor_agent,
            session_service=self.state.session_service)
        

    async def run(self):
        # first user response
        user_input = await asyncio.to_thread(input, "[Agent]: How is your pet doing today?\n[User]: ")
        
        # call agent to provide guidance
        while True:
            if user_input.strip() in ["exit", "quit"]:
                print("exiting app")
                return

            try:
                await self.runner.run_debug(user_input, session_id=self.state.session.id)
                break # exit loop if successful

            except ClarificationNeeded as e:
                # ask for clarification
                user_input = await asyncio.to_thread(input, f"[Agent]: {e.question}\n[User]: ")