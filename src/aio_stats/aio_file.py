# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import csv
import pathlib

from Adafruit_IO import Data

__all__ = ["AioFile"]


class AioFile:

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
            creader = csv.reader(ifile)
            for row in creader:
                created_time = "T".join(row[3].split()[:-1]) + "Z"
                data_list.append(
                    Data(
                        id=row[0],
                        value=float(row[1]),
                        feed_id=int(row[2]),
                        created_at=created_time,
                    )
                )

        return data_list
