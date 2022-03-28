from typing import Dict, Any, Optional

from events.event_log.model import EventLog
from events.model.mqtt import EventTopic, BridgeEventType, BridgeEventData, BridgeEvent, DeviceRemoveEvent, \
    DeviceRemoveEventData

IEEE_ADDRESS = "0xffffff"


def event_log_stub(
        ieee_address: str = IEEE_ADDRESS,
        topic: EventTopic = EventTopic.DEVICE,
        body: Optional[Dict[str, Any]] = None
):
    body = {} if not body else body
    return EventLog(
        ieee_address=ieee_address,
        topic=topic,
        body=body
    )


def bridge_event_stub(
        type: BridgeEventType = BridgeEventType.DEVICE_JOINED,
        data: Optional[BridgeEventData] = None
):
    data = data if data else BridgeEventData(
        friendly_name=IEEE_ADDRESS,
        ieee_address=IEEE_ADDRESS
    )
    return BridgeEvent(
        type=type,
        data=data
    )


def bridge_remove_event(
    data: Optional[DeviceRemoveEventData] = None,
    status: str = "active",
    transaction: str = "0"
):
    data = data if data else DeviceRemoveEventData(block=True, force=True, id="0")
    return DeviceRemoveEvent(data=data, status=status, transaction=transaction)
