# SPDX-FileCopyrightText: 2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
import pathlib
import tomllib

import plotly.graph_objects as go
import plotly.io as pio

from ..data_reader import DataReader
from ..helpers import load_feed_settings
from .raw_data import make_line_plot

__all__ = ["runner"]


def main(opts: argparse.Namespace) -> None:
    # Plotting things that only need to be done once.
    pio.templates.default = "plotly_dark"
    layout = dict(height=525, width=700)

    dr = DataReader(opts.file_path.expanduser())
    dr.read_day(opts.year, opts.month, opts.day)

    name = opts.file_path.parts[-1]
    shorts = load_feed_settings()["shorts"]
    short = shorts[name]

    fig = go.Figure(layout=layout)

    if opts.plot_info:
        info = tomllib.loads(opts.plot_info.expanduser().read_text())
        file_stem = info["file_stem"]
        plot_title = info["plot_title"]
    else:
        file_stem = "test"
        plot_title = file_stem.capitalize()

    make_line_plot(plot_title, short, fig, dr.table.to_pandas())

    if opts.html:
        fig.write_html(f"{file_stem}.html")
    else:
        fig.write_image(f"{file_stem}.svg")


def runner() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=pathlib.Path, help="Path to the data file.")
    parser.add_argument("year", type=int, help="Year for plotting.")
    parser.add_argument("month", type=int, help="Month for plotting.")
    parser.add_argument("day", type=int, help="Day for plotting.")

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
