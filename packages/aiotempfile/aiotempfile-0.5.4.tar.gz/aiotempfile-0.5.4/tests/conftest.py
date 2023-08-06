#!/usr/bin/env python

"""Configures execution of pytest."""

from pytest_asyncio.plugin import Mode


def pytest_configure(config):
    """pytest configuration hook."""
    config.option.asyncio_mode = Mode.AUTO
