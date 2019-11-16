import pandas as pd
from flask import jsonify, request

from human_flow.app import app
from human_flow.data import bike_station


@app.route("/stations", methods=["GET"])
def stations():
    return jsonify(
        [
            {"id": id_, "lat": info[2], "lon": info[1]}
            for id_, info in bike_station.LOCATIONS.items()
        ]
    )


@app.route("/drives", methods=["POST"])
def drives():

    payload = request.json
    start = pd.Timestamp(payload["start"])
    end = pd.Timestamp(payload["end"])
    df = app.bike_drives_df
    df = df.loc[(df.departure_time >= start) & (df.return_time <= end)]

    return jsonify(
        [
            {
                "path": [[row.start_lon, row.start_lat], [row.end_lon, row.end_lat]],
                "timestamps": [str(row.departure_time), str(row.return_time)],
            }
            for _, row in df.iterrows()
        ]
    )
