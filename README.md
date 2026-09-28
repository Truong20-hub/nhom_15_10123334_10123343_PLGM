# 📱 Mobile Price AI — Dự đoán phân khúc giá smartphone

> **Bài tập lớn:** Học máy cơ bản (Nhóm 15)
> **Bộ dữ liệu:** [Mobile Price Classification – Kaggle](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification) (2000 mẫu, 20 đặc trưng, 4 lớp)
> **Mô hình:** K-Nearest Neighbors (KNN) · Naive Bayes · Logistic Regression
> **Kiến trúc:** Microservices, chạy bằng một lệnh `docker compose up`

---

## Mục lục

1. [Bài toán](#1-bài-toán)
2. [Kiến trúc](#2-kiến-trúc)
3. [Các mô hình](#3-các-mô-hình)
4. [Chạy hệ thống](#4-chạy-hệ-thống)
5. [Hướng dẫn test API từng bước](#5-hướng-dẫn-test-api-từng-bước)
6. [Spam test / Load test](#6-spam-test--load-test)
7. [Xem log](#7-xem-log)
8. [Xử lý sự cố](#8-xử-lý-sự-cố)
9. [Cấu trúc thư mục](#9-cấu-trúc-thư-mục)
10. [Demo online](#10-demo-online)

---

## 1. Bài toán

Phân loại đa lớp có giám sát: dự đoán `price_range` của điện thoại từ 20 thông số phần cứng.

| Nhãn | Ý nghĩa | Tham khảo |
|:---:|---|---|
| 0 | Giá thấp (Low Cost) | Dưới 3 triệu |
| 1 | Giá trung bình (Medium Cost) | 3 – 7 triệu |
| 2 | Giá cao (High Cost) | 7 – 12 triệu |
| 3 | Giá rất cao (Very High Cost) | Trên 12 triệu |

Nguyên tắc chống rò rỉ dữ liệu: chia Train/Test trước, `StandardScaler` chỉ `fit` trên tập Train.

---

## 2. Kiến trúc

```
Người dùng / Script test
        │
        ▼
┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│  Frontend   │───►│   Backend   │───►│  AI Service  │  (nạp model khi khởi động)
│  :5173      │    │   :5000     │    │  :8000       │
└─────────────┘    └──────┬──────┘    └──────────────┘
                          ▼
                   ┌─────────────┐
                   │  MongoDB    │  (lưu lịch sử dự đoán)
                   │  :27017     │
                   └─────────────┘
```

| Service | Cổng | Vai trò |
|---|:---:|---|
| Frontend | 5173 | Giao diện nhập 20 thông số và xem kết quả |
| Backend | 5000 | Kiểm tra dữ liệu đầu vào, chuyển sang AI Service, lưu lịch sử |
| AI Service | 8000 | FastAPI, suy luận bằng mô hình đã huấn luyện (chạy online trên Colab qua ngrok) |
| MongoDB | 27017 | Lưu lịch sử dự đoán |

Mỗi request mang một mã `X-Request-ID` xuyên suốt Frontend → Backend → AI Service, dùng để lần theo log.

---

## 3. Các mô hình

| Mô hình | Ý tưởng ngắn gọn | Lưu ý |
|---|---|---|
| **KNN** | Gán nhãn theo đa số của k điểm gần nhất | Cần chuẩn hóa dữ liệu, suy luận chậm hơn khi dữ liệu lớn |
| **Naive Bayes** | Áp dụng định lý Bayes, giả định các đặc trưng độc lập | Rất nhanh, giả định độc lập thường không đúng hoàn toàn |
| **Logistic Regression** | Mô hình tuyến tính, đầu ra là xác suất từng lớp | Ổn định, dễ giải thích |
| **SVM** | Tìm siêu phẳng tối ưu để phân tách các lớp, có thể sử dụng kernel để xử lý dữ liệu phi tuyến | Cần chuẩn hóa dữ liệu, lựa chọn kernel và tham số ảnh hưởng lớn đến kết quả |

**Kết quả đánh giá** (lấy từ `colab/04_evaluate.ipynb`, điền số thật của nhóm):

| Mô hình                 |  5-Fold CV |  Train Acc |   Test Acc |   Macro F1 | Ghi chú        |
| ----------------------- | ---------: | ---------: | ---------: | ---------: | -------------- |
| **KNN**                 |     51.25% |     66.25% |     55.00% |     53.96% | k = 5          |
| **Naive Bayes**         |     50.00% |     71.25% |     60.00% |     58.33% | GaussianNB     |
| **Logistic Regression** | **58.75%** |     70.00% | **70.00%** | **69.70%** | StandardScaler |
| **SVM**                 |     45.00% | **82.50%** |     60.00% |     58.33% | RBF, C = 1.0   |


**Mô hình đang chạy trên server:** `___` (điền tên mô hình được nạp trong AI Service).

---

## 4. Chạy hệ thống

Hệ thống chạy theo mô hình lai: **AI Service chạy online trên Google Colab** (qua ngrok), còn **Frontend, Backend, MongoDB chạy bằng Docker** trên máy. Backend gọi AI Service qua địa chỉ công khai.

```
Docker (máy bạn)                          Online (Colab)
Frontend :̀5173 → Backend :̀5000 ──────────► AI Service (ngrok URL)
                     │
                 MongoDB :27017
```

### Yêu cầu
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (đã bật), Git
- Tài khoản Google (Colab) và tài khoản [ngrok](https://dashboard.ngrok.com/get-started/your-authtoken) để lấy authtoken

### Bước 1 — Chạy AI Service online trên Colab

1. Trong Colab, mở **Secrets** (biểu tượng chìa khóa), thêm secret `NGROK_TOKEN` (dán authtoken của ngrok) và bật *Notebook access*. Không dán token trực tiếp vào cell.
2. Chạy lần lượt các cell sau (thư mục model nằm trên Google Drive):

```python
from google.colab import drive
drive.mount('/content/drive')
%cd /content/drive/MyDrive/AI_model/service

!pip -q install -r requirements.txt pyngrok nest_asyncio
```

```python
import sys, nest_asyncio, uvicorn
from google.colab import userdata
from pyngrok import ngrok

nest_asyncio.apply()
ngrok.set_auth_token(userdata.get('NGROK_TOKEN'))
tunnel = ngrok.connect(8001)
print("AI_SERVICE_URL =", tunnel.public_url)   # copy dòng này

sys.path.insert(0, '.')
from app import app                            # đổi nếu file/biến khác tên
uvicorn.run(app, host='0.0.0.0', port=8000)
```

3. Copy URL in ra (dạng `https://xxxx.ngrok-free.app`). Cell này phải để chạy liên tục, không tắt.
4. Kiểm tra AI Service đã sống:

```bash
curl https://xxxx.ngrok-free.app/health
```

### Bước 2 — Chạy Frontend, Backend, MongoDB bằng Docker

```bash
# 1. Lấy code (nhánh truong)
git clone -b truong https://github.com/Truong20-hub/nhom_15_10123334_10123343_PLGM.git
cd nhom_15_10123334_10123343_PLGM

# 2. Tạo file biến môi trường
cp .env.example .env          # Windows CMD: copy .env.example .env
```

Mở `.env`, trỏ Backend sang AI Service online (thay bằng URL ở Bước 1, không có dấu `/` ở cuối):

```env
AI_SERVICE_URL=https://xxxx.ngrok-free.app
```

Khởi động **3 container**. Tên service lấy theo `docker-compose.yml`:

```bash
docker compose up --build frontend backend mongodb
```

Kiểm tra:

```bash
docker compose ps                       # 3 service phải Up
curl http://localhost:8000/health       # AI Service phải báo kết nối được
```

| Truy cập | URL |
|---|---|
| Giao diện web | http://localhost:5173 |
| Backend | http://localhost:̀5000 |
| AI Service (online) | URL ngrok ở Bước 1, thêm `/docs` |

Dừng hệ thống: `Ctrl+C` hoặc `docker compose down`.

### Khi khởi động lại

URL ngrok bản miễn phí **đổi mỗi lần chạy lại Colab**. Mỗi lần như vậy:

1. Chạy lại cell ở Bước 1, copy URL mới.
2. Sửa `AI_SERVICE_URL` trong `.env`.
3. Nạp lại Backend: `docker compose up -d --force-recreate backend`

Phiên Colab sẽ ngắt khi máy ngủ hoặc để lâu không hoạt động, nên trước giờ test hãy mở tab Colab và kiểm tra `/health`.

---

## 5. Hướng dẫn test API từng bước

Ai cũng test được chỉ bằng `curl`. Trên Windows PowerShell hãy gõ `curl.exe` (không phải `curl`). Đổi `http://localhost:8000` thành URL ngrok nếu test từ xa (xem [mục 10](#10-demo-online)).

### Bước 1 — Kiểm tra server sống

```bash
curl http://localhost:8000/health
```

Kết quả mong đợi: HTTP 200, JSON báo trạng thái Backend, AI Service, MongoDB.

### Bước 2 — Xem thông tin mô hình

```bash
curl http://localhost:8000/api/model-info
```

Trả về tên mô hình, phiên bản, các chỉ số đánh giá.

### Bước 3 — Gửi một dự đoán hợp lệ

File mẫu có sẵn tại [`scripts/sample_request.json`](scripts/sample_request.json):

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: test-001" \
  -d @scripts/sample_request.json
```

Kết quả mong đợi (HTTP 200):

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
  "model_version": "1.0.0",
  "latency_ms": 3.8,
  "request_id": "test-001"
}
```

Giá trị cụ thể phụ thuộc mô hình đang nạp. Điều cần kiểm tra là có đủ các trường `prediction`, `label_index`, `probabilities`, `request_id` và `request_id` khớp với header đã gửi.

### Bước 4 — Thử dữ liệu sai (phải bị từ chối)

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"ram": 99999}}'
```

Kết quả mong đợi: HTTP **400**, JSON có `error`, `detail`, `field` chỉ ra trường sai.

### Bước 5 — Xem lịch sử dự đoán

```bash
curl http://localhost:8000/api/history
```

Phải thấy lần dự đoán ở Bước 3 trong danh sách.

### Bước 6 — Gọi thẳng AI Service online (bỏ qua Backend)

```bash
curl -X POST https://xxxx.ngrok-free.app/predict \
  -H "Content-Type: application/json" \
  -d @scripts/sample_request.json
```

### Ý nghĩa 20 trường đầu vào

| Trường | Ý nghĩa | Trường | Ý nghĩa |
|---|---|---|---|
| `battery_power` | Dung lượng pin (mAh) | `px_height` / `px_width` | Độ phân giải màn hình (pixel) |
| `blue` | Có Bluetooth (0/1) | `ram` | RAM (MB) |
| `clock_speed` | Tốc độ CPU (GHz) | `sc_h` / `sc_w` | Cao / rộng màn hình (cm) |
| `dual_sim` | Hỗ trợ 2 SIM (0/1) | `talk_time` | Thời gian đàm thoại (giờ) |
| `fc` / `pc` | Camera trước / sau (MP) | `three_g` / `four_g` | Hỗ trợ 3G / 4G (0/1) |
| `int_memory` | Bộ nhớ trong (GB) | `touch_screen` | Cảm ứng (0/1) |
| `m_dep` | Độ dày máy (cm) | `wifi` | Có WiFi (0/1) |
| `mobile_wt` | Cân nặng (g) | `n_cores` | Số nhân CPU |

### Test bằng giao diện

Mở http://localhost:5173, kéo các thanh trượt hoặc chọn cấu hình mẫu, bấm **Dự đoán**.

### Test bằng Postman

`POST` tới `/api/predict`, Body chọn `raw` → `JSON`, dán nội dung `scripts/sample_request.json`.

---

## 6. Spam test / Load test

Script chỉ dùng thư viện chuẩn của Python 3, không cần cài thêm.

```bash
# Mặc định: 200 request, 10 luồng song song, gọi localhost:8000
python scripts/load_test.py

# Tăng tải và trỏ tới server khác
python scripts/load_test.py --url https://xxxx.ngrok-free.app --n 500 --workers 20
```

Kết quả in ra: số request/giây, phân bố mã trạng thái, độ trễ trung bình / p50 / p95 / max. Nếu có request khác 200, xem log ở mục 7.

Bản rút gọn bằng bash:

```bash
for i in $(seq 1 100); do
  curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" \
    -X POST http://localhost:8000/api/predict \
    -H "Content-Type: application/json" -d @scripts/sample_request.json &
done; wait
```

### Checklist trước giờ test

- [ ] Cell Colab (AI Service) đang chạy, `curl <ngrok-url>/health` trả 200
- [ ] `docker compose ps` các service đang Up, `.env` đã trỏ đúng URL ngrok mới
- [ ] `curl /health` trả 200
- [ ] Chạy `load_test.py` ở máy mình và toàn bộ trả 200
- [ ] Ngrok đang chạy, URL công khai đã cập nhật ở mục 10
- [ ] Mở sẵn một cửa sổ `docker compose logs -f`
- [ ] Máy cắm sạc, tắt chế độ ngủ

---

## 7. Xem log

```bash
docker compose logs -f                    # tất cả service
docker compose logs -f ai-service         # riêng AI Service
docker compose logs -f backend            # riêng Backend
docker compose logs --tail 100 backend    # 100 dòng gần nhất
```

Một request đi xuyên suốt hệ thống có cùng mã `req`:

```
10:15:02 INFO  frontend   req=7f3a  click Dự đoán -> POST /api/predict
10:15:02 INFO  backend    req=7f3a  validate OK -> gọi ai-service
10:15:02 INFO  ai-service req=7f3a  predict class_3 p=0.98 in 4ms
10:15:02 INFO  backend    req=7f3a  200 OK total 18ms, saved history
```

Muốn lần theo một request cụ thể, tìm theo mã đó:

```bash
docker compose logs | grep "req=7f3a"
```

---

## 8. Xử lý sự cố

| Triệu chứng | Nguyên nhân thường gặp | Cách xử lý |
|---|---|---|
| `port is already allocated` | Cổng 3000/8000/8001/27017 đang bị chiếm | Tắt chương trình đang dùng cổng, hoặc đổi cổng trong `docker-compose.yml` |
| `/health` báo AI Service lỗi | Chưa nạp xong model, hoặc thiếu file model | `docker compose logs ai-service`, kiểm tra file model có trong thư mục AI Service |
| `/health` báo MongoDB lỗi | Mongo chưa lên | Chờ vài giây, `docker compose restart backend` |
| Trả 400 | Dữ liệu ngoài khoảng cho phép hoặc thiếu trường | Đọc `detail` và `valid_range` trong phản hồi |
| Trả 502/504 khi spam | AI Service quá tải | Giảm `--workers`, xem log `ai-service` |
| Ngrok trả trang cảnh báo HTML | Ngrok bản miễn phí chèn trang chắn | Thêm header `ngrok-skip-browser-warning: 1` (script đã có sẵn) |
| Build lỗi thư viện | Sai phiên bản | `docker compose build --no-cache` |

---

## 9. Cấu trúc thư mục

```
├── app/
│   ├── frontend/                 # Giao diện web
│   └── backend/                  # API Gateway
├── ai-models/
│   └── AI_model/
│       ├── colab/                # 01_eda, 02_preprocessing, 03_train, 04_evaluate
│       ├── data/DATA.md          # Nguồn dữ liệu và mô tả đặc trưng
│       └── service/              # FastAPI: app.py, routers/, services/, schemas/, config/
├── scripts/
│   ├── load_test.py              # Spam test
│   └── sample_request.json       # Dữ liệu mẫu
├── docs/                         # Báo cáo, slide, hình
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 10. Demo online

Mở tunnel để giáo viên truy cập:

```bash
ngrok http 8000      # public Backend (dùng để test API)
ngrok http 3000      # public Frontend (giao diện), mở ở terminal khác
```

| | URL |
|---|---|
| Backend API | `https://______.ngrok-free.app` |
| Frontend | `https://______.ngrok-free.app` |
| Cập nhật lúc | __/__/2026 __:__ |

Ví dụ test từ xa:

```bash
curl https://______.ngrok-free.app/health
python scripts/load_test.py --url https://______.ngrok-free.app --n 300 --workers 15
```

---

## Thành viên nhóm 15

| MSSV | Họ tên | Phụ trách |
|---|---|---|
| 10123334 | Đặng Tiến Trường | KNN · Logistic Regression |
| 10123343 | _Điền tên_ |  Naive Bayes · svm |
