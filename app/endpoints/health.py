from fastapi import APIRouter
from app.core.config import MLFLOW_TRACKING_URI, MODEL_NAME, DEFAULT_SELECTOR
from app.core.model_service import model_svc

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    sel = model_svc.selector or DEFAULT_SELECTOR  # ensure_loaded inside property
    return {
        "status": "ok",
        "tracking_uri": MLFLOW_TRACKING_URI,
        "model_name": MODEL_NAME,
        "selector": sel,
        "model_uri": model_svc.model_uri,
    }
