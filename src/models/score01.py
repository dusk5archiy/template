import tensorflow as tf
from src.models.shared.base import BaseAIModel
from src.models.shared.dataset_info import ImageClassificationDsInfo
from src.models.shared.heads import classify, ClassifyArgs
from pydantic import Field
from typing import Literal


class Score01(BaseAIModel):
    class Config(BaseAIModel.Config, ImageClassificationDsInfo):
        filter_list: list[int] = Field([32, 16, 80, 96, 128], min_length=1)
        padding: Literal["valid", "same"] = "same"
        activation: str = "swish"
        classify: ClassifyArgs = ClassifyArgs()

    def __init__(self, config: Config):
        filter_list = config.filter_list

        x = inp = tf.keras.layers.Input(
            shape=(*config.image_resolution, config.num_channels)
        )
        x = x / 255.0
        x = tf.keras.layers.Conv2D(
            filter_list[0],
            3,
            padding=config.padding,
            activation=config.activation,
        )(inp)
        for filter in filter_list[1:]:
            x = tf.keras.layers.MaxPooling2D(2, 2)(x)
            x = tf.keras.layers.Conv2D(
                filter,
                3,
                padding=config.padding,
                activation=config.activation,
            )(x)
        x = tf.keras.layers.Flatten()(x)
        x = classify(
            x,
            n_classes=config.num_classes,
            args=config.classify,
        )
        tf.keras.Model.__init__(self, inputs=inp, outputs=x)
        BaseAIModel.__init__(self, config)
