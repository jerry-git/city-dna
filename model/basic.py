from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, LSTM, Reshape
from keras.utils import to_categorical

from sklearn.model_selection import train_test_split

import pandas as pd
from utils import load_weather_df, load_results_df

from datetime import datetime
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm


def data_preprocessing(data):
    train_data, test_data = train_test_split(
        data, test_size=0.2, shuffle=False)

    return train_data, test_data


def clean_data(data):
    # get weekdays
    data['weekday'] = data.apply(lambda row: row['time'].weekday(), axis=1)

    # unique days
    weekdays = data.weekday.unique()
    test = pd.get_dummies(data.weekday).reindex(
        columns=weekdays, fill_value=0)
    data = pd.concat([data, test], axis=1, join='inner')
    data.columns = ['time', 'cloud_amount_1_8', 'pressure', 'humidity_percentage', 'precipitation', 'snow_depth', 'air_temperature', 'dew_point_temperature',
                    'horizontal_visibility', 'wind_direction', 'gust_speed', 'wind_speed', 'weekday', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    # unique hours
    data['hour'] = data.apply(lambda row: row.time.hour, axis=1)
    hours = data.hour.unique()
    test = pd.get_dummies(data.hour).reindex(
        columns=hours, fill_value=0)

    data = pd.concat([data, test], axis=1, join='inner')

    # drop extra
    drop_list = ['pressure', 'humidity_percentage', 'snow_depth',
                 'dew_point_temperature', 'horizontal_visibility', 'wind_direction', 'gust_speed', 'wind_speed', 'weekday']

    # get hour averaged data
    data['ntime'] = pd.to_datetime(data['time'])
    data.index = data['ntime']
    data = data.resample('1H').mean()

    data = data.drop(drop_list, axis=1)

    return data


def generate_model(train_x, train_y):

    train_x = np.asarray(train_x)
    train_y = np.asarray(train_y)

    model = Sequential()
    model.add(Dense(64, activation='relu',
                    input_dim=train_x.shape[1]))
    model.add(Dense(64, activation='sigmoid'))
    model.add(Dropout(0.4))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.4))

    model.add(Dense(train_y.shape[1], activation='relu'))

    model.compile(optimizer='adam',
                  loss='mean_squared_error',
                  metrics=['accuracy'])

    # Train the model, iterating on the data in batches of 32 samples
    model.fit(train_x, train_y,
              epochs=50, batch_size=32)

    model.save("model.h5")
    return model


if __name__ == '__main__':
    train = True
    predict = True

    train_y = []
    test_y = []

    data = load_weather_df()
    data = clean_data(data)
    data = data[:-1]
    train_x, test_x = data_preprocessing(data)

    output_data = load_results_df()
    train_y, test_y = data_preprocessing(output_data)

    if train:
        model = generate_model(train_x, train_y)

    if predict:
        model = load_model("model.h5")
        score = model.evaluate(test_x, test_y, batch_size=64)
        print(score)
        print(model.summary())

        predicted_data = model.predict(test_x)
        print(predicted_data)

        new_data = pd.DataFrame(predicted_data, index=test_y.index)
        test = np.asarray(test_y)

        # visualize
        fig = plt.figure()
        fig.patch.set_facecolor((0.6, 0.6, 0.7))
        ax1 = fig.add_subplot(121)
        # Bilinear interpolation - this will look blurry
        ax1.imshow(test_y, interpolation='bilinear',
                   cmap=cm.Greys_r)
        plt.title('Truth')
        plt.xlabel('Unique routes')
        plt.ylabel('time')


        ax2 = fig.add_subplot(122)
        # 'nearest' interpolation - faithful but blocky
        ax2.imshow(predicted_data, interpolation='nearest',
                   cmap=cm.Greys_r)
        plt.title('Prediction')
        plt.xlabel('Unique routes')
        plt.ylabel('time')

        plt.show()
        # new_data.to_csv("test_20percent.csv", index=True)
