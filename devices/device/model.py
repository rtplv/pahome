from typing import Optional

from pydantic.main import BaseModel


class Device(BaseModel):
    ieee_address: str
    friendly_name: Optional[str]
