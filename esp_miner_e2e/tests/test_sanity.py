"""Sanity test to ensure device reports positive hashrate."""
from esp_miner_e2e.tests.base import BaseTestCase


class TestSanity(BaseTestCase):
    """Ensure device can be instantiated and returns a positive hashrate."""

    def test_hashrate_positive(self):
        self.assertTrue(self.dev.expect_hashrate_above(0.0, timeout=1.0))




