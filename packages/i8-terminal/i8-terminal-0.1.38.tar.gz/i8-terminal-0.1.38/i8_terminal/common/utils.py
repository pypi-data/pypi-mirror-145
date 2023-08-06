import enum
from difflib import SequenceMatcher
from typing import Optional

import click
from pandas import DataFrame
from rich.console import Console


class PlotType(enum.Enum):
    CHART = "chart"
    TABLE = "table"


def to_snake_case(value: str) -> str:
    return "_".join(value.lower().split())


def get_period_code(period: str) -> int:
    return {"1D": 1, "5D": 2, "1M": 3, "3M": 4, "6M": 5, "1Y": 6, "3Y": 7, "5Y": 8}.get(period, 3)


def get_period_days(period: str) -> int:
    return {"1D": 1, "5D": 5, "1M": 30, "3M": 90, "6M": 180, "1Y": 365, "3Y": 1095, "5Y": 1825}.get(period, 365)


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def export_data(export_df: DataFrame, export_path: str, index: bool = False) -> None:
    console = Console()
    extension = export_path.split(".")[-1]
    if extension == "csv":
        export_df.to_csv(export_path, index=index)
        console.print(f"Data is saved on: {export_path}")
    elif extension == "xlsx":
        export_df.to_excel(export_path, index=index)
        console.print(f"Data is saved on: {export_path}")
    else:
        console.print("export_path is not valid")


def validate_ticker(ctx: click.Context, param: str, value: str) -> Optional[str]:
    if len(value.replace(" ", "").split(",")) > 1:
        click.echo(click.style(f"`{value}` is not a valid ticker name.", fg="yellow"))
        ctx.exit()
    return value
