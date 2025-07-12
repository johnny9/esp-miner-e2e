"""Timing helpers."""
from __future__ import annotations

import time
from typing import Callable


def until(
    cond: Callable[[], bool],
    timeout: float,
    interval: float = 10,
    message: str | None = None,
) -> bool:
    """Return True if *cond* becomes True within *timeout*, polling *interval*."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if cond():
            return True
        time.sleep(interval)
    # Timeout reached; raise with optional custom message for clarity
    if message is None:
        message = (
            f"Condition not satisfied within {timeout} seconds."
        )
    raise TimeoutError(message)
