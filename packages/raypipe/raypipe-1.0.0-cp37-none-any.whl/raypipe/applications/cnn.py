from typing import Dict
from raypipe.applications.base import BaseNN
import tensorflow as tf
import numpy as np


class CNN(BaseNN):
    def model_strategy_func(self,learning_cfg:Dict):
        learning_rate = learning_cfg.get("lr",0.001)

        model = tf.keras.Sequential([
            tf.keras.Input(shape=(28, 28)),
            tf.keras.layers.Reshape(target_shape=(28, 28, 1)),
            tf.keras.layers.Conv2D(32, 3, activation="relu"),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(10)
        ])

        model.compile(
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
            metrics=["accuracy"])
        return model

    def data_generator_func(self,data_cfg:Dict,batch_size:int):
        (x_train, y_train), _ = tf.keras.datasets.mnist.load_data()
        # The `x` arrays are in uint8 and have values in the [0, 255] range.
        # You need to convert them to float32 with values in the [0, 1] range.
        x_train = x_train / np.float32(255)
        y_train = y_train.astype(np.int64)
        train_dataset = tf.data.Dataset.from_tensor_slices(
            (x_train, y_train)).shuffle(60000).repeat().batch(batch_size)

        return train_dataset


