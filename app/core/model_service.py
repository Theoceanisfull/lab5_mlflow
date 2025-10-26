# app/core/model_service.py
import os
import threading
from typing import List, Optional

import pandas as pd
import mlflow
import mlflow.pyfunc

from app.core.config import (
    MLFLOW_TRACKING_URI, MODEL_NAME,
    DEFAULT_SELECTOR, STATE_FILE
)

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

IRIS_LABELS = {0: "setosa", 1: "versicolor", 2: "virginica"}

class ModelService:
    """Owns model selector state and mlflow model instance."""
    def __init__(self):
        self._lock = threading.Lock()
        self._selector: Optional[str] = None
        self._model: Optional[mlflow.pyfunc.PyFuncModel] = None

    # ---------- State persistence ----------
    def _read_state_file(self) -> Optional[str]:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                val = f.read().strip()
                return val or None
        return None

    def _write_state_file(self, val: str):
        with open(STATE_FILE, "w") as f:
            f.write(val)

    # ---------- URI & loading ----------
    def _resolve_uri(self, selector: str) -> str:
        if selector.startswith("stage:"):
            stage = selector.split(":", 1)[1]
            return f"models:/{MODEL_NAME}/{stage}"
        if selector.startswith("version:"):
            ver = selector.split(":", 1)[1]
            return f"models:/{MODEL_NAME}/{ver}"
        return f"models:/{MODEL_NAME}/{selector}"

    def _load_model(self, selector: str) -> mlflow.pyfunc.PyFuncModel:
        uri = self._resolve_uri(selector)
        return mlflow.pyfunc.load_model(uri)

    def ensure_loaded(self):
        with self._lock:
            if self._model is None:
                sel = self._read_state_file() or DEFAULT_SELECTOR
                self._model = self._load_model(sel)
                self._selector = sel
                self._write_state_file(sel)

    # ---------- Public API ----------
    @property
    def selector(self) -> str:
        self.ensure_loaded()
        return self._selector  # type: ignore

    @property
    def model_uri(self) -> str:
        return self._resolve_uri(self.selector)

    def switch(self, selector: str):
        if not (selector.startswith("version:") or selector.startswith("stage:")):
            raise ValueError("selector must be 'version:<N>' or 'stage:<Name>'")
        with self._lock:
            new_model = self._load_model(selector)  # will raise if invalid
            self._model = new_model
            self._selector = selector
            self._write_state_file(selector)

    def predict(self, df: pd.DataFrame) -> List[int]:
        self.ensure_loaded()
        raw = self._model.predict(df)  # type: ignore
        arr = raw.tolist() if hasattr(raw, "tolist") else list(raw)
        return [int(x) for x in arr]

# Singleton service used by endpoints
model_svc = ModelService()
