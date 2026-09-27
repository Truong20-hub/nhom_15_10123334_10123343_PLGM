import { SLIDER_GROUPS } from "../constants.js";
import SliderField from "./SliderField.jsx";
import ToggleField from "./ToggleField.jsx";
import GroupIcon from "./GroupIcon.jsx";

export default function HardwareForm({
  features,
  onFieldChange,
  onToggleChange,
  onSubmit,
  onReset,
  isSubmitting,
}) {
  return (
    <section className="form-container card">
      <div className="card-header">
        <div>
          <h2 className="card-title">Thông Số Phần Cứng Thiết Bị</h2>
          <p className="card-desc">Nhập 20 đặc trưng kỹ thuật theo chuẩn Kaggle Mobile Price Dataset</p>
        </div>
        <button type="button" className="btn-secondary btn-sm" onClick={onReset}>
          Đặt lại
        </button>
      </div>

      <form
        id="predictForm"
        noValidate
        onSubmit={(e) => {
          e.preventDefault();
          onSubmit();
        }}
      >
        {SLIDER_GROUPS.map((group) => (
          <div className="form-group-card" key={group.title}>
            <div className="group-title">
              <GroupIcon name={group.icon} />
              <span>{group.title}</span>
              {group.keyBadge && <span className="key-badge">{group.keyBadge}</span>}
            </div>

            <div className={`input-grid${group.grid3 ? " grid-3" : ""}`}>
              {group.fields.map((field) => (
                <SliderField
                  key={field.name}
                  field={field}
                  value={features[field.name]}
                  onChange={onFieldChange}
                />
              ))}
            </div>

            {group.toggles && (
              <div className="toggles-grid">
                {group.toggles.map((t) => (
                  <ToggleField
                    key={t.name}
                    name={t.name}
                    label={t.label}
                    checked={Boolean(features[t.name])}
                    onChange={onToggleChange}
                  />
                ))}
              </div>
            )}
          </div>
        ))}

        <button
          type="submit"
          className={`btn-primary btn-submit${isSubmitting ? " loading" : ""}`}
          disabled={isSubmitting}
        >
          <span className="btn-text">DỰ ĐOÁN PHÂN KHÚC GIÁ</span>
          <div className="btn-spinner"></div>
        </button>
      </form>
    </section>
  );
}
