import asyncio

import pytest
from databases import Database
from alembic import command
from alembic.config import Config

import conf


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def db() -> Database:
    db = Database(conf.DB_URL + "tests", min_size=1, max_size=5)
    await db.connect()
    conf.db = db
    return db


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    alembic_cfg = Config(conf.ROOT_PATH + "/alembic.ini")
    alembic_cfg.set_main_option('script_location', conf.ROOT_PATH + "/migrations")
    alembic_cfg.set_main_option('sqlalchemy.url', conf.DB_URL + "tests")
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")
