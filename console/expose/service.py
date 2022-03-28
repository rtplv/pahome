from typing import List

from console.model.expose import ExposeType, Expose, BinaryExpose, NumericExpose, EnumExpose, CompositeExpose, \
    ListExpose


def parse_exposes(exposes: List[dict]) -> List[Expose]:
    parsed_exposes = []

    for expose in exposes:
        parsed_expose = None
        if expose['type'] == ExposeType.BINARY:
            parsed_expose = BinaryExpose.parse_obj(expose)
        if expose['type'] == ExposeType.NUMERIC:
            parsed_expose = NumericExpose.parse_obj(expose)
        if expose['type'] == ExposeType.ENUM:
            parsed_expose = EnumExpose.parse_obj(expose)
        if expose['type'] == ExposeType.TEXT:
            parsed_expose = Expose.parse_obj(expose)
        if expose['type'] == ExposeType.LIST:
            parsed_expose = ListExpose.parse_obj(expose)
        if expose['type'] in (ExposeType.COMPOSITE, ExposeType.LIGHT, ExposeType.SWITCH, ExposeType.FAN,
                              ExposeType.COVER, ExposeType.LOCK, ExposeType.CLIMATE):
            parsed_expose = CompositeExpose.parse_obj(expose)

        parsed_exposes.append(parsed_expose)

    return parsed_exposes
