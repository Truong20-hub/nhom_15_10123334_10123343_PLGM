from pathlib import Path

import pandas as pd

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

from config.model_config import DATA_DIR, FEATURE_NAMES, TARGET_NAME
from core.model_loader import load_model, load_scaler


def get_dataset_path(dataset_name: str) -> Path:
    if not dataset_name:
        raise ValueError("dataset_name không được để trống")
    if not dataset_name.endswith(".csv"):
        raise ValueError("Dataset phải là file .csv")

    data_dir = Path(DATA_DIR).resolve()

    dataset_path = None
    for path in data_dir.rglob(dataset_name):
        if path.is_file():
            dataset_path = path.resolve()
            break

    if dataset_path is None:
        raise FileNotFoundError(f"Không tìm thấy dataset: {dataset_name}")
    if data_dir not in dataset_path.parents:
        raise ValueError("Đường dẫn dataset không hợp lệ")

    return dataset_path


def evaluate_model(model_name: str, dataset_name: str):

    model = load_model(model_name)
    scaler = load_scaler()

    dataset_path = get_dataset_path(dataset_name)
    df = pd.read_csv(dataset_path)

    missing_features = [c for c in FEATURE_NAMES if c not in df.columns]
    if missing_features:
        raise ValueError(f"Dataset thiếu feature: {missing_features}")
    if TARGET_NAME not in df.columns:
        raise ValueError(f"Dataset không có cột target '{TARGET_NAME}'")

    X = df[FEATURE_NAMES].copy()
    y = df[TARGET_NAME]

    # Chỉ scale đúng các cột numeric mà scaler đã fit
    numeric_cols = list(scaler.feature_names_in_)
    X[numeric_cols] = scaler.transform(X[numeric_cols])
    X = X[FEATURE_NAMES]

    y_pred = model.predict(X)

    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average="weighted", zero_division=0)
    recall = recall_score(y, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y, y_pred, average="weighted", zero_division=0)
    cm = confusion_matrix(y, y_pred)
    report = classification_report(y, y_pred, output_dict=True, zero_division=0)

    return {
        "model": model_name,
        "dataset": dataset_name,
        "samples": len(df),
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "confusion_matrix": cm.tolist(),
        "classification_report": report
    }
