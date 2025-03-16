# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
from datetime import datetime, timedelta
import json
import pathlib
from zoneinfo import ZoneInfo

from .aio_client import AioClient
from .helpers import Bounds, cdleq_to_dict, load_feed_settings
from .stats_maker import StatsMaker


def main(opts: argparse.Namespace) -> None:
    zone = ZoneInfo(opts.timezone)
    now = datetime.now(zone)
    yesterday = now - timedelta(days=1)

    stat_feeds = load_feed_settings()

    if opts.location is not None:
        locations = [opts.location]
    else:
        locations = list(stat_feeds["locations"])

    aioclient = AioClient()

    for location in locations:
        for feed in stat_feeds["locations"][location]["feeds"]:
            print(f"Processing {location}.{feed}")
            if opts.calc_points:
                delay = stat_feeds["locations"][location]["delay"]
                if opts.day_bound:
                    timestamp = yesterday.replace(hour=0, minute=0, second=0)
                else:
                    timestamp = yesterday
                max_points = round((now - timestamp) / timedelta(minutes=delay)) + 10
                print(max_points)
            else:
                max_points = 350
            data = aioclient.fetch_data(f"{location}.{feed}", max_points=max_points)
            tdata = aioclient.transform_data(data, opts.timezone)
            stats = StatsMaker()
            stats.create_dataframe(tdata, feed)
            stats.filter_time(yesterday, now, opts.day_bound)
            stats.save_raw(opts.output_dir, location)
            # Mainly for autolux
            bounds: Bounds | None = None
            try:
                bound_feed = stat_feeds["locations"][location]["bounds"][feed]
                bound_data = aioclient.fetch_data(
                    f"{location}.{bound_feed}", max_points=5
                )
                tbound_data = aioclient.transform_data(bound_data, opts.timezone)
                for items in tbound_data:
                    if items[0].date() == yesterday.date():
                        bound_info = items[1]
                bound_set = cdleq_to_dict(bound_info)
                # Save bounds info
                ipath = (
                    opts.output_dir
                    / "info"
                    / location
                    / feed
                    / str(stats.timestamp.year)
                    / f"{stats.timestamp.strftime('%m')}"
                )
                ipath.mkdir(parents=True, exist_ok=True)
                outfile = ipath / f"{stats.timestamp.strftime('%d')}.json"
                with outfile.open("w") as ofile:
                    json.dump(bound_set, ofile)
                bounds = (
                    datetime.fromtimestamp(bound_set["sunrise"]).astimezone(zone),
                    datetime.fromtimestamp(bound_set["on"]).astimezone(zone),
                )
            except KeyError:
                pass
            stats.make_stats(bounds)
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

    parser.add_argument(
        "--calc-points",
        action="store_true",
        help="Calculate the number of points to ask from Adafruit IO.",
    )

    args = parser.parse_args()

    main(args)
