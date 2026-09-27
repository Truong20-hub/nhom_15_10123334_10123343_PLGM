from pathlib import Path
import joblib

from config.model_config import MODEL_DIR, SCALER_NAME


def get_model_path(model_name: str) -> Path:
    """
    Lấy đường dẫn model từ tên file.
    """

    if not model_name:
        raise ValueError("model_name không được để trống")

    if not model_name.endswith(".pkl"):
        raise ValueError("Model phải là file .pkl")

    model_dir = Path(MODEL_DIR).resolve()
    model_path = (model_dir / model_name).resolve()

    # Không cho phép truy cập ra ngoài MODEL_DIR
    if model_dir not in model_path.parents:
        raise ValueError("Đường dẫn model không hợp lệ")

    if not model_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy model: {model_name}"
        )

    return model_path


def load_model(model_name: str):
    """
    Load model theo tên file.
    """

    model_path = get_model_path(model_name)

    return joblib.load(model_path)


def get_scaler_path() -> Path:
    """
    Lấy đường dẫn scaler.
    """

    scaler_path = Path(MODEL_DIR) / SCALER_NAME

    if not scaler_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy scaler: {SCALER_NAME}"
        )

    return scaler_path


def load_scaler():
    """
    Load scaler dùng chung.
    """

    return joblib.load(get_scaler_path())


def list_models():
    """
    Trả về danh sách các model .pkl.
    Không tính scaler.pkl.
    """

    model_dir = Path(MODEL_DIR)

    if not model_dir.exists():
        raise FileNotFoundError(
            f"Không tìm thấy thư mục model: {MODEL_DIR}"
        )

    models = []

    for file in model_dir.glob("*.pkl"):
        if file.name != SCALER_NAME:
            models.append(file.name)

    return sorted(models)
