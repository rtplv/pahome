from devices.device import repository
from devices.device.model import Device


async def create(created_device: Device):
    await repository.create(created_device)


async def get_by_ieee_address(ieee_address: str) -> Device:
    return await repository.get_by_ieee_address(ieee_address)


async def update(updated_device: Device):
    await repository.update(updated_device)


async def delete(ieee_address: str):
    await repository.delete(ieee_address)
