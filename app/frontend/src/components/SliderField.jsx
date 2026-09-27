export default function SliderField({ field, value, onChange }) {
  const { name, label, unit, min, max, step, highlight, footer } = field;

  return (
    <div className={`input-field${highlight ? " field-highlight" : ""}`}>
      <div className="field-header">
        <label htmlFor={name}>{label}</label>
        <span className="field-val">
          <strong>{value}</strong> {unit}
        </span>
      </div>
      <input
        type="range"
        id={name}
        name={name}
        min={min}
        max={max}
        step={step}
        value={value}
        className="slider-input"
        onChange={(e) => onChange(name, parseFloat(e.target.value))}
      />
      {footer && (
        <div className="field-footer">
          <small>{footer[0]}</small>
          <small>{footer[1]}</small>
        </div>
      )}
    </div>
  );
}
