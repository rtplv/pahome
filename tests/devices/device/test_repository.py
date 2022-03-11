import pytest
from databases import Database
from devices.device import repository
from devices.device.model import Device


@pytest.mark.asyncio
async def test_create_hp(db: Database):
    device_bp = Device(
        ieee_address="0x50325ffffe71f9a1",
        friendly_name="lamp 1"
    )
    await repository.create(device_bp)

    device_record = await db.fetch_one(
        "SELECT * FROM devices WHERE ieee_address = :ieee_address",
        {"ieee_address": device_bp.ieee_address}
    )
    device_model = Device.parse_obj(device_record)

    assert device_model is not None
    assert device_model.ieee_address == device_bp.ieee_address
    assert device_model.friendly_name == device_bp.friendly_name

