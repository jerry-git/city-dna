"""
isort:skip_file
"""

from pathlib import Path

import pandas as pd
from flask import Flask
from flask_cors import CORS

DRIVES_DATA_CSV = str(
    Path(__file__).parents[1] / "data" / "clean" / "bike" / "2019-07-09.csv"
)
bike_drives_df = pd.read_csv(
    DRIVES_DATA_CSV, parse_dates=["departure_time", "return_time"]
)

PREDICTIONS_CSV = str(Path(__file__).parents[1] / "data" / "predictions.csv")
predicted_drives_df = pd.read_csv(
    DRIVES_DATA_CSV, parse_dates=["departure_time", "return_time"]
)


WEATHER_DIR = str(
    Path(__file__).parents[1] / "data" / "clean" / "weather" / "2019-07-09.csv"
)
weather_df = pd.read_csv(WEATHER_DIR, parse_dates=["time"])
weather_df = weather_df.iloc[::6, :]


app = Flask(__name__)
CORS(app)
app.bike_drives_df = bike_drives_df
app.weather_df = weather_df
app.predicted_drives_df = predicted_drives_df
from human_flow import routes
