# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

"""Module to create plots for statistics."""

import pandas as pd
import plotly.graph_objects as go

__all__ = ["make_min_max_dist", "make_stats_trend"]


def make_min_max_dist(type: str, fig: go.Figure, df: pd.DataFrame) -> None:
    plot_title = "Time in Day of Min/Max "
    if type == "Temp":
        plot_title += "Temperature"
    if type == "RH":
        plot_title += "Relative Humidity"

    t_min = [
        (
            x.to_pydatetime() - x.to_pydatetime().replace(hour=0, minute=0, second=0)
        ).seconds
        / 3600
        for x in df["time_of_min"]
    ]
    t_max = [
        (
            x.to_pydatetime() - x.to_pydatetime().replace(hour=0, minute=0, second=0)
        ).seconds
        / 3600
        for x in df["time_of_max"]
    ]

    binning = dict(start=0, end=24, size=1)
    min_time_trace = go.Histogram(x=t_min, xbins=binning, name="min")
    max_time_trace = go.Histogram(x=t_max, xbins=binning, name="max")

    fig.add_trace(min_time_trace)
    fig.add_trace(max_time_trace)
    fig.update_xaxes(title_text="Hour in Day", range=(0, 24))
    fig.update_layout(title=dict(text=plot_title, xanchor="center", x=0.5))
    fig.show()


def make_stats_trend(type: str, fig: go.Figure, df: pd.DataFrame) -> None:
    y_axis_title = ""
    plot_title = ""
    if type == "Temp":
        y_axis_title = "Temperature (°F)"
        plot_title = "Temperature Trend"
    if type == "RH":
        y_axis_title = "Relative Humidity (%)"
        plot_title = "Relative Humidity Trend"

    mean_trace = go.Scatter(
        mode="markers",
        marker_color="black",
        x=df.day,
        y=df["mean"],
        error_y=dict(type="data", array=df["std"], visible=True),
    )
    max_trace = go.Scatter(mode="lines", line=dict(color="blue"), x=df.day, y=df["max"])
    min_trace = go.Scatter(mode="lines", line=dict(color="blue"), x=df.day, y=df["min"])

    fig.add_trace(mean_trace)
    fig.add_trace(max_trace)
    fig.add_trace(min_trace)
    fig.update_xaxes(title_text="Day in Month", tickmode="array", tickvals=df.day)
    fig.update_yaxes(title_text=y_axis_title)
    fig.update_layout(
        title=dict(text=plot_title, xanchor="center", x=0.5), showlegend=False
    )
    fig.show()