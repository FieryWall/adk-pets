import asyncio

from abc import ABC, abstractmethod
from google.genai import types
from google.adk.agents import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from utils.adk_utils import build_retry_options

# Abstract base class for flows
class Flow(ABC):
    @abstractmethod
    async def execute(self):
        pass

APP_NAME = "EXAMPLE_APP"
USER_ID = "user_123"

# Concrete implementation of a guidance flow
class GuidanceFlow(Flow):
    async def execute(self):
        # Define the agent with specific model and instructions
        example_agent = Agent(
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=build_retry_options()),
            name="ExampleAgent",
            instruction="Answer user questions about pets."
        )

        # Initialize session service and runner
        self.session_service = InMemorySessionService()

        # Create the runner
        self.runner = Runner(
            agent=example_agent,
            app_name=APP_NAME,
            session_service=self.session_service)
        
        await self.dialogue()

    async def dialogue(self):
        # Create a new session
        session = await self.session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
        
        while True:
            # Get user input asynchronously
            user_input = await asyncio.to_thread(input, "Please describe your issue with a pet: ")
            query = types.Content(role="user", parts=[types.Part(text=user_input)])

            # Run the agent and stream responses
            async for event in self.runner.run_async(
                new_message=query,
                session_id=session.id,
                user_id=USER_ID):
                if event.is_final_response() and event.content and event.content.parts:
                    print("Agent:", event.content.parts[0].text)