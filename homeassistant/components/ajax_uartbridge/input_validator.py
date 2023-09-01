"""Class with methods for validate inputs from config flow."""
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import USB_DEVICE, USB_DEVICE_PATH
from .device_handler import find_usb_port_by_dev_path

_LOGGER = logging.getLogger(__name__)


async def validate(
    hass: HomeAssistant, data: dict[str, Any], errors: dict[str, str]
) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    info: dict[str, Any] = {}
    try:
        info = await __validate_input_user(hass, data)
    except CannotConnect:
        errors["base"] = "cannot_connect"
    except InvalidAuth:
        errors["base"] = "invalid_auth"
    except NoDevicesFound:
        errors["base"] = "no_devices_found"
    except NoDeviceSelected:
        errors["base"] = "no_device_selected"
    except Exception:  # pylint: disable=broad-except
        _LOGGER.exception("Unexpected exception")
        errors["base"] = "unknown"

    return info


async def __validate_input_user(
    hass: HomeAssistant, data: dict[str, Any]
) -> dict[str, Any]:
    device = data[USB_DEVICE_PATH]
    if not device:
        raise NoDeviceSelected

    usb_device = await find_usb_port_by_dev_path(device, hass)
    if usb_device is None:
        raise NoDevicesFound

    data.update({USB_DEVICE: usb_device})

    return await __validate_input(hass, data)


async def __validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    usb_device = data[USB_DEVICE]

    # validate the data can be used to set up a connection.
    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    # hub = PlaceholderHub(usb_device.dev_path)
    # Create async method hub.connect()
    # if not await hub.connect():
    #     raise CannotConnect

    # Return info that you want to store in the config entry.
    return {
        "title": "Ajax UartBridge",
        "usb_device": usb_device,
        "device_unique_id": usb_device.generate_unique_id(),
    }


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class NoDevicesFound(HomeAssistantError):
    """Error to indicate there is no devices matching the device selected from UI."""


class NoDeviceSelected(HomeAssistantError):
    """Error to indicate there is no device selected from UI."""
