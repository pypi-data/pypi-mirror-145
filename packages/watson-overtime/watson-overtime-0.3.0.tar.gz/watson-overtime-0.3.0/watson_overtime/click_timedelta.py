from typing import Any, Optional

import click
from pytimeparse import parse


class TimeDeltaParamType(click.ParamType):  # type: ignore
    name = "timedelta"

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> Optional[Any]:
        try:
            return parse(value)
        except ValueError:
            self.fail(f"{value!r} is not a valid ISO datetime", param, ctx)


TIME_DELTA = TimeDeltaParamType()
