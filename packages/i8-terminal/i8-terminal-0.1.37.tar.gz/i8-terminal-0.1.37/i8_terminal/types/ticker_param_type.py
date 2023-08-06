import os
from typing import List, Tuple

import investor8_sdk
from pandas import DataFrame, read_csv

from i8_terminal.config import SETTINGS_FOLDER
from i8_terminal.types.auto_complete_choice import AutoCompleteChoice


def sort_stocks(df: DataFrame) -> DataFrame:
    df["default_rank"] = 11
    default_rank = {
        "A": 1,
        "AAL": 2,
        "AAP": 3,
        "AAPL": 4,
        "AABV": 5,
        "ABC": 6,
        "ABMD": 7,
        "ABT": 8,
        "ACN": 9,
        "ADBE": 10,
    }
    df["default_rank"] = df["ticker"].apply(lambda x: default_rank.get(x, 11))
    df = df.sort_values("default_rank").reset_index(drop=True)
    return df[["ticker", "name"]]


def get_stocks() -> List[Tuple[str, str]]:
    companies_path = f"{SETTINGS_FOLDER}/companies.csv"
    if os.path.exists(companies_path):
        df = read_csv(companies_path)
    else:
        results = investor8_sdk.StockInfoApi().get_all_active_companies()
        df = DataFrame([d.to_dict() for d in results])[["ticker", "name"]]
        df = sort_stocks(df)
        df.to_csv(companies_path, index=False)

    return list(df.to_records(index=False))


class TickerParamType(AutoCompleteChoice):
    name = "ticker"

    def get_suggestions(self, keyword: str, pre_populate: bool = False) -> List[Tuple[str, str]]:
        if not self.is_loaded:
            self.set_choices(get_stocks())

        if pre_populate and keyword.strip() == "":
            return self._choices[: self.size]

        return self.search_keyword(keyword)

    def __repr__(self) -> str:
        return "TICKER"
