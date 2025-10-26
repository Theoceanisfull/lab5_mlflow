# app/endpoints/admin.py
from fastapi import APIRouter, HTTPException

# If you already created app/core/model_service.py, keep the next import:
try:
    from app.core.model_service import model_svc
except Exception:
    # Fallback stub so the app still starts (remove once model_service exists)
    class _Stub:
        selector = "version:1"
        model_uri = "models:/iris-classifier/1"
        def switch(self, s: str): 
            if not (s.startswith("version:") or s.startswith("stage:")):
                raise ValueError("selector must be 'version:<N>' or 'stage:<Name>'")
            self.selector = s
            self.model_uri = f"models:/iris-classifier/{s.split(':',1)[1]}"
    model_svc = _Stub()

router = APIRouter(tags=["admin"])

@router.get("/served-version", summary="Get current served selection")
def served_version():
    return {
        "model_name": "iris-classifier",
        "selector": model_svc.selector,
        "model_uri": model_svc.model_uri,
    }

@router.post("/serve-version", summary="Switch served model to a version or stage")
def serve_version(selector: str):
    try:
        model_svc.switch(selector)
        return {"ok": True, "selector": model_svc.selector, "model_uri": model_svc.model_uri}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not load selector '{selector}': {e}" )
