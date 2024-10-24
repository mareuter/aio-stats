# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
import calendar
from datetime import datetime
from importlib.resources import files
import pathlib
import shutil
import tomllib

from jinja2 import Template
import plotly.graph_objects as go
import plotly.io as pio

from ..data_reader import DataReader
from .creators import make_min_max_dist, make_stats_trend

__all__ = ["runner"]


def main(opts: argparse.Namespace) -> None:
    # Plotting things that only need to be done once.
    pio.templates.default = "plotly_dark"
    layout = dict(height=500, width=700)

    input_template = files("aio_stats.data").joinpath("stats_plotting.html")
    j2_template = Template(input_template.read_text())

    if opts.year is None and opts.month is None:
        local_time = datetime.now()
        year = local_time.year
        month = local_time.month
    else:
        year = opts.year
        month = opts.month

    m = calendar.Month(month)
    m_str = f"{month:02d}"

    stat_feeds_file = files("aio_stats.data").joinpath("stat_feeds.toml")
    with stat_feeds_file.open("rb") as cfile:
        stat_feeds = tomllib.load(cfile)

    if opts.location is not None:
        locations = [opts.location]
    else:
        locations = list(stat_feeds["locations"])

    for location in locations:

        template_data = {
            "location": location.title(),
            "year": year,
            "month": m.name.title(),
            "figs": [],
        }

        top_data_path = f"~/Documents/SensorData/{location}"

        for feed in stat_feeds["locations"][location]["feeds"]:
            data_path = f"{top_data_path}/{feed}/{year}/{m_str}"

            data = DataReader(pathlib.Path(data_path))
            data.read_month()
            df = data.table.to_pandas()

            plot_functions = stat_feeds["plotting"][feed]
            for plot_function in plot_functions:
                short_name = stat_feeds["shorts"][feed]
                fig = go.Figure(layout=layout)
                if plot_function == "stats_trend":
                    make_stats_trend(short_name, fig, df)
                if plot_function == "min_max_dist":
                    make_min_max_dist(short_name, fig, df)
                template_data["figs"].append(fig.to_html(full_html=False))

        output_html = pathlib.Path(f"{location.title()}_{year}{m_str}.html")

        with output_html.open("w", encoding="utf-8") as ofile:
            ofile.write((j2_template.render(template_data)))

    if opts.output_dir is not None:
        full_path = opts.output_dir.expanduser() / str(year) / m_str
        if not full_path.exists():
            full_path.mkdir(parents=True)

        curdir = pathlib.Path(".")
        for html_file in curdir.glob("*.html"):
            shutil.copy(html_file, full_path)
            html_file.unlink()


def runner() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--location", help="Provide the location for the environment plot generation."
    )

    parser.add_argument("--year", type=int, help="The year to read.")

    parser.add_argument("--month", type=int, help="The month to read.")

    parser.add_argument(
        "--output-dir", type=pathlib.Path, help="Directory to move output to."
    )

    args = parser.parse_args()

    main(args)
