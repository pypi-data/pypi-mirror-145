import click
import datetime as dt
import traceback

from dateutil.parser import parse
from functools import wraps
from typing import Any, Callable, List, Optional

from metricflow.cli.constants import CONFIG_DWH_URL, CONFIG_DWH_PASSWORD, CONFIG_DWH_SCHEMA, CONFIG_MODEL_PATH
from metricflow.time.time_source import TimeSource

CONFIG_TEMPLATE = {
    CONFIG_DWH_URL: "",
    CONFIG_DWH_PASSWORD: "",
    CONFIG_DWH_SCHEMA: "",
    CONFIG_MODEL_PATH: "",
}


# Click Options
def query_options(function: Callable) -> Callable:
    """Common options for a query"""
    function = click.option(
        "--order",
        required=False,
        multiple=True,
        help='Metrics or dimensions to order by ("-" in front of a column means descending). For example: --order -ds',
    )(function)

    function = click.option(
        "--limit",
        required=False,
        type=str,
        help="Limit the number of rows out using an int or leave blank for no limit. For example: --limit 100",
        callback=lambda ctx, param, value: validate_limit(value),
    )(function)

    function = click.option(
        "--where",
        required=False,
        type=str,
        default=None,
        help='SQL-like where statement provided as a string. For example: --where "revenue > 100"',
    )(function)

    function = start_end_time_options(function)
    return function


def start_end_time_options(function: Callable) -> Callable:
    """Options for start_time and end_time."""
    function = click.option(
        "--start-time",
        required=False,
        type=str,
        default=None,
        help="Optional iso8601 timestamp to constraint the start time of the data (inclusive)",
        callback=lambda ctx, param, value: convert_to_datetime(value),
    )(function)

    function = click.option(
        "--end-time",
        required=False,
        type=str,
        default=None,
        help="Optional iso8601 timestamp to constraint the end time of the data (inclusive)",
        callback=lambda ctx, param, value: convert_to_datetime(value),
    )(function)
    return function


def separated_by_comma_option(option_name: str, help_msg: str = "") -> Callable:
    """Parse input containing a string separated by commma to a List."""

    def wraps(function: Callable) -> Callable:
        function = click.option(
            option_name,
            required=True,
            help=help_msg,
            callback=lambda ctx, param, value: parse_comma_separated_inputs(value),
        )(function)
        return function

    return wraps


# Parsers/Validators
def convert_to_datetime(datetime_str: Optional[str]) -> Optional[dt.datetime]:
    """Callback to convert string to datetime given as an iso8601 timestamp."""
    if datetime_str is None:
        return None

    if not valid_datetime(datetime_str):
        raise click.BadParameter("must be valid iso8601 timestamp")

    return dt.datetime.fromisoformat(datetime_str)


def valid_datetime(dt_str: str) -> bool:
    """Returns true if string is valid iso8601 timestamp, false otherwise"""
    try:
        parse(dt_str)
    except Exception:
        return False
    return True


def parse_comma_separated_inputs(value: str) -> List[str]:  # noqa: D
    # If comma exist, explode this into a list and return
    if "," in value:
        return [i.strip() for i in value.split(",")]

    # Return a list of the single value
    return [value]


def validate_limit(limit: Optional[str]) -> Optional[int]:
    """Validates and transform limit input."""
    if limit and not limit.isnumeric():
        raise click.BadParameter("limit must be an int. For no limit, do not pass this argument")
    return int(limit) if limit else None


# Misc
def exception_handler(func: Callable[..., Any]) -> Callable[..., Any]:  # type: ignore[misc]
    """Decorator to handle exceptions."""

    @wraps(func)
    def wrapper(*args, **kwargs):  # type: ignore
        try:
            func(*args, **kwargs)
        except Exception as e:
            # Checks if CLIContext has verbose flag set
            if args and hasattr(args[0], "verbose") and args[0].verbose is True:
                click.echo(traceback.format_exc())
            else:
                click.echo(f"\nERROR: {str(e)}")
            exit(1)

    return wrapper


class ServerTimeSource(TimeSource):
    """A time source that represents the current datetime in UTC."""

    def get_time(self) -> dt.datetime:  # noqa: D
        return dt.datetime.utcnow()
