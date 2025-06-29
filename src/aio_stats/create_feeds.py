# SPDX-FileCopyrightText: 2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse

from .aio_client import AioClient

FEEDS = {
    "temp_rh": [
        "Temperature",
        "Relative Humidity",
        "Battery Percent",
        "Battery Voltage",
    ],
    "light": [
        "Light",
        "Autolux",
        "White",
        "Gain",
        "Integration-Time",
        "Battery Percent",
        "Battery Voltage",
    ],
    "lamp_timer": ["Notifier", "Lamptimer"],
}


def main(opts: argparse.Namespace) -> None:

    feeds = FEEDS[opts.sensor_type]
    if opts.prefix is not None:
        for i, f in enumerate(feeds):
            if f.startswith("Battery"):
                feeds[i] = f"{opts.prefix} {f}"

    client = AioClient()
    client.create_feeds(opts.group_name, feeds)


def runner() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "group_name", type=str, help="Set the group name to contain the feeds"
    )

    parser.add_argument(
        "sensor_type",
        choices=FEEDS.keys(),
        help="Specify the type of sensor which will set the feed names.",
    )

    parser.add_argument(
        "--prefix", type=str, help="Set a prefix for the battery related feeds."
    )

    args = parser.parse_args()

    main(args)
