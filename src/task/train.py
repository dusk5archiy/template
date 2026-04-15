from pydantic import TypeAdapter
import tensorflow as tf
from typing import TypedDict, Unpack
from src.backend import yaml
from src.plot.classification import plot_classification_training_history
from src.models.shared.dataset_info import ImageClassificationDsInfo
from src.dataset.mnist import Mnist
from tqdm.keras import TqdmCallback
from datetime import datetime
import os
from pydantic import validate_call
from src.backend.logging import logger
from src.models.api.load import load_model

# =============================================================================


class TrainResults(TypedDict):
    model_name: str
    batch_size: int
    n_epochs: int
    image_resolution: tuple[int, int]


def report_training_results(
    path_base: str, model: tf.keras.Model, **kwargs: Unpack[TrainResults]
):
    kwargs = TypeAdapter(TrainResults).validate_python(kwargs)
    info = {
        **kwargs,
        "n_params": model.count_params(),
    }

    with open(f"{path_base}.yml", "w") as f:
        yaml.dump(info, f, default_flow_style=False, sort_keys=False)


# =============================================================================


@validate_call
def train(
    model_name: str,
    batch_size: int,
    epochs: int,
):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = f"output/{model_name}/{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    model_filepath = f"{output_dir}/model.keras"

    # Create ASL dataset
    full_ds = Mnist(config=Mnist.Config())

    # Get full unbatched dataset
    train_ds = full_ds.get_dataset(
        split="train", args=Mnist.SplitArgs(batch_size=batch_size)
    )
    val_ds = full_ds.get_dataset(
        split="test", args=Mnist.SplitArgs(batch_size=batch_size)
    )

    # Create model
    ds_info = ImageClassificationDsInfo(
        image_resolution=full_ds.image_resolution,
        colored=full_ds.colored,
        num_classes=full_ds.num_classes,
    )
    model = load_model(model_name=model_name, ds_info=ds_info)

    # Compile model
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )

    logger.success("Model compiled successfully")
    model.summary()

    # Callbacks
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            model_filepath, save_best_only=True, monitor="val_accuracy", mode="max"
        ),
        TqdmCallback(verbose=1),
    ]

    # Train
    logger.info("Starting training...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
    )
    # Plot and report
    plot_classification_training_history(
        path_base=f"{output_dir}/train",
        history=history,
    )
    report_training_results(
        path_base=f"{output_dir}/train",
        model=model,
        model_name=model_name,
        batch_size=batch_size,
        n_epochs=len(history.history["loss"]) + 1,
        image_resolution=full_ds.image_resolution,
    )

    logger.info(f"Training completed. Model saved to {model_filepath}")
