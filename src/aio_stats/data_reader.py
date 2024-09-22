# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import pathlib

import pyarrow as pa
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
        p = pa.dataset.partitioning(field_names=["year", "month"])
        self.table = pq.read_table(data_dir, partitioning=p)
