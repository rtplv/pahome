from typing import Optional, Tuple
from unittest.mock import patch

import pytest
from asyncpg import Pool
from gmqtt import Client

from devices.device.model import DeviceMeta, Device
from events.model.mqtt import EventTopic, BridgeEventType
from events.mqtt import listener
from events.mqtt.listener import process_bridge_event, process_device_remove, process_device_event
from tests.devices.stub import device_stub, device_meta_stub
from tests.events.stub import bridge_event_stub, bridge_remove_event, IEEE_ADDRESS


@pytest.mark.asyncio
@pytest.mark.parametrize("topic,topic_type", [
    ("zigbee2mqtt/bridge/event", EventTopic.BRIDGE_EVENT),
    ("zigbee2mqtt/0xffffff", EventTopic.DEVICE_EVENT),
    ("zigbee2mqtt/0xffffff/get", EventTopic.DEVICE_EVENT),
    ("zigbee2mqtt/bridge/response/device/remove", EventTopic.DEVICE_REMOVE),
    ("zigbee2mqtt/bridge/response/device/add", None),
    ("zigbee2mqtt/02552", None),
    ("zigbee2mqtt/processing/0xffffff", None)
])
async def test_process_event(topic: str, topic_type: Optional[EventTopic]):
    process_bridge_event_mock = patch('events.mqtt.listener.process_bridge_event').start()
    process_device_event_mock = patch('events.mqtt.listener.process_device_event').start()
    process_device_remove_mock = patch('events.mqtt.listener.process_device_remove').start()

    await listener.process_event(Client("test"), topic, "{}", 0, {})

    if topic_type == EventTopic.BRIDGE_EVENT:
        assert process_bridge_event_mock.called
    if topic_type == EventTopic.DEVICE_EVENT:
        assert process_device_event_mock.called
    if topic_type == EventTopic.DEVICE_REMOVE:
        assert process_device_remove_mock.called
    if topic_type is None:
        assert not process_bridge_event_mock.called
        assert not process_device_event_mock.called
        assert not process_device_remove_mock.called


@pytest.mark.asyncio
@pytest.mark.parametrize("event_type,device_with_meta", [
    (BridgeEventType.DEVICE_JOINED, (device_stub(), device_meta_stub())),
    (BridgeEventType.DEVICE_INTERVIEW, (device_stub(), device_meta_stub())),
    (BridgeEventType.DEVICE_ANNOUNCE, (device_stub(), device_meta_stub())),
    (BridgeEventType.DEVICE_JOINED, (None, None)),
    (BridgeEventType.DEVICE_JOINED, (device_stub(removed=True), device_meta_stub())),
    (BridgeEventType.DEVICE_INTERVIEW, (None, None)),
])
async def test_process_bridge_event_device_exist(db_pool: Pool,
                                                 event_type: BridgeEventType,
                                                 device_with_meta: Tuple[Optional[Device], Optional[DeviceMeta]]):
    event_stub = bridge_event_stub(type=event_type)
    (device, meta) = device_with_meta
    get_with_meta_mock = patch('devices.device.service.get_with_meta', return_value=(device, meta)).start()
    create_mock = patch('devices.device.service.create').start()
    change_removed_state_mock = patch('devices.device.service.change_removed_state').start()
    create_meta_mock = patch('devices.device.service.create_meta').start()
    event_log_create_mock = patch('events.event_log.service.create').start()

    body = event_stub.dict()
    await process_bridge_event(body)

    assert get_with_meta_mock.called
    assert event_log_create_mock.called

    if event_type == BridgeEventType.DEVICE_JOINED:
        if device is None:
            assert create_mock.called
        else:
            assert not create_mock.called
            if device.removed:
                assert change_removed_state_mock.called
            else:
                assert not change_removed_state_mock.called
    elif event_type == BridgeEventType.DEVICE_JOINED:
        if meta is None:
            assert create_meta_mock.called
        else:
            assert not create_meta_mock.called
    else:
        assert not create_mock.called
        assert not change_removed_state_mock.called
        assert not create_meta_mock.called


@pytest.mark.asyncio
@pytest.mark.parametrize("device", [device_stub(), None])
async def test_process_bridge_event_device_exist(db_pool: Pool, device: Optional[Device]):
    remove_event_stub = bridge_remove_event()
    get_mock = patch('devices.device.service.get', return_value=device.copy() if device else None).start()
    update_mock = patch('devices.device.service.update').start()

    await process_device_remove(remove_event_stub.dict())

    assert get_mock.called

    if device:
        update_passed_device: Device = update_mock.call_args.args[1]
        assert update_mock.called
        assert update_passed_device.removed is not device.removed
    else:
        assert not update_mock.called


@pytest.mark.asyncio
@pytest.mark.parametrize("device", [device_stub(), None])
async def test_process_bridge_event_device_exist(db_pool: Pool, device: Device):
    get_mock = patch('devices.device.service.get', return_value=device.copy() if device else None).start()
    create_mock = patch('devices.device.service.create').start()
    save_state_mock = patch('devices.device.service.save_state').start()
    event_log_create_mock = patch('events.event_log.service.create').start()

    await process_device_event(f"zigbee2mqtt/{IEEE_ADDRESS}", {})

    assert get_mock.called
    assert save_state_mock.called
    assert event_log_create_mock.called

    if device:
        assert not create_mock.called
    else:
        assert create_mock.called
