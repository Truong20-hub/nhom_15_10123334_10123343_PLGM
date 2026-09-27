export default function ToggleField({ name, label, checked, onChange }) {
  return (
    <label className="toggle-control">
      <input
        type="checkbox"
        name={name}
        checked={checked}
        onChange={(e) => onChange(name, e.target.checked)}
      />
      <span className="toggle-track"></span>
      <span className="toggle-text">{label}</span>
    </label>
  );
}
