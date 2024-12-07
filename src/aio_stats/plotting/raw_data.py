# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

"""Module for plotting raw data."""

import pandas as pd
import plotly.graph_objects as go

__all__ = ["make_line_plot"]


def make_line_plot(
    plot_title: str, type: str, fig: go.Figure, df: pd.DataFrame
) -> None:
    # This function is used for plotting the raw data.
    y_axis_title = ""
    if type == "Temp":
        y_axis_title = "Temperature (°F)"
    if type == "RH":
        y_axis_title = "Relative Humidity (%)"

    trace = go.Scatter(
        mode="lines", line=dict(color="blue"), x=df.index, y=df[df.columns[0]]
    )

    fig.add_trace(trace)
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text=y_axis_title)
    fig.update_layout(
        title=dict(text=plot_title, xanchor="center", x=0.5), showlegend=False
    )
