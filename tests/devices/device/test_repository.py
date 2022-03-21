import pytest
from asyncpg import Pool, ForeignKeyViolationError
from devices.device import repository
from devices.device.model import Device, DeviceMeta, DeviceState
from tests.devices.stub import device_stub, device_meta_stub, device_state_stub


@pytest.fixture
@pytest.mark.asyncio
async def device(db_pool: Pool):
    async with db_pool.acquire() as ctx:
        stub = device_stub()
        await repository.create(ctx, stub)
        return await repository.get(ctx, stub.ieee_address)


@pytest.mark.asyncio
async def test_create(db_pool: Pool):
    async with db_pool.acquire() as ctx:
        stub = device_stub()

        await repository.create(ctx, stub)
        device_record = await ctx.fetchrow(
            "SELECT * FROM devices WHERE ieee_address = $1",
            stub.ieee_address
        )
        result = Device.parse_obj(device_record)

        assert result is not None
        assert result.ieee_address == stub.ieee_address
        assert result.friendly_name == stub.friendly_name


@pytest.mark.asyncio
async def test_create_meta(db_pool: Pool, device: Device):
    async with db_pool.acquire() as ctx:
        async with ctx.transaction():
            stub = device_meta_stub()

            await repository.create_meta(ctx, stub)
            record = await ctx.fetchrow(
                "SELECT * FROM device_meta WHERE ieee_address = $1",
                stub.ieee_address
            )
            result = DeviceMeta.parse_obj(record)

            assert result.ieee_address == stub.ieee_address
            assert result.model == stub.model
            assert result.vendor == stub.vendor
            assert result.description == stub.description
            assert len(result.exposes) == len(stub.exposes)
            assert len(result.options) == len(stub.options)


@pytest.mark.asyncio
async def test_create_meta_foreign_constraint_check(db_pool: Pool):
    async with db_pool.acquire() as ctx:
        stub = device_meta_stub()
        stub.ieee_address = ""

        with pytest.raises(ForeignKeyViolationError):
            await repository.create_meta(ctx, stub)


@pytest.mark.asyncio
async def test_create_state(db_pool: Pool, device: Device):
    async with db_pool.acquire() as ctx:
        stub = device_state_stub(state={"enable": True})

        await repository.create_state(ctx, stub)
        device_state_record = await ctx.fetchrow(
            "SELECT * FROM device_state WHERE ieee_address = $1",
            stub.ieee_address
        )
        result = DeviceState.parse_obj(device_state_record)

        assert result is not None
        assert result.ieee_address == stub.ieee_address
        assert all(map(lambda k: k in result.state and result.state[k] == stub.state[k], stub.state.keys()))


@pytest.mark.asyncio
async def test_get(db_pool: Pool, device: Device):
    async with db_pool.acquire() as ctx:
        result = await repository.get(ctx, device.ieee_address)

        assert result is not None
        assert result.ieee_address == device.ieee_address
        assert result.friendly_name == device.friendly_name
        assert result.removed == device.removed
        assert result.created_at is not None
        assert result.updated_at is not None


@pytest.mark.asyncio
async def test_get_with_meta(db_pool: Pool, device: Device):
    async with db_pool.acquire() as ctx:
        meta_stub = device_meta_stub()
        await repository.create_meta(ctx, meta_stub)

        result = await repository.get_with_meta(ctx, device.ieee_address)
        (device_r, device_meta) = result

        assert result is not None
        assert len(result) == 2
        assert any(map(lambda i: i, result))
        assert device_r.ieee_address == device.ieee_address
        assert device_meta.ieee_address == device.ieee_address
        assert device_meta.model == meta_stub.model
        assert device_meta.vendor == meta_stub.vendor
        assert len(device_meta.options) == len(meta_stub.options)
        assert len(device_meta.exposes) == len(meta_stub.exposes)


@pytest.mark.asyncio
async def test_get_state(db_pool: Pool, device: Device):
    async with db_pool.acquire() as ctx:
        stub = device_state_stub(state={"enable": True})
        await repository.create_state(ctx, stub)

        result = await repository.get_state(ctx, device.ieee_address)

        assert result is not None
        assert result.ieee_address == device.ieee_address
        assert all(map(lambda k: k in result.state and result.state[k], stub.state.keys()))


@pytest.mark.asyncio
async def test_update(db_pool: Pool, device: Device):
    async with db_pool.acquire() as ctx:
        await repository.update(ctx, device.copy(update={"removed": True}))
        updated_device = await repository.get(ctx, device.ieee_address)
        assert updated_device.removed is True


@pytest.mark.asyncio
async def test_delete(db_pool: Pool, device: Device):
    async with db_pool.acquire() as ctx:
        await repository.delete(ctx, device.ieee_address)
        result = await repository.get(ctx, device.ieee_address)
        assert result is None


@pytest.mark.asyncio
async def test_update_state(db_pool: Pool, device: Device):
    async with db_pool.acquire() as ctx:
        stub = device_state_stub(state={"enabled": True})
        await repository.create_state(ctx, stub)
        await repository.update_state(ctx, stub.copy(update={"state": {"enabled": False}}))
        updated_device_state = await repository.get_state(ctx, device.ieee_address)
        assert updated_device_state.state["enabled"] is False
