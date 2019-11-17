import logging

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


@app.route("/weather", methods=["GET"])
def weather():
    df = app.weather_df
    return jsonify(
        [
            {
                "time": str(row.time),
                "temp": row.air_temperature,
                "rain": row.precipitation,
                "clouds": row.cloud_amount_1_8,
            }
            for _, row in df.iterrows()
        ]
    )


@app.route("/drives", methods=["POST"])
def drives():
    predicted = request.args.get("predicted")
    if predicted:
        logging.warning("Returning predictions")
    payload = request.json
    start = pd.Timestamp(payload["start"])
    end = pd.Timestamp(payload["end"])
    df = app.predicted_drives_df if predicted else app.bike_drives_df
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
