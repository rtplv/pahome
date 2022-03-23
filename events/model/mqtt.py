from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EventTopic(str, Enum):
    BRIDGE_EVENT = "zigbee2mqtt/bridge/event"
    DEVICE_EVENT = "zigbee2mqtt/0x"
    DEVICE_REMOVE = "zigbee2mqtt/bridge/response/device/remove"


class BridgeEventType(str, Enum):
    DEVICE_JOINED = "device_joined"
    DEVICE_ANNOUNCE = "device_announce"
    DEVICE_INTERVIEW = "device_interview"
    DEVICE_LEAVE = "device_leave"


class BridgeEventData(BaseModel):
    friendly_name: str
    ieee_address: str


class BridgeEvent(BaseModel):
    type: BridgeEventType
    data: BridgeEventData


# device_interview
class DeviceInterviewStatus(str, Enum):
    STARTED = "started"
    SUCCESSFUL = "successful"
    FAILED = "failed"


class DeviceInterviewDefinition(BaseModel):
    model: str
    vendor: str
    description: str
    exposes: list
    options: list


class DeviceInterviewEventData(BridgeEventData):
    definition: Optional[DeviceInterviewDefinition] = None
    supported: Optional[bool] = False
    status: Optional[DeviceInterviewStatus]


class DeviceInterviewEvent(BridgeEvent):
    data: DeviceInterviewEventData


class DeviceRemoveEventData(BaseModel):
    block: bool
    force: bool
    id: str


class DeviceRemoveEvent(BaseModel):
    data: DeviceRemoveEventData
    status: str
    transaction: str
