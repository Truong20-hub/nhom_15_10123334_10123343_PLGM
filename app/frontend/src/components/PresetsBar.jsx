const PRESET_BUTTONS = [
  { key: "low", dot: "dot-low", label: "Phổ thông (Low)" },
  { key: "mid", dot: "dot-mid", label: "Tầm trung (Medium)" },
  { key: "high", dot: "dot-high", label: "Cận cao cấp (High)" },
  { key: "flagship", dot: "dot-flagship", label: "Flagship (Very High)" },
];

export default function PresetsBar({ onApplyPreset, onRandomize }) {
  return (
    <section className="presets-section">
      <div className="presets-wrapper">
        <span className="presets-label">⚡ Chọn cấu hình mẫu:</span>
        <div className="preset-buttons">
          {PRESET_BUTTONS.map((p) => (
            <button
              key={p.key}
              type="button"
              className="btn-preset"
              onClick={() => onApplyPreset(p.key, p.label)}
            >
              <span className={`preset-dot ${p.dot}`}></span> {p.label}
            </button>
          ))}
          <button type="button" className="btn-preset btn-random" onClick={onRandomize}>
            🎲 Xáo trộn ngẫu nhiên
          </button>
        </div>
      </div>
    </section>
  );
}
