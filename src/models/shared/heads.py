from src.backend import tf
from pydantic import BaseModel
from typing import Any

# -----------------------------------------------------------------------------

class ClassifyArgs(BaseModel):
    dense_dim: int = 96
    activation: str = "swish"
    dropout: float = 0.5

def classify(
    x: Any,
    n_classes: int,
    args: ClassifyArgs,
):
    x = tf.keras.layers.Dense(args.dense_dim, activation=args.activation)(x)
    x = tf.keras.layers.Dropout(args.dropout)(x)
    x = tf.keras.layers.Dense(n_classes, activation="softmax")(x)
    return x


# -----------------------------------------------------------------------------
