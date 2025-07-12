"""Bitaxe miner abstraction using helper interfaces."""
from __future__ import annotations

from esp_miner_e2e.interface.serial_comm import SerialInterface
from esp_miner_e2e.interface.axeapi import AxeAPI
try:
    from esp_miner_e2e.interface.webgui import WebGUI  # requires selenium
except ModuleNotFoundError:
    WebGUI = None  # optional
from esp_miner_e2e.device import DeviceInterface, register


@register
class Bitaxe(DeviceInterface):
    NAME = "bitaxe"

    def __init__(self, serial_port: str, baud: int = 115200, ip: str | None = None):
        super().__init__(serial_port=serial_port, baud=baud, ip=ip)
        self.serial = SerialInterface(serial_port, baud)
        self.api = AxeAPI(ip) if ip else None
        self.gui = WebGUI(ip) if (ip and WebGUI) else None

    def connect(self):
        self.serial.open()

    def disconnect(self):
        self.serial.close()
        if self.gui:
            self.gui.quit()

    # Example validation helper
    def expect_hashrate_above(self, target: float, timeout: float = 30.0) -> bool:
        """Return True if device reaches *target* MH/s within *timeout*."""
        from esp_miner_e2e.util.timing import until

        def _condition():
            if not self.api:
                return False
            stats = self.api.get_stats()
            return stats.get("hashRate", 0) >= target

        return until(_condition, timeout)
