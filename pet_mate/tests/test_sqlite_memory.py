import pytest
from pet_mate.utils.sqlite_memory import SQLiteMemoryService


class DummySession:
    def __init__(self, messages=None):
        self.messages = messages or []


@pytest.mark.asyncio
async def test_add_and_search(tmp_path):
    db_file = tmp_path / "mem.db"
    service = SQLiteMemoryService(db_path=str(db_file))

    session = DummySession(messages=["hello world", "another message"])
    sid = await service.add_session_to_memory(session)
    assert isinstance(sid, int)

    results = await service.search_memory("hello", top_k=5)
    assert len(results) >= 1
    assert any("hello world" in r.text for r in results)


@pytest.mark.asyncio
async def test_search_empty_query(tmp_path):
    db_file = tmp_path / "mem2.db"
    service = SQLiteMemoryService(db_path=str(db_file))
    
    # Test empty query on empty database
    results = await service.search_memory("")
    assert results == []
    
    # Add some data to the database
    session = DummySession(messages=["test message", "another test"])
    sid = await service.add_session_to_memory(session)
    assert isinstance(sid, int)
    
    # Test empty query on populated database - should still return empty
    results = await service.search_memory("")
    assert results == []
    
    # Verify that a non-empty query works correctly
    results = await service.search_memory("test")
    assert len(results) >= 1
    assert any("test message" in r.text or "another test" in r.text for r in results)
