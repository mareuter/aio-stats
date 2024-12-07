# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
import calendar
from datetime import datetime
from importlib.resources import files
import pathlib
import shutil

from jinja2 import Template


__all__ = ["runner"]


def main(opts: argparse.Namespace) -> None:
    index_page = pathlib.Path("index.html")

    if opts.generator == "year":
        template_data = {
            "years": [],
        }
        year_nav_template = files("aio_stats.data").joinpath("year_nav.html")
        j2_template = Template(
            year_nav_template.read_text(), trim_blocks=True, lstrip_blocks=True
        )
        for ydir in opts.data_dir.iterdir():
            if ydir.is_dir():
                template_data["years"].append(ydir.name)

        with index_page.open("w", encoding="utf-8") as ofile:
            ofile.write((j2_template.render(template_data)))

        shutil.copy(index_page, opts.data_dir)
        index_page.unlink()

    if opts.generator == "month":
        local_time = datetime.now()
        year = local_time.year

        month_nav_template = files("aio_stats.data").joinpath("month_nav.html")
        j2_template = Template(
            month_nav_template.read_text(), trim_blocks=True, lstrip_blocks=True
        )

        month_path: pathlib.Path = opts.data_dir / str(year)
        m_template_data = {"year": year, "months": []}
        for mdir in month_path.iterdir():
            if mdir.is_dir():
                month = int(mdir.name)
                m = calendar.Month(month)
                m_template_data["months"].append((mdir.name, m.name.title()))

        with index_page.open("w", encoding="utf-8") as ofile:
            ofile.write((j2_template.render(m_template_data)))

        shutil.copy(index_page, month_path)
        index_page.unlink()

    if opts.generator == "location":
        local_time = datetime.now()
        year = local_time.year
        if opts.month is not None:
            month = opts.month
        else:
            month = local_time.month

        m = calendar.Month(month)
        m_str = f"{month:02d}"

        location_nav_template = files("aio_stats.data").joinpath("location_nav.html")
        j2_template = Template(
            location_nav_template.read_text(), trim_blocks=True, lstrip_blocks=True
        )

        location_path: pathlib.Path = opts.data_dir / str(year) / m_str
        l_template_data = {"year": year, "month": m.name.title(), "locations": []}
        for lfile in location_path.iterdir():
            if lfile.is_file() and lfile.suffix == ".html" and lfile.stem != "index":
                loc = lfile.stem.split("_")[0]
                l_template_data["locations"].append((lfile.name, loc))

        with index_page.open("w", encoding="utf-8") as ofile:
            ofile.write((j2_template.render(l_template_data)))

        shutil.copy(index_page, location_path)
        index_page.unlink()


def runner() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "data_dir", type=pathlib.Path, help="Directory for page generation."
    )

    parser.add_argument("generator", choices=["year", "month", "location"])

    parser.add_argument(
        "--month", type=int, help="The month to generate the location page."
    )

    args = parser.parse_args()

    main(args)
