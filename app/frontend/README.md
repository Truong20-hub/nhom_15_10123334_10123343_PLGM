# Mobile Price AI — React + Vite

Bản chuyển đổi từ `index.html` / `styles.css` / `app.js` (vanilla JS) sang React + Vite, giữ nguyên giao diện và toàn bộ logic gốc.

## Cài đặt & chạy

```bash
npm install
npm run dev
```

Mở trình duyệt tại địa chỉ Vite in ra (mặc định `http://localhost:5173`).

## Build production

```bash
npm run build
npm run preview
```

## Cấu hình backend

Sửa hằng số `API_BASE` trong `src/constants.js` thành URL Node backend của bạn (ví dụ URL ngrok khi expose ra ngoài):

```js
export const API_BASE = "https://xxxx-xx-xx-xx-xx.ngrok-free.app/api/ai";
```

## Cấu trúc thư mục

```
mobile-price-ai/
├── index.html              # Entry HTML cho Vite
├── src/
│   ├── main.jsx             # Điểm khởi chạy React
│   ├── App.jsx               # Component gốc, chứa toàn bộ state & logic form/predict
│   ├── api.js                 # Gọi backend: predict, health check
│   ├── constants.js           # API_BASE, PRESETS, LABELS, cấu hình slider
│   ├── index.css              # CSS gốc (giữ nguyên từ styles.css)
│   ├── hooks/
│   │   ├── useHistory.js       # Lịch sử dự đoán lưu localStorage
│   │   └── useToasts.js        # Quản lý toast thông báo
│   └── components/
│       ├── Navbar.jsx
│       ├── PresetsBar.jsx
│       ├── HardwareForm.jsx
│       ├── SliderField.jsx
│       ├── ToggleField.jsx
│       ├── GroupIcon.jsx
│       ├── ResultCard.jsx
│       ├── HistoryCard.jsx
│       └── ToastContainer.jsx
```

## Ghi chú chuyển đổi

- Toàn bộ 20 đặc trưng phần cứng được quản lý trong một object state `features` ở `App.jsx` (trước đây đọc trực tiếp từ DOM qua `collectFormData()`).
- Lịch sử dự đoán và theme vẫn dùng `localStorage`/thuộc tính `data-theme` trên `<html>` như bản gốc.
- Backend hiện chưa trả về `predict_proba` nên phần "phân phối xác suất" của bản gốc (luôn bị ẩn bằng JS) đã được lược bỏ khỏi JSX; có thể thêm lại dễ dàng trong `ResultCard.jsx` khi backend hỗ trợ.
