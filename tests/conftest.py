import asyncio

import asyncpg
import pytest
from asyncpg import Pool
from alembic import command
from alembic.config import Config

import conf
from database.functions import init_connection


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def db_pool() -> Pool:
    conf.db_pool = await asyncpg.create_pool(conf.DB_URL + "tests",
                                             min_size=conf.DB_POOL_MIN,
                                             max_size=conf.DB_POOL_MAX,
                                             init=init_connection)
    return conf.db_pool


@pytest.fixture(autouse=True)
def run_migrations():
    alembic_cfg = Config(conf.ROOT_PATH + "/alembic.ini")
    alembic_cfg.set_main_option('script_location', conf.ROOT_PATH + "/database/migrations")
    alembic_cfg.set_main_option('sqlalchemy.url', conf.DB_URL + "tests")
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")
