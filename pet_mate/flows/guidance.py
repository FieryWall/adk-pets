import asyncio
from common import ClarificationNeeded
from flows import Flow, FlowAction
from state import State, APP_NAME
from agents import build_care_advisor_agent
from google.adk.runners import Runner   
from utils.adk_utils import run
from logger import log
import traceback

class GuidanceFlow(Flow):

    def __init__(self, state: State, shutdown_event: asyncio.Event):
        self.state = state
        self.shutdown_event = shutdown_event
        self.runner = None


    async def setup(self):
        care_advisor_agent = build_care_advisor_agent(self.state.db_service)
        self.runner = Runner(
            app_name=APP_NAME,
            agent=care_advisor_agent,
            session_service=self.state.session_service)


    async def run(self) -> FlowAction:
        print("[Agent]: Hello, I'm a PetMateAI! I can help you with your pet's care. How can I assist you today?")

        while not self.shutdown_event.is_set():
            user_input, action = await self._get_user_input()
            if action == FlowAction.EXIT:
                return action

            action = await self._dialogue_cycle(user_input)
            if action == FlowAction.EXIT:
                return action


    async def _dialogue_cycle(self, user_input: str) -> FlowAction:
        while not self.shutdown_event.is_set():
            try:
                await run(user_input, runner=self.runner, session=self.state.session)
                return FlowAction.CONTINUE
                
            except ClarificationNeeded as e:
                user_input, action = await self._get_user_input(f"[Agent]: {e.question}\n[User]: ")
                if action == FlowAction.EXIT:
                    return action
                
                # IMPORTANT: Feed the user's clarification back into the runner
                # This ensures the agent receives the answer to its question
                # We do NOT return FlowAction.CONTINUE here, as we want to loop back to 'await run'
                continue
                    
            except Exception as e:
                if not self.shutdown_event.is_set():
                    log(f"{e}\n{traceback.format_exc(limit=2)}")
                    print("[App]: Agent execution failed. Please try again.")
                return FlowAction.ERROR


    async def _get_user_input(self, prompt="[User]: ") -> (str, FlowAction):
        try:
            while not self.shutdown_event.is_set():
                user_input = await asyncio.to_thread(input, prompt)
                if self._is_valid_input(user_input):
                    break
                elif not self.shutdown_event.is_set():
                    print("[App] Invalid input. Please try again.")

            if self.shutdown_event.is_set():
                return None, FlowAction.EXIT

            exit_action = self._should_exit(user_input)
            return user_input, exit_action
        except KeyboardInterrupt:
            self.shutdown_event.set()
            return None, FlowAction.EXIT
        except asyncio.CancelledError:
            return None, FlowAction.EXIT
    

    def _is_valid_input(self, user_input: str) -> bool:
        return user_input and user_input.strip() != ""


    def _should_exit(self, user_input: str = None) -> FlowAction:
        if self.shutdown_event.is_set():
            return FlowAction.EXIT
        if user_input and user_input.strip() in ["exit", "quit"]:
            print("Exiting application...")
            return FlowAction.EXIT

        return FlowAction.CONTINUE


    async def cleanup(self):
        if self.runner:
            try:
                self.runner.cancel()
                await asyncio.sleep(0.1)
                await self.runner.close()
                await asyncio.sleep(0.1)
            except Exception:
                pass