import json
from json import JSONDecodeError
from typing import Optional

import conf
from gmqtt import Client
from loguru import logger

from devices.device.model import Device, DeviceMeta
from events.event_log.model import EventLog
from events.model.mqtt import EventTopic, DeviceInterviewEvent, DeviceInterviewStatus, \
    BridgeEventType, BridgeEvent, DeviceRemoveEvent
import devices.device.service as device_service
import events.event_log.service as event_log_service


def init_subscriptions():
    conf.mqtt.subscribe("zigbee2mqtt/#")


async def process_event(client: Client, topic: str, payload: str, qos: int, options: dict):
    if topic not in [t.value for t in EventTopic] and not topic.startswith(EventTopic.DEVICE_EVENT.value):
        logger.debug(f"Skip event. Topic: {topic}, payload: {payload}")
        return

    if len(payload) == 0:
        logger.debug(f"Empty payload. Topic: {topic}")
        return

    try:
        body = json.loads(payload)
    except JSONDecodeError as e:
        logger.exception(e)
        return

    if topic == EventTopic.BRIDGE_EVENT.value:
        await process_bridge_event(body)
    if topic.startswith(EventTopic.DEVICE_EVENT.value):
        await process_device_event(topic, body)
    if topic == EventTopic.DEVICE_REMOVE.value:
        await process_device_remove(body)


async def process_bridge_event(body: dict):
    """Обработчик событий поступаемых при обнаружении и регистрации устройства"""
    async with conf.db_pool.acquire() as ctx:
        async with ctx.transaction():
            event = BridgeEvent.parse_obj(body)
            device, device_meta = await device_service.get_with_meta(ctx, event.data.ieee_address)

            if event.type == BridgeEventType.DEVICE_JOINED:
                if not device:
                    await device_service.create(ctx, Device(
                        ieee_address=event.data.ieee_address,
                        friendly_name=event.data.ieee_address,
                    ))
                elif device.removed:
                    await device_service.change_removed_state(ctx, device.ieee_address, False)

            if event.type == BridgeEventType.DEVICE_INTERVIEW:
                interview_event = DeviceInterviewEvent.parse_obj(body)
                if interview_event.data.status == DeviceInterviewStatus.SUCCESSFUL:
                    if not device_meta:
                        await device_service.create_meta(ctx, DeviceMeta(
                            ieee_address=interview_event.data.ieee_address,
                            model=interview_event.data.definition.model,
                            vendor=interview_event.data.definition.vendor,
                            description=interview_event.data.definition.description,
                            exposes=interview_event.data.definition.exposes,
                            options=interview_event.data.definition.options
                        ))

            await event_log_service.create(ctx, EventLog(
                ieee_address=event.data.ieee_address,
                topic=EventTopic.BRIDGE_EVENT,
                body=event.dict()
            ))


async def process_device_remove(body: dict):
    """Обработчик событий при удалении зарегистрированного устройства"""
    async with conf.db_pool.acquire() as ctx:
        event = DeviceRemoveEvent.parse_obj(body)
        device = await device_service.get(ctx, event.data.id)

        if not device:
            logger.error(f"device not found. ieee_address: {event.data.id}")
            return

        device.removed = True
        await device_service.update(ctx, device)


async def process_device_event(topic: str, body: dict):
    """Обработчик событий поступаемых при изменения состояния устройства"""
    async with conf.db_pool.acquire() as ctx:
        ieee_address = __get_ieee_address_by_topic(topic)

        device = await device_service.get(ctx, ieee_address)

        if not device:
            await device_service.create(ctx, Device(
                ieee_address=ieee_address,
                friendly_name=ieee_address
            ))

        await device_service.save_state(ctx, ieee_address, body)
        await event_log_service.create(ctx, EventLog(
            ieee_address=ieee_address,
            topic=EventTopic.DEVICE_EVENT,
            body=body
        ))


def __get_ieee_address_by_topic(topic: str) -> Optional[str]:
    topic_items = topic.split("/")
    return next(i for i in topic_items if i.startswith("0x"))
