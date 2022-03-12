import conf
from devices.device.model import Device


async def create(created_device: Device):
    query = "INSERT INTO devices(ieee_address, friendly_name) "\
            "VALUES (:ieee_address, :friendly_name)"
    values = {
        "ieee_address": created_device.ieee_address,
        "friendly_name": created_device.friendly_name
    }

    await conf.db.execute(query, values)


async def get_by_ieee_address(ieee_address: str) -> Device:
    query = "SELECT * FROM devices WHERE ieee_address = :ieee_address"
    value = {"ieee_address": ieee_address}

    device_map = await conf.db.fetch_one(query, value)
    return Device.parse_obj(device_map) if device_map else None


async def update(updated_device: Device):
    query = "UPDATE devices SET friendly_name = :friendly_name "\
            "WHERE ieee_address = :ieee_address"
    values = {
        "ieee_address": updated_device.ieee_address,
        "friendly_name": updated_device.friendly_name
    }
    await conf.db.execute(query, values)


async def delete(ieee_address: str):
    query = "DELETE FROM devices WHERE ieee_address = :ieee_address"
    values = {"ieee_address": ieee_address}
    await conf.db.execute(query, values)
