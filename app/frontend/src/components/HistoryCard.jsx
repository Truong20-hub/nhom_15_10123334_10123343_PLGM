export default function HistoryCard({ history, onRefresh }) {
  return (
    <div className="history-card card">
      <div className="card-header">
        <div>
          <h2 className="card-title">Lịch Sử Dự Đoán</h2>
          <p className="card-desc">Lưu tạm trên trình duyệt (localStorage)</p>
        </div>
        <button type="button" className="btn-icon" title="Làm mới lịch sử" onClick={onRefresh}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="23 4 23 10 17 10"></polyline>
            <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
          </svg>
        </button>
      </div>

      <div className="history-list">
        {history.length === 0 && (
          <div className="empty-history">Chưa có bản ghi nào</div>
        )}

        {history.map((item, idx) => {
          const timeStr = item.timestamp
            ? new Date(item.timestamp).toLocaleTimeString()
            : "--:--";
          const ram = item.features?.ram ?? "--";
          const bat = item.features?.battery_power ?? "--";
          const rom = item.features?.int_memory ?? "--";

          return (
            <div className="history-item" key={`${item.request_id}-${idx}`}>
              <div className="history-header">
                <span className="history-time">
                  {timeStr} • req={item.request_id || "-"}
                </span>
                <span className="badge" style={{ fontSize: "0.7rem" }}>
                  {item.model || ""}
                </span>
              </div>
              <div
                className="history-pred"
                style={{ color: `var(--tier-${item.label_index ?? 1})` }}
              >
                {item.prediction || `Class ${item.label_index}`}
              </div>
              <div className="history-specs">
                RAM: <strong>{ram}MB</strong> | Pin: <strong>{bat}mAh</strong> | ROM: <strong>{rom}GB</strong>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
