# app/core/predictor.py

from tensorflow.keras.models import load_model #type: ignore
import numpy as np
import cv2
import tempfile
import os

# Load model once globally
model = load_model("cervical.keras")

# Label categories
categories = ["dyskeratotic", "koilocytotic", "metaplastic", "parabasal", "superficial"]

def predict_cervical_cancer(image_bytes: bytes) -> str:
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bmp") as tmp:
            tmp.write(image_bytes)
            tmp.flush()
            temp_file_path = tmp.name

        image = cv2.imread(temp_file_path) #type: ignore
        if image is None:
            raise ValueError("Invalid image data or format not supported by OpenCV.")

        image = cv2.resize(image, (224, 224)) #type: ignore
        image = image / 255.0
        image = np.expand_dims(image, axis=0)

        predictions = model.predict(image)
        predicted_class = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))

        return categories[predicted_class]  # Or return (categories[predicted_class], confidence)

    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
