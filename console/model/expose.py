from enum import Enum
from typing import List

from pydantic import BaseModel


class AccessLevel(str, Enum):
    CONTAIN_IN_STATE = "CONTAIN_IN_STATE"
    SET = "SET"
    GET = "GET"


class ExposeType(str, Enum):
    BINARY = "binary"
    NUMERIC = "numeric"
    ENUM = "enum"
    TEXT = "text"
    COMPOSITE = "composite"
    LIST = "list"
    LIGHT = "light"
    SWITCH = "switch"
    FAN = "fan"
    COVER = "cover"
    LOCK = "lock"
    CLIMATE = "climate"


class Expose(BaseModel):
    access: List[AccessLevel]
    description: str
    name: str
    property: str
    type: ExposeType


class BinaryExpose(Expose):
    value_on: str
    value_off: str
    value_toggle: str


class NumericExposePreset(BaseModel):
    name: str
    value: str
    description: str


class NumericExpose(Expose):
    value_max: int
    value_min: int
    value_step: int
    unit: str
    presets: List[NumericExposePreset]


class EnumExpose(Expose):
    values: List[str]


class CompositeExpose(Expose):
    features: List[Expose]


class ListExposeItemType(BaseModel):
    NUMBER = "number"


class ListExpose(Expose):
    # TODO: need enum
    item_type: str
