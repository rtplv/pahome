from unittest.mock import patch

from asyncpg import Pool

from events.event_log import service
import pytest

from tests.events.stub import event_log_stub


@pytest.mark.asyncio
async def test_create(db_pool: Pool):
    with patch('events.event_log.repository.create') as repo_m:
        async with db_pool.acquire() as ctx:
            await service.create(ctx, event_log_stub())
            assert repo_m.called is True
