"""
Module Đánh Giá Mô Hình Toàn Diện (Model Evaluation)
Kiểm tra tính nhất quán và độ chính xác của model.joblib đã xuất xưởng.
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from preprocess import prepare_train_test, FEATURE_COLUMNS, LABEL_MAPPING

def evaluate_saved_model(model_path="ai-models/models/model.joblib", schema_path="ai-models/models/schema.json"):
    print("=" * 60)
    print("BƯỚC 4: KIỂM ĐỊNH MÔ HÌNH ĐÃ ĐÓNG GÓI (MODEL.JOBLIB)")
    print("=" * 60)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Không tìm thấy file mô hình tại {model_path}. Vui lòng chạy train.py trước.")
        
    print(f"[+] Đang nạp mô hình từ: {model_path}")
    pipeline = joblib.load(model_path)
    
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    print(f"[+] Đã nạp schema: {schema['title']} - Phiên bản {schema['version']}")
    
    # Chuẩn bị dữ liệu kiểm thử
    _, X_test, _, y_test = prepare_train_test()
    
    # Tiến hành dự đoán
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test) if hasattr(pipeline, "predict_proba") else None
    
    # Tính toán các chỉ số
    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    
    print(f"\nKẾT QUẢ ĐÁNH GIÁ TRÊN TẬP TEST ({len(y_test)} mẫu):")
    print(f"  - Độ chính xác (Accuracy): {acc * 100:.2f}%")
    print(f"  - Macro F1-Score:           {macro_f1 * 100:.2f}%")
    print(f"  - So với Baseline ngẫu nhiên (25.0%): Vượt trội +{(acc - 0.25) * 100:.2f}%")
    
    print("\nBÁO CÁO CHI TIẾT TỪNG PHÂN KHÚC (Classification Report):")
    target_names = [f"Lớp {k}: {LABEL_MAPPING[k]}" for k in sorted(LABEL_MAPPING.keys())]
    print(classification_report(y_test, y_pred, target_names=target_names, digits=4))
    
    print("MA TRẬN NHẦM LẪN (Confusion Matrix):")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # Thử nghiệm suy luận mẫu thực tế
    print("\n" + "-" * 60)
    print("THỬ NGHIỆM SUY LUẬN VỚI 1 MẪU ĐIỆN THOẠI CAO CẤP (FLAGSHIP SAMPLE):")
    sample_phone = {
        "battery_power": 1850,
        "blue": 1,
        "clock_speed": 2.8,
        "dual_sim": 1,
        "fc": 16,
        "four_g": 1,
        "int_memory": 64,
        "m_dep": 0.3,
        "mobile_wt": 130,
        "n_cores": 8,
        "pc": 20,
        "px_height": 1400,
        "px_width": 1920,
        "ram": 3850,
        "sc_h": 17,
        "sc_w": 9,
        "talk_time": 18,
        "three_g": 1,
        "touch_screen": 1,
        "wifi": 1
    }
    
    sample_df = pd.DataFrame([sample_phone])[FEATURE_COLUMNS]
    sample_pred = int(pipeline.predict(sample_df)[0])
    sample_prob = float(np.max(pipeline.predict_proba(sample_df)[0])) if hasattr(pipeline, "predict_proba") else 1.0
    
    print(f"  - Kết quả dự đoán: Phân khúc {sample_pred} -> {LABEL_MAPPING[sample_pred]}")
    print(f"  - Độ tin cậy (Probability): {sample_prob * 100:.2f}%")
    print("-" * 60)
    
    return acc, macro_f1

if __name__ == "__main__":
    evaluate_saved_model()
