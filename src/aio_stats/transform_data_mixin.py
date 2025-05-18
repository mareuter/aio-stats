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
    ) -> list[tuple[datetime, float | str]]:
        """Simplify data from that retrieved from Adafruit IO.

        Parameters
        ----------
        data : list[Data]
            List of data points.
        timezone : str
            Time zone for the data point translation.

        Returns
        -------
        list[tuple[datetime, float | str]]
            Simplified data points.
        """
        zone = ZoneInfo(timezone)
        tdata = []
        for x in data:
            t = datetime.fromisoformat(x.created_at).astimezone(zone)
            try:
                v = float(x.value)
            except ValueError:
                v = x.value
            tdata.append((t, v))
        return tdata
