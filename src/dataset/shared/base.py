from pydantic import BaseModel, validate_call
from src.backend import tf
from typing import Literal


class BaseDataset:
    class Config(BaseModel):
        pass

    @validate_call()
    def __init__(self, config: BaseModel):
        self.config = config

    @classmethod
    def from_config(cls, config):
        return cls(config=cls.Config(**config))

    def get_config(self):
        return self.config.model_dump()

    @validate_call()
    def get_dataset(self, split: Literal["train", "test"], args: BaseModel):
        split = split
        args = args
        return tf.data.Dataset.from_tensors([])
