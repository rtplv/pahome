import asyncio

import asyncpg
import pytest
from asyncpg import Pool
from alembic import command
from alembic.config import Config

import conf


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def db_pool() -> Pool:
    db_pool = await asyncpg.create_pool(conf.DB_URL + "tests",
                                        min_size=conf.DB_POOL_MIN, max_size=conf.DB_POOL_MAX)
    return db_pool


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    alembic_cfg = Config(conf.ROOT_PATH + "/alembic.ini")
    alembic_cfg.set_main_option('script_location', conf.ROOT_PATH + "/migrations")
    alembic_cfg.set_main_option('sqlalchemy.url', conf.DB_URL + "tests")
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")
