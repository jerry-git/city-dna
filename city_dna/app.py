"""
isort:skip_file
"""
from pathlib import Path

import pandas as pd
from flask import Flask

DRIVES_DATA_CSV = str(
    Path(__file__).parents[1] / "data" / "clean" / "bike" / "2019-07-09.csv"
)
bike_drives_df = pd.read_csv(
    DRIVES_DATA_CSV, parse_dates=["departure_time", "return_time"]
)

app = Flask(__name__)
app.bike_drives_df = bike_drives_df


from city_dna import routes
