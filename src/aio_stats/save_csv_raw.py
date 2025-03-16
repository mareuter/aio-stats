# SPDX-FileCopyrightText: 2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
from datetime import datetime, timedelta
import pathlib
from zoneinfo import ZoneInfo

from .aio_file import AioFile
from .stats_maker import StatsMaker


def main(opts: argparse.Namespace) -> None:
    one_day = timedelta(days=1)
    raw_date = datetime.strptime(opts.date, "%Y-%m-%d").astimezone(
        ZoneInfo(opts.timezone)
    )
    end = raw_date + one_day

    feed: str = opts.raw_file.stem.split("-")[0].lower()
    feed = feed.replace("_", "-")

    client = AioFile(opts.raw_file)
    data = client.read_data()
    tdata = client.transform_data(data, opts.timezone)
    stats = StatsMaker()
    stats.create_dataframe(tdata, feed)
    stats.filter_time(raw_date, end)
    stats.save_raw(opts.output_dir, opts.location)


def runner() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "raw_file", type=pathlib.Path, help="File containing the raw data."
    )

    parser.add_argument(
        "output_dir", type=pathlib.Path, help="Location for writing the raw data."
    )

    parser.add_argument(
        "location", type=str, help="The location for the data in lowercase."
    )

    parser.add_argument("timezone", type=str, help="Set the timezone.")

    parser.add_argument("date", help="Date to save for in YYYY-MM-DD format.")

    args = parser.parse_args()

    main(args)
