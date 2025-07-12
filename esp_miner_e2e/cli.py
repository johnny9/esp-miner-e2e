"""Command-line interface for ESP-Miner end-to-end tests.

Examples
--------
List available tests:
    python -m esp_miner_e2e.cli list

Run specific test with overrides:
    python -m esp_miner_e2e.cli run tests.test_ota_upgrade --ip 192.168.1.50 \
        --www-bin /path/www.bin --fw-bin /path/esp-miner.bin
"""
from __future__ import annotations

import argparse
import os
import sys
import unittest
from types import ModuleType
from typing import List

# Local imports must use relative because package name may contain hyphen
from . import config as _config  # type: ignore


# ---------------------------------------------------------------------------
# Argparse
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="esp-e2e", description="ESP-Miner E2E test runner")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Shared options function
    def add_common(p: argparse.ArgumentParser):
        p.add_argument("--ip", dest="E2E_IP")
        p.add_argument("--serial", dest="E2E_SERIAL")
        p.add_argument("--target", dest="E2E_TARGET")
        p.add_argument("--www-bin", dest="E2E_WWW_BIN")
        p.add_argument("--fw-bin", dest="E2E_FW_BIN")

    # list command
    p_list = sub.add_parser("list", help="List discovered test cases")
    add_common(p_list)

    # run command
    p_run = sub.add_parser("run", help="Run tests (all by default)")
    add_common(p_run)
    p_run.add_argument("tests", nargs="*", help="Optional dot-qualified test ids to run")

    return parser


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _apply_overrides(args: argparse.Namespace):
    for key in ("E2E_IP", "E2E_SERIAL", "E2E_TARGET", "E2E_WWW_BIN", "E2E_FW_BIN"):
        val = getattr(args, key, None)
        if val:
            os.environ[key] = val


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def _discover(loader: unittest.TestLoader, patterns: List[str] | None = None) -> unittest.TestSuite:
    """Discover tests within the package."""
    start_dir = sys.modules[__name__.rsplit(".", 1)[0]].__path__[0]  # package dir
    if patterns:
        suites = [loader.loadTestsFromName(p) for p in patterns]
        return loader.suiteClass(suites)
    return loader.discover(start_dir, pattern="test_*.py")


def _cmd_list(args: argparse.Namespace):
    loader = unittest.TestLoader()
    suite = _discover(loader)
    for test in loader._iter_suite_tests(suite):  # type: ignore
        print(test.id())


def _cmd_run(args: argparse.Namespace):
    loader = unittest.TestLoader()
    # Normalize test names: if no dot, assume within esp_miner_e2e.tests
    tests = None
    if args.tests:
        tests = []
        for t in args.tests:
            if "." not in t:
                tests.append(f"esp_miner_e2e.tests.{t}")
            else:
                tests.append(t)
    suite = _discover(loader, tests)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


# Expose private helper of loader for listing
def _iter_suite_tests(self, suite):
    for t in suite:
        if isinstance(t, unittest.TestSuite):
            yield from _iter_suite_tests(self, t)
        else:
            yield t

unittest.TestLoader._iter_suite_tests = _iter_suite_tests  # type: ignore


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: List[str] | None = None):
    parser = _build_parser()
    args = parser.parse_args(argv)

    # Apply env overrides so config.load() picks them up
    _apply_overrides(args)

    # Execute command
    if args.cmd == "list":
        _cmd_list(args)
    elif args.cmd == "run":
        _cmd_run(args)
    else:  # pragma: no cover
        parser.error("Unknown command")


if __name__ == "__main__":  # pragma: no cover
    main()
