# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

from datetime import datetime
import pathlib

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

__all__ = ["StatsMaker"]


class StatsMaker:

    def __init__(self) -> None:
        """Class constructor."""
        self.df: pd.DataFrame = None
        self.timestamp: datetime = None
        self.stats: pa.Table = None

    def create_dataframe(
        self, data: list[tuple[datetime, float]], data_column: str
    ) -> None:
        """Take data and create dataframe.

        Parameters
        ----------
        data : list[tuple[datetime, float]]
            The input data.
        data_column : str
            The name of the feed for the column.
        """
        self.df = pd.DataFrame.from_records(
            data, index="datetime", columns=["datetime", data_column]
        )

    def filter_time(
        self, begin: datetime, end: datetime, day_bound: bool = False
    ) -> None:
        """Filter data by a time ranage.

        Parameters
        ----------
        begin : datetime
            The start time for the filter.
        end : datetime
            The end time for the filter.
        day_bound : bool, optional
            Remove time portion of timestamps, by default False
        """
        if day_bound:
            self.timestamp = begin.replace(hour=0, minutes=0, second=0)
            end = end.replace(hour=0, minutes=0, second=0)
        else:
            self.timestamp = begin
        self.df = self.df.loc[begin:end]

    def make_stats(self) -> None:
        """Calculate statistics from data."""
        column = self.df.columns[0]
        v_min = self.df.min().values[0]
        v_max = self.df.max().values[0]
        v_mean = self.df.mean().values[0]
        v_median = self.df.median().values[0]
        v_std = self.df.std().values[0]
        v_var = self.df.var().values[0]
        time_of_min = self.df[self.df[column] == v_min].index.tolist()[0]
        time_of_max = self.df[self.df[column] == v_max].index.tolist()[0]

        stats = {
            "min": [v_min],
            "max": [v_max],
            "mean": [v_mean],
            "median": [v_median],
            "std": [v_std],
            "var": [v_var],
            "time_of_min": [time_of_min],
            "time_of_max": [time_of_max],
            "day": [self.timestamp.day],
        }

        self.stats = pa.Table.from_pydict(stats)

    def save_stats(self, top_level: pathlib.Path, sub_path: str) -> None:
        """Save the calculated statistics to file.

        Parameters
        ----------
        top_level : pathlib.Path
            Main directory where the data should be saved.
        sub_path : str
            Sensor location.
        """
        tpath = (
            top_level
            / sub_path
            / self.df.columns[0]
            / str(self.timestamp.year)
            / f"{self.timestamp.strftime('%m')}"
        )
        tpath.mkdir(parents=True, exist_ok=True)
        outfile = tpath / f"{self.timestamp.strftime('%d')}.parquet"
        pq.write_table(self.stats, outfile)
