# 📱 Hệ Thống Dự Đoán Phân Khúc Giá Smartphone (Mobile Price AI)

> **Bài tập lớn môn:** Học máy cơ bản  
> **Bộ dữ liệu:** [Mobile Price Classification - Kaggle](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification)  
> **Mô hình triển khai:** Logistic Regression Pipeline (Độ chính xác: **97.50%**, Macro F1: **97.50%**)  
> **Kiến trúc:** Microservices độc lập đóng gói hoàn chỉnh bằng **Docker Compose**

---

## 1. Tổng Quan Dự Án

Dự án giải quyết bài toán **phân loại đa lớp có giám sát (Multiclass Classification)** nhằm dự đoán phân khúc giá của điện thoại thông minh dựa trên 20 thông số kỹ thuật phần cứng.

Biến mục tiêu `price_range` gồm 4 phân khúc:

- `0`: **Giá thấp (Low Cost)** — Dưới 3 triệu VNĐ (Phổ thông, cơ bản).
- `1`: **Giá trung bình (Medium Cost)** — 3 - 7 triệu VNĐ (Tầm trung).
- `2`: **Giá cao (High Cost)** — 7 - 12 triệu VNĐ (Cận cao cấp).
- `3`: **Giá rất cao (Very High Cost)** — Trên 12 triệu VNĐ (Cao cấp / Flagship).

### Điểm nổi bật kỹ thuật:

- **Chống rò rỉ dữ liệu (No Data Leakage):** Scaler chỉ fit duy nhất trên tập Train (80%), biến đổi transform cho tập Test (20%).
- **Đóng gói trọn gói:** Pipeline tiền xử lý (`StandardScaler`) và mô hình học máy được đóng gói trong một file `ai-models/models/model.joblib` duy nhất (2.1 KB).
- **Khởi động tức thì (Instant Startup):** AI Service nạp `model.joblib` ngay khi container khởi động (Lifespan handler), không phát sinh độ trễ ở request đầu tiên.
- **Quan sát xuyên suốt:** Mọi request đều mang mã `X-Request-ID` được đồng bộ qua Frontend, Backend, AI Service và lưu vết vào MongoDB.
- **Bộ kiểm thử toàn diện:** 12/12 unit test cases (`pytest`) vượt qua 100%.

---

## 2. Kiến Trúc Hệ Thống

Toàn bộ hệ thống gồm 4 container độc lập kết nối qua mạng nội bộ Docker (`mobile_net`):

```
[ Người dùng ]
      │
      ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Frontend   │ ────► │   Backend    │ ────► │  AI Service  │ (Nạp model.joblib)
│  (Port 3000) │       │ (Port 8000)  │       │ (Port 8001)  │
└──────────────┘       └──────┬───────┘       └──────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │   MongoDB    │ (Lưu lịch sử dự đoán)
                       │ (Port 27017) │
                       └──────────────┘
```

- **Frontend (Port 3000):** Giao diện Nginx hiện đại, hỗ trợ Dark/Light mode, điều khiển thanh trượt 20 thông số, presets cấu hình mẫu và biểu đồ phân phối xác suất 4 lớp.
- **Backend (Port 8000):** FastAPI API Gateway, kiểm thực dữ liệu nghiêm ngặt theo `schema.json`, chuyển tiếp sang AI Service, lưu lịch sử vào MongoDB (kèm cơ chế bộ nhớ đệm dự phòng).
- **AI Service (Port 8001):** FastAPI Microservice chuyên trách suy luận học máy, nạp `model.joblib` ngay khi container khởi động.
- **MongoDB (Port 27017):** Lưu vết toàn bộ lịch sử dự đoán, thời gian, thông số và độ trễ.

---

## 3. Cấu Trúc Thư Mục Repository

Cấu trúc tuân thủ chính xác 100% quy định tại `AGENT.md`:

```
thuNghiem/
├── app/
│   ├── frontend/               # Nginx, HTML5, CSS3, JavaScript, Dockerfile
│   └── backend/                # FastAPI, Dockerfile, tests/ (pytest)
├── ai-models/
│   ├── colab/                  # 01_eda.ipynb, 02_preprocess.ipynb, 03_train.ipynb, 04_evaluate.ipynb
│   ├── src/                    # preprocess.py, train.py, evaluate.py, generate_figures.py
│   ├── data/
│   │   ├── dataset.zip         # Tệp nén gốc train.csv và test.csv
│   │   └── DATA.md             # Nguồn dữ liệu, bản quyền, mô tả 20 đặc trưng
│   ├── models/                 # model.joblib (2.1 KB), schema.json, metadata.json
│   ├── service/                # AI Service: /predict, /health, /model-info, Dockerfile
│   └── requirements.txt        # Ghim chính xác phiên bản thư viện
├── docs/
│   ├── slide.pptx              # Slide thuyết trình bảo vệ đề tài (12 slides)
│   ├── baocao.docx             # Báo cáo học thuật hoàn chỉnh môn học
│   └── figures/                # 8 hình EDA & đánh giá khoa học (300 DPI)
├── docker-compose.yml          # Cấu hình khởi chạy 4 service bằng 1 lệnh
├── .env.example                # Mẫu biến môi trường an toàn (không có secret)
├── .gitignore
├── AGENT.md                    # Hướng dẫn quy chuẩn đồ án
└── README.md
```

---

## 4. Bảng So Sánh Hiệu Năng 4 Mô Hình

| Thuật Toán                       | 5-Fold CV Score | Train Accuracy | Test Accuracy | Macro F1-Score | Đánh Giá & Lựa Chọn            |
| -------------------------------- | :-------------: | :------------: | :-----------: | :------------: | ------------------------------ |
| **Logistic Regression**          |   **96.31%**    |   **98.25%**   |  **97.50%**   |   **97.50%**   | 🏆 **Mô hình sản xuất (Best)** |
| **Support Vector Machine (SVC)** |     95.81%      |     98.19%     |    96.50%     |     96.50%     | Hiệu năng rất tốt              |
| **Gradient Boosting**            |     89.50%      |    100.00%     |    92.00%     |     91.98%     | Bị quá khớp (Overfitting)      |
| **Random Forest**                |     87.44%      |    100.00%     |    89.00%     |     88.94%     | Bị quá khớp (Overfitting)      |

> **Lý do chọn Logistic Regression:** Dữ liệu có đặc trưng RAM tương quan tuyến tính rất mạnh ($r=0.917$) với phân khúc giá. Logistic Regression kết hợp `StandardScaler` vừa đạt độ chính xác cao nhất (97.50%), vừa không bị quá khớp (chênh lệch Train - Test chỉ 0.75%), dung lượng siêu nhỏ (2.1 KB) và tốc độ suy luận dưới 5ms.

---

## 5. Hợp Đồng API

### A. Dự đoán phân khúc giá

- **Endpoint:** `POST /api/predict` (Backend) hoặc `POST /predict` (AI Service)
- **Headers:** `Content-Type: application/json`, `X-Request-ID: <string>`

**Request Body mẫu:**

```json
{
  "features": {
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
}
```

**Response 200 OK:**

```json
{
  "prediction": "Giá rất cao (Very High Cost)",
  "label_index": 3,
  "probability": 0.98,
  "probabilities": {
    "0": { "label": "Giá thấp (Low Cost)", "percentage": "0.0%" },
    "1": { "label": "Giá trung bình (Medium Cost)", "percentage": "0.0%" },
    "2": { "label": "Giá cao (High Cost)", "percentage": "2.0%" },
    "3": { "label": "Giá rất cao (Very High Cost)", "percentage": "98.0%" }
  },
  "description": "Phân khúc cao cấp / Flagship với cấu hình đỉnh cao nhất.",
  "model_version": "1.0.0",
  "latency_ms": 3.8,
  "request_id": "7f3a9b1c"
}
```

**Lỗi dữ liệu (400 Bad Request):**

```json
{
  "error": "invalid_input",
  "detail": "Trường 'ram' (99999) nằm ngoài khoảng quy định [256, 3998]",
  "field": "ram",
  "valid_range": [256, 3998],
  "request_id": "7f3a9b1c"
}
```

### B. Kiểm tra trạng thái & Metadata

- `GET /health` (Backend): Trả về trạng thái kết nối Backend, AI Service, MongoDB và Uptime.
- `GET /api/model-info`: Trả về tên mô hình, phiên bản, các chỉ số đánh giá và cấu trúc schema.
- `GET /api/history`: Lấy danh sách các lần dự đoán gần nhất từ MongoDB.

---

## 6. Hướng Dẫn Cài Đặt & Vận Hành

### Cách 1: Chạy toàn bộ hệ thống bằng 1 lệnh Docker (Khuyến nghị)

```bash
# 1. Sao chép biến môi trường mẫu
cp .env.example .env

# 2. Khởi động toàn bộ 4 container
docker compose up --build
```

Mở trình duyệt truy cập:

- **Giao diện người dùng (Frontend):** `http://localhost:3000`
- **Tài liệu API Backend (Swagger UI):** `http://localhost:8000/docs`
- **Tài liệu API AI Service:** `http://localhost:8001/docs`

Kiểm tra trạng thái các container:

```bash
docker compose ps
```

Xem log có cấu trúc thời gian thực:

```bash
docker compose logs -f
```

### Cách 2: Chạy cục bộ bằng Python Virtual Environment

```bash
# 1. Tạo môi trường ảo và cài đặt thư viện
python -m venv .venv
source .venv/bin/activate  # Hoặc .venv\Scripts\activate trên Windows
pip install -r ai-models/requirements.txt -r app/backend/requirements.txt

# 2. Huấn luyện mô hình và xuất artifact
python ai-models/src/train.py

# 3. Khởi động AI Service (Terminal 1)
uvicorn ai-models.service.service:app --port 8001

# 4. Khởi động Backend (Terminal 2)
AI_SERVICE_URL=http://localhost:8001 uvicorn app.backend.main:app --port 8000
```

---

## 7. Kiểm Thử Hệ Thống (Pytest)

Chạy bộ kiểm thử tự động 12 test cases:

```bash
pytest app/backend/tests -v
```

Kết quả:

```
============================= test session starts =============================
app/backend/tests/test_api.py::test_health_endpoint PASSED               [  8%]
app/backend/tests/test_api.py::test_model_info_endpoint PASSED           [ 16%]
app/backend/tests/test_api.py::test_history_endpoint PASSED              [ 25%]
app/backend/tests/test_api.py::test_predict_mock_success PASSED          [ 33%]
app/backend/tests/test_model.py::test_model_file_exists PASSED           [ 41%]
app/backend/tests/test_model.py::test_model_loading_and_prediction PASSED [ 50%]
app/backend/tests/test_validation.py::test_validation_success PASSED     [ 58%]
app/backend/tests/test_validation.py::test_validation_missing_field PASSED [ 66%]
app/backend/tests/test_validation.py::test_validation_out_of_range_ram PASSED [ 75%]
app/backend/tests/test_validation.py::test_validation_out_of_range_negative_battery PASSED [ 83%]
app/backend/tests/test_validation.py::test_validation_invalid_binary_flag PASSED [ 91%]
app/backend/tests/test_validation.py::test_validation_non_numeric_string PASSED [100%]
======================== 12 passed, 1 warning in 4.27s ========================
```

---

## 8. Log Có Cấu Trúc (Structured Logging)

Hệ thống ghi log có định dạng nhất quán với mã truy vết `req=<id>`:

```
10:15:02 INFO  frontend  req=7f3a  click Dự đoán -> POST /api/predict
10:15:02 INFO  backend   req=7f3a  validate OK -> gọi ai-service
10:15:02 INFO  ai-service req=7f3a  predict class_3 (Very High) p=0.98 model=1.0.0 in 4ms
10:15:02 INFO  backend   req=7f3a  200 OK total 18ms, saved history
```

---

## 9. Triển Khai Public (Demo Online)

Để mở truy cập công khai cho giáo viên chấm bài hoặc demo trực tiếp:

### Sử dụng Ngrok Tunnel:

```bash
# Public cổng Frontend 3000
ngrok http 3000
```

Cập nhật URL được cấp bởi ngrok vào phần dưới đây:

- **Frontend Online Demo:** `https://your-ngrok-subdomain.ngrok-free.app`
- **Backend API Docs:** `https://your-backend-subdomain.ngrok-free.app/docs`
- **Thời điểm cập nhật:** 25/09/2026
