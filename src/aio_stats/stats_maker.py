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
        self.df: pd.DataFrame = None
        self.timestamp: datetime = None
        self.stats: pa.Table = None

    def create_dataframe(
        self, data: list[tuple[datetime, float]], data_column: str
    ) -> None:
        self.df = pd.DataFrame.from_records(
            data, index="datetime", columns=["datetime", data_column]
        )

    def filter_time(
        self, begin: datetime, end: datetime, day_bound: bool = False
    ) -> None:
        if day_bound:
            self.timestamp = begin.date()
            end = end.date()
        else:
            self.timestamp = begin
        self.df = self.df.loc[begin:end]

    def make_stats(self) -> None:
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
        }

        self.stats = pa.Table.from_pydict(stats)

    def save_stats(self, top_level: pathlib.Path, sub_path: str) -> None:
        tpath = top_level / sub_path / self.df.columns[0] / str(self.timestamp.year)
        tpath.mkdir(parents=True, exist_ok=True)
        outfile = tpath / f"{self.timestamp.strftime('%m_%d')}.parquet"
        pq.write_table(self.stats, outfile)
