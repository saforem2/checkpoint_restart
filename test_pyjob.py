#!/usr/bin/env python
"""Backwards-compatibility shim for the packaged test job."""
from __future__ import annotations

from check_mate.examples.test_pyjob import main


if __name__ == "__main__":
    raise SystemExit(main())
