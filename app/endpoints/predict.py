from fastapi import APIRouter, HTTPException
import pandas as pd

from app.core.model_service import model_svc, IRIS_LABELS
from app.schemas.iris import PredictRequest, PredictResponse

router = APIRouter(tags=["prediction"])

@router.post(
    "/predict",
    response_model=PredictResponse,
    summary="Predict Iris species"
)
def predict(req: PredictRequest) -> PredictResponse:
    try:
        # fixed column order to match training
        cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
        rows = [s.model_dump() for s in req.samples]
        df = pd.DataFrame(rows, columns=cols)

        class_ids = model_svc.predict(df)
        class_labels = [IRIS_LABELS.get(i, f"unknown-{i}") for i in class_ids]
        return PredictResponse(class_id=class_ids, class_label=class_labels)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
