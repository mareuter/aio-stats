# SPDX-FileCopyrightText: 2026 Michael Reuter
#
# SPDX-License-Identifier: MIT
import os
import pathlib

__all__ = ["InfluxIngestor"]


class InfluxIngestor:
    def __init__(self, conn_file: pathlib.Path) -> None:
        _ = self._get_conn_info(conn_file)

    def _db_conn_info(conn_file: pathlib.Path) -> dict[str, str]:
        content = conn_file.read_text().split(os.linesep)
        return {"host": content[0], "database": content[1], "token": content[2]}
