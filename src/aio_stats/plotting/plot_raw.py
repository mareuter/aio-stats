# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
from datetime import datetime
import pathlib
from zoneinfo import ZoneInfo

import plotly.graph_objects as go
import plotly.io as pio

from ..aio_file import AioFile
from .raw_data import make_line_plot
from ..stats_maker import StatsMaker

__all__ = ["runner"]


def main(opts: argparse.Namespace) -> None:
    # Plotting things that only need to be done once.
    pio.templates.default = "plotly_dark"
    layout = dict(height=525, width=700)

    tzinfo = ZoneInfo(opts.timezone)
    if opts.start is not None:
        start_dt = datetime.fromisoformat(opts.start).astimezone(tzinfo)
    else:
        start_dt = opts.start
    if opts.end is not None:
        end_dt = datetime.fromisoformat(opts.end).astimezone(tzinfo)
    else:
        end_dt = opts.end

    if "file_path" in opts:
        af = AioFile(opts.file_path.expanduser())
        af.read_data()
        data_records = af.read_data()
        data = af.transform_data(data_records, opts.timezone)
        name = opts.file_path.name.split("-")[0].lower()
        if opts.file_path.name.startswith("Temperature"):
            short = "Temp"

    if "feed" in opts:
        print("B")

    stats = StatsMaker()
    stats.create_dataframe(data, name)
    stats.filter_time(start_dt, end_dt)

    fig = go.Figure(layout=layout)

    make_line_plot("Test", short, fig, stats.df)

    fig_file: pathlib.Path = "test.svg"
    fig.write_image(fig_file)


def runner() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start", help="The datetime for the beginning of the data in ISO-8601 format."
    )
    parser.add_argument(
        "--end", help="The datetime for the end of the data in ISO-8601 format."
    )
    parser.add_argument(
        "--timezone",
        type=str,
        required=True,
        help="The timezone for datetime conversion as data is in UTC.",
    )

    subparsers = parser.add_subparsers(help="subcommand help")

    data_file = subparsers.add_parser("file", help="Read and plot a data file.")
    data_file.add_argument(
        "file_path", type=pathlib.Path, help="Path to the data file."
    )

    client_call = subparsers.add_parser(
        "client", help="Read data from Adafruit IO and plot."
    )
    client_call.add_argument(
        "feed", help="The Adafruit IO feed name to gather data from."
    )

    args = parser.parse_args()

    main(args)
