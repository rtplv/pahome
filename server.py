import asyncpg
from fastapi import FastAPI

import conf
import events.mqtt.listener
from database.functions import init_connection

app = FastAPI()


@app.on_event("startup")
async def on_app_startup():
    # MQTT
    conf.db_pool = await asyncpg.create_pool(
        conf.DB_URL + conf.DB_DATABASE,
        min_size=conf.DB_POOL_MIN, max_size=conf.DB_POOL_MAX,
        init=init_connection
    )
    conf.mqtt.on_message = events.mqtt.listener.process_event
    await conf.mqtt.connect(conf.MQTT_HOST, int(conf.MQTT_PORT))
    events.mqtt.listener.init_subscriptions()


@app.on_event("shutdown")
async def on_app_shutdown():
    await conf.db_pool.close()
    await conf.mqtt.disconnect()


@app.get("/")
def root():
    return "Welcome to 🐹 pahome. Work in progress"

