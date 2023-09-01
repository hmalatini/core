"""Device handler is an utility class for get or retrieve usb ports from a machine."""
import serial.tools.list_ports

from homeassistant.core import HomeAssistant

from .usb_device import UsbDevice, UsbDeviceFactory


async def get_all_usb_ports(hass: HomeAssistant) -> list[UsbDevice]:
    """Get all connected USB ports."""
    ports = await hass.async_add_executor_job(serial.tools.list_ports.comports)
    mappedPorts = []
    for port in ports:
        mappedPorts.append(UsbDeviceFactory().from_list_port_info(port))

    return mappedPorts


async def find_usb_port_by_dev_path(
    dev_path: str, hass: HomeAssistant
) -> UsbDevice | None:
    """Find the usb port based on a dev path. Rerturns None if no device was found."""
    ports = await get_all_usb_ports(hass)
    return __get_usb_port_by_dev_path(dev_path, ports)


def __get_usb_port_by_dev_path(
    dev_path: str, ports: list[UsbDevice]
) -> UsbDevice | None:
    for port in ports:
        if port.dev_path == dev_path:
            return port

    return None
