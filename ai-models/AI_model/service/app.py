from fastapi import FastAPI

from routers.prediction import router as prediction_router
from routers.evaluation import router as evaluation_router

from core.model_loader import list_models


app = FastAPI(
    title="Mobile Price AI Service",
    description="AI Service for Mobile Price Classification",
    version="1.0.0"
)


# =========================
# ROUTERS
# =========================

app.include_router(
    prediction_router
)

app.include_router(
    evaluation_router
)


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "service": "Mobile Price AI Service",
        "status": "running",
        "message": "AI Service is running successfully"
    }


# =========================
# HEALTH
# =========================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# =========================
# LIST MODELS
# =========================

@app.get("/api/models")
def models():

    return {
        "models": list_models()
    }
