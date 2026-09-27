function errorHandler(err, req, res, next) {
  console.error(err.message);

  // Lỗi từ AI service trả về (vd 404, 400 từ FastAPI)
  if (err.response) {
    return res.status(err.response.status).json({
      success: false,
      message: err.response.data?.detail || 'Lỗi từ AI service',
    });
  }

  // Không kết nối được AI service (ngrok tắt, Colab ngắt...)
  if (err.request) {
    return res.status(502).json({
      success: false,
      message: 'Không thể kết nối tới AI service. Kiểm tra lại ngrok/Colab đang chạy chưa.',
    });
  }

  res.status(500).json({ success: false, message: 'Lỗi server nội bộ' });
}

module.exports = errorHandler;