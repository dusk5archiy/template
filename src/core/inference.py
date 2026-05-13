import numpy as np
from src.backend import tf


class DotKerasInference:
    def __init__(self, model_path: str):
        from src.models import CUSTOM_OBJECTS

        self.model = tf.keras.models.load_model(
            model_path, custom_objects=CUSTOM_OBJECTS
        )

    @tf.function(reduce_retracing=True)
    def _inference(self, x):
        return self.model(x, training=False)

    def __call__(self, x):
        pred = self._inference(x)
        class_indices = np.argmax(pred, axis=1)
        return class_indices


class DotTfliteInference:
    def __init__(self, model_path: str):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def _inference(self, x):
        self.interpreter.set_tensor(self.input_details[0]["index"], x)
        self.interpreter.invoke()
        pred = self.interpreter.get_tensor(self.output_details[0]["index"])
        return pred

    def __call__(self, x):
        pred = self._inference(x)
        class_indices = np.argmax(pred, axis=1)
        return class_indices

