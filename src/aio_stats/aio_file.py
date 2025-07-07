# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

import csv
import pathlib

from Adafruit_IO import Data

from .transform_data_mixin import TransformDataMixin

__all__ = ["AioFile"]


class AioFile(TransformDataMixin):

    def __init__(self, data_file: pathlib.Path) -> None:
        """Class constructor."""
        self.data_file_path = data_file.expanduser()

    def read_data(self) -> list[Data]:
        """Read the CSV file to return data.

        Returns
        -------
        list[Data]
            The feed data from the file.
        """
        data_list = []
        with self.data_file_path.open() as ifile:
            creader = csv.DictReader(ifile)
            for row in creader:
                created_time = "T".join(row["created_at"].split()[:-1]) + "Z"
                data_list.append(
                    Data(
                        id=row["id"],
                        value=float(row["value"]),
                        feed_id=int(row["feed_id"]),
                        created_at=created_time,
                    )
                )

        return data_list
