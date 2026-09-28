import pandas as pd

from core.model_loader import load_model, load_scaler
from config.model_config import FEATURE_NAMES


def predict_mobile(data, model_name: str):

    model = load_model(model_name)
    scaler = load_scaler()

    input_data = pd.DataFrame(
        [data.model_dump()],
        columns=FEATURE_NAMES
    )

    # Chỉ scale đúng các cột mà scaler đã được fit (numeric_cols)
    numeric_cols = list(scaler.feature_names_in_)
    input_scaled = input_data.copy()
    input_scaled[numeric_cols] = scaler.transform(input_data[numeric_cols])

    # Đảm bảo đúng thứ tự cột như lúc train model
    input_scaled = input_scaled[FEATURE_NAMES]

    prediction = model.predict(input_scaled)

    return int(prediction[0])
