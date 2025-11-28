import os
from pyclbr import Function
from utils.sqlite_memory import get_memory_service
import json
from typing import List
from settings import VERBOSE
from logger import log


# session is just a class with an array - 
# Define DummySession locally for testing data insertion
class DummySession:
    def __init__(self, messages: List[str] = None):
        self.messages = messages or []
        # ADK Message objects typically have a 'text' attribute, but a simple list of strings works with SQLiteMemoryService
        # If using real ADK messages, they would have a 'text' property.

class PetDBService:

    # --- Database Service Initialization ---
    # The path to the SQLite database file. It will be created if it doesn't exist.
    # We place it in the project root for persistence across runs.
    # We use get_memory_service, which wraps SQLiteMemoryService.
    # Since this service is used as a tool, we will use a dummy file path if 
    # the environment doesn't provide one, although in a real ADK setup, 
    # you might manage this database persistence differently.
    async def initialize(self):
        # Ensure the database file is placed relative to the run location
        DB_PATH = os.path.join(os.getcwd(), ".pet_profile.db")
        try:
            # Initialize the memory service for persistence
            # Use 'sqlite' kind which utilizes SQLiteMemoryService
            self.db = get_memory_service(kind="sqlite", db_path=DB_PATH)
        except Exception as e:
            # Handle case where get_memory_service might not be fully defined or working
            log(f"Warning: Could not initialize SQLiteMemoryService. Using in-memory fallback. Error: {e}")
            self.db = get_memory_service(kind="memory")
        log(f"Pet DB Service initialized with DB path: {DB_PATH} ")


    async def save(self, guidence: str):
        session = DummySession([guidence])
        await self.db.add_session_to_memory(session)


    # --- Pet Database Search Tool Definition ---
    # This function is what the LLM agent will call.
    async def search(self, query: str, top_k: int = 5) -> str:
        """
        Search the persistent pet care instructions database for relevant information.
        
        The database contains previously generated care instructions and notes.
        
        Args:
            query: The specific search query, which should include keywords like 
                pet species, symptoms, or previously discussed topics.
            top_k: The maximum number of results to return.

        Returns:
            A JSON string containing the search results.
        """
        # if not query:
        #     return json.dumps({"status": "error", "message": "Search query cannot be empty."})

        # The SQLiteMemoryService returns a list of _Res objects, 
        # where each object has a '.text' attribute.
        results = await self.db.search_memory(query, top_k)
        
        # Convert the results into a list of strings (the content) for the LLM
        search_results = [res.text for res in results]
        log(f"Pet query results: {search_results}")
    
        if not search_results:
            return json.dumps({"status": "success", "results": [], "message": f"No instructions found for query: '{query}'"})
        
        # Return the results as a JSON string for structured consumption by the LLM
        return json.dumps({"status": "success", "results": search_results})

