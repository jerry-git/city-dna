if __name__ == "__main__":
    import pandas as pd
    from pathlib import Path
    import datetime as dt

    DATA_CSV = (
        Path(__file__).parents[1]
        / "data-raw"
        / "raw"
        / "weather"
        / "Helsinki_weather_data.csv"
    )

    df = pd.read_csv(DATA_CSV)

    df.columns = [
        "year",
        "month",
        "day",
        "time",
        "tz",
        "cloud_amount_1_8",
        "pressure",
        "humidity_percentage",
        "precipitation",
        "snow_depth",
        "air_temperature",
        "dew_point_temperature",
        "horizontal_visibility",
        "wind_direction",
        "gust_speed",
        "wind_speed",
    ]

    df = df.fillna(method="ffill")

    df["time"] = df.apply(
        lambda row: pd.Timestamp(
            dt.datetime(
                row.year,
                row.month,
                row.day,
                int(row.time.split(":")[0]),
                int(row.time.split(":")[1]),
            )
        ),
        axis=1,
    )

    df = df.drop(columns=["year", "month", "day", "tz"])

    RESULT_CSV = (
        Path(__file__).parents[1] / "data" / "clean" / "weather" / "2019-07-09.csv"
    )
    df.to_csv(RESULT_CSV, index=False)
