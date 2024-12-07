# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

from datetime import datetime
from zoneinfo import ZoneInfo

from Adafruit_IO import Data

__all__ = ["TransformDataMixin"]


class TransformDataMixin:

    def transform_data(
        self, data: list[Data], timezone: str
    ) -> list[tuple[datetime, float]]:
        """Simplify data from that retrieved from Adafruit IO.

        Parameters
        ----------
        data : list[Data]
            List of data points.
        timezone : str
            Time zone for the data point translation.

        Returns
        -------
        list[tuple[datetime, float]]
            Simplified data points.
        """
        zone = ZoneInfo(timezone)
        tdata = [
            (datetime.fromisoformat(x.created_at).astimezone(zone), float(x.value))
            for x in data
        ]
        return tdata
