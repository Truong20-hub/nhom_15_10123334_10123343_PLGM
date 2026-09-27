from fastapi import APIRouter, HTTPException

from schemas.mobile import MobileData
from services.prediction_service import predict_mobile


router = APIRouter(
    prefix="/api",
    tags=["Prediction"]
)


@router.post("/predict")
def predict(
    data: MobileData,
    model: str = "best_model.pkl"
):

    try:

        prediction = predict_mobile(
            data,
            model
        )

        return {
            "model": model,
            "price_range": prediction
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
