# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
import calendar
from datetime import datetime, timedelta
from importlib.resources import files
import pathlib
import shutil
import tomllib

from jinja2 import Template
import plotly.graph_objects as go
import plotly.io as pio

from . import creators
from ..data_reader import DataReader

__all__ = ["runner"]


def main(opts: argparse.Namespace) -> None:
    # Plotting things that only need to be done once.
    pio.templates.default = "plotly_dark"
    layout = dict(height=525, width=700)

    input_template = files("aio_stats.data").joinpath("stats_plotting.html")
    j2_template = Template(input_template.read_text())

    if opts.year is None and opts.month is None:
        local_time = datetime.now()
        if opts.shift_day:
            local_time -= timedelta(days=1)
        year = local_time.year
        month = local_time.month
    else:
        year = opts.year
        month = opts.month

    m = calendar.Month(month)
    m_str = f"{month:02d}"

    stat_feeds_file = files("aio_stats.data").joinpath("stat_feeds.toml")
    stat_feeds = tomllib.loads(stat_feeds_file.read_text())

    if opts.location is not None:
        locations = [opts.location]
    else:
        locations = list(stat_feeds["locations"])

    fig_paths = []
    for location in locations:

        template_data = {
            "location": location.title(),
            "year": year,
            "month": m.name.title(),
            "figs": [],
        }

        top_data_path = f"~/Documents/SensorData/{location}"
        location_stem = f"{location.title()}_{year}{m_str}"
        fig_path = pathlib.Path(location_stem)
        fig_path.mkdir(exist_ok=True)
        fig_paths.append(fig_path)

        for feed in stat_feeds["locations"][location]["feeds"]:
            data_path = f"{top_data_path}/{feed}/{year}/{m_str}"

            data = DataReader(pathlib.Path(data_path))
            data.read_month()
            df = data.table.to_pandas()

            plot_functions = stat_feeds["plotting"][feed]
            for plot_function in plot_functions:
                short_name = stat_feeds["shorts"][feed]
                fig = go.Figure(layout=layout)
                plotter = getattr(creators, f"make_{plot_function}")
                plotter(short_name, fig, df)
                fig_file: pathlib.Path = fig_path / f"{feed}_{plot_function}.svg"
                fig.write_image(fig_file)
                template_data["figs"].append(fig_file)

        output_html = pathlib.Path(f"{location_stem}.html")

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

        for p in fig_paths:
            try:
                shutil.copytree(
                    p, full_path / p, copy_function=shutil.copy, dirs_exist_ok=True
                )
            except OSError:
                # This is shutil.copy trying to copy the directory.
                pass
            shutil.rmtree(p)


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

    parser.add_argument(
        "--shift-day",
        action="store_true",
        help="Shift the time used by a day to support data collection.",
    )

    args = parser.parse_args()

    main(args)
