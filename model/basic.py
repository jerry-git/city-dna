from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, LSTM, Embedding, Reshape
from keras.utils import to_categorical

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import pandas as pd


def data_preprocessing(data):
    train_data, test_data = train_test_split(
        data, test_size=0.2, shuffle=False)

    return train_data, test_data


def generate_model(input_training_data, output_training_data):

    model = Sequential()
    model.add(Dense(64, activation='relu',
                    input_dim=input_training_data.shape[0]))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(512, activation='relu'))

    model.add(Dense(output_training_data.shape[0]), activation='relu')

    model.compile(optimizer='adam',
                  loss='mean_squared_error',
                  metrics=['accuracy'])

    # Train the model, iterating on the data in batches of 32 samples
    model.fit(input_training_data, output_training_data,
              epochs=20, batch_size=32)

    model.save("model.h5")
    return model


if __name__ == '__main__':
    train = False

    train_x = []
    train_y = []

    test_x = []
    test_y = []

    if train:
        model = generate_model(train_x, train_y)
    else:
        model = load_model("model.h5")

    score = model.evaluate(test_x, test_y, batch_size=64)
    print(score)
    print(model.summary())

    predicet_data = model.predict(test_x)
