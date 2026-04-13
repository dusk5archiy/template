from src.models.shared.base import BaseAIModel, ImageClassificationDsInfo

from pydantic import validate_call
import keras
import tensorflow as tf


class Resnet(BaseAIModel):
    class Config(BaseAIModel.Config, ImageClassificationDsInfo):
        dense_dim: int = 64
        dropout: float = 0.5
        activation: str = "swish"

    @validate_call()
    def __init__(self, config: Config):
        x = inp = tf.keras.layers.Input(
            shape=(
                config.image_resolution[1],
                config.image_resolution[0],
                config.num_channels,
            )
        )
        if config.num_channels == 1:
            x = tf.keras.layers.Concatenate(axis=-1)([x, x, x])
        x = tf.keras.applications.resnet.preprocess_input(x)

        base_model = keras.applications.ResNet50V2(include_top=False, pooling="avg")

        x = base_model(x)
        x = tf.keras.layers.Dense(config.dense_dim, activation=config.activation)(x)
        x = tf.keras.layers.Dropout(config.dropout)(x)
        x = tf.keras.layers.Dense(config.num_classes, activation="softmax")(x)

        tf.keras.Model.__init__(self, inputs=inp, outputs=x)
        BaseAIModel.__init__(self, config)
