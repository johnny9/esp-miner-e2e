"""End-to-end test for OTA upgrade (OTAWWW then OTA).

Configuration sources (priority):
1. Environment variables:
   * E2E_WWW_BIN – path to www.bin
   * E2E_FW_BIN  – path to esp-miner.bin
2. pytest/unittest CLI overrides via --www-bin / --fw-bin if using a custom runner.
3. Fallback: build/www.bin and build/esp-miner.bin relative to repo root.
"""
from __future__ import annotations

import os
import pathlib
import time
import unittest
from typing import Optional

from esp_miner_e2e.device import create as create_device
from esp_miner_e2e.util.timing import until

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]  # esp_miner_e2e/tests/../../.. -> project root


def _resolve_artifact(env_var: str, default_rel: str) -> pathlib.Path:
    path = os.getenv(env_var)
    if path:
        return pathlib.Path(path).expanduser().resolve()
    return (REPO_ROOT / default_rel).resolve()


class OTAUpgradeTest(unittest.TestCase):
    WWW_BIN: pathlib.Path
    FW_BIN: pathlib.Path

    @classmethod
    def setUpClass(cls):
        cls.WWW_BIN = _resolve_artifact("E2E_WWW_BIN", "build/www.bin")
        cls.FW_BIN = _resolve_artifact("E2E_FW_BIN", "build/esp-miner.bin")
        for p in (cls.WWW_BIN, cls.FW_BIN):
            if not p.is_file():
                raise FileNotFoundError(f"Required artifact {p} not found.")

    def setUp(self):
        target = os.getenv("E2E_TARGET", "bitaxe")
        ip = os.getenv("E2E_IP", "127.0.0.1")
        serial_port = os.getenv("E2E_SERIAL", "/dev/ttyUSB0")
        self.dev = create_device(target, serial_port=serial_port, ip=ip)
        self.dev.connect()

    def tearDown(self):
        self.dev.disconnect()

    def test_ota_upgrade(self):
        """Upload web UI then firmware and verify device responds afterwards."""
        if not hasattr(self.dev, "api"):
            self.skipTest("Device API helper not available")

        # Upload web interface
        resp_www = self.dev.api.upload_ota_www(self.WWW_BIN)
        self.assertEqual(resp_www.status_code, 200, "OTAWWW failed")

        # Upload firmware
        resp_www = self.dev.api.upload_ota(self.FW_BIN)
        self.assertEqual(resp_www.status_code, 200, "OTA failed")

        # Wait for device to reboot and report stats
        def _device_back() -> bool:
            try:
                stats = self.dev.api.get_stats()
            except Exception:
                return False
            return bool(stats)

        until(
            _device_back,
            timeout=60,
            message="Device did not come back online after OTA",
        )


if __name__ == "__main__":
    unittest.main()
