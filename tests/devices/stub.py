from typing import Optional

from devices.device.model import Device, DeviceMeta, DeviceState

IEEE_ADDRESS = "0xffffff"


def device_stub(ieee_address: str = IEEE_ADDRESS, friendly_name: str = IEEE_ADDRESS, removed: bool = False):
    return Device(
        ieee_address=ieee_address,
        friendly_name=friendly_name,
        removed=removed
    )


def device_meta_stub(
        ieee_address: str = IEEE_ADDRESS,
        model: str = "kuntus lamp",
        vendor: str = "ikea",
        description: str = "lamp with more rgb modes",
        exposes: Optional[list] = None,
        options: Optional[list] = None
):
    exposes = exposes if exposes else []
    options = options if options else []
    return DeviceMeta(
        ieee_address=ieee_address,
        model=model,
        vendor=vendor,
        description=description,
        exposes=exposes,
        options=options,
    )


def device_state_stub(
    ieee_address: str = IEEE_ADDRESS,
    state: Optional[dict] = None
):
    state = state if state else {}
    return DeviceState(
        ieee_address=ieee_address,
        state=state
    )