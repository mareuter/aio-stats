# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

import pathlib
import time
import tomllib

from Adafruit_IO import Client, Data, Feed, Group

from .transform_data_mixin import TransformDataMixin

__all__ = ["AioClient"]


class AioClient(TransformDataMixin):

    def __init__(self, key_file: pathlib.Path = None) -> None:
        """Class constructor.

        Parameters
        ----------
        key_file : pathlib.Path, optional
            Full path for a file containing the Adafruit IO secret, by default None
        """
        creds = self._get_credentials(key_file)
        self.client = Client(creds["AIO_USERNAME"], creds["AIO_KEY"])

    def _get_credentials(self, key_file: pathlib.Path) -> dict[str, str]:
        """Parse the Adafruit IO secrets from a file.

        Parameters
        ----------
        key_file : pathlib.Path
            File containing the Adafruit IO secrets.

        Returns
        -------
        dict[str, str]
            The parsed secrets.
        """
        if key_file is None:
            key_file = pathlib.Path("~/.auth/settings_aio.toml").expanduser()

        with key_file.open("rb") as cfile:
            cdict = tomllib.load(cfile)
        return cdict

    def create_feeds(self, group_name: str, feeds: list[str]) -> None:
        """Create AIO feeds in the requested group.

        Parameters
        ----------
        group_name : str
            The name of the group to create.
        feeds : list[str]
            The list of feeds to create.
        """
        group = Group(name=group_name)
        groups = self.client.groups()
        group_exists = False
        a_group = None
        for g in groups:
            if g.name == group.name:
                group_exists = True
                a_group = g
                break
        if not group_exists:
            print(f"Creating group {group.name}")
            a_group = self.client.create_group(group)

        time.sleep(5)

        for f in feeds:
            feed = Feed(name=f)
            a_feed = self.client.create_feed(feed, group_key=a_group.key)
            print(f"Created feed {a_feed.key}")
            time.sleep(5)

    def fetch_data(self, feed: str, max_points: int = None) -> list[Data]:
        """Retrieve data from Adafruit IO.

        Parameters
        ----------
        feed : str
            The feed to retrieve data from.
        max_points : int, optional
            The number of data points to retrieve, by default None

        Returns
        -------
        list[Data]
            The data points from the feed.
        """
        data = self.client.data(feed, max_results=max_points)
        # Adafruit IO returns newest data first.
        data.reverse()
        return data
