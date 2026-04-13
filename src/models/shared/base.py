from pydantic import BaseModel, validate_call
from typing import Any
import keras
from src.backend import tf
import yaml

# =============================================================================


class BaseAIModel(tf.keras.Model):
    class Config(BaseModel):
        pass

    @validate_call()
    def __init__(self, config: BaseModel):
        self.config = config

    @classmethod
    def from_config(cls, config, custom_objects=None):
        custom_objects = custom_objects
        return cls(config=cls.Config(**config))

    def get_config(self):
        return self.config.model_dump()


# =============================================================================


class ModelInfo(BaseModel):
    module: str
    class_name: str
    config: dict[str, Any] | None = None


def load_model(
    model_name: str,
    ds_info: BaseModel,
):
    from src.models.resnet import Resnet
    with open("config/models.yml", encoding="utf-8") as f:
        c = yaml.safe_load(f)[model_name]
    c = ModelInfo(**c)
    config = {**ds_info.model_dump(), **(c.config or {})}
    model = keras.saving.deserialize_keras_object(
        {
            "module": c.module,
            "class_name": c.class_name,
            "config": config,
        }, custom_objects={
            "Resnet": Resnet
        }
    )
    return model


# =============================================================================


class ImageProcessingDsInfo(BaseModel):
    colored: bool
    image_resolution: tuple[int, int] # W x H

    @property
    def num_channels(self):
        return 3 if self.colored else 1


class ClassificationDsInfo(BaseModel):
    num_classes: int

class ImageClassificationDsInfo(ImageProcessingDsInfo, ClassificationDsInfo):
    pass

# -----------------------------------------------------------------------------
