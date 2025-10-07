"""Thin wrappers that expose bundled shell utilities as console scripts."""

from __future__ import annotations

import argparse
import subprocess
import sys
from importlib import resources
from typing import Iterable

_RESOURCE_PACKAGE = "check_mate.resources"


def _run_shell(script: str, argv: Iterable[str]) -> int:
    """Execute a packaged shell script with ``bash``."""
    try:
        resource = resources.files(_RESOURCE_PACKAGE) / script
    except (FileNotFoundError, ModuleNotFoundError):  # pragma: no cover - importlib edge cases
        raise RuntimeError(f"Unable to locate bundled script: {script}") from None

    with resources.as_file(resource) as path:
        result = subprocess.run(["bash", str(path), *argv], check=False)
    return result.returncode


def get_healthy_nodes(argv: list[str] | None = None) -> int:
    """Proxy console script for :mod:`get_healthy_nodes.sh`."""
    parser = argparse.ArgumentParser(
        prog="get-healthy-nodes",
        description=(
            "Select a subset of responsive nodes from a nodefile by delegating to the "
            "bundled shell implementation."
        ),
        add_help=False,
    )
    parser.add_argument("args", nargs=argparse.REMAINDER)
    ns = parser.parse_args(argv)
    return _run_shell("get_healthy_nodes.sh", ns.args)


def launcher(argv: list[str] | None = None) -> int:
    """Proxy console script for :mod:`launcher.sh`."""
    parser = argparse.ArgumentParser(prog="check-mate-launcher", add_help=False)
    parser.add_argument("args", nargs=argparse.REMAINDER)
    ns = parser.parse_args(argv)
    return _run_shell("launcher.sh", ns.args)


def flush(argv: list[str] | None = None) -> int:
    """Proxy console script for :mod:`flush.sh`."""
    parser = argparse.ArgumentParser(prog="check-mate-flush", add_help=False)
    parser.add_argument("args", nargs=argparse.REMAINDER)
    ns = parser.parse_args(argv)
    return _run_shell("flush.sh", ns.args)


def main() -> int:  # pragma: no cover - convenience dispatcher
    parser = argparse.ArgumentParser(
        prog="check-mate",
        description="Utility command dispatcher for check-mate tools.",
    )
    parser.add_argument(
        "tool",
        choices={"get-healthy-nodes", "launcher", "flush"},
        help="Select which bundled tool to execute.",
    )
    parser.add_argument("args", nargs=argparse.REMAINDER)
    parsed = parser.parse_args()

    mapping = {
        "get-healthy-nodes": get_healthy_nodes,
        "launcher": launcher,
        "flush": flush,
    }
    return mapping[parsed.tool](parsed.args)


if __name__ == "__main__":  # pragma: no cover - script entry point
    sys.exit(main())
