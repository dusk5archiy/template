from src.models.shared.base import BaseAIModel
from src.models.shared.dataset_info import ImageClassificationDsInfo
from src.models.shared.heads import ClassifyArgs, classify
import keras
from src.backend import tf


class Mobilenet(BaseAIModel):
    class Config(BaseAIModel.Config, ImageClassificationDsInfo):
        # classify
        classify: ClassifyArgs = ClassifyArgs()

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

        x = tf.keras.applications.mobilenet_v3.preprocess_input(x)

        base_model = keras.applications.MobileNetV3Small(
            include_top=False,
            pooling="avg",
        )
        x = base_model(x)
        x = classify(
            x,
            n_classes=config.num_classes,
            args=config.classify,
        )

        tf.keras.Model.__init__(self, inputs=inp, outputs=x)
        BaseAIModel.__init__(self, config)
