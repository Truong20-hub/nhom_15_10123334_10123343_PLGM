# Dữ Liệu: Mobile Price Classification (Phân Loại Phân Khúc Giá Điện Thoại)

## 1. Nguồn Gốc & Bản Quyền
- **Nguồn dữ liệu:** Kaggle — [Mobile Price Classification](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification)
- **Tác giả:** Abhishek Sharma
- **Giấy phép:** Open Database License (ODbL) / CC0: Public Domain. Dữ liệu được phép sử dụng tự do cho mục đích nghiên cứu, học tập và phát triển ứng dụng.
- **Tệp nén gốc:** `ai-models/data/dataset.zip` (chứa `train.csv` 2000 dòng và `test.csv` 1000 dòng).

---

## 2. Bài Toán Máy Học
- **Loại bài toán:** Phân loại đa lớp có giám sát (Multiclass Classification - 4 lớp).
- **Mục tiêu:** Dự đoán phân khúc khoảng giá của điện thoại di động (`price_range`) dựa trên 20 thông số kỹ thuật phần cứng và tính năng kết nối.
- **Biến mục tiêu (Target):** `price_range`
  - `0`: **Giá thấp (Low Cost)** — Phân khúc bình dân / phổ thông.
  - `1`: **Giá trung bình (Medium Cost)** — Phân khúc tầm trung.
  - `2`: **Giá cao (High Cost)** — Phân khúc cận cao cấp.
  - `3`: **Giá rất cao (Very High Cost)** — Phân khúc cao cấp / Flagship.

---

## 3. Danh Sách Đặc Trưng (Features)

Tập dữ liệu gồm 20 đặc trưng đầu vào, chia thành các nhóm phần cứng như sau:

### A. Hiệu năng & Bộ nhớ (Performance & Memory)
| Tên đặc trưng | Kiểu dữ liệu | Đơn vị / Phạm vi | Mô tả chi tiết |
|---|---|---|---|
| `ram` | Số nguyên | 256 – 3998 MB | Dung lượng bộ nhớ RAM của thiết bị (đặc trưng quan trọng nhất). |
| `int_memory` | Số nguyên | 2 – 64 GB | Dung lượng bộ nhớ trong lưu trữ. |
| `n_cores` | Số nguyên | 1 – 8 | Số lượng nhân xử lý của vi xử lý CPU (Single, Quad, Octa-core). |
| `clock_speed` | Số thực | 0.5 – 3.0 GHz | Tốc độ xung nhịp của vi xử lý. |

### B. Màn hình & Kích thước (Display & Dimensions)
| Tên đặc trưng | Kiểu dữ liệu | Đơn vị / Phạm vi | Mô tả chi tiết |
|---|---|---|---|
| `px_height` | Số nguyên | 0 – 1960 pixel | Chiều cao độ phân giải điểm ảnh màn hình. |
| `px_width` | Số nguyên | 500 – 1998 pixel | Chiều rộng độ phân giải điểm ảnh màn hình. |
| `sc_h` | Số nguyên | 5 – 19 cm | Chiều cao kích thước vật lý màn hình điện thoại. |
| `sc_w` | Số nguyên | 0 – 18 cm | Chiều rộng kích thước vật lý màn hình điện thoại. |
| `m_dep` | Số thực | 0.1 – 1.0 cm | Độ dày thân máy (cm). |
| `mobile_wt` | Số nguyên | 80 – 200 gram | Khối lượng thiết bị (gram). |
| `touch_screen` | Nhị phân | 0 hoặc 1 | Có màn hình cảm ứng hay không (1 = Có, 0 = Không). |

### C. Pin & Nguồn (Battery & Power)
| Tên đặc trưng | Kiểu dữ liệu | Đơn vị / Phạm vi | Mô tả chi tiết |
|---|---|---|---|
| `battery_power`| Số nguyên | 501 – 1998 mAh | Tổng dung lượng lưu trữ năng lượng của pin trong 1 lần sạc. |
| `talk_time` | Số nguyên | 2 – 20 giờ | Thời gian đàm thoại liên tục tối đa sau một lần sạc đầy. |

### D. Camera & Kết nối (Camera & Connectivity)
| Tên đặc trưng | Kiểu dữ liệu | Đơn vị / Phạm vi | Mô tả chi tiết |
|---|---|---|---|
| `pc` | Số nguyên | 0 – 20 MP | Độ phân giải camera chính phía sau (Primary Camera Megapixels). |
| `fc` | Số nguyên | 0 – 19 MP | Độ phân giải camera selfie phía trước (Front Camera Megapixels). |
| `blue` | Nhị phân | 0 hoặc 1 | Hỗ trợ kết nối Bluetooth (1 = Có, 0 = Không). |
| `dual_sim` | Nhị phân | 0 hoặc 1 | Hỗ trợ 2 SIM (1 = Có, 0 = Không). |
| `four_g` | Nhị phân | 0 hoặc 1 | Hỗ trợ mạng di động thế hệ 4 (4G/LTE). |
| `three_g` | Nhị phân | 0 hoặc 1 | Hỗ trợ mạng di động thế hệ 3 (3G). |
| `wifi` | Nhị phân | 0 hoặc 1 | Hỗ trợ kết nối mạng không dây Wi-Fi. |

---

## 4. Đặc Điểm Phân Bố Dữ Liệu
- **Số lượng mẫu:** 2,000 dòng huấn luyện, 1,000 dòng kiểm thử.
- **Giá trị khuyết thiếu (Missing values):** 0 (dữ liệu sạch hoàn chỉnh, không có ô trống NaN).
- **Cân bằng lớp:** Hoàn hảo — Mỗi phân khúc giá (0, 1, 2, 3) có đúng 500 mẫu (chiếm 25.0% tập dữ liệu). Không xảy ra hiện tượng mất cân bằng lớp (class imbalance).
