from google.adk.sessions import InMemorySessionService
from pet_db_service import PetDBService

APP_NAME = "pet_mate_app"
USER_ID = "default_user"

class State:
    def __init__(self):
        self.session_service = InMemorySessionService()
        self.db_service = PetDBService()

    async def reset(self):
        self.session = await self.session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
        await self.db_service.initialize()