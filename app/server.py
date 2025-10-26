# app/server.py
from fastapi import FastAPI
from app.core.config import APP_TITLE, APP_DESC, APP_VERSION
from app.endpoints.health import router as health_router
from app.endpoints.admin import router as admin_router
from app.endpoints.predict import router as predict_router

app = FastAPI(title=APP_TITLE, description=APP_DESC, version=APP_VERSION)

# Include routers (optionally add prefixes, e.g., prefix="/v1")
app.include_router(health_router)
app.include_router(admin_router)
app.include_router(predict_router)
