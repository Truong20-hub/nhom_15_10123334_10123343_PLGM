/**
 * Hằng số dùng chung cho ứng dụng Mobile Price AI
 */

// Đường dẫn tương đối — vite.config.js sẽ tự proxy "/api" sang backend (localhost:5000).
// Khi chạy qua ngrok, chỉ cần trỏ ngrok vào port 5173 (port của Vite), KHÔNG cần sửa dòng này.
export const API_BASE = "api/ai";
export const DATASET_NAME = "train.csv";

// Map giá trị <select modelSelect> -> tên file model thật có trong /model
export const MODEL_FILE_MAP = {
  lr: "logistic_regression.pkl",
  knn: "knn.pkl",
  best: "best_model.pkl",
};

// Key lưu lịch sử ở localStorage (vì backend chưa có /api/history)
export const HISTORY_KEY = "mobile_price_history";
export const HISTORY_MAX = 10;

// Giá trị mặc định + cấu hình từng thanh trượt (min/max/step/đơn vị/nhãn)
export const DEFAULT_FEATURES = {
  ram: 2048,
  int_memory: 32,
  clock_speed: 1.5,
  n_cores: 4,
  battery_power: 1200,
  talk_time: 11,
  px_height: 650,
  px_width: 1250,
  mobile_wt: 140,
  m_dep: 0.5,
  sc_h: 12,
  sc_w: 6,
  pc: 10,
  fc: 4,
  four_g: 1,
  three_g: 1,
  wifi: 1,
  blue: 1,
  dual_sim: 1,
  touch_screen: 1,
};

// Preset configurations cho 4 tầm giá chuẩn
export const PRESETS = {
  low: {
    battery_power: 800, blue: 0, clock_speed: 1.0, dual_sim: 1, fc: 2,
    four_g: 0, int_memory: 8, m_dep: 0.8, mobile_wt: 180, n_cores: 2,
    pc: 5, px_height: 250, px_width: 800, ram: 750, sc_h: 8, sc_w: 3,
    talk_time: 5, three_g: 1, touch_screen: 0, wifi: 1,
  },
  mid: {
    battery_power: 1250, blue: 1, clock_speed: 1.6, dual_sim: 1, fc: 5,
    four_g: 1, int_memory: 32, m_dep: 0.5, mobile_wt: 145, n_cores: 4,
    pc: 12, px_height: 650, px_width: 1200, ram: 1850, sc_h: 12, sc_w: 6,
    talk_time: 12, three_g: 1, touch_screen: 1, wifi: 1,
  },
  high: {
    battery_power: 1600, blue: 1, clock_speed: 2.2, dual_sim: 1, fc: 10,
    four_g: 1, int_memory: 64, m_dep: 0.4, mobile_wt: 135, n_cores: 6,
    pc: 16, px_height: 1100, px_width: 1600, ram: 2850, sc_h: 15, sc_w: 8,
    talk_time: 16, three_g: 1, touch_screen: 1, wifi: 1,
  },
  flagship: {
    battery_power: 1950, blue: 1, clock_speed: 2.9, dual_sim: 1, fc: 16,
    four_g: 1, int_memory: 64, m_dep: 0.2, mobile_wt: 125, n_cores: 8,
    pc: 20, px_height: 1600, px_width: 1950, ram: 3850, sc_h: 17, sc_w: 9,
    talk_time: 19, three_g: 1, touch_screen: 1, wifi: 1,
  },
};

// Tên hiển thị / mô tả cho từng phân khúc (backend chỉ trả về số price_range 0-3)
export const LABELS = {
  0: { name: "Giá thấp (Low Cost)", desc: "Phân khúc phổ thông, cấu hình cơ bản." },
  1: { name: "Giá trung bình (Medium Cost)", desc: "Phân khúc tầm trung, cân bằng hiệu năng/giá." },
  2: { name: "Giá cao (High Cost)", desc: "Phân khúc cận cao cấp, cấu hình mạnh." },
  3: { name: "Giá rất cao (Very High Cost)", desc: "Phân khúc cao cấp/Flagship, cấu hình đỉnh." },
};

// Cấu hình các thanh trượt: [name, label, unit, min, max, step]
export const SLIDER_GROUPS = [
  {
    title: "Hiệu năng & Bộ nhớ (Performance & Memory)",
    keyBadge: "Quan trọng nhất",
    icon: "cpu",
    fields: [
      { name: "ram", label: "RAM (Bộ nhớ truy xuất)", unit: "MB", min: 256, max: 3998, step: 32, highlight: true, footer: ["Min: 256 MB", "Max: 3998 MB"] },
      { name: "int_memory", label: "Bộ nhớ trong (ROM)", unit: "GB", min: 2, max: 64, step: 2, footer: ["Min: 2 GB", "Max: 64 GB"] },
      { name: "clock_speed", label: "Xung nhịp CPU", unit: "GHz", min: 0.5, max: 3.0, step: 0.1, footer: ["Min: 0.5 GHz", "Max: 3.0 GHz"] },
      { name: "n_cores", label: "Số nhân vi xử lý", unit: "Cores", min: 1, max: 8, step: 1, footer: ["1 (Đơn nhân)", "8 (Bát nhân)"] },
    ],
  },
  {
    title: "Pin & Nguồn điện (Battery & Power)",
    icon: "battery",
    fields: [
      { name: "battery_power", label: "Dung lượng Pin", unit: "mAh", min: 500, max: 2000, step: 25, highlight: true, footer: ["Min: 500 mAh", "Max: 2000 mAh"] },
      { name: "talk_time", label: "Thời gian đàm thoại", unit: "giờ", min: 2, max: 20, step: 1, footer: ["Min: 2h", "Max: 20h"] },
    ],
  },
  {
    title: "Màn hình & Kích thước (Display & Dimensions)",
    icon: "display",
    grid3: true,
    fields: [
      { name: "px_height", label: "Độ phân giải dọc", unit: "px", min: 0, max: 1960, step: 20 },
      { name: "px_width", label: "Độ phân giải ngang", unit: "px", min: 500, max: 1998, step: 20 },
      { name: "mobile_wt", label: "Trọng lượng máy", unit: "g", min: 80, max: 200, step: 2 },
      { name: "m_dep", label: "Độ mỏng thân máy", unit: "cm", min: 0.1, max: 1.0, step: 0.1 },
      { name: "sc_h", label: "Chiều cao màn hình", unit: "cm", min: 5, max: 19, step: 1 },
      { name: "sc_w", label: "Chiều rộng màn hình", unit: "cm", min: 0, max: 18, step: 1 },
    ],
  },
  {
    title: "Camera & Chuẩn Kết Nối (Camera & Connectivity)",
    icon: "camera",
    fields: [
      { name: "pc", label: "Camera chính (Sau)", unit: "MP", min: 0, max: 20, step: 1 },
      { name: "fc", label: "Camera Selfie (Trước)", unit: "MP", min: 0, max: 19, step: 1 },
    ],
    toggles: [
      { name: "four_g", label: "Mạng 4G LTE" },
      { name: "three_g", label: "Mạng 3G" },
      { name: "wifi", label: "Wi-Fi" },
      { name: "blue", label: "Bluetooth" },
      { name: "dual_sim", label: "2 SIM" },
      { name: "touch_screen", label: "Cảm ứng" },
    ],
  },
];