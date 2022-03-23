import pytest
from events.event_log import repository
from asyncpg import Pool

from events.event_log.model import EventLog
from tests.events.stub import event_log_stub


@pytest.mark.asyncio
async def test_create(db_pool: Pool):
    async with db_pool.acquire() as ctx:
        stub = event_log_stub(body={"type": "event"})

        await repository.create(ctx, stub)
        row = await ctx.fetchrow(
            "SELECT * FROM event_log WHERE ieee_address = $1",
            stub.ieee_address
        )
        result: EventLog = EventLog.parse_obj(row)

        assert result is not None
        assert result.ieee_address == stub.ieee_address
        assert all(map(lambda k: k in result.body and result.body[k] == stub.body[k], stub.body.keys()))