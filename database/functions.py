import json

from asyncpg import Connection


async def init_connection(conn: Connection):
    await conn.set_type_codec('json', encoder=json.dumps, decoder=json.loads, schema="pg_catalog")
    await conn.set_type_codec('jsonb', encoder=json.dumps, decoder=json.loads, schema="pg_catalog")
