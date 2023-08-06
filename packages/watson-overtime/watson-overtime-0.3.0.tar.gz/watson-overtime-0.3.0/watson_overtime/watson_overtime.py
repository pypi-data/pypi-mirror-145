from datetime import datetime, timedelta
from typing import Any, Dict


def _calc_diff(
    worked_time: timedelta,
    start_date: datetime,
    end_date: datetime,
    working_hours: timedelta,
    period: timedelta,
) -> timedelta:
    total_time = end_date - start_date
    total_goal_work_time = working_hours * (total_time / period)
    return worked_time - total_goal_work_time


def watson_overtime(
    watson_report: Dict[str, Any], working_hours: timedelta, period: timedelta
) -> timedelta:
    worked_time = timedelta(seconds=watson_report["time"])
    start_date = datetime.fromisoformat(watson_report["timespan"]["from"])
    end_date = datetime.fromisoformat(watson_report["timespan"]["to"])

    return _calc_diff(worked_time, start_date, end_date, working_hours, period)
