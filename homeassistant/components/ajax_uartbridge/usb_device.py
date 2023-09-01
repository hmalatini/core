"""UsbDevice provide utilities for handling an port during the config and option flow."""
from typing import Any

from serial.tools.list_ports_common import ListPortInfo

from homeassistant.components import usb

from .const import UNIQUE_ID_PREFIX


class UsbDevice:
    """UsbDevice class with its utility methods."""

    def __init__(
        self,
        dev_path: str,
        vid: str,
        pid: str,
        serial_number: str,
        manufacturer: str,
        description: str,
    ) -> None:
        """Initialize."""
        self.dev_path = dev_path
        self.vid = vid
        self.pid = pid
        self.serial_number = serial_number
        self.manufacturer = manufacturer
        self.description = description

    def generate_unique_id(self) -> str:
        """Generate unique id from usb attributes."""
        return f"{UNIQUE_ID_PREFIX}-{self.vid}:{self.pid}_{self.serial_number}_{self.manufacturer}_{self.description}"

    def get_label(self) -> str:
        """Get human readable device name."""
        return usb.human_readable_device_name(
            self.dev_path,
            self.serial_number,
            self.manufacturer,
            self.description,
            self.vid,
            self.pid,
        )

    def as_dict(self) -> dict[str, str]:
        """Convert object to dictionary."""
        data: dict[str, Any] = {}
        data.update(
            {
                "dev_path": self.dev_path,
                "vid": self.vid,
                "pid": self.pid,
                "serial_number": self.serial_number,
                "manufacturer": self.manufacturer,
                "description": self.description,
                "unique_id": self.generate_unique_id(),
            }
        )

        return data


class UsbDeviceFactory:
    """Create instances of UsbDevice from different type of instances."""

    def from_list_port_info(self, port: ListPortInfo) -> UsbDevice:
        """Create USB Device from ListPortInfo object."""
        return UsbDevice(
            port.device,
            port.vid,
            port.pid,
            port.serial_number,
            port.manufacturer,
            port.description,
        )
