from datetime import timedelta
import json
import sys

import click
from humanize import naturaldelta

from . import __version__
from .click_timedelta import TIME_DELTA
from .watson_overtime import watson_overtime


def _build_work_diff_msg(diff: timedelta) -> str:
    msg = f"You are {naturaldelta(diff)} "
    if diff < timedelta(0):
        msg += "behind"
    else:
        msg += "ahead of"
    msg += " schedule."
    return msg


@click.command()
@click.version_option(version=__version__)
@click.option(
    "--watson-report",
    "-r",
    help="Read json style of watson report",
    type=click.File("r"),
    default=sys.stdin,
)
@click.option(
    "--working-hours",
    "-w",
    help="Amount of planned working time",
    type=TIME_DELTA,
    default="40 hours",
)
@click.option(
    "--period",
    "-p",
    help="Duration in which the amount of planned working time should be achieved",
    type=TIME_DELTA,
    default="1 week",
)
def main(
    watson_report: click.File, working_hours: timedelta, period: timedelta
) -> None:
    watson_report = json.load(watson_report)

    diff = watson_overtime(watson_report, working_hours, period)
    click.echo(_build_work_diff_msg(diff))


if __name__ == "__main__":
    main()
