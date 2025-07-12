"""Wrapper around Axe REST API as defined in openapi.yaml."""
from __future__ import annotations

import requests
from typing import Any, Union


class AxeAPI:
    def __init__(self, ip: str, default_timeout: float | None = 10):
        self.base = f"http://{ip}"
        self.session = requests.Session()
        self.default_timeout = default_timeout


    def _post(self, path: str, *, timeout: float | None = None, **kwargs: Any):
        url = self.base + path
        if timeout is None:
            timeout = self.default_timeout
        resp = self.session.post(url, timeout=timeout, **kwargs)
        resp.raise_for_status()
        return resp

    def get_stats(self, *, timeout: float | None = None) -> dict[str, Any]:
        if timeout is None:
            timeout = self.default_timeout
        resp = self.session.get(self.base + "/api/system/statistics", timeout=timeout)
        resp.raise_for_status()
        return resp

    def upload_ota(self, path: str, *, timeout: float | None = 120) -> dict[str, Any]:
        with open(path, "rb") as f:
            resp = self._post(
                "/api/system/OTA",
                data=f,
                headers={"Content-Type": "application/octet-stream"},
                timeout=timeout,
            )
        resp.raise_for_status()
        return resp

    def upload_ota_www(self, path: str, *, timeout: float | None = 120) -> dict[str, Any]:
        with open(path, "rb") as f:
            resp = self._post(
                "/api/system/OTAWWW",
                data=f,
                headers={"Content-Type": "application/octet-stream"},
                timeout=timeout,
            )
        resp.raise_for_status()
        return resp
