"""Helpers for producing nice HTML test result summaries."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

_HTML_TEMPLATE = """<html><head><title>ESP-Miner Test Report</title></head><body>
<h1>ESP-Miner Test Report</h1>
<table border="1" cellpadding="4" cellspacing="0">
<tr><th>Test</th><th>Status</th><th>Details</th></tr>
{rows}
</table></body></html>"""


def _row(name: str, status: str, details: str = "") -> str:
    color = {"PASS": "#cfc", "FAIL": "#fcc"}.get(status, "#eee")
    return f"<tr style='background:{color}'><td>{name}</td><td>{status}</td><td>{details}</td></tr>"


def write_html(path: str | Path, results: Iterable[tuple[str, bool, str]]):
    """Write an HTML file at *path* listing test results."""
    rows = "\n".join(_row(name, "PASS" if ok else "FAIL", details) for name, ok, details in results)
    Path(path).write_text(_HTML_TEMPLATE.format(rows=rows), encoding="utf-8")
