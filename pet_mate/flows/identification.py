import asyncio
from common import ClarificationNeeded, GuessConfirmationNeeded
from flows import Flow, FlowAction
from state import State, APP_NAME
from utils.adk_utils import run
from google.adk.runners import Runner
from agents.pet_identifier import pet_identifier_agent
from agents.profile_generator import build_pet_profile_generator_agent

class IdentificationFlow(Flow):

    # Constructor
    def __init__(self, state: State):
        self.state = state
        

    async def setup(self):
        pass


    async def run(self) -> FlowAction:
        action = await self.identify_pet()
        if action == FlowAction.BREAK:
            return action

        return await self.generate_pet_profile()


    async def identify_pet(self) -> FlowAction:
        user_input = await asyncio.to_thread(input, "[Agent]: This is the Pet Mate AI. Please, describe your pet for identification.\n[User]: ")

        pet_identifier_runner = Runner(
            app_name=APP_NAME,
            agent=pet_identifier_agent,
            session_service=self.state.session_service)
        
        while True:
            if user_input.strip() in ["exit", "quit"]:
                return FlowAction.BREAK

            try:
                await run(user_input, runner=pet_identifier_runner, session_id=self.state.session.id)
                break

            except ClarificationNeeded as e:
                # ask for clarification - continue the orchestration
                user_input = await asyncio.to_thread(input, f"[Agent]: {e.question}\n[User]: ")
            
            except GuessConfirmationNeeded as e:
                # ask for confirmation of the guess - let the agent interpret the response
                user_input = await asyncio.to_thread(
                    input, 
                    f"[Agent]: {e.question}\n[User]: "
                )
        
        return FlowAction.CONTINUE

    async def generate_pet_profile(self) -> FlowAction:
        generate_pet_profile_runner = Runner(
            app_name=APP_NAME,
            agent=build_pet_profile_generator_agent(self.state.db_service),
            session_service=self.state.session_service)
        
        await run("generate pet profile", runner=generate_pet_profile_runner, session_id=self.state.session.id)
        return FlowAction.CONTINUE