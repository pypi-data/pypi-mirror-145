import investor8_sdk
from pandas import DataFrame
from rich.console import Console

from i8_terminal.commands.earnings import earnings
from i8_terminal.common.formatting import get_formatter
from i8_terminal.common.layout import df2Table, format_df


def get_upcoming_earnings_df(size: int) -> DataFrame:
    earnings = investor8_sdk.EarningsApi().get_upcoming_earnings(size=size)
    earnings = [d.to_dict() for d in earnings]
    df = DataFrame(earnings)
    return df


def format_upcoming_earnings_df(df: DataFrame, target: str) -> DataFrame:
    formatters = {
        "latest_price": get_formatter("number", target),
        "change": get_formatter("perc", target),
        "fyq": get_formatter("fyq", target),
        "eps_ws": get_formatter("number", target),
    }
    col_names = {
        "ticker": "Ticker",
        "name": "Name",
        "exchange": "Exchange",
        "sector": "Sector",
        "latest_price": "Price",
        "change": "Change",
        "actual_report_date": "Report Date",
        "fyq": "Period",
        "call_time": "Call Time",
        "eps_ws": "Eps Cons.",
    }
    return format_df(df, col_names, formatters)


@earnings.command()
def upcoming() -> None:
    """Lists upcoming company earnings."""
    console = Console()
    with console.status("Fetching data...", spinner="material"):
        df = get_upcoming_earnings_df(size=20)
    df_formatted = format_upcoming_earnings_df(df, "console")
    table = df2Table(df_formatted)
    console.print(table)
