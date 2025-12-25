#!/usr/bin/env python3
"""Backwards-compatible entry point. Use `python -m stream_counter` instead."""

from stream_counter.__main__ import main

if __name__ == "__main__":
    exit(main())
