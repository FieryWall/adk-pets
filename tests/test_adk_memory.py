import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from utils.adk_memory import MemoryIngestionTool, MemoryRetrievalTool

class DummySession:
	def __init__(self, messages=None):
		self.messages = messages or []

@pytest.mark.asyncio
async def test_save_session_to_memory():
	# Mock MemoryService
	mock_memory_service = MagicMock()
	mock_memory_service.add_session_to_memory = AsyncMock()

	# Create tool instance
	tool = MemoryIngestionTool(memory_service=mock_memory_service)

	# Create dummy session with messages
	session = DummySession(messages=["msg1", "msg2", "msg3"])

	# Run the async method
	result = await tool.save_session_to_memory(session)

	# Assert correct result
	assert result == "Successfully archived 3 messages into long-term memory."
	mock_memory_service.add_session_to_memory.assert_awaited_once_with(session)

@pytest.mark.asyncio
async def test_save_session_to_memory_empty():
	mock_memory_service = MagicMock()
	tool = MemoryIngestionTool(memory_service=mock_memory_service)
	session = DummySession(messages=[])
	result = await tool.save_session_to_memory(session)
	assert result == "Error: Session is empty or not provided. Nothing saved."
	mock_memory_service.add_session_to_memory.assert_not_called()


@pytest.mark.asyncio
async def test_query_memory_returns_entries():
	# Mock memory service search_memory
	mock_memory_service = MagicMock()
	# prepare fake result objects with a 'text' attribute
	class Res:
		def __init__(self, text):
			self.text = text
	mock_results = [Res("entry1"), Res("entry2")]
	mock_memory_service.search_memory = AsyncMock(return_value=mock_results)

	tool = MemoryRetrievalTool(memory_service=mock_memory_service)
	entries = await tool.query_memory("some query", top_k=2)

	assert entries == ["entry1", "entry2"]
	mock_memory_service.search_memory.assert_awaited_once_with("some query", top_k=2)


@pytest.mark.asyncio
async def test_query_memory_empty_query():
	mock_memory_service = MagicMock()
	mock_memory_service.search_memory = AsyncMock()
	tool = MemoryRetrievalTool(memory_service=mock_memory_service)
	entries = await tool.query_memory("")
	assert entries == []
	mock_memory_service.search_memory.assert_not_called()

