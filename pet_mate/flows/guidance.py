import asyncio
from common import ClarificationNeeded
from flows import Flow
from flows.flow import FlowAction
from state import State, APP_NAME
from agents import build_care_advisor_agent, build_greeting_runner
from google.adk.runners import Runner
import google.genai.types as types
from utils.adk_utils import run

class GuidanceFlow(Flow):

    # Constructor
    def __init__(self, state: State):
        self.state = state


    async def setup(self):
        self.greeting_runner = build_greeting_runner(self.state)
        care_advisor_agent = build_care_advisor_agent(self.state.db_service)
        self.runner = Runner(
            app_name=APP_NAME,
            agent=care_advisor_agent,
            session_service=self.state.session_service)
        

    async def run(self) -> FlowAction:
        while True:
            user_input = await self.greeting()
            # call agent to provide guidance
            while True:
                if user_input.strip() in ["exit", "quit"]:
                    print("exiting app")
                    return FlowAction.BREAK

                try:
                    await run(user_input, runner=self.runner, session_id=self.state.session.id)
                    break

                except ClarificationNeeded as e:
                    # ask for clarification
                    user_input = await asyncio.to_thread(input, f"[Agent]: {e.question}\n[User]: ")

    
    async def greeting(self):
        await run(user_message="Hi!", runner=self.greeting_runner, session_id=self.state.session.id)
        return await asyncio.to_thread(input, "[User]: ")