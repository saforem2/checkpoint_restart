"""Thin wrappers that expose bundled shell utilities as console scripts."""

from __future__ import annotations

import argparse
import signal
import subprocess
import sys
from importlib import resources
from typing import Iterable

from . import __version__

_RESOURCE_PACKAGE = "check_mate.resources"

_TOOLS: tuple[tuple[str, str, str, str | None], ...] = (
    (
        "get-healthy-nodes",
        "get_healthy_nodes.sh",
        "Select responsive nodes from a nodefile.",
        (
            "Selects a subset of responsive nodes from a nodefile by delegating to "
            "the bundled shell implementation."
        ),
    ),
    (
        "launcher",
        "launcher.sh",
        "Launch the check-mate job runner.",
        None,
    ),
    (
        "flush",
        "flush.sh",
        "Flush all check-mate caches.",
        None,
    ),
)
_TOOL_MAP = {name: (script, help_text, desc) for name, script, help_text, desc in _TOOLS}


def _run_shell(script: str, argv: Iterable[str]) -> int:
    """Execute a packaged shell script with ``bash``."""
    try:
        resource = resources.files(_RESOURCE_PACKAGE) / script
    except (FileNotFoundError, ModuleNotFoundError):  # pragma: no cover - importlib edge cases
        raise RuntimeError(f"Unable to locate bundled script: {script}") from None

    with resources.as_file(resource) as path:
        process = subprocess.Popen(
            ["bash", str(path), *argv],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            stdout, stderr = process.communicate()
        except KeyboardInterrupt:  # pragma: no cover - user interrupt
            try:
                process.send_signal(signal.SIGINT)
            except ProcessLookupError:  # pragma: no cover - process already exited
                pass
            process.wait()
            print("Execution interrupted by user.", file=sys.stderr)
            return 130

    if stdout:
        print(stdout, end="")
    if process.returncode != 0:
        print(
            f"Error running script '{script}':\n{stderr}",
            file=sys.stderr,
        )
    return process.returncode


def _dispatch(command: str, argv: list[str] | None = None) -> int:
    script, _, description = _TOOL_MAP[command]
    parser = argparse.ArgumentParser(
        prog=f"check-mate {command}",
        description=description,
    )
    parser.add_argument("args", nargs=argparse.REMAINDER)
    ns = parser.parse_args(argv)
    return _run_shell(script, ns.args)


def get_healthy_nodes(argv: list[str] | None = None) -> int:
    return _dispatch("get-healthy-nodes", argv)


def launcher(argv: list[str] | None = None) -> int:
    return _dispatch("launcher", argv)


def flush(argv: list[str] | None = None) -> int:
    return _dispatch("flush", argv)


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - convenience dispatcher
    parser = argparse.ArgumentParser(
        prog="check-mate",
        description="Utility command dispatcher for check-mate tools.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, (script, help_text, desc) in _TOOL_MAP.items():
        sub = subparsers.add_parser(name, help=help_text, description=desc)
        sub.add_argument("args", nargs=argparse.REMAINDER)
        sub.set_defaults(script=script)

    ns = parser.parse_args(argv)
    return _run_shell(ns.script, ns.args)


if __name__ == "__main__":  # pragma: no cover - script entry point
    sys.exit(main())
