"""Device implementations and factory."""
from __future__ import annotations

from importlib import import_module
from typing import Dict, Type, Any

__all__ = ["DeviceInterface", "register", "create"]


class DeviceInterface:  # Lightweight base; extend as needed
    """Minimal abstract interface common to all devices."""

    NAME: str = "base"

    def __init__(self, **kwargs: Any):
        self._kwargs = kwargs

    # Override in subclass
    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError


_REGISTRY: Dict[str, Type[DeviceInterface]] = {}


def register(cls: Type[DeviceInterface]) -> Type[DeviceInterface]:
    """Class decorator to register a device implementation."""
    if not getattr(cls, "NAME", None):
        raise ValueError("Device must define unique NAME")
    _REGISTRY[cls.NAME] = cls
    return cls


def create(name: str, **kwargs: Any) -> DeviceInterface:
    try:
        cls = _REGISTRY[name]
    except KeyError as exc:
        raise ValueError(f"Unknown device '{name}', known: {list(_REGISTRY)}") from exc
    return cls(**kwargs)


# Auto-import built-in devices so they're registered
for _mod in ("esp_miner_e2e.device.bitaxe",):
    try:
        import_module(_mod)
    except ModuleNotFoundError:
        pass
