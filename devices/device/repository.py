import datetime
from typing import Optional, Tuple
from asyncpg import Connection
from devices.device.model import Device, DeviceMeta, DeviceState


async def create(ctx: Connection, created_device: Device):
    await ctx.execute(
        "INSERT INTO devices(ieee_address, friendly_name, removed) VALUES ($1, $2, $3)",
        created_device.ieee_address,
        created_device.friendly_name,
        created_device.removed
    )


async def create_meta(ctx: Connection, created_meta: DeviceMeta):
    await ctx.execute(
        "INSERT INTO device_meta(ieee_address, model, vendor, description, exposes, options) "
        "VALUES ($1, $2, $3, $4, $5, $6)",
        created_meta.ieee_address,
        created_meta.model,
        created_meta.vendor,
        created_meta.description,
        created_meta.exposes,
        created_meta.options
    )


async def create_state(ctx: Connection, created_state: DeviceState):
    await ctx.execute(
        "INSERT INTO device_state(ieee_address, state) VALUES ($1, $2)",
        created_state.ieee_address,
        created_state.state
    )


async def get(ctx: Connection, ieee_address: str) -> Optional[Device]:
    row = await ctx.fetchrow(
        "SELECT * FROM devices WHERE ieee_address = $1",
        ieee_address
    )
    return Device.parse_obj(row) if row else None


async def get_with_meta(ctx: Connection, ieee_address: str) -> Tuple[Optional[Device], Optional[DeviceMeta]]:
    row = await ctx.fetchrow(
        "SELECT d.*, dm.model, dm.vendor, dm.description, dm.\"options\", dm.exposes "
        "FROM devices d LEFT JOIN device_meta dm ON d.ieee_address = dm.ieee_address "
        "WHERE d.ieee_address = $1",
        ieee_address
    )

    if row:
        if row["model"]:
            return Device.parse_obj(row), DeviceMeta(
                ieee_address=row["ieee_address"],
                model=row["model"],
                vendor=row["vendor"],
                description=row["description"],
                exposes=row["exposes"],
                options=row["options"]
            )
        else:
            return Device.parse_obj(row), None
    else:
        return None, None


async def get_state(ctx: Connection, ieee_address: str) -> Optional[DeviceState]:
    row = await ctx.fetchrow(
        "SELECT * FROM device_state WHERE ieee_address = $1",
        ieee_address
    )

    return DeviceState(
        ieee_address=row['ieee_address'],
        state=row['state'],
        created_at=row['created_at'],
        updated_at=row['updated_at']
    ) if row else None


async def update(ctx: Connection, updated_device: Device):
    await ctx.execute(
        "UPDATE devices SET friendly_name = $1, removed = $2, updated_at = $3 "
        "WHERE ieee_address = $4",
        updated_device.friendly_name,
        updated_device.removed,
        datetime.datetime.utcnow(),
        updated_device.ieee_address,
    )


async def delete(ctx: Connection, ieee_address: str):
    await ctx.execute(
        "DELETE FROM devices WHERE ieee_address = $1",
        ieee_address
    )


async def update_state(ctx: Connection, updated_state: DeviceState):
    await ctx.execute(
        "UPDATE device_state SET state = $1, updated_at = $2 WHERE ieee_address = $3",
        updated_state.state,
        datetime.datetime.utcnow(),
        updated_state.ieee_address
    )