import datetime as dt
import random
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from human_flow.data import bike_station

CLUSTERED_LOCATIONS = bike_station.CLUSTERED_LOCATIONS_115

STATION_IDS = list(sorted(CLUSTERED_LOCATIONS.keys()))

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


def load_predictions_df():
    df = pd.read_csv(
        str(Path(__file__).parent / "test_20percent.csv"), parse_dates=True, index_col=0
    )
    return df


def project_results_to_rides(results_df):
    rides = defaultdict(list)
    for index, row in results_df.iterrows():
        start = pd.Timestamp(index)
        for idx, val in row[row >= 0.5].iteritems():
            idx = int(idx)
            val = int(val)
            # TODO: double check these
            # breakpoint()
            start_cluster_id = idx // len(STATION_IDS)
            end_cluster_id = idx % len(STATION_IDS)
            start_station_ids = CLUSTERED_LOCATIONS[start_cluster_id]
            end_station_ids = CLUSTERED_LOCATIONS[end_cluster_id]

            for ride_number in range(val):
                # split rides equally over the hour
                time_offset = dt.timedelta(
                    minutes=int((ride_number + 1) / (val + 1) * 60)
                )
                ride_start = start + time_offset
                end = ride_start + dt.timedelta(minutes=15)  # avg drive time
                start_station_id = random.choice(start_station_ids)
                end_station_id = random.choice(end_station_ids)

                rides["departure_time"].append(ride_start)
                rides["return_time"].append(end)
                rides["departure_station_id"].append(start_station_id)
                rides["return_station_id"].append(end_station_id)
                rides["start_lat"].append(bike_station.LOCATIONS[start_station_id][2])
                rides["start_lon"].append(bike_station.LOCATIONS[start_station_id][1])
                rides["end_lat"].append(bike_station.LOCATIONS[end_station_id][2])
                rides["end_lon"].append(bike_station.LOCATIONS[end_station_id][1])

            """
            start_idx, end_idx = (
                find_clustered_id(row.departure_station_id),
                find_clustered_id(row.return_station_id),
            )
            ride_idx = start_idx * len(STATION_IDS) + end_idx
            """
    rides_df = pd.DataFrame(rides)
    rides_df.to_csv("predictions.csv")

    return rides_df


def load_rides_distribution_vectors(
    rides_df,
    start_time=dt.datetime(2019, 7, 15),
    end_time=dt.datetime(2019, 9, 16),
    sample_time=dt.timedelta(minutes=60),
):
    def empty_rides_vector():
        return np.zeros(len(STATION_IDS) ** 2)

    def find_clustered_id(station_id):
        for key, id_list in CLUSTERED_LOCATIONS.items():
            if station_id in id_list:
                return key
        raise KeyError(station_id)

    index, rows = [], []
    start = pd.Timestamp(start_time)
    end = pd.Timestamp(start + sample_time)
    sample = rides_df.loc[
        (rides_df.departure_time >= start) & (rides_df.return_time <= end)
    ]
    while not sample.empty:
        index.append(start)
        rides = empty_rides_vector()
        for _, row in sample.iterrows():
            start_idx, end_idx = (
                find_clustered_id(row.departure_station_id),
                find_clustered_id(row.return_station_id),
            )
            ride_idx = start_idx * len(STATION_IDS) + end_idx
            rides[ride_idx] += 1

        rows.append(rides)
        start = end
        end = pd.Timestamp(start + sample_time)
        sample = rides_df.loc[
            (rides_df.departure_time >= start) & (rides_df.return_time <= end)
        ]
        print(start)

    result_df = pd.DataFrame(rows, index=index)
    result_df.to_csv("clustered-results-20.csv")
    breakpoint()

    return result_df

    # df.loc[(df.departure_time >= start) & (df.return_time <= end)]
    breakpoint()

    pass


# def project_rides_distribution_vector(vector):
#     pass


def main():
    rides_df = load_rides_df()
    # breakpoint()
    # load_rides_distribution_vectors(df)
    # df_rides = load_rides_df()
    # breakpoint()
    # load_rides_distribution_vectors(df_rides)
    # df_results = load_results_df()
    # breakpoint()

    # df_results = load_results_df()
    # projected_rides_df = project_results_to_rides(df_results)

    df_predictions = load_predictions_df()
    project_results_to_rides(df_predictions)

    breakpoint()


if __name__ == "__main__":
    main()
