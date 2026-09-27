# DATA.md

## Nguồn dữ liệu

* Tên dataset: Mobile Price Classification
* Link: https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification/data
* Tác giả/đơn vị cung cấp: Abhishek Sharma
* Giấy phép (license): Chưa xác định rõ trên trang Kaggle hiện tại
* Ngày tải: 24/09/2026

## Mô tả bài toán

* Loại bài toán: Phân loại đa lớp (Multiclass Classification)
* Cột mục tiêu (target): `price_range`, ý nghĩa: Phân loại điện thoại theo khoảng giá dựa trên các thông số kỹ thuật của điện thoại.
* Số lớp / khoảng giá trị của target: 4 lớp `{0, 1, 2, 3}`

  * `0`: Giá thấp (Low Cost)
  * `1`: Giá trung bình (Medium Cost)
  * `2`: Giá cao (High Cost)
  * `3`: Giá rất cao (Very High Cost)

## Mô tả các cột dữ liệu

| Cột             | Kiểu dữ liệu | Ý nghĩa                          | Ghi chú                    |
| --------------- | ------------ | -------------------------------- | -------------------------- |
| `battery_power` | int          | Dung lượng pin                   | Đơn vị mAh                 |
| `blue`          | int          | Có Bluetooth hay không           | `0`: Không, `1`: Có        |
| `clock_speed`   | float        | Tốc độ CPU                       | Đơn vị GHz                 |
| `dual_sim`      | int          | Hỗ trợ 2 SIM                     | `0`: Không, `1`: Có        |
| `fc`            | int          | Độ phân giải camera trước        | Đơn vị MP                  |
| `four_g`        | int          | Hỗ trợ mạng 4G                   | `0`: Không, `1`: Có        |
| `int_memory`    | int          | Bộ nhớ trong                     | Đơn vị GB                  |
| `m_dep`         | float        | Độ dày điện thoại                | Đơn vị cm                  |
| `mobile_wt`     | int          | Khối lượng điện thoại            | Đơn vị gram                |
| `n_cores`       | int          | Số lõi CPU                       | Giá trị từ 1 đến 8         |
| `pc`            | int          | Độ phân giải camera chính        | Đơn vị MP                  |
| `px_height`     | int          | Chiều cao độ phân giải màn hình  | Đơn vị pixel               |
| `px_width`      | int          | Chiều rộng độ phân giải màn hình | Đơn vị pixel               |
| `ram`           | int          | Dung lượng RAM                   | Đơn vị MB                  |
| `sc_h`          | int          | Chiều cao màn hình               | Đơn vị cm                  |
| `sc_w`          | int          | Chiều rộng màn hình              | Đơn vị cm                  |
| `talk_time`     | int          | Thời gian sử dụng liên tục       | Thời gian đàm thoại        |
| `three_g`       | int          | Hỗ trợ mạng 3G                   | `0`: Không, `1`: Có        |
| `touch_screen`  | int          | Có màn hình cảm ứng hay không    | `0`: Không, `1`: Có        |
| `wifi`          | int          | Hỗ trợ Wi-Fi                     | `0`: Không, `1`: Có        |
| `price_range`   | int          | Nhãn phân loại khoảng giá        | `0`, `1`, `2`, `3`; target |

## Số lượng

* Số dòng: 2.000 dòng trong `train.csv`
* Số cột: 21 cột
* Số dòng của `test.csv`: 1.000 dòng
* Tỉ lệ thiếu dữ liệu: 0% theo các mô tả và kiểm tra được công bố cho dataset
* Phân bố nhãn (classification): 4 lớp `0, 1, 2, 3`, mỗi lớp có 500 mẫu trong `train.csv`, tương ứng 25% mỗi lớp.

## Các file dữ liệu

### train.csv

* Số dòng: 2.000
* Số cột: 21
* Bao gồm 20 feature và 1 target `price_range`
* Được sử dụng để phân tích dữ liệu và huấn luyện các mô hình Machine Learning.

### test.csv

* Số dòng: 1.000
* Số cột: 21
* Bao gồm các feature của điện thoại.
* Không sử dụng `price_range` làm target trong file test khi thực hiện dự đoán.
* Được sử dụng để kiểm tra khả năng dự đoán của mô hình.

## Mục tiêu Machine Learning

Xây dựng các mô hình Machine Learning để dự đoán `price_range` của một chiếc điện thoại dựa trên 20 thông số kỹ thuật:

* Logistic Regression
* K-Nearest Neighbors (KNN)
* Naive Bayes
* Support Vector Machine (SVM)

Các mô hình sẽ được đánh giá bằng:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

Đặc biệt, mỗi mô hình cần có Confusion Matrix để đánh giá khả năng phân loại 4 nhóm giá.
