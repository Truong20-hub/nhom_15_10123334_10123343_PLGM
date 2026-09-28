from pathlib import Path
import zipfile

from fastapi import APIRouter, HTTPException

from config.model_config import DATA_DIR, DATASET_ZIP
from services.evaluation_service import evaluate_model


router = APIRouter(
    prefix="/api",
    tags=["Evaluation"]
)


def ensure_dataset_extracted():
    data_dir = Path(DATA_DIR)
    zip_path = data_dir / DATASET_ZIP

    if not zip_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file ZIP: {zip_path}")

    csv_files = list(data_dir.rglob("*.csv"))
    if csv_files:
        print("Dataset đã được giải nén.")
        return

    print(f"Đang giải nén: {zip_path}")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(data_dir)
    print("Giải nén dataset thành công.")


@router.get("/evaluate")
def evaluate(
    model_name: str = "best_model.pkl",
    dataset_name: str = "mobile_price.csv"
):
    try:
        ensure_dataset_extracted()
        result = evaluate_model(model_name, dataset_name)
        return result

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
