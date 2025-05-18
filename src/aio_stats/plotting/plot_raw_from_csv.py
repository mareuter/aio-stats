# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
from datetime import datetime
import pathlib
import tomllib
from zoneinfo import ZoneInfo

import plotly.graph_objects as go
import plotly.io as pio

from ..aio_file import AioFile
from ..helpers import load_feed_settings
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

    af = AioFile(opts.file_path.expanduser())
    af.read_data()
    data_records = af.read_data()
    data = af.transform_data(data_records, opts.timezone)
    name = opts.file_path.name.split("-")[0].lower()
    if "_" in name:
        name = name.replace("_", "-")

    shorts = load_feed_settings()["shorts"]
    short = shorts[name]

    stats = StatsMaker()
    stats.create_dataframe(data, name)
    stats.filter_time(start_dt, end_dt)

    fig = go.Figure(layout=layout)

    if opts.plot_info:
        info = tomllib.loads(opts.plot_info.expanduser().read_text())
        file_stem = info["file_stem"]
        plot_title = info["plot_title"]
    else:
        file_stem = "test"
        plot_title = file_stem.capitalize()

    make_line_plot(plot_title, short, fig, stats.df)

    if opts.html:
        fig.write_html(f"{file_stem}.html")
    else:
        fig.write_image(f"{file_stem}.svg")


def runner() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=pathlib.Path, help="Path to the data file.")
    parser.add_argument(
        "timezone",
        type=str,
        help="The timezone for datetime conversion as data is in UTC.",
    )
    parser.add_argument(
        "--start", help="The datetime for the beginning of the data in ISO-8601 format."
    )
    parser.add_argument(
        "--end", help="The datetime for the end of the data in ISO-8601 format."
    )

    parser.add_argument(
        "--plot-info",
        type=pathlib.Path,
        help="Specify a file containing information for the plot.",
    )

    parser.add_argument(
        "--html", action="store_true", help="Create HTML plot instead of SVG."
    )

    args = parser.parse_args()

    main(args)
