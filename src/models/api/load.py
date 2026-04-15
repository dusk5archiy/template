from pydantic import BaseModel
from src.backend import yaml, keras
from typing import Any


class ModelInfo(BaseModel):
    module: str
    class_name: str
    config: dict[str, Any] | None = None


def load_model(
    model_name: str,
    ds_info: BaseModel,
):
    from src.models import CUSTOM_OBJECTS

    with open("config/models.yml", encoding="utf-8") as f:
        c = yaml.safe_load(f)[model_name]
    c = ModelInfo(**c)
    config = {**ds_info.model_dump(), **(c.config or {})}
    model = keras.saving.deserialize_keras_object(
        {
            "module": c.module,
            "class_name": c.class_name,
            "config": config,
        },
        custom_objects=CUSTOM_OBJECTS,
    )
    return model


# =============================================================================
