# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

"""Module for common stuff."""

from datetime import datetime
from importlib.resources import files
import tomllib
from typing import Any

__all__ = ["Bounds", "cdleq_to_dict", "load_feed_settings"]

Bounds = tuple[datetime, datetime]


def cdleq_to_dict(items: str) -> dict[str, str | float]:
    """Parse comma-delimited list with equals items.

    This function takes a string of this format:

    item1=value1,item2=value2...

    and returns a dictionary with the items as string keys and the values
    as either strings or floats.

    Parameters
    ----------
    items : str
        Set of values to parse.

    Returns
    -------
    dict[str, str | float]
        The results from the string parsing.
    """
    result = {}
    for item in items.split(","):
        key, value = item.split("=")
        try:
            value = float(value)
        except ValueError:
            pass
        result[key] = value
    return result


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
