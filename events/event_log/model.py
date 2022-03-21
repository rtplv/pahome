from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel
from events.model.mqtt import EventTopic


class EventLog(BaseModel):
    ieee_address: str
    topic: EventTopic
    body: Dict[str, Any]
    created_at: Optional[datetime] = None
