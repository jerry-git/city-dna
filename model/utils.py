from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parents[1] / "data" / "clean"


def load_rides_df():
    return pd.read_csv(
        str(DATA_DIR / "bike" / "2019-07-09.csv"),
        parse_dates=["departure_time", "return_time"],
    )


def load_weather_df():
    return pd.read_csv(
        str(DATA_DIR / "weather" / "2019-07-09.csv"), parse_dates=["time"]
    )
