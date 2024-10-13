# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
import pathlib
import time

import nbconvert
import papermill as pm
from traitlets.config import Config

from .process_helpers import run_cmd

__all__ = ["runner"]


def main(opts: argparse.Namespace) -> None:

    notebook_stem = "Environment_Stats"
    temp_notebook = pathlib.Path(f"{notebook_stem}_temp.ipynb")

    convert_to = [
        "jupytext",
        "--to",
        "ipynb",
        "-o",
        temp_notebook,
        f"md_notebooks/{notebook_stem}.md",
    ]
    output = run_cmd(convert_to)
    print(output)

    output_notebook = (
        f"{notebook_stem}_{opts.location.title()}_{opts.year}{opts.month:02d}.ipynb"
    )
    output_html = output_notebook.replace("ipynb", "html")

    report_notebook = pathlib.Path(output_notebook)
    report_output = pathlib.Path(output_html)

    pm.execute_notebook(
        temp_notebook,
        output_notebook,
        parameters=dict(location=opts.location, year=opts.year, month=opts.month),
    )

    c = Config()
    c.template_file = "full"
    c.HTMLExporter.exclude_input = True
    c.HTMLExporter.exclude_output_prompt = True

    converter = nbconvert.HTMLExporter(config=c)
    body, _ = converter.from_filename(output_notebook)
    with report_output.open("w") as ofile:
        ofile.writelines(body)

    while True:
        if report_output.exists():
            report_notebook.unlink()
            break
        time.sleep(0.01)
    temp_notebook.unlink()


def runner() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "location", help="Provide the location for the environment plot generation."
    )

    parser.add_argument("year", type=int, help="The year to read.")

    parser.add_argument("month", type=int, help="The month to read.")

    args = parser.parse_args()

    main(args)
