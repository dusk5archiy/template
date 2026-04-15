from pydantic import BaseModel, validate_call
from src.backend import tf

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
