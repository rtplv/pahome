import json
from asyncpg import Connection
from events.event_log.model import EventLog


async def create(ctx: Connection, created_log: EventLog):
    await ctx.execute(
        "INSERT INTO event_log(ieee_address, topic, body) "
        "VALUES ($1, $2, $3)",
        created_log.ieee_address,
        created_log.topic.value,
        json.dumps(created_log.body)
    )
