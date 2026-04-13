import numpy as np
from tqdm import tqdm
import time
from src.metrics.classification import calc_classification_metrics
import os
import yaml
from src.dataset.mnist import Mnist
from src.backend.logging import logger
from src.task.inference import DotKerasInference, DotTfliteInference
from src.plot.classification import plot_evaluation_results


def evaluate(model_path: str):
    # Get model extension
    _, ext = os.path.splitext(model_path)
    ext = ext[1:] if ext else "keras"  # Remove leading dot, default to keras
    if ext == "tflite":
        evaluator = DotTfliteInference(model_path=model_path)
    else:
        evaluator = DotKerasInference(
            model_path=model_path,
        )

    # Get validation dataset
    logger.info("Loading validation dataset...")

    full_ds = Mnist(config=Mnist.Config())
    batch_size = 16
    val_ds = full_ds.get_dataset(split="test", args=Mnist.SplitArgs(batch_size=batch_size))

    # Calculate precision, recall, and F1 score on validation set
    # Get model name from path
    model_name_base = os.path.splitext(os.path.basename(model_path))[0]
    output_dir = os.path.dirname(model_path)

    logger.info("Calculating metrics on validation set...")
    all_true_labels = []
    all_predictions = []
    inference_times = []  # Store inference times for average calculation

    viz_images = []
    viz_data = {"img_count": 0}

    processed_samples = 0
    total_inference_time = 0.0

    rows = 4
    cols = 4

    n_samples = rows * cols

    with tqdm(total=len(val_ds), desc="Evaluating", unit="sample") as pbar:
        for batch_images, batch_labels in val_ds:
            start_time = time.perf_counter()
            preds = evaluator(batch_images)
            end_time = time.perf_counter()
            for img, lbl, pred in zip(batch_images, batch_labels, preds):
                pred = int(pred)
                lbl = int(lbl)
                
                elapsed = end_time - start_time
                inference_times.append(elapsed)

                all_predictions.append(pred)
                all_true_labels.append(lbl)

                # Capture for visualization after inference
                if viz_data["img_count"] < n_samples:
                    viz_images.append(
                        {
                            "img": img.numpy(),
                            "actual": lbl,
                            "predicted": pred,
                        }
                    )
                    viz_data["img_count"] += 1

                processed_samples += 1
                total_inference_time += elapsed
                avg_inference_time = (
                    total_inference_time / processed_samples
                    if processed_samples
                    else 0.0
                )

                pbar.set_postfix(
                    avg_inf_ms=f"{avg_inference_time * 1000:.2f}",
                    last_sample_ms=f"{elapsed * 1000:.2f}",
                )
            pbar.update(1)

    plot_evaluation_results(
        path_base=f"{output_dir}/eval-{ext}",
        viz_images=viz_images,
        rows=rows,
        cols=cols
    )

    # Create metrics dict
    avg_inference_time = np.mean(inference_times) if inference_times else 0.0

    precision, recall, f1 = calc_classification_metrics(
        targets=np.array(all_true_labels), preds=np.array(all_predictions)
    )

    metrics = {
        "model": model_name_base,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "model_type": ext,
        "avg_inference_time": float(avg_inference_time),
    }

    # Write metrics to YAML
    yml_path = f"{output_dir}/eval-{ext}.yml"
    with open(yml_path, "w") as f:
        yaml.dump(metrics, f, default_flow_style=False, sort_keys=False)
    logger.info(f"Evaluation metrics saved to {yml_path}")
