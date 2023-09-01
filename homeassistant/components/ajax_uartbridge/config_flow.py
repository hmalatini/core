"""Config flow for Ajax UartBridge integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, USB_DEVICE, USB_DEVICE_PATH
from .device_handler import find_usb_port_by_dev_path
from .input_validator import validate
from .select_device_data_schema import select_device_data_schema

_LOGGER = logging.getLogger(__name__)


class AjaxUartBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ajax UartBridge."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        data_schema = await select_device_data_schema(self.hass)
        return self.async_show_form(step_id="select_device", data_schema=data_schema)

    async def async_step_select_device(self, user_input: dict[str, Any]) -> FlowResult:
        """Handle the step when the user already select an usb device."""
        errors: dict[str, str] = {}

        info = await validate(self.hass, user_input, errors)

        if len(errors) > 0:
            data_schema = await select_device_data_schema(self.hass)
            return self.async_show_form(
                step_id="select_device", data_schema=data_schema, errors=errors
            )

        # Validate unique_id
        await self.__validate_unique_id(user_input[USB_DEVICE_PATH])

        # Finish config flow
        return self.async_create_entry(
            title=info["title"], data=info[USB_DEVICE].as_dict()
        )

    async def __validate_unique_id(self, dev_path: str) -> None:
        usb_device = await find_usb_port_by_dev_path(dev_path, self.hass)
        if usb_device is None:
            return

        device_unique_id = usb_device.generate_unique_id()
        await self.async_set_unique_id(device_unique_id)
        self._abort_if_unique_id_configured()
