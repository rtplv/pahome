from typing import Tuple, Optional
from asyncpg import Connection

from devices.device import repository
from devices.device.model import Device, DeviceMeta, DeviceState


async def create(ctx: Connection, created_device: Device):
    await repository.create(ctx, created_device)


async def create_meta(ctx: Connection, created_meta: DeviceMeta):
    await repository.create_meta(ctx, created_meta)


async def save_state(ctx: Connection, ieee_address: str, state: dict):
    prev_state = await get_state(ctx, ieee_address)
    state_mdl = DeviceState(
        ieee_address=ieee_address,
        state=state
    )

    if not prev_state:
        await repository.create_state(ctx, state_mdl)
    else:
        await repository.update_state(ctx, state_mdl)


async def get(ctx: Connection, ieee_address: str) -> Device:
    return await repository.get(ctx, ieee_address)


async def get_state(ctx: Connection, ieee_address: str) -> Optional[DeviceState]:
    return await repository.get_state(ctx, ieee_address)


async def get_with_meta(ctx: Connection, ieee_address: str) -> Tuple[Device, Optional[DeviceMeta]]:
    return await repository.get_with_meta(ctx, ieee_address)


async def update(ctx: Connection, updated_device: Device):
    await repository.update(ctx, updated_device)


async def change_removed_state(ctx: Connection, ieee_address: str, removed: bool):
    async with ctx.transaction():
        device = await get(ctx, ieee_address)
        device.removed = removed
        await update(ctx, device)


async def delete(ctx: Connection, ieee_address: str):
    await repository.delete(ctx, ieee_address)
