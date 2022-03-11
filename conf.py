import asyncio
import os

from asyncpg import Pool
from dotenv import load_dotenv
import gmqtt.client

load_dotenv()

# Paths
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# DB
DB_URL = os.environ.get("DB_URL")
DB_DATABASE = os.environ.get("DB_DATABASE")
DB_POOL_MIN = 5
DB_POOL_MAX = 20

# MQTT
MQTT_HOST = os.environ.get("MQTT_HOST")
MQTT_PORT = os.environ.get("MQTT_PORT")

# Connections
db_pool: Pool
mqtt = gmqtt.client.Client("pahome-main")
