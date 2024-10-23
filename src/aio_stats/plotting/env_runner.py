# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
import calendar
from importlib.resources import files
import pathlib

from jinja2 import Template
import plotly.graph_objects as go
import plotly.io as pio

from ..data_reader import DataReader
from .creators import make_min_max_dist, make_stats_trend

__all__ = ["runner"]


def main(opts: argparse.Namespace) -> None:
    pio.templates.default = "plotly_dark"
    data_path = f"~/Documents/SensorData/{opts.location}"
    temp_data_path = f"{data_path}/temperature/{opts.year}/{opts.month:02}"
    rh_data_path = f"{data_path}/relative-humidity/{opts.year}/{opts.month:02}"

    m = calendar.Month(opts.month)

    temp_data = DataReader(pathlib.Path(temp_data_path))
    rh_data = DataReader(pathlib.Path(rh_data_path))

    temp_data.read_month()
    rh_data.read_month()

    temp_df = temp_data.table.to_pandas()
    rh_df = rh_data.table.to_pandas()

    layout = dict(height=500, width=700)

    fig1 = go.Figure(layout=layout)
    make_stats_trend("Temp", fig1, temp_df)

    fig2 = go.Figure(layout=layout)
    make_min_max_dist("Temp", fig2, temp_df)

    fig3 = go.Figure(layout=layout)
    make_stats_trend("RH", fig3, rh_df)

    fig4 = go.Figure(layout=layout)
    make_min_max_dist("RH", fig4, rh_df)

    template_data = {
        "location": opts.location.title(),
        "year": opts.year,
        "month": m.name.title(),
        "fig1": fig1.to_html(full_html=False),
        "fig2": fig2.to_html(full_html=False),
        "fig3": fig3.to_html(full_html=False),
        "fig4": fig4.to_html(full_html=False),
    }

    output_html = pathlib.Path(
        f"{opts.location.title()}_{opts.year}{opts.month:02d}.html"
    )
    input_template = files("aio_stats.data").joinpath("stats_plotting.html")

    with output_html.open("w", encoding="utf-8") as ofile:
        j2_template = Template(input_template.read_text())
        ofile.write((j2_template.render(template_data)))


def runner() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "location", help="Provide the location for the environment plot generation."
    )

    parser.add_argument("year", type=int, help="The year to read.")

    parser.add_argument("month", type=int, help="The month to read.")

    args = parser.parse_args()

    main(args)
