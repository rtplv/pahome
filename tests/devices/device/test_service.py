from unittest import mock
from unittest.mock import patch, Mock

from asyncpg import Pool

from devices.device import service

import pytest

from devices.device.model import DeviceState
from tests.devices.stub import device_stub, device_meta_stub, device_state_stub


@pytest.mark.asyncio
async def test_create(db_pool: Pool):
    with patch('devices.device.repository.create') as r_m:
        async with db_pool.acquire() as ctx:
            await service.create(ctx, device_stub())
            assert r_m.called


@pytest.mark.asyncio
async def test_create_meta(db_pool: Pool):
    with patch('devices.device.repository.create_meta') as r_m:
        async with db_pool.acquire() as ctx:
            await service.create_meta(ctx, device_meta_stub())
            assert r_m.called


@pytest.mark.asyncio
@pytest.mark.parametrize("prev_state", [device_state_stub(), None])
async def test_save_state(db_pool: Pool, prev_state: DeviceState):
    state_stub = device_state_stub(state={"enabled": True})
    get_state_mock = mock.patch('devices.device.repository.get_state', return_value=prev_state).start()
    create_state_mock = mock.patch('devices.device.repository.create_state').start()
    update_state_mock = mock.patch('devices.device.repository.update_state').start()

    async with db_pool.acquire() as ctx:
        await service.save_state(ctx, state_stub.ieee_address, {"enabled": False})

        assert get_state_mock.called
        if prev_state:
            assert update_state_mock.called
            assert not create_state_mock.called
        else:
            assert create_state_mock.called
            assert not update_state_mock.called


@pytest.mark.asyncio
async def test_get(db_pool: Pool):
    stub = device_stub()
    with patch('devices.device.repository.get', return_value=stub) as r_m:
        async with db_pool.acquire() as ctx:
            result = await service.get(ctx, stub.ieee_address)
            assert result is not None
            assert r_m.called


@pytest.mark.asyncio
async def test_get_state(db_pool: Pool):
    stub = device_state_stub()
    with patch('devices.device.repository.get_state', return_value=stub) as r_m:
        async with db_pool.acquire() as ctx:
            result = await service.get_state(ctx, stub.ieee_address)
            assert result is not None
            assert r_m.called


@pytest.mark.asyncio
async def test_get_with_meta(db_pool: Pool):
    device_s = device_stub()
    meta_s = device_meta_stub()

    with patch('devices.device.repository.get_with_meta', return_value=(device_s, meta_s)) as r_m:
        async with db_pool.acquire() as ctx:
            (device, meta) = await service.get_with_meta(ctx, device_s.ieee_address)
            assert device is not None
            assert meta is not None
            assert r_m.called


@pytest.mark.asyncio
async def test_update(db_pool: Pool):
    stub = device_stub()
    with patch('devices.device.repository.update') as r_m:
        async with db_pool.acquire() as ctx:
            await service.update(ctx, stub)
            assert r_m.called


@pytest.mark.asyncio
async def test_change_removed_state(db_pool: Pool):
    stub = device_stub()
    get_mock = mock.patch('devices.device.repository.get', return_value=stub).start()
    update_mock = mock.patch('devices.device.repository.update').start()
    async with db_pool.acquire() as ctx:
        await service.change_removed_state(ctx, stub, removed=False)
        assert get_mock.called
        assert update_mock.called


@pytest.mark.asyncio
async def test_delete(db_pool: Pool):
    stub = device_stub()
    with patch('devices.device.repository.delete') as r_m:
        async with db_pool.acquire() as ctx:
            await service.delete(ctx, stub.ieee_address)
