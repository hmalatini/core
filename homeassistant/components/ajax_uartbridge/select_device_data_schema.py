"""Data schemas for config flow."""
import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import USB_DEVICE_PATH
from .device_handler import get_all_usb_ports


async def select_device_data_schema(hass: HomeAssistant) -> vol.Schema:
    """Return the data schema used for when the user has to select an usb port."""
    device_selector = await __get_all_usb_devices_selector(hass)

    return vol.Schema(
        {
            vol.Required(USB_DEVICE_PATH): device_selector,
        }
    )


async def __get_all_usb_devices_selector(hass: HomeAssistant) -> SelectSelector:
    ports = await get_all_usb_ports(hass)
    devices: list[SelectOptionDict] = []
    for port in ports:
        devices.append(SelectOptionDict(value=port.dev_path, label=port.get_label()))

    return SelectSelector(
        SelectSelectorConfig(options=devices, mode=SelectSelectorMode.DROPDOWN)
    )
