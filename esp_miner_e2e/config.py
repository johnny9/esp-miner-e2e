"""Central configuration helper for esp-miner end-to-end tests.

Priority order (high → low):
1. Environment variables (e.g. `E2E_IP`)
2. YAML file (path given by `$E2E_CONFIG` or `config.yaml` in project root)
3. Hard-coded defaults below.
"""
from __future__ import annotations

import os
import pathlib
from typing import Any, Dict

try:
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    yaml = None  # fallback without YAML support

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULTS: Dict[str, Any] = {
    "E2E_TARGET": "bitaxe",
    "E2E_IP": "127.0.0.1",
    "E2E_SERIAL": "/dev/ttyACM0",
    "E2E_WWW_BIN": "build/www.bin",
    "E2E_FW_BIN": "build/esp-miner.bin",
}


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

def load() -> Dict[str, Any]:
    """Return merged configuration dict."""
    cfg: Dict[str, Any] = DEFAULTS.copy()

    # 1. YAML file -----------------------------------------------------------
    yaml_path = os.getenv("E2E_CONFIG")
    if yaml_path is None:
        # default to repo_root/config.yaml if present
        repo_root = pathlib.Path(__file__).resolve().parents[1]
        yaml_path = repo_root / "config.yaml"
    yaml_path = pathlib.Path(yaml_path)
    if yaml_path.is_file() and yaml:
        with open(yaml_path, "r", encoding="utf-8") as fp:
            data = yaml.safe_load(fp) or {}
        cfg.update({k: v for k, v in data.items() if v is not None})

    # 2. Environment vars ----------------------------------------------------
    for key in DEFAULTS:
        val = os.getenv(key)
        if val is not None:
            cfg[key] = val

    # Normalise paths --------------------------------------------------------
    for key in ("E2E_WWW_BIN", "E2E_FW_BIN"):
        cfg[key] = str(pathlib.Path(cfg[key]).expanduser().resolve())

    return cfg
