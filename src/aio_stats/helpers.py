# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

"""Module for common stuff."""

from importlib.resources import files
import tomllib
from typing import Any

__all__ = ["load_feed_settings"]


def load_feed_settings() -> dict[str, Any]:
    """Return the feed settings.

    Returns
    -------
    dict[str, Any]
        The feed settings.
    """
    stat_feeds_file = files("aio_stats.data").joinpath("stat_feeds.toml")
    stat_feeds = tomllib.loads(stat_feeds_file.read_text())
    return stat_feeds
