if __name__ == "__main__":
    import pandas as pd
    from pathlib import Path
    import json

    RESULT_PATH = (
        Path(__file__).parents[1] / "data" / "clean" / "bike" / "2019-07-09.json"
    )

    DRIVES_DATA_CSV = str(
        Path(__file__).parents[1] / "data" / "clean" / "bike" / "2019-07-09.csv"
    )
    df = pd.read_csv(DRIVES_DATA_CSV, parse_dates=["departure_time", "return_time"])

    res = []
    for _, row in df.iterrows():
        trip = {
            "path": [[row.start_lat, row.start_lon], [row.end_lat, row.end_lon]],
            "timestamps": [str(row.departure_time), str(row.return_time)],
        }
        res.append(trip)
    with open(RESULT_PATH, "w") as f:
        f.write(json.dumps(res))
