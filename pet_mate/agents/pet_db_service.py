import os
from pet_mate.utils.sqlite_memory import SQLiteMemoryService, get_memory_service
from typing import List, Dict, Any, Optional
import json

# --- Database Service Initialization ---
# The path to the SQLite database file. It will be created if it doesn't exist.
# We place it in the project root for persistence across runs.
# We use get_memory_service, which wraps SQLiteMemoryService.
# Since this service is used as a tool, we will use a dummy file path if 
# the environment doesn't provide one, although in a real ADK setup, 
# you might manage this database persistence differently.

# Ensure the database file is placed relative to the run location
DB_PATH = os.path.join(os.getcwd(), ".pet_care_instructions.db")
try:
    # Initialize the memory service for persistence
    # Use 'sqlite' kind which utilizes SQLiteMemoryService
    pet_db_service = get_memory_service(kind="sqlite", db_path=DB_PATH)
except Exception as e:
    # Handle case where get_memory_service might not be fully defined or working
    print(f"Warning: Could not initialize SQLiteMemoryService. Using in-memory fallback. Error: {e}")
    pet_db_service = get_memory_service(kind="memory")
print(f"Pet DB Service initialized with DB path: {DB_PATH} ")

# --- Pet Database Search Tool Definition ---
# This function is what the LLM agent will call.
async def pet_db_search(query: str, top_k: int = 5) -> str:
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
    if not query:
        return json.dumps({"status": "error", "message": "Search query cannot be empty."})

    # The SQLiteMemoryService returns a list of _Res objects, 
    # where each object has a '.text' attribute.
    results = await pet_db_service.search_memory(query, top_k)
    
    # Convert the results into a list of strings (the content) for the LLM
    search_results = [res.text for res in results]
    print(f"Pet query results: {search_results}")
  
    if not search_results:
        return json.dumps({"status": "success", "results": [], "message": f"No instructions found for query: '{query}'"})
    
    # Return the results as a JSON string for structured consumption by the LLM
    return json.dumps({"status": "success", "results": search_results})

print(f"Pet DB Search Tool initialized.")

# Define the ADK Tool object
pet_db_search_tool = pet_db_search
print(f"Pet DB Search Tool defined as raw callable.")
