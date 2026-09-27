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

/** Kiểm tra sức khỏe hệ thống (Node backend tự gọi AI service) */
export async function checkSystemHealth() {
  const resp = await fetch(`${API_BASE}/health`);
  const payload = await resp.json().catch(() => ({}));
  return resp.ok && payload.success;
}
/**
 * Gọi backend để đánh giá độ chính xác (accuracy) của 1 model trên dataset chỉ định.
 * Backend trả { success: true, data: { accuracy, ... } }.
 */
export async function evaluateModelAccuracy(modelFile, datasetName, reqId) {
  const resp = await fetch(
    `${API_BASE}/evaluate?model_name=${encodeURIComponent(modelFile)}&dataset_name=${encodeURIComponent(datasetName)}`,
    { headers: { "X-Request-ID": reqId } },
  );

  const payload = await resp.json().catch(() => ({}));

  if (!resp.ok || payload.success === false) {
    const msg = payload.message || "Lỗi đánh giá model";
    const error = new Error(msg);
    error.status = resp.status;
    throw error;
  }

  return payload.data?.accuracy;
}