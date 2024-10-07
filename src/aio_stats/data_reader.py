# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import pathlib

import pyarrow.dataset as ds
import pyarrow.parquet as pq

__all__ = ["DataReader"]


class DataReader:

    def __init__(self, data_dir: pathlib.Path) -> None:
        """Class constructor.

        Parameters
        ----------
        data_dir : pathlib.Path
            Directory containing the structure data.
        """
        self.data_dir = data_dir.expanduser()

    def read_all(self) -> None:
        """Read all data from directory."""
        p = ds.partitioning(field_names=["year", "month"])
        self.table = pq.read_table(self.data_dir, partitioning=p)

    def read_month(self) -> None:
        """Read data from specific month."""
        self.table = pq.read_table(self.data_dir)

    def read_year(self) -> None:
        """Read data from specific year."""
        p = ds.partitioning(field_names=["month"])
        self.table = pq.read_table(self.data_dir, partitioning=p)
