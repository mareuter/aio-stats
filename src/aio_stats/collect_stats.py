# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
from datetime import datetime, timedelta
import pathlib
import tomllib

import aio_stats


def main(opts: argparse.Namespace) -> None:
    now = datetime.now()
    yesterday = now - timedelta(days=1)

    config_file: pathlib.Path = opts.config_file.expanduser()
    with config_file.open("rb") as cfile:
        cdict = tomllib.load(cfile)

    # # Create top level-directories
    # for entry in cdict:
    #     for feed in cdict[entry]["feeds"]:
    #         opath = opts.output_dir / entry / feed / yesterday.year
    #         if not opath.exists():
    #             opath.mkdir(parents=True)

    aioclient = aio_stats.AioClient()

    for entry in cdict:
        for feed in cdict[entry]["feeds"]:
            data = aioclient.fetch_data(f"{entry}.{feed}", max_points=350)
            tdata = aioclient.transform_data(data, opts.timezone)
            stats = aio_stats.StatsMaker()
            stats.create_dataframe(tdata, feed)
            stats.filter_time(yesterday, now, opts.day_bound)
            stats.make_stats()
            stats.save_stats(opts.output_dir, entry)


def runner() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "output_dir", type=pathlib.Path, help="Location for stats output."
    )
    parser.add_argument(
        "config_file",
        type=pathlib.Path,
        help="Configuration of feeds to collect stats for.",
    )
    parser.add_argument("--timezone", type=str, help="Set the timezone.")

    parser.add_argument(
        "--day-bound", action="store_true", help="Truncate timestamps to day bounds."
    )

    args = parser.parse_args()

    main(args)
