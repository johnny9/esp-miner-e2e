"""Serial communication wrapper."""
from __future__ import annotations

import serial  # type: ignore


class SerialInterface:
    def __init__(self, port: str, baud: int = 115200):
        self._port = port
        self._baud = baud
        self._ser: serial.Serial | None = None

    def open(self):
        self._ser = serial.Serial(self._port, self._baud, timeout=0.1)

    def close(self):
        if self._ser:
            self._ser.close()
            self._ser = None

    def readline(self, timeout: float = 1.0) -> str:
        if not self._ser:
            raise RuntimeError("Serial not open")
        self._ser.timeout = timeout
        return self._ser.readline().decode(errors="ignore").rstrip()
