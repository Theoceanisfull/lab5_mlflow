# app/core/config.py
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
MODEL_NAME          = os.getenv("MLFLOW_MODEL_NAME", "iris-classifier")
DEFAULT_SELECTOR    = os.getenv("SERVE_SELECTOR", "version:1")    # or "stage:Production"
STATE_FILE          = os.getenv("SERVE_STATE_FILE", ".serve_state.txt")  # persists current selection
APP_TITLE           = "Iris Classifier API"
APP_DESC            = "Predict Iris species from sepal/petal measurements (cm)."
APP_VERSION         = "1.0.0"
