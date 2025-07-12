"""Common unittest base with automatic device setup/teardown.

All test cases should inherit from :class:`BaseTestCase` instead of
``unittest.TestCase``.
"""
from __future__ import annotations

import unittest
from typing import Any

from esp_miner_e2e import config
from esp_miner_e2e.device import create as create_device


class BaseTestCase(unittest.TestCase):
    """TestCase that builds a device from :pymod:`esp_miner_e2e.config`."""

    cfg: dict[str, Any]
    dev: Any  # actual device instance

    @classmethod
    def setUpClass(cls):  # noqa: D401, N802
        super().setUpClass()
        cls.cfg = config.load()

    def setUp(self):  # noqa: D401, N802
        super().setUp()
        self.dev = create_device(
            self.cfg["E2E_TARGET"],
            serial_port=self.cfg["E2E_SERIAL"],
            ip=self.cfg["E2E_IP"],
        )
        self.dev.connect()

    def tearDown(self):  # noqa: D401, N802
        self.dev.disconnect()
        super().tearDown()
