"""Tool wrappers for AFC (Automatic Function Calling) compatibility.

This module is reserved for tool wrappers that need to adapt ADK tool objects
to be compatible with automatic function calling. Currently, no wrappers are
needed as the pet_db_search and ask_clarification functions are already plain
Python callables that work directly with AFC.

Note: google_search from google.adk.tools.google_search_tool is not directly
callable via AFC and has been removed from agent tool registrations. If needed,
a proper wrapper would need to interface with the ADK framework's ToolContext
and LlmRequest structures.
"""


