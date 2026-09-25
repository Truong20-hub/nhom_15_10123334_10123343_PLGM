# AGENT.md

Hướng dẫn cho AI agent (Claude Code, Copilot, Cursor, v.v.) khi làm việc trong repo bài tập lớn môn **Học máy cơ bản**. Nội dung bám sát `HUONG_DAN_BAI_TAP_LON.md` của giảng viên — đọc kỹ trước khi tạo/sửa file.

> Nhãn **[Bắt buộc]** = thiếu là không đạt. **[Khuyến nghị]** = nên làm để hệ thống ổn định, dễ bảo vệ.

## 1. Tổng quan

Sản phẩm gồm 3 khối chạy độc lập bằng Docker, ghép lại qua `docker-compose.yml`:

```
Người dùng → Frontend → Backend → AI Service (nạp model.joblib) → MongoDB (lưu lịch sử)
```

- **AI Service**: nạp `model.joblib` **ngay khi container khởi động**, nhận đặc trưng → trả kết quả dự đoán.
- **Backend**: validate dữ liệu theo `schema.json`, gọi AI Service, lưu lịch sử vào MongoDB, xử lý lỗi.
- **Frontend**: dựng form theo `schema.json`, gọi `/api/predict`, hiển thị kết quả + tên model/metric.

Mọi request cần mang `X-Request-ID` để log xuyên suốt 3 service (xem mục 8).

## 2. Cấu trúc repo (bắt buộc giữ nguyên tên/vị trí thư mục cấp cao nhất)

```
<ten-du-an>/
├── app/
│   ├── frontend/               # FE (có Dockerfile)
│   └── backend/                # BE (có Dockerfile, tests/)
├── ai-models/
│   ├── colab/                  # 01_eda, 02_preprocess, 03_train, 04_evaluate
│   ├── src/                    # preprocess.py, train.py, evaluate.py
│   ├── data/
│   │   └── dataset.zip         # dataset Kaggle + DATA.md (nguồn, giấy phép)
│   ├── models/                 # model.joblib, schema.json, metadata.json
│   ├── service/                # AI Service: /predict, /health, /model-info
│   └── requirements.txt        # ghim phiên bản thư viện
├── docs/
│   ├── slide.pptx
│   ├── baocao.docx
│   └── figures/                # ≥5 hình EDA + biểu đồ so sánh model
├── docker-compose.yml
├── .env.example                # KHÔNG chứa mật khẩu thật
├── .gitignore
└── README.md
```

Bên trong mỗi thư mục con (`frontend/`, `backend/`, `service/`) được tự do tổ chức, miễn `docker compose up --build` chạy đúng.

**Agent không được:** đổi tên hoặc bỏ bớt các thư mục cấp cao nhất (`app/`, `ai-models/`, `docs/`) hay 3 file gốc (`docker-compose.yml`, `.env.example`, `.gitignore`, `README.md`).

## 3. Quy trình 6 bước — đầu ra của bước này là đầu vào bước sau

| Bước | Việc chính | Đầu ra | Nằm ở |
|---|---|---|---|
| 0. Dữ liệu | Chọn dataset Kaggle, xác định bài toán | `dataset.zip`, mô tả cột mục tiêu | `ai-models/data/` |
| 1. EDA | ≥5 hình, mỗi hình: quan sát → ý nghĩa → quyết định xử lý | Hình + ghi chú | `ai-models/colab/`, `docs/figures/` |
| 2. Xử lý dữ liệu | Pipeline (fit trên train, tránh leakage) | Pipeline + `schema.json` | `ai-models/src/`, `ai-models/models/` |
| 3. Huấn luyện | ≥4 model cùng bài toán, cùng cách chia dữ liệu | Bảng tham số đã thử | `ai-models/colab/` |
| 4. Đánh giá | Metric phù hợp, so với baseline, train vs test, chọn model cuối | Bảng so sánh + lý do chọn | `ai-models/colab/`, `docs/` |
| 5. App/Product | Đóng gói, Docker, public, test, log | Xem mục 5–8 | `app/`, `ai-models/` |

**5 điểm nhất quán agent phải tự kiểm tra khi sinh/sửa code:**
1. Cùng danh sách đặc trưng ở EDA, pipeline, model, `schema.json`, validate BE, form FE.
2. Tiền xử lý lúc dự đoán = lúc huấn luyện — lưu pipeline **cùng** model, không viết lại tay ở BE.
3. Cùng phiên bản `scikit-learn`/`numpy`/`pandas` giữa Colab và `requirements.txt` của AI Service.
4. Cùng ánh xạ nhãn (0/1 ứng lớp nào) từ huấn luyện đến giao diện.
5. Metric hiển thị trên app (`/model-info`) đúng là metric của model đã chọn ở bước 4.

## 4. Đóng gói model (bước cầu nối Colab → App)

- `ai-models/models/model.joblib`: **pipeline + model trong một file** (`joblib.dump(pipeline, ...)`), hoặc ONNX.
- `metadata.json`: tên model, `model_version`, metric, ngày huấn luyện, phiên bản thư viện đã dùng.
- `schema.json`: tên cột, kiểu, khoảng giá trị hợp lệ, danh sách nhãn (từ bước 2).
- File model nên < 50MB (giới hạn cảnh báo của GitHub); nếu lớn hơn: giảm số cây, nén (`compress=3`), hoặc Git LFS.

## 5. Hợp đồng API

| Thành phần | Trách nhiệm | Endpoint |
|---|---|---|
| AI Service | Nạp model lúc container start; predict | `POST /predict`, `GET /health`, `GET /model-info` |
| Backend | Validate theo `schema.json`; gọi AI Service; lưu lịch sử MongoDB | `POST /api/predict`, `GET /api/history`, `GET /health` |
| Frontend | Form theo `schema.json`; hiển thị kết quả/model/metric | trang chủ, trang kết quả/lịch sử |

```json
// POST /api/predict
{ "features": { "cot_1": 12.5, "cot_2": "A", "cot_3": 3 } }

// 200 OK
{ "prediction": "class_1", "probability": 0.87, "model_version": "1.0.0", "request_id": "7f3a…" }

// Lỗi dữ liệu (400)
{ "error": "invalid_input", "detail": "cot_2 phải thuộc {A, B, C}", "request_id": "7f3a…" }
```

Validate dữ liệu ở **cả BE lẫn AI Service** (không tin dữ liệu từ FE), trả đúng mã HTTP (400 vs 5xx), bật CORS đúng domain FE.

## 6. Docker & biến môi trường

- Mỗi service (`ai-service`, `backend`, `frontend`) là **một container riêng**, ghép qua `docker-compose.yml`. Chạy toàn hệ thống bằng đúng 1 lệnh:
  ```
  cp .env.example .env
  docker compose up --build
  ```
- AI Service **nạp model ngay lúc container khởi động**, không đợi request đầu tiên.
- `GET /health` ở mỗi service trả tình trạng, cổng, uptime. Kiểm tra trạng thái bằng `docker compose ps`.
- Các service gọi nhau **qua tên service trong Docker network** (ví dụ `http://ai-service:8001`), **không hardcode `localhost`/IP**.
- Mọi địa chỉ (`API_URL`, `AI_SERVICE_URL`, `MONGODB_URI`) đọc từ `.env`. Không commit `.env` thật, chỉ commit `.env.example`.

## 7. Triển khai public

- Cả AI Service lẫn App phải public được — deploy cloud (Render/Vercel/…) **hoặc** Docker trên máy cá nhân/Colab public bằng IP tĩnh/tunnel (ngrok).
- **Mỗi lần cổng/tunnel đổi địa chỉ**: cập nhật `.env`, cập nhật mục "Demo online" trong `README.md`, ghi log thời điểm đổi.
- Không có IP tĩnh → phải cập nhật link **mỗi sáng thứ Hai** cho đến ngày bảo vệ.
- Nạp model một lần lúc khởi động (RAM free-tier thường ít). "Làm nóng" hệ thống trước khi test/bảo vệ.

## 8. Log & khả năng quan sát

**[Bắt buộc]** log có cấu trúc, cùng `request_id` xuyên suốt 3 service, xem được mỗi khi có request:

```
10:15:02 INFO  frontend  req=7f3a  click Dự đoán -> POST /api/predict
10:15:02 INFO  backend   req=7f3a  validate OK -> gọi ai-service
10:15:02 INFO  ai-service req=7f3a  predict class_1 p=0.87 model=1.0.0 in 12ms
10:15:02 INFO  backend   req=7f3a  200 OK total 84ms, saved history
```

Không ghi dữ liệu nhạy cảm vào log. Xem log: `docker compose logs -f <service>` (local) hoặc trang Logs của nền tảng deploy.

## 9. Kiểm thử

| Loại | Việc cần làm |
|---|---|
| Chức năng | Test API (đúng/sai/thiếu trường), test model nạp được — dùng `pytest` |
| Smoke test | Mở địa chỉ public, gửi 1 request, xem log cả 3 service |
| Tải | Nhiều người gọi `/api/predict` đồng thời — k6/Locust/Apache Bench |
| Giao diện | Lighthouse (tốc độ tải, kích thước tài nguyên) |

Mục tiêu gợi ý: 10–20 người dùng đồng thời/1 phút, tỉ lệ lỗi < 1%, p95 < 2s cho `/api/predict` khi hệ thống đã nóng.

## 10. Git

- Repo **public**. Mỗi người code chung một phần phải làm trên **nhánh riêng**, merge bằng `git merge`/PR — **không commit đè lên `main`**.
- Không đưa bí mật lên Git: `kaggle.json`, chuỗi kết nối MongoDB, token, `.env` thật.
- Dataset đẩy dạng file zip, để `docs/`, `app/`, `ai-models/` đúng vị trí.
- Mốc thời gian: commit đầu tiên + `docs/baocao.docx` **chậm nhất 18h30 25/09/2026**; `docs/slide.pptx` **chậm nhất 6h30 28/09/2026**.

## 11. Việc agent nên làm khi được giao task

1. Xác định task thuộc bước nào (0–5) và module nào (`app/frontend`, `app/backend`, `ai-models/service`, `ai-models/src`, `ai-models/colab`).
2. Sửa pipeline tiền xử lý → sửa đồng thời ở nơi huấn luyện (`ai-models/src` hoặc notebook) **và** đảm bảo AI Service dùng lại đúng pipeline đã lưu trong `model.joblib`, không viết lại logic tiền xử lý tay ở Backend.
3. Thêm/sửa cột dữ liệu → cập nhật đồng bộ ở: pipeline huấn luyện, `schema.json`, validate ở Backend, form ở Frontend.
4. Không hardcode địa chỉ/cổng — luôn đọc qua biến môi trường từ `.env`.
5. Không sửa file model (`.joblib`) bằng tay — chỉ sinh ra từ `ai-models/src` hoặc notebook rồi export lại.
6. Khi thêm log, giữ định dạng có `request_id` như mục 8.

## 12. Việc agent không nên làm

- Không đổi tên/xoá các thư mục cấp cao nhất (`app/`, `ai-models/`, `docs/`) hay `docker-compose.yml`, `.env.example`, `README.md`.
- Không fit scaler/encoder trên toàn bộ dữ liệu trước khi chia train/test (data leakage).
- Không nạp lại model mỗi request — chỉ nạp một lần lúc container khởi động.
- Không commit `.env` thật, `kaggle.json`, hay bất kỳ secret nào.
- Không dùng mỗi Accuracy làm metric duy nhất khi dữ liệu mất cân bằng.
