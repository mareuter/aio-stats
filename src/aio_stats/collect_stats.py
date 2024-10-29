# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
from datetime import datetime, timedelta
from importlib.resources import files
import pathlib
import tomllib
from zoneinfo import ZoneInfo

import aio_stats


def main(opts: argparse.Namespace) -> None:
    now = datetime.now(ZoneInfo(opts.timezone))
    yesterday = now - timedelta(days=1)

    stat_feeds_file = files("aio_stats.data").joinpath("stat_feeds.toml")
    stat_feeds = tomllib.loads(stat_feeds_file.read_text())

    if opts.location is not None:
        locations = [opts.location]
    else:
        locations = list(stat_feeds["locations"])

    aioclient = aio_stats.AioClient()

    for location in locations:
        for feed in stat_feeds["locations"][location]["feeds"]:
            print(f"Processing {location}.{feed}")
            data = aioclient.fetch_data(f"{location}.{feed}", max_points=350)
            tdata = aioclient.transform_data(data, opts.timezone)
            stats = aio_stats.StatsMaker()
            stats.create_dataframe(tdata, feed)
            stats.filter_time(yesterday, now, opts.day_bound)
            stats.make_stats()
            stats.save_stats(opts.output_dir, location)


def runner() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "output_dir", type=pathlib.Path, help="Location for stats output."
    )

    parser.add_argument("--timezone", type=str, help="Set the timezone.")

    parser.add_argument(
        "--day-bound", action="store_true", help="Truncate timestamps to day bounds."
    )

    parser.add_argument(
        "--location", help="Provide the location for the feed data retrieval."
    )

    args = parser.parse_args()

    main(args)
