from google.adk.tools import BaseTool
from google.adk.memory import BaseMemoryService
from google.adk.sessions import Session

# --- Custom Tool Definition ---
class MemoryIngestionTool(BaseTool):
    """
    A custom tool that allows the Agent to explicitly save a completed 
    session's content into the MemoryService (Long-Term Memory).
    """
    
    # Tool Name: Used by the LLM when deciding which tool to call.
    name: str = "save_session_to_memory"
    
    # Tool Description: Crucial for the LLM's understanding of the tool's purpose.
    description: str = "Saves the current session's entire history and context into long-term memory for future recall."

    # Dependencies: This tool needs access to the MemoryService.
    # The Runner will inject this dependency when the tool is initialized.
    dependencies = [BaseMemoryService]

    def __init__(self, memory_service: BaseMemoryService):
        """Initializes the tool with the MemoryService provided by the Runner."""
        self.memory_service = memory_service

    # The method the LLM calls. It must have standard type hints for the LLM to understand the arguments.
    async def save_session_to_memory(self, session: Session) -> str:
        """
        The utility function that performs the memory ingestion.

        Args:
            session: The completed session object to be archived.
        Returns:
            A string confirmation message.
        """
        if not session or not session.messages:
            return "Error: Session is empty or not provided. Nothing saved."
            
        # The core logic from your original 'main' function:
        await self.memory_service.add_session_to_memory(session)
        
        return f"Successfully archived {len(session.messages)} messages into long-term memory."


class MemoryRetrievalTool(BaseTool):
    """
    A tool that queries the memory service for relevant memory entries.
    Provides a simple interface to search long-term memory by a query string
    and return matching memory entries.
    """

    name: str = "query_memory"
    description: str = "Searches long-term memory for entries relevant to a query."
    dependencies = [BaseMemoryService]

    def __init__(self, memory_service: BaseMemoryService):
        self.memory_service = memory_service

    async def query_memory(self, query: str, top_k: int = 5):
        """
        Query the memory service and return up to `top_k` matching entries.

        Args:
            query (str): The natural-language query to search memory.
            top_k (int): Maximum number of results to return.

        Returns:
            list[str]: A list of string representations of matching memory entries.
        """
        if not query or not isinstance(query, str):
            return []

        # BaseMemoryService exposes `search_memory(query, top_k=...)`
        results = await self.memory_service.search_memory(query, top_k=top_k)

        # `results` may be a list of memory_entry objects; convert to readable strings
        entries = []
        for r in results or []:
            # try common attributes, fall back to str()
            text = None
            if hasattr(r, 'text'):
                text = r.text
            elif hasattr(r, 'content'):
                text = r.content
            elif hasattr(r, 'metadata'):
                text = str(r.metadata)
            else:
                text = str(r)
            entries.append(text)

        return entries