from typing import Literal
from src.backend import tf
from .shared.base import BaseDataset
from pydantic import BaseModel, validate_call
import numpy as np

class Mnist(BaseDataset):
    class Config(BaseDataset.Config):
        pass

    class SplitArgs(BaseModel):
        batch_size: int
        buffer_size: int = 10000
        shuffle: bool = True

    @validate_call()
    def __init__(self, config: Config):
        self.config = config
        self.train_data, self.test_data = tf.keras.datasets.mnist.load_data()

    @property
    def image_resolution(self):
        x_train = self.train_data[0]
        shape = x_train.shape[1:]
        if len(shape) >= 2:
            return (int(shape[1]), int(shape[0]))
        raise ValueError(f"Unexpected image shape: {shape}")
    
    @property
    def colored(self):
        return False
    
    @property
    def num_classes(self):
        y_train = self.train_data[1]
        y_test = self.test_data[1]
        labels = np.concatenate([y_train, y_test])
        return int(np.unique(labels).size)

    @validate_call()
    def get_dataset(
        self,
        split: Literal["train", "test"],
        args: BaseModel,
    ):
        args = self.SplitArgs(**args.model_dump())
        ds = tf.data.Dataset.from_tensor_slices(
            self.train_data if split == "train" else self.test_data
        )
        if args.shuffle:
            ds = ds.shuffle(args.buffer_size)
        ds = ds.batch(args.batch_size)
        ds = ds.prefetch(tf.data.AUTOTUNE)
        return ds
