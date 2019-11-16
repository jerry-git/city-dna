from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, LSTM, Embedding
from keras.utils import to_categorical

from sklearn.model_selection import train_test_split


def data_preprocessing(data):
    train_data, test_data = train_test_split(
        data, test_size=0.2, shuffle=False)

    return train_data, test_data


def generate_model(data):
    num_of_diff_bike_trips = 1000
    model = Sequential()

    model.add(Dense(500, activation='relu', input_dim=100))
    model.add(Dense(1000, activation='sigmoid'))
    model.add(Dropout(0.3))
    model.add(Dense(2000, activation='sigmoid'))
    model.add(Dropout(0.3))
    model.add(Dense(2000, activation='sigmoid'))
    model.add(Dense(num_of_diff_bike_trips, activation='sigmoid'))
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # Train the model, iterating on the data in batches of 32 samples
    model.fit(data, labels, epochs=10, batch_size=32)

    model.save("model.h5")
    return model


if __name__ == '__main__':
    train = False

    if train:
        model = model_generation(train_data)
    else:
        model = load_model("model.h5")

    model.predict()
