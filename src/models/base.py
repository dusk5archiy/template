from pydantic import BaseModel
from typing import Any
import keras
import tensorflow as tf
import yaml


# =============================================================================


class BaseAIModel(tf.keras.Model):
    class Config:
        pass

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
    config: dict[str, Any] = {}


def load_model(
    model_name: str,
    task_args: BaseModel,
):
    with open("config/models.yml", encoding="utf-8") as f:
        c = yaml.safe_load(f)[model_name]
    c = ModelInfo(**c)
    config = {**task_args.model_dump(), **c.config}
    model = keras.saving.deserialize_keras_object(
        {
            "module": c.module,
            "class_name": c.class_name,
            "config": config,
        }
    )
    return model


# =============================================================================
