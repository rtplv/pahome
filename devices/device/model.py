from datetime import datetime
from typing import Optional, Dict, Any

from pydantic.main import BaseModel


class Device(BaseModel):
    ieee_address: str
    friendly_name: Optional[str]
    removed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class DeviceMeta(BaseModel):
    ieee_address: str
    model: str
    vendor: Optional[str]
    description: Optional[str]
    exposes: Optional[list]
    options: Optional[list]


class DeviceState(BaseModel):
    ieee_address: str
    state: dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
