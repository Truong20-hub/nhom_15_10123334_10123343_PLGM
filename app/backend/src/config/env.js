require('dotenv').config();

// Ưu tiên PORT_BACKEND (dùng khi chạy qua Docker Compose),
// fallback về PORT (dùng khi chạy `npm run dev` trực tiếp với .env riêng trong app/backend),
// cuối cùng mặc định 5000 nếu không có gì cả.
const PORT = process.env.PORT_BACKEND || process.env.PORT || 5000;

module.exports = {
  PORT,
  AI_SERVICE_URL: process.env.AI_SERVICE_URL,
};