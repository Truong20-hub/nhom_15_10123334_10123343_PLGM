"""
AI Service - Microservice phục vụ mô hình học máy Mobile Price Classification
- Nạp model.joblib NGAY KHI KHỞI ĐỘNG (lifespan)
- Validate dữ liệu đầu vào theo schema.json
- Cung cấp /predict, /health, /model-info
- Hỗ trợ X-Request-ID và Structured Logging
"""

import os
import sys
import time
import uuid
import json
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Cấu hình logging có cấu trúc
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-5s ai-service req=%(request_id)s  %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("ai-service")

# Custom log filter để tiêm request_id
class RequestIdFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.request_id = "-"

    def filter(self, record):
        record.request_id = getattr(record, "request_id", self.request_id)
        return True

log_filter = RequestIdFilter()
logger.addFilter(log_filter)

# Đường dẫn tệp model, schema, metadata
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(MODELS_DIR, "model.joblib"))
SCHEMA_PATH = os.getenv("SCHEMA_PATH", os.path.join(MODELS_DIR, "schema.json"))
METADATA_PATH = os.getenv("METADATA_PATH", os.path.join(MODELS_DIR, "metadata.json"))

# Biến trạng thái toàn cục
START_TIME = time.time()
ml_pipeline = None
schema_data = None
metadata_data = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Nạp model.joblib và schema.json NGAY KHI KHỞI ĐỘNG CONTAINER"""
    global ml_pipeline, schema_data, metadata_data
    logger.info("Đang khởi động AI Service...", extra={"request_id": "startup"})
    
    # 1. Nạp Schema
    if not os.path.exists(SCHEMA_PATH):
        logger.error(f"Không tìm thấy schema tại: {SCHEMA_PATH}", extra={"request_id": "startup"})
        raise RuntimeError(f"Thiếu file schema tại {SCHEMA_PATH}")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_data = json.load(f)
    logger.info(f"Đã nạp schema thành công ({len(schema_data['features'])} đặc trưng)", extra={"request_id": "startup"})
    
    # 2. Nạp Metadata
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata_data = json.load(f)
        logger.info(f"Đã nạp metadata: model={metadata_data.get('model_name')}, v={metadata_data.get('model_version')}", extra={"request_id": "startup"})
    else:
        metadata_data = {"model_name": "Logistic Regression", "model_version": "1.0.0"}
        
    # 3. Nạp Model Joblib
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Không tìm thấy model.joblib tại: {MODEL_PATH}", extra={"request_id": "startup"})
        raise RuntimeError(f"Thiếu file model.joblib tại {MODEL_PATH}")
        
    t0 = time.time()
    ml_pipeline = joblib.load(MODEL_PATH)
    load_time_ms = (time.time() - t0) * 1000
    logger.info(f"Đã nạp model.joblib thành công trong {load_time_ms:.2f}ms!", extra={"request_id": "startup"})
    
    yield
    
    logger.info("AI Service đang dừng lại...", extra={"request_id": "shutdown"})

app = FastAPI(
    title="AI Service - Mobile Price Classification",
    version="1.0.0",
    description="API dự đoán phân khúc giá điện thoại thông minh phục vụ Backend",
    lifespan=lifespan
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware trích xuất và gắn X-Request-ID
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
    request.state.request_id = req_id
    response: Response = await call_next(request)
    response.headers["X-Request-ID"] = req_id
    return response

# Schema dữ liệu cho endpoint dự đoán
class PredictRequest(BaseModel):
    features: Dict[str, Any] = Field(..., description="Từ điển chứa đầy đủ 20 đặc trưng phần cứng")

def validate_features(features: Dict[str, Any], req_id: str):
    """Kiểm tra tính hợp lệ của dữ liệu theo schema.json"""
    if not schema_data:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "service_not_ready", "detail": "Schema chưa được nạp", "request_id": req_id}
        )
        
    feature_defs = schema_data.get("features", {})
    required_cols = schema_data.get("feature_order", list(feature_defs.keys()))
    
    # 1. Kiểm tra thiếu trường
    missing = [c for c in required_cols if c not in features]
    if missing:
        msg = f"Thiếu các trường bắt buộc: {', '.join(missing)}"
        logger.warning(f"Lỗi dữ liệu: {msg}", extra={"request_id": req_id})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_input", "detail": msg, "missing_fields": missing, "request_id": req_id}
        )
        
    validated = {}
    # 2. Kiểm tra kiểu và khoảng giá trị
    for name in required_cols:
        val = features[name]
        spec = feature_defs[name]
        try:
            val = float(val) if spec["type"] == "number" else int(float(val))
        except (ValueError, TypeError):
            msg = f"Trường '{name}' phải là kiểu số ({spec['type']})"
            logger.warning(f"Lỗi dữ liệu: {msg}", extra={"request_id": req_id})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "invalid_input", "detail": msg, "field": name, "request_id": req_id}
            )
            
        # Kiểm tra min/max
        if val < spec["min"] or val > spec["max"]:
            msg = f"Trường '{name}' có giá trị {val} nằm ngoài phạm vi cho phép [{spec['min']}, {spec['max']}]"
            logger.warning(f"Lỗi dữ liệu: {msg}", extra={"request_id": req_id})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "invalid_input", "detail": msg, "field": name, "valid_range": [spec["min"], spec["max"]], "request_id": req_id}
            )
            
        # Kiểm tra biến nhị phân
        if spec.get("is_binary", False) and val not in (0, 1):
            msg = f"Trường '{name}' là cờ nhị phân, chỉ chấp nhận giá trị 0 hoặc 1"
            logger.warning(f"Lỗi dữ liệu: {msg}", extra={"request_id": req_id})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "invalid_input", "detail": msg, "field": name, "request_id": req_id}
            )
            
        validated[name] = val
        
    return validated

@app.get("/health", tags=["Monitoring"])
async def health_check(request: Request):
    """Kiểm tra tình trạng hoạt động của AI Service"""
    req_id = getattr(request.state, "request_id", "-")
    uptime = time.time() - START_TIME
    model_version = metadata_data.get("model_version", "1.0.0") if metadata_data else "1.0.0"
    
    return {
        "status": "healthy" if ml_pipeline is not None else "degraded",
        "service": "ai-service",
        "port": 8001,
        "model_loaded": ml_pipeline is not None,
        "model_name": metadata_data.get("model_name", "Logistic Regression") if metadata_data else "Logistic Regression",
        "model_version": model_version,
        "uptime_seconds": round(uptime, 1),
        "request_id": req_id
    }

@app.get("/model-info", tags=["Metadata"])
async def get_model_info(request: Request):
    """Trả thông tin chi tiết về mô hình học máy đang phục vụ"""
    req_id = getattr(request.state, "request_id", "-")
    return {
        "model_name": metadata_data.get("model_name", "Logistic Regression") if metadata_data else "Logistic Regression",
        "model_version": metadata_data.get("model_version", "1.0.0") if metadata_data else "1.0.0",
        "dataset": "Mobile Price Classification (Kaggle)",
        "selected_metrics": metadata_data.get("selected_metrics", {}) if metadata_data else {},
        "labels": schema_data.get("labels", {}) if schema_data else {},
        "label_descriptions": schema_data.get("label_descriptions", {}) if schema_data else {},
        "features": schema_data.get("features", {}) if schema_data else {},
        "feature_order": schema_data.get("feature_order", []) if schema_data else [],
        "model_comparison": metadata_data.get("model_comparison", {}) if metadata_data else {},
        "request_id": req_id
    }

@app.post("/predict", tags=["Inference"])
async def predict_price_range(payload: PredictRequest, request: Request):
    """
    Tiếp nhận 20 đặc trưng phần cứng điện thoại -> trả phân khúc giá và xác suất
    """
    req_id = getattr(request.state, "request_id", str(uuid.uuid4())[:8])
    t_start = time.time()
    
    if ml_pipeline is None:
        logger.error("Yêu cầu dự đoán thất bại: Model chưa được nạp", extra={"request_id": req_id})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "model_not_ready", "detail": "Mô hình AI chưa sẵn sàng", "request_id": req_id}
        )
        
    # Validate dữ liệu đầu vào
    validated_features = validate_features(payload.features, req_id)
    
    # Tạo DataFrame với đúng thứ tự đặc trưng
    feature_cols = schema_data.get("feature_order", list(validated_features.keys()))
    df_input = pd.DataFrame([validated_features])[feature_cols]
    
    try:
        # Dự đoán phân lớp và xác suất
        label_idx = int(ml_pipeline.predict(df_input)[0])
        labels = schema_data.get("labels", {})
        label_text = labels.get(str(label_idx), labels.get(label_idx, f"Class {label_idx}"))
        
        # Lấy phân phối xác suất nếu mô hình hỗ trợ
        probabilities = {}
        if hasattr(ml_pipeline, "predict_proba"):
            probs = ml_pipeline.predict_proba(df_input)[0]
            for idx, p in enumerate(probs):
                key = str(idx)
                name = labels.get(key, labels.get(idx, f"Class {idx}"))
                probabilities[key] = {
                    "label": name,
                    "probability": round(float(p), 4),
                    "percentage": f"{p * 100:.1f}%"
                }
            best_prob = round(float(probs[label_idx]), 4)
        else:
            best_prob = 1.0
            
        latency_ms = round((time.time() - t_start) * 1000, 2)
        model_version = metadata_data.get("model_version", "1.0.0") if metadata_data else "1.0.0"
        
        # Log có cấu trúc chuẩn theo yêu cầu mục 8 của AGENT.md
        # Ví dụ: 10:15:02 INFO  ai-service req=7f3a  predict class_1 p=0.87 model=1.0.0 in 12ms
        logger.info(
            f"predict class_{label_idx} ({label_text}) p={best_prob:.2f} model={model_version} in {latency_ms:.0f}ms",
            extra={"request_id": req_id}
        )
        
        return {
            "prediction": label_text,
            "label_index": label_idx,
            "probability": best_prob,
            "probabilities": probabilities,
            "description": schema_data.get("label_descriptions", {}).get(str(label_idx), ""),
            "model_version": model_version,
            "latency_ms": latency_ms,
            "request_id": req_id
        }
        
    except Exception as e:
        logger.error(f"Lỗi trong quá trình suy luận mô hình: {str(e)}", extra={"request_id": req_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "inference_error", "detail": str(e), "request_id": req_id}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("service:app", host="0.0.0.0", port=8001, reload=False)
