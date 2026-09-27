from pathlib import Path
import zipfile

import pandas as pd

from fastapi import APIRouter, HTTPException

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from config.model_config import (
    DATA_DIR,
    DATASET_ZIP,
    FEATURE_NAMES,
    TARGET_NAME
)

from core.model_loader import (
    load_model,
    load_scaler
)


router = APIRouter(
    prefix="/api",
    tags=["Evaluation"]
)


# =========================================================
# GIẢI NÉN DATASET NẾU CHƯA GIẢI NÉN
# =========================================================

def ensure_dataset_extracted():

    data_dir = Path(DATA_DIR)

    zip_path = data_dir / DATASET_ZIP

    if not zip_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file ZIP: {zip_path}"
        )

    # Kiểm tra xem đã có CSV chưa
    csv_files = list(data_dir.rglob("*.csv"))

    if csv_files:
        print("Dataset đã được giải nén.")
        return

    print("Chưa tìm thấy CSV.")
    print(f"Đang giải nén: {zip_path}")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(data_dir)

    print("Giải nén dataset thành công.")


# =========================================================
# TÌM DATASET
# =========================================================

def get_dataset_path(dataset_name: str) -> Path:

    ensure_dataset_extracted()

    data_dir = Path(DATA_DIR).resolve()

    dataset_path = None

    # Tìm cả trong thư mục con
    for path in data_dir.rglob(dataset_name):
        if path.is_file():
            dataset_path = path.resolve()
            break

    if dataset_path is None:
        raise FileNotFoundError(
            f"Không tìm thấy dataset: {dataset_name}"
        )

    # Bảo vệ đường dẫn
    if data_dir not in dataset_path.parents:
        raise ValueError(
            "Đường dẫn dataset không hợp lệ"
        )

    return dataset_path


# =========================================================
# EVALUATE MODEL
# =========================================================

def evaluate_model(
    model_name: str,
    dataset_name: str
):

    # -----------------------------------------------------
    # LOAD MODEL
    # -----------------------------------------------------

    model = load_model(model_name)

    # -----------------------------------------------------
    # LOAD SCALER
    # -----------------------------------------------------

    scaler = load_scaler()

    # -----------------------------------------------------
    # LOAD DATASET
    # -----------------------------------------------------

    dataset_path = get_dataset_path(
        dataset_name
    )

    df = pd.read_csv(dataset_path)

    # -----------------------------------------------------
    # CHECK FEATURES
    # -----------------------------------------------------

    missing_features = [
        col
        for col in FEATURE_NAMES
        if col not in df.columns
    ]

    if missing_features:

        raise ValueError(
            f"Dataset thiếu feature: "
            f"{missing_features}"
        )

    # -----------------------------------------------------
    # CHECK TARGET
    # -----------------------------------------------------

    if TARGET_NAME not in df.columns:

        raise ValueError(
            f"Dataset không có cột target "
            f"'{TARGET_NAME}'"
        )

    # -----------------------------------------------------
    # X / Y
    # -----------------------------------------------------

    X = df[FEATURE_NAMES]

    y = df[TARGET_NAME]

    # -----------------------------------------------------
    # SCALE
    # -----------------------------------------------------

    X_scaled = scaler.transform(X)

    # -----------------------------------------------------
    # PREDICT
    # -----------------------------------------------------

    y_pred = model.predict(X_scaled)

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    accuracy = accuracy_score(
        y,
        y_pred
    )

    precision = precision_score(
        y,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y,
        y_pred,
        average="weighted",
        zero_division=0
    )

    cm = confusion_matrix(
        y,
        y_pred
    )

    report = classification_report(
        y,
        y_pred,
        output_dict=True,
        zero_division=0
    )

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


# =========================================================
# ENDPOINT
# =========================================================

@router.get("/evaluate")
def evaluate(
    model_name: str = "best_model.pkl",
    dataset_name: str = "mobile_price.csv"
):

    try:

        result = evaluate_model(
            model_name,
            dataset_name
        )

        return result

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
