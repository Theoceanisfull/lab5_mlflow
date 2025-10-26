# app/schemas/iris.py
from typing import List
from pydantic import BaseModel, Field

class IrisSample(BaseModel):
    sepal_length: float = Field(..., ge=0, description="Sepal length in cm")
    sepal_width:  float = Field(..., ge=0, description="Sepal width in cm")
    petal_length: float = Field(..., ge=0, description="Petal length in cm")
    petal_width:  float = Field(..., ge=0, description="Petal width in cm")

class PredictRequest(BaseModel):
    samples: List[IrisSample]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"samples": [
                    {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}
                ]}
            ]
        }
    }

class PredictResponse(BaseModel):
    class_id: List[int]
    class_label: List[str]

    model_config = {
        "json_schema_extra": {
            "examples": [{"class_id": [0], "class_label": ["setosa"]}]
        }
    }

class ServeSelection(BaseModel):
    selector: str = Field(..., examples=["version:2", "stage:Production"])
