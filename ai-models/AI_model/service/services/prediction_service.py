import pandas as pd

from core.model_loader import load_model, load_scaler
from config.model_config import FEATURE_NAMES


def predict_mobile(data, model_name: str):

    # Load model được yêu cầu
    model = load_model(model_name)

    # Load scaler
    scaler = load_scaler()

    # Chuyển dữ liệu JSON thành DataFrame
    input_data = pd.DataFrame(
        [data.model_dump()],
        columns=FEATURE_NAMES
    )

    # Scale giống lúc train
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)

    return int(prediction[0])
