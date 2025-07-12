"""esp_miner_e2e

Cross-platform end-to-end test framework for ESP-Miner firmware and software.

Importing this top-level package registers built-in targets in
:pydata:`esp_miner_e2e.targets` so that they are discoverable via the factory.
"""
from importlib import import_module
import sys as _sys

# Eagerly register built-in targets
for _module in ("esp_miner_e2e.device.bitaxe",):
    try:
        import_module(_module)
    except ModuleNotFoundError:
        # Optional dependency missing; skip silently
        pass

# Provide underscore alias to permit 'import esp_miner_e2e'
_sys.modules.setdefault("esp_miner_e2e", _sys.modules[__name__])
