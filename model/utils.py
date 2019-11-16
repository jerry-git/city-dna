import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd

from human_flow.data import bike_station

STATION_IDS = list(sorted(bike_station.CLUSTERED_LOCATIONS.keys()))

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


def load_results_df():
    df = pd.read_csv(
        str(Path(__file__).parents[1] / "data" / "clustered-results.csv"),
        parse_dates=True,
    )
    df.index = df["Unnamed: 0"]
    df = df.drop(["Unnamed: 0"], axis=1)
    return df


# def load_rides_distribution_vectors(
#     rides_df,
#     start_time=dt.datetime(2019, 7, 15),
#     end_time=dt.datetime(2019, 9, 16),
#     sample_time=dt.timedelta(minutes=60),
# ):
#     def empty_rides_vector():
#         return np.zeros(len(STATION_IDS) ** 2)
#
#     def find_clustered_id(station_id):
#         for key, id_list in bike_station.CLUSTERED_LOCATIONS.items():
#             if station_id in id_list:
#                 return key
#         raise KeyError(station_id)
#
#     index, rows = [], []
#     start = pd.Timestamp(start_time)
#     end = pd.Timestamp(start + sample_time)
#     sample = rides_df.loc[
#         (rides_df.departure_time >= start) & (rides_df.return_time <= end)
#     ]
#     while not sample.empty:
#         index.append(start)
#         rides = empty_rides_vector()
#         for _, row in sample.iterrows():
#             row.departure_station_id
#
#             start_idx, end_idx = (
#                 find_clustered_id(row.departure_station_id),
#                 find_clustered_id(row.return_station_id),
#             )
#             ride_idx = start_idx * len(STATION_IDS) + end_idx
#             rides[ride_idx] += 1
#
#         rows.append(rides)
#         start = end
#         end = pd.Timestamp(start + sample_time)
#         sample = rides_df.loc[
#             (rides_df.departure_time >= start) & (rides_df.return_time <= end)
#         ]
#         print(start)
#     breakpoint()
#     result_df = pd.DataFrame(rows, index=index)
#     result_df.to_csv("clustered-results.csv")
#
#     return result_df
#
#     # df.loc[(df.departure_time >= start) & (df.return_time <= end)]
#     breakpoint()
#
#     pass


def project_rides_distribution_vector(vector):
    pass


def main():
    # df = load_rides_df()
    # load_rides_distribution_vectors(df)
    df = load_results_df()
    breakpoint()


if __name__ == "__main__":
    main()
