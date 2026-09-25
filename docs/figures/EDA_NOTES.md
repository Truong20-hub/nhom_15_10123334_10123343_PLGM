# Ghi Chú Phân Tích Khám Phá Dữ Liệu (EDA Notes)

Báo cáo chi tiết cho từng hình ảnh phân tích khám phá dữ liệu (EDA) theo chuẩn cấu trúc:
**Quan sát (Observation) → Ý nghĩa thực tiễn (Insight) → Quyết định xử lý kỹ thuật (Action/Decision)**

---

## Hình 1: Phân Phối Biến Mục Tiêu (`01_target_distribution.png`)
- **Quan sát:**
  - Tập dữ liệu gồm chính xác 2,000 mẫu.
  - Cả 4 phân khúc giá (0: Low Cost, 1: Medium Cost, 2: High Cost, 3: Very High Cost) đều có chính xác 500 mẫu, chiếm tỷ lệ cân bằng hoàn hảo 25.0% mỗi lớp.
- **Ý nghĩa:**
  - Bài toán không bị hiện tượng mất cân bằng lớp (Class Imbalance).
  - Dự đoán ngẫu nhiên (Random guess baseline) sẽ có độ chính xác kỳ vọng là 25.0%.
- **Quyết định xử lý:**
  - Không cần áp dụng các kỹ thuật cân bằng dữ liệu như SMOTE, Oversampling hay Undersampling.
  - Khi chia tập Train/Test, áp dụng `StratifiedKFold` hoặc `train_test_split(..., stratify=y)` để bảo toàn phân bố 25% đồng đều qua các tập.
  - Đánh giá mô hình sử dụng cả **Accuracy** và **Macro F1-Score** để đảm bảo khả năng nhận diện tốt đồng đều trên cả 4 phân khúc.

---

## Hình 2: Ma Trận Hệ Số Tương Quan Pearson (`02_correlation_heatmap.png`)
- **Quan sát:**
  - `ram` có hệ số tương quan tuyến tính mạnh nhất với `price_range` ($r \approx 0.917$).
  - `battery_power` ($r \approx 0.201$), `px_width` ($r \approx 0.166$), và `px_height` ($r \approx 0.149$) có tương quan dương ở mức vừa phải với giá.
  - Đa số các đặc trưng nhị phân (`blue`, `dual_sim`, `wifi`, `four_g`) có hệ số tương quan rất nhỏ ($|r| < 0.05$) với phân khúc giá.
  - Giữa các đặc trưng đầu vào: `fc` và `pc` có tương quan dương ($r \approx 0.64$), `px_width` và `px_height` ($r \approx 0.51$), `sc_h` và `sc_w` ($r \approx 0.51$).
- **Ý nghĩa:**
  - Dung lượng RAM là yếu tố chi phối mạnh mẽ nhất đến giá thành của smartphone trên thị trường.
  - Hiện tượng đa cộng tuyến giữa các biến độc lập ở mức chấp nhận được (cao nhất là 0.64 giữa camera trước và camera sau, không vượt quá ngưỡng nguy hiểm 0.8).
- **Quyết định xử lý:**
  - Giữ lại đầy đủ 20 đặc trưng trong pipeline để đảm bảo mô hình nắm bắt được cả các thông số phụ trợ thực tế của người dùng.
  - Cần chuẩn hóa thang đo (StandardScaler) cho các biến có biên độ lớn (`ram`, `battery_power`, `px_width`, `px_height`) để các thuật toán tuyến tính (Logistic Regression, SVM) hội tụ tối ưu.

---

## Hình 3: Phân Phối Dung Lượng RAM Theo Tầm Giá (`03_ram_vs_price.png`)
- **Quan sát:**
  - Tầm giá 0 (Low): RAM dao động chủ yếu từ 256 MB đến 1,500 MB (Trung vị ~1,000 MB).
  - Tầm giá 1 (Medium): RAM dao động từ 1,000 MB đến 2,500 MB (Trung vị ~1,900 MB).
  - Tầm giá 2 (High): RAM dao động từ 2,000 MB đến 3,500 MB (Trung vị ~2,600 MB).
  - Tầm giá 3 (Very High): RAM dao động từ 3,000 MB đến 4,000 MB (Trung vị ~3,500 MB).
  - Các hộp phân vị (IQR) gần như tách biệt theo bậc thang rất rõ nét, không xuất hiện điểm dị biệt ngoại lai (outliers) cực đoan.
- **Ý nghĩa:**
  - RAM tạo nên các siêu phẳng phân tách rất thuận lợi cho các mô hình phân lớp tuyến tính (Linear Hyperplanes) và cây quyết định.
- **Quyết định xử lý:**
  - Không cần cắt tỉa hoặc xử lý outlier đối với biến `ram`.
  - Khuyến nghị thử nghiệm mô hình tuyến tính phân lớp (như Logistic Regression, Linear SVM) vì tính phân tách cao của biến này.

---

## Hình 4: Dung Lượng Pin và Tổng Độ Phân Giải Màn Hình (`04_battery_and_resolution.png`)
- **Quan sát:**
  - Ở cùng một mức dung lượng pin, điện thoại có độ phân giải màn hình cao hơn và pin lớn hơn thường nghiêng về các phân khúc giá 2 và 3.
  - Tuy nhiên các điểm dữ liệu giữa tầm giá 1 và 2 có độ đan xen nhất định nếu chỉ xét 2 biến này.
- **Ý nghĩa:**
  - Pin và màn hình là các yếu tố phần cứng đắt đỏ thứ nhì sau RAM; một chiếc máy cao cấp bắt buộc phải có màn hình sắc nét và thời lượng pin tương xứng.
- **Quyết định xử lý:**
  - Kết hợp đồng thời `battery_power`, `px_height`, `px_width` vào mô hình máy học thay vì chỉ dựa vào `ram`.
  - Lưu ý kiểm tra miền giá trị hợp lệ của `px_height` trong `schema.json` (từ 0 đến 1960) và `px_width` (500 đến 1998).

---

## Hình 5: Tỷ Lệ Trang Bị Các Chuẩn Kết Nối Hiện Đại (`05_connectivity_distribution.png`)
- **Quan sát:**
  - Tỷ lệ có 3G trên 75% ở mọi phân khúc giá.
  - Tỷ lệ trang bị 4G, Wi-Fi, 2 SIM và Bluetooth dao động quanh mức 50% - 55% ở cả 4 phân khúc giá mà không có sự chênh lệch áp đảo.
- **Ý nghĩa:**
  - Các chuẩn kết nối như Wi-Fi, Bluetooth và 3G/4G đã trở thành trang bị tiêu chuẩn phổ cập trên điện thoại thông minh, không còn là đặc quyền riêng của máy đắt tiền.
- **Quyết định xử lý:**
  - Thiết kế form nhập liệu trên Frontend cho phép người dùng bật/tắt (toggle switch hoặc checkbox) trực quan cho 5 tính năng này.
  - Trong `schema.json`, định nghĩa các trường này là kiểu `integer` với `enum: [0, 1]`.

---

## Hình 6: So Sánh Hiệu Năng 4 Mô Hình Học Máy (`06_model_comparison.png`)
- **Quan sát:**
  - **Logistic Regression:** Train Acc = 97.69%, Test Acc = 96.50%, Macro F1 = 96.50%.
  - **Support Vector Machine (SVC Linear):** Train Acc = 97.31%, Test Acc = 96.25%, Macro F1 = 96.25%.
  - **Gradient Boosting:** Train Acc = 100.00%, Test Acc = 92.50%, Macro F1 = 92.48%.
  - **Random Forest:** Train Acc = 100.00%, Test Acc = 89.00%, Macro F1 = 88.94%.
- **Ý nghĩa:**
  - Do biến `ram`, `battery_power` và độ phân giải tạo nên ranh giới phân tách gần như tuyến tính tuyệt vời, mô hình Logistic Regression và Linear SVM cho độ chính xác cao nhất (96.5%) và khái quát hóa (generalization) tốt nhất.
  - Các mô hình cây (Random Forest, Gradient Boosting) bị overfit trên tập huấn luyện (100% train accuracy) nhưng đạt test accuracy thấp hơn (~89 - 92.5%).
- **Quyết định xử lý:**
  - Lựa chọn **Logistic Regression** (hoặc Linear SVC) có kết hợp `StandardScaler` trong `Pipeline` làm mô hình sản xuất chính (Production Model) lưu trong `model.joblib`.
  - Mô hình vừa nhẹ (< 1MB), suy luận cực nhanh (< 5ms), vừa đạt độ chính xác cao nhất.

---

## Hình 7: Ma Trận Nhầm Lẫn Của Mô Hình Tốt Nhất (`07_confusion_matrix.png`)
- **Quan sát:**
  - Trên 400 mẫu kiểm thử (100 mẫu/lớp):
    - Lớp 0 (Low): 97/100 mẫu đúng (chỉ 3 mẫu nhầm sang Lớp 1).
    - Lớp 1 (Medium): 95/100 mẫu đúng (chỉ 3 nhầm sang 0, 2 nhầm sang 2).
    - Lớp 2 (High): 96/100 mẫu đúng (chỉ 2 nhầm sang 1, 2 nhầm sang 3).
    - Lớp 3 (Very High): 98/100 mẫu đúng (chỉ 2 mẫu nhầm sang Lớp 2).
  - Không có bất kỳ trường hợp nào nhầm lẫn nhảy cóc từ Lớp 0 sang Lớp 2 hoặc 3.
- **Ý nghĩa:**
  - Sai số của mô hình hoàn toàn là sai số giữa các lớp liền kề (vùng giáp ranh giá cả), phản ánh đúng bản chất thị trường ngoài đời thực.
- **Quyết định xử lý:**
  - Xác nhận mô hình đạt độ tin cậy rất cao, sẵn sàng đóng gói đưa vào AI Service.

---

## Hình 8: Tầm Quan Trọng Của 20 Đặc Trưng (`08_feature_importance.png`)
- **Quan sát:**
  - `ram` chiếm hơn 45% trọng số phân loại.
  - `battery_power`, `px_height`, `px_width` là nhóm quan trọng kế tiếp (chiếm khoảng 25%).
  - Các đặc trưng còn lại (`mobile_wt`, `int_memory`, `talk_time`, ...) đóng góp phân tách tinh chỉnh cho các trường hợp giáp ranh.
- **Ý nghĩa:**
  - Phân tích mức độ quan trọng giúp đội ngũ phát triển xây dựng UI/UX làm nổi bật 4 thông số chủ chốt nhất (RAM, Pin, Màn hình, Bộ nhớ) cho người dùng dễ nhập liệu.
- **Quyết định xử lý:**
  - Tổ chức form Frontend thành 4 cụm tính năng logic, đặt nhóm "Hiệu năng & Bộ nhớ" và "Pin & Nguồn" ở vị trí ưu tiên đầu tiên.
