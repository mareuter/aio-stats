# SPDX-FileCopyrightText: 2026 Michael Reuter
#
# SPDX-License-Identifier: MIT
import argparse
import pathlib

from .influx_ingestor import InfluxIngestor


def main(opts: argparse.Namespace) -> None:
    _ = InfluxIngestor(opts.conn_file.expanduser())


def runner() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--conn-file",
        default=pathlib.Path("~/.auth/influx3"),
        type=pathlib.Path,
        help="Set the path to the credential files for the database.",
    )

    args = parser.parse_args()

    main(args)
