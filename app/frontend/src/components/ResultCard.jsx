import { LABELS } from "../constants.js";

export default function ResultCard({ result }) {
  const hasResult = Boolean(result);
  const labelIdx = result?.labelIndex ?? 0;
  const info = LABELS[labelIdx] || { name: `Class ${labelIdx}`, desc: "" };

  return (
    <div className="result-card card" id="resultCard">
      <div className="card-header">
        <h2 className="card-title">Kết Quả Dự Đoán</h2>
        <span className="badge badge-subtle">
          {hasResult ? `${result.latencyMs} ms` : "Chưa dự đoán"}
        </span>
      </div>

      {!hasResult && (
        <div className="result-body" id="resultPlaceholder">
          <div className="empty-state">
            <div className="empty-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <h3>Sẵn sàng dự đoán</h3>
            <p>
              Chọn một cấu hình mẫu hoặc điều chỉnh thanh trượt rồi nhấn{" "}
              <strong>"Dự đoán phân khúc giá"</strong>
            </p>
          </div>
        </div>
      )}

      {hasResult && (
        <div className="result-body result-active" id="resultActive">
          {/* Tier Highlight Box */}
          <div className={`tier-box tier-${labelIdx}`} id="tierBox">
            <div className="tier-header">
              <span className="tier-badge">Phân khúc {labelIdx}</span>
              {/* Backend hiện chưa trả predict_proba nên không có % độ tin cậy cụ thể */}
              <span className="tier-confidence">Độ tin cậy: <strong>N/A</strong></span>
            </div>
            <h3 className="tier-name">{info.name}</h3>
            <p className="tier-desc">{info.desc}</p>
          </div>

          {/* Diagnostics & Traceability */}
          <div className="meta-trace">
            <div className="trace-row">
              <span>Request ID:</span>
              <code>{result.requestId}</code>
            </div>
            <div className="trace-row">
              <span>Model dùng:</span>
              <span>{result.model}</span>
            </div>
            <div className="trace-row">
              <span>Độ trễ xử lý:</span>
              <span>{result.latencyMs} ms</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
