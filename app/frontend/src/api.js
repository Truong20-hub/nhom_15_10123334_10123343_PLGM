import { API_BASE } from "./constants.js";

// Hàm sinh mã request_id ngắn gọn
export function generateRequestId() {
  return Math.random().toString(36).substring(2, 10);
}

// Log chuẩn cấu trúc có request_id hiển thị trên Console
export function logStructured(level, reqId, message) {
  const now = new Date();
  const timeStr = now.toTimeString().split(" ")[0];
  console.log(
    `${timeStr} ${level.toUpperCase().padEnd(5)} frontend  req=${reqId}  ${message}`,
  );
}

/**
 * Gửi yêu cầu dự đoán tới backend.
 * Backend nhận model qua query string, body là feature object thô (không bọc {features}).
 * Backend trả { success: true, data: { model, price_range } }.
 */
export async function predictPriceRange(features, modelFile, reqId) {
  const startTime = performance.now();

  const resp = await fetch(
    `${API_BASE}/predict?model=${encodeURIComponent(modelFile)}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Request-ID": reqId,
      },
      body: JSON.stringify(features),
    },
  );

  const totalClientTime = Math.round(performance.now() - startTime);
  const payload = await resp.json().catch(() => ({}));

  if (!resp.ok || payload.success === false) {
    const msg = payload.message || "Lỗi dự đoán dữ liệu";
    const error = new Error(msg);
    error.status = resp.status;
    throw error;
  }

  return {
    labelIndex: payload.data?.price_range,
    model: payload.data?.model || modelFile,
    latencyMs: totalClientTime,
  };
}

/**
 * Lấy các chỉ số đánh giá model (accuracy, precision, recall, f1_score, confusion_matrix,
 * classification_report chi tiết từng lớp) trên một dataset cho trước.
 * Backend trả { success: true, data: {...} } y hệt response của AI service.
 */
export async function evaluateModel(modelFile, datasetName, reqId) {
  const resp = await fetch(
    `${API_BASE}/evaluate?model_name=${encodeURIComponent(modelFile)}&dataset_name=${encodeURIComponent(datasetName)}`,
    {
      method: "GET",
      headers: { "X-Request-ID": reqId },
    },
  );

  const payload = await resp.json().catch(() => ({}));

  if (!resp.ok || payload.success === false) {
    const msg = payload.message || "Lỗi lấy chỉ số đánh giá model";
    const error = new Error(msg);
    error.status = resp.status;
    throw error;
  }

  return payload.data;
}

/** Kiểm tra sức khỏe hệ thống (Node backend tự gọi AI service) */
export async function checkSystemHealth() {
  const resp = await fetch(`${API_BASE}/health`);
  const payload = await resp.json().catch(() => ({}));
  return resp.ok && payload.success;
}