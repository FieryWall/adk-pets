from google.adk.sessions import InMemorySessionService

APP_NAME = "pet_mate_app"
USER_ID = "default_user"

class State:
    def __init__(self):
        self.session_service = InMemorySessionService()

    async def reset(self):
        self.session = await self.session_service.create_session(app_name=APP_NAME, user_id=USER_ID)