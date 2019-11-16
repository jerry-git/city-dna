if __name__ == "__main__":

    from pathlib import Path

    import pandas as pd

    from human_flow.data.bike_station import LOCATIONS

    DATA_DIR = Path(__file__).parents[1] / "data-raw" / "raw" / "bike"
    START = pd.Timestamp("2019-07-15 00:00:00")
    END = pd.Timestamp("2019-09-16 00:00:00")

    df1 = pd.read_csv(
        str(DATA_DIR / "2019-07.csv"), parse_dates=["Departure", "Return"]
    )
    df2 = pd.read_csv(
        str(DATA_DIR / "2019-08.csv"), parse_dates=["Departure", "Return"]
    )
    df3 = pd.read_csv(
        str(DATA_DIR / "2019-09.csv"), parse_dates=["Departure", "Return"]
    )

    df = pd.concat([df1, df2, df3])
    df.columns = [
        "departure_time",
        "return_time",
        "departure_station_id",
        "departure_station_name",
        "return_station_id",
        "return_station_name",
        "distance",
        "duration",
    ]
    df = df.sort_values(by=["departure_time"])
    df = df.dropna()
    df = df.loc[(df.departure_time >= START) & (df.return_time <= END)]

    no_location_ids = set(df.departure_station_id.unique()) - set(LOCATIONS)

    for id_ in no_location_ids:
        df = df[df.departure_station_id != id_]
        df = df[df.return_station_id != id_]

    df["start_lat"] = df.apply(
        lambda row: LOCATIONS[row.departure_station_id][2], axis=1
    )
    df["start_lon"] = df.apply(
        lambda row: LOCATIONS[row.departure_station_id][1], axis=1
    )
    df["end_lat"] = df.apply(lambda row: LOCATIONS[row.return_station_id][2], axis=1)
    df["end_lon"] = df.apply(lambda row: LOCATIONS[row.return_station_id][1], axis=1)

    RESULT_CSV = (
        Path(__file__).parents[1] / "data" / "clean" / "bike" / "2019-07-09.csv"
    )
    df.to_csv(RESULT_CSV, index=False)
