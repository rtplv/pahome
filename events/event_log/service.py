from asyncpg import Connection
from events.event_log import repository
from events.event_log.model import EventLog


async def create(ctx: Connection, created_log: EventLog):
    await repository.create(ctx, created_log)
